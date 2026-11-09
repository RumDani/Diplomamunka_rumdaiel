"""A* globális útvonal és DWA lokális vezérlés integrációja."""

from __future__ import annotations  # Típusannotációk késleltetett kiértékelése (előre hivatkozható típusok)
import math  # Matematikai műveletekhez (hypot, gyökvonás, trigonometria)
from typing import Any, Dict, List, Optional, Sequence, Tuple

# Külső projektmodulok importálása a tervezéshez és konfigurációhoz
from codes_diploma.astar_project.astar_baseline import astar_search  # Diszkrét A* kereső algoritmus
from codes_diploma.astar_project.path_smoothing import smooth_path  # Bézier-alapú saroklekerekítő algoritmus
from codes_diploma.DWA import optimisation, pairstochoose  # DWA sebességtér mintavételezés és költségoptimalizálás
from codes_diploma.robot import Goal, robotconfig  # Célpont reprezentáció és robot fizikai paraméterei
from typing import Tuple  # Típusjelölések a tiszta C++-os kódképhez

# Típusaliasok a C++ 'using' vagy 'typedef' mintájára
Point2D = Tuple[float, float]  # Folytonos világkoordináta: (x, y) méterben
GridCoord = Tuple[int, int]  # Diszkrét térképkoordináta: (sor, oszlop) cellaindexben


class AStarDWAPlanner:
    """Kétszintű hibrid útvonaltervező és mozgásvezérlő osztály."""

    def __init__(
        self,
        grid_map: Any,  # Bemeneti foglaltsági rácstérkép
        config: Optional[Any] = None,  # Robot dinamikai és geometriai korlátai
        diagonal: bool = True,  # Engedélyezi-e a 8-irányú (átlós) mozgást az A*-ban
        waypoint_tolerance: float = 0.2,  # Alapértelmezett elfogadási sugár egy ponthoz [m]
        waypoint_spacing: float = 0.2,  # Waypointok közötti egyenletes távolság az újramintavételezéskor [m]
    ) -> None:
        self.grid_map = grid_map  # Térkép elmentése a koordináta-transzformációkhoz
        self.config = config if config is not None else robotconfig()  # Konfiguráció inicializálása
        self.diagonal: bool = diagonal  # Átlós szomszédok engedélyezésének mentése
        self.waypoint_tolerance: float = waypoint_tolerance  # Névleges toleranciasugár rögzítése
        self.waypoint_spacing: float = waypoint_spacing  # Újramintavételezési lépésköz rögzítése

        self.path: List[Point2D] = []  # Végleges, aktívan követett folytonos útvonal pontjai
        self.astar_path: List[Point2D] = []  # Nyers, töréspontos A* világkoordináták listája
        self.bezier_path: List[Point2D] = []  # Saroklekerekített, simított Bézier pontok listája
        self.waypoints: List[Point2D] = []  # Egyenletesen diszkretizált célpontok láncolata
        self.waypoint_index: int = 0  # Az aktuálisan követett referencia waypoint sorszáma

    def _current_tolerance(self, state: Any) -> float:
        """Kiszámítja az adaptív toleranciát a célhoz mért távolság alapján."""
        if not self.waypoints:  # Ha nincs betöltve útvonal
            return self.waypoint_tolerance  # Az alapértelmezett tűréssel tér vissza

        goal_x, goal_y = self.waypoints[-1]  # A legutolsó pont (globális végcél) koordinátái
        goal_distance: float = math.hypot(goal_x - state.x, goal_y - state.y)  # Robot-végcél távolság

        # 0.05m és waypoint_tolerance közé szorított, távolságarányos dinamikus tűrés
        return max(0.05, min(self.waypoint_tolerance, goal_distance * 0.2))

    @staticmethod
    def _create_waypoints(path: Sequence[Point2D], spacing: float = 0.2) -> List[Point2D]:
        """A nyers/simított görbét egyenlő ívhosszúságú szakaszokra osztja fel."""
        if not path:  # Üres útvonal esetén
            return []  # Üres listát ad vissza

        waypoints: List[Point2D] = [path[0]]  # A kezdőpont mindig bekerül első waypointként
        remaining_distance: float = spacing  # A következő pont lehelyezéséig hátralévő távolság
        segment_start: Point2D = path[0]  # A vizsgált útszakasz kezdőkoordinátája

        for segment_end in path[1:]:  # Végiglépked az útvonal egymást követő pontjain
            dx: float = segment_end[0] - segment_start[0]  # Szakasz X irányú hossza
            dy: float = segment_end[1] - segment_start[1]  # Szakasz Y irányú hossza
            segment_length: float = math.hypot(dx, dy)  # Két pont közötti euklideszi távolság

            if segment_length == 0.0:  # Ha a két egymást követő pont egybeesik
                continue  # Átugorjuk a felesleges nullosztást

            while segment_length >= remaining_distance:  # Ha a szakasz hosszabb a szükséges távnál
                ratio: float = remaining_distance / segment_length  # Interpolációs arány [0.0, 1.0]
                point: Point2D = (  # Beszúrt új pont kiszámítása lineáris arányosítással
                    segment_start[0] + ratio * dx,  # Új pont X koordinátája
                    segment_start[1] + ratio * dy,  # Új pont Y koordinátája
                )
                waypoints.append(point)  # Pont hozzáadása a diszkrét lánchoz

                segment_start = point  # A szakasz új kezdőpontja az imént beszúrt pont lesz
                dx = segment_end[0] - segment_start[0]  # Hátralévő szakasz X távolságának frissítése
                dy = segment_end[1] - segment_start[1]  # Hátralévő szakasz Y távolságának frissítése
                segment_length = math.hypot(dx, dy)  # Hátralévő szakasz hosszának újraszámolása
                remaining_distance = spacing  # Visszaállítjuk a teljes lépésközt a következő ponthoz

            remaining_distance -= segment_length  # Levonjuk a szakaszból megmaradt tört távolságot
            segment_start = segment_end  # Átlépünk a következő szakaszra

        if waypoints[-1] != path[-1]:  # Ha a lépésközök miatt a legvégső pont kimaradt volna
            waypoints.append(path[-1])  # Explicit hozzáadjuk a pontos célpontot

        return waypoints  # Visszaadjuk a kiszámított, egyenletes pontlistát

    def _update_pruned_lookahead_target(self, state: Any) -> Tuple[Point2D, int]:
        """Elvégzi a szakasz-metszést (pruning) és kijelöli az előretekintő célpontot."""
        search_window: int = 25  # Keresési ablak mérete (ennyi pontot vizsgál előre a robot előtt)
        end_search: int = min(len(self.waypoints), self.waypoint_index + search_window)  # Keresés felső indexe

        min_dist: float = float("inf")  # Legkisebb távolság kezdeti értéke végtelenre állítva
        closest_idx: int = self.waypoint_index  # Legközelebbi pont indexének tárolója

        for i in range(self.waypoint_index, end_search):  # Ciklus az előretekintési ablakon
            dist: float = math.hypot(self.waypoints[i][0] - state.x, self.waypoints[i][1] - state.y)  # Távolság mérése
            if dist < min_dist:  # Ha találtunk közelebbi pontot a robot pillanatnyi helyéhez
                min_dist = dist  # Elmentjük az új minimális távolságot
                closest_idx = i  # Elmentjük a legközelebbi pont sorszámát

        self.waypoint_index = max(self.waypoint_index, closest_idx)  # Monotonitás: index nem léphet vissza

        # Adaptív előretekintési távolság a pillanatnyi transzlációs sebesség (v) alapján: [0.35m - 0.80m]
        lookahead_distance: float = max(0.35, min(0.80, abs(state.v) * 1.2))

        accumulated_dist: float = 0.0  # Görbe mentén kumulált ívhossz összegzője
        target_idx: int = self.waypoint_index  # A kijelölt előretekintési pont indexe

        for i in range(self.waypoint_index, len(self.waypoints) - 1):  # Ívhossz összegzése a metszett indextől
            p1: Point2D = self.waypoints[i]  # Szakasz kezdőpontja
            p2: Point2D = self.waypoints[i + 1]  # Szakasz végpontja
            accumulated_dist += math.hypot(p2[0] - p1[0], p2[1] - p1[1])  # Távolság hozzáadása az ívhosszhoz
            if accumulated_dist >= lookahead_distance:  # Ha elértük a sebességfüggő előretekintést
                target_idx = i + 1  # Kijelöljük ezt a pontot közvetlen célpontnak
                break  # Megvan a pont, kilépünk a ciklusból
        else:
            target_idx = len(self.waypoints) - 1  # Ha elfogyott a pálya, a legutolsó pontra állunk rá

        return self.waypoints[target_idx], target_idx  # Visszaadjuk a koordinátát és annak indexét

    def plan_global(
        self,
        start_world: Point2D,  # Start pozíció világkoordinátában (x, y) [m]
        goal_world: Point2D,  # Cél pozíció világkoordinátában (x, y) [m]
        heuristic: Optional[Any] = None,  # Egyedi A* heurisztika függvény (ha nincs, euklideszi)
        smooth: bool = True,  # Engedélyezze-e a Bézier íves simítást
        samples_per_curve: int = 8,  # Görbénkénti mintavételi pontok száma a simításnál
        max_cut_distance: Optional[float] = None,  # Saroklevágás maximális megengedett távolsága
    ) -> Optional[Tuple[Point2D, ...]]:
        """Globális A* keresés, saroksimítás és waypoint lánc generálása."""
        start_grid: GridCoord = self.grid_map.world_to_grid(*start_world)  # Start átváltása rácskoordinátára
        goal_grid: GridCoord = self.grid_map.world_to_grid(*goal_world)  # Cél átváltása rácskoordinátára

        raw_path: Optional[List[GridCoord]] = astar_search(  # A* útvonalkeresés futtatása a rácson
            self.grid_map,  # Bemeneti térkép
            start_grid,  # Kezdőcella
            goal_grid,  # Célcella
            diagonal=self.diagonal,  # 8-irányú szomszédság vizsgálata
            heuristic=heuristic,  # Heurisztika átadása
        )

        if raw_path is None:  # Ha nincs járható út a start és a cél között
            self.path.clear()  # Végleges út ürítése
            self.astar_path.clear()  # Nyers A* út ürítése
            self.bezier_path.clear()  # Simított út ürítése
            self.waypoints.clear()  # Diszkrét pontok ürítése
            self.waypoint_index = 0  # Index nullázása
            return None  # Tervezési hiba jelzése

        # A* cellaindexek visszaváltása méter alapú világkoordinátákra
        self.astar_path = [self.grid_map.grid_to_world(r, c) for r, c in raw_path]

        if smooth:  # Ha kértünk saroklekerekítést
            if max_cut_distance is None:  # Ha nincs explicit beállítva vágási limit
                max_cut_distance = 0.5 * self.grid_map.resolution  # Fél cellányi felbontást engedünk vágni

            smoothed_raw_path = smooth_path(  # Bézier simítás végrehajtása
                self.grid_map,  # Térkép az ütközésmentes ívekhez
                raw_path,  # Nyers rácsútvonal
                diagonal=self.diagonal,  # Átlós mozgás figyelembevétele
                samples_per_curve=samples_per_curve,  # Ívminták sűrűsége
                max_cut_distance=max_cut_distance,  # Maximális sarokvágási távolság
            )
            # Simított rácspontok transzformálása világkoordinátákra
            self.bezier_path = [self.grid_map.grid_to_world(r, c) for r, c in smoothed_raw_path]
        else:
            self.bezier_path = list(self.astar_path)  # Simítás nélkül az A* út marad

        self.path = list(self.bezier_path)  # Aktív trajektória frissítése
        self.waypoints = self._create_waypoints(self.path, self.waypoint_spacing)  # Egyenletes újramintavétel
        self.waypoint_index = min(1, len(self.waypoints) - 1)  # Az első aktív waypoint

        return tuple(self.path)  # Útvonal visszaadása konstans tuple formátumban

    def plan_local(self, state: Any, obstacles: Sequence[Any] = ()) -> Optional[Dict[str, Any]]:
        """Egy vezérlési ciklust hajt végre: célpontot frissít és DWA parancsot generál."""
        if not self.waypoints:  # Ha nincs követhető waypoint generálva
            return None  # Nincs feladat, visszatérés

        if self.reached_goal(state):  # Ha a robot beért a legvégső cél toleranciakörébe
            return {
                "waypoint": self.waypoints[-1],  # Elért utolsó pont
                "target": self.waypoints[-1],  # Célként rögzített utolsó pont
                "best_pair": [0.0, 0.0, 0.0, 0.0],  # Nulla sebesség: robot megállítása [v, w, ...]
                "safe_pairs": [],  # Nincsenek további vizsgált ágak
                "all_pairs": [],  # Nincsenek további vizsgált ágak
                "finished": True,  # Sikeres célba érés flag-je
            }

        current = self.waypoints[self.waypoint_index]
        current_tolerance = self._current_tolerance(state)
        if self.waypoint_index < len(self.waypoints) - 1:
            next_point = self.waypoints[self.waypoint_index + 1]
            to_current = (current[0] - state.x, current[1] - state.y)
            next_direction = (
                next_point[0] - current[0],
                next_point[1] - current[1],
            )
            passed_waypoint = (
                to_current[0] * next_direction[0]
                + to_current[1] * next_direction[1]
                < 0
            )
            if (
                math.hypot(current[0] - state.x, current[1] - state.y)
                <= current_tolerance
                or passed_waypoint
            ) and abs(state.v) <= 0.3:
                self.waypoint_index += 1

        target = self.waypoints[self.waypoint_index]
        is_final_waypoint: bool = self.waypoint_index == len(self.waypoints) - 1
        slow_down_distance: float = 0.5 if is_final_waypoint else 0.35  # Végcélnál korábban kezdünk lassítani

        # Lassítás engedélyezése ha konfigurálva van, vagy ha a pálya legvégére értünk
        enable_slowdown: bool = (
            getattr(self.config, "enable_waypoint_slowdown", False) or is_final_waypoint
        )

        goal = Goal(  # DWA lokális célpont objektum példányosítása
            target[0],  # Cél X koordinátája
            target[1],  # Cél Y koordinátája
            self.waypoint_tolerance,  # Célhoz tartozó hibatűrés
            slow_down=enable_slowdown,  # Sebességcsökkentési kényszer bekapcsolása
            slow_down_distance=slow_down_distance,  # Lassítási zóna sugara
        )

        # DWA sebességtér kiértékelése: optimális sebességpár és ütközésmentes alternatívák
        best_pair, safe_pairs = optimisation(self.config, state, goal, obstacles)
        all_pairs = pairstochoose(self.config, state)  # Az összes kinematikailag lehetséges ablak-mintavétel

        return {
            "waypoint": self.waypoints[self.waypoint_index],  # Aktív referencia-waypoint
            "target": target,  # DWA által közvetlenül célzott előretekintési pont
            "best_pair": best_pair,  # Kiválasztott optimális beavatkozójel: [v, w, ...]
            "safe_pairs": safe_pairs,  # Ütközésmentes pályák halmaza (megjelenítéshez/naplózáshoz)
            "all_pairs": all_pairs,  # Összes dinamikai ablakba eső sebességpár
            "finished": self.reached_goal(state),  # Végcél elérési állapotának visszajelzése
        }

    def reached_goal(self, state: Any) -> bool:
        """Megvizsgálja, hogy a robot elérte-e a globális végcélt a dinamikus tolerancián belül."""
        if not self.waypoints:  # Ha nincs útvonal
            return False  # Nem érhettünk célba

        goal_x, goal_y = self.waypoints[-1]  # Globális cél X és Y pozíciója
        dist_to_goal: float = math.hypot(goal_x - state.x, goal_y - state.y)  # Aktuális távolság a célig
        return dist_to_goal <= self._current_tolerance(state)  # Távolság összevetése a szűkített toleranciával