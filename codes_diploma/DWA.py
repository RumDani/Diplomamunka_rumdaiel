"""Dinamikus ablakos lokális útvonaltervezés (Dynamic Window Approach - DWA)."""

import math
import numpy as np
from .robot import get_robot_kinematics, robotstate, update


"""
Kiszámítja a megtett utat az ív mentén az első ütközésig.
Ha nincs ütközés a predict_time alatt, egy nagy értéket ad vissza.
"""
def get_dist_on_trajectory(state, config, w_L, w_R, obstacle_list):
    temp_robot = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
    accumulated_dist = 0.0
    v_actual, _ = get_robot_kinematics(w_L, w_R, config)
    
    # --- SZENZOR PARAMÉTEREK ---
    max_sensor_dist = 3.0  # 3 méterig lát el a LiDAR
    fov_angle = math.radians(180)  # 180 fokos látószög elöl
    
    for t in np.arange(0, config.predict_time, config.dt):
        for obs in obstacle_list:
            # 1. Szenzor szűrés: Csak azt látja, ami közel van
            dist_now = math.hypot(state.x - obs.x, state.y - obs.y)
            if dist_now > max_sensor_dist:
                continue
                
            # 2. FOV szűrés: Csak azt látja, ami előtte van (+-90 fok)
            angle_to_obs = math.atan2(obs.y - state.y, obs.x - state.x)
            diff_angle = math.atan2(
                math.sin(angle_to_obs - state.irany),
                math.cos(angle_to_obs - state.irany)
            )
            if abs(diff_angle) > fov_angle / 2:
                continue

            # 3. DINAMIKUS PREDIKCIÓ: Hol lesz az akadály 't' idő múlva?
            obs_future_x = obs.x + obs.vx * t
            obs_future_y = obs.y + obs.vy * t
            
            dist_centers = math.hypot(temp_robot.x - obs_future_x, temp_robot.y - obs_future_y)
            
            # 4. KÜLÖNVÁLASZTOTT INFLÁCIÓ: Statikus fal mellett szűk ráhagyás, mozgónál teljes
            is_static = (obs.vx == 0.0 and obs.vy == 0.0)
            if is_static:
                collision_threshold = obs.radius + config.rob_radius + getattr(config, "static_safety_margin", 0.01)
            else:
                collision_threshold = config.rob_radius + obs.radius + config.safety_margin
            
            if dist_centers <= collision_threshold:
                return accumulated_dist 
        
        # Állapotfrissítés az ív mentén
        update(temp_robot, config, w_L, w_R, config.dt)
        accumulated_dist += abs(v_actual) * config.dt
                
    return 10.0


#############xx FÉKEZÉSI FELTÉTELEK ###############
def AdmissableVelocity(robotconfig, w_L, w_R, state, obstacle_list):
    """
    Ellenőrzi, hogy a robot meg tud-e állni az adott íven az ütközés előtt.
    """
    # 1. Kiszámítjuk a távolságot az ív mentén az ütközésig
    dist_to_obs = get_dist_on_trajectory(state, robotconfig, w_L, w_R, obstacle_list)
    
    # 2. Megkapjuk a lineáris sebességet (v)
    v, _ = get_robot_kinematics(w_L, w_R, robotconfig)
    
    # Fékezési feltétel: |v| <= sqrt(2 * a_max * dist)
    if abs(v) <= math.sqrt(2 * robotconfig.a_max * dist_to_obs):
        return True
    return False


"""        
Összes választható v,w pár kiszámolása kerekekből számítva
"""
def pairstochoose(robotconfig, robotstate):

    w_dot_max = robotconfig.a_max / robotconfig.r_kerek         # w_dot = a / r
   
    w_L_min_actual = max(robotconfig.w_kerek_min, robotstate.w_L - w_dot_max * robotconfig.dt)
    w_L_max_actual = min(robotconfig.w_kerek_max, robotstate.w_L + w_dot_max * robotconfig.dt)

    w_R_min_actual = max(robotconfig.w_kerek_min, robotstate.w_R - w_dot_max * robotconfig.dt)
    w_R_max_actual = min(robotconfig.w_kerek_max, robotstate.w_R + w_dot_max * robotconfig.dt)
   
    w_L_samples = np.arange(w_L_min_actual, w_L_max_actual + robotconfig.w_kerek_resolution, robotconfig.w_kerek_resolution)
    w_R_samples = np.arange(w_R_min_actual, w_R_max_actual + robotconfig.w_kerek_resolution, robotconfig.w_kerek_resolution)

    all_pairs = []
    for w_L in w_L_samples:
        for w_R in w_R_samples:
            v, w = get_robot_kinematics(w_L, w_R, robotconfig)

            all_pairs.append([v, w, w_L, w_R])
    return all_pairs


########################Összes lehetséges választható pálya eltárolása ami biztonságos megállást biztosít#######################x

def safepairs(robotconfig, state, obstacle_list):
    """
    Eredő keresési tér (Vr = Vs ∩ Vd ∩ Va):
    Kiszűri azokat a sebességpárokat, amelyek kielégítik a megállási feltételt,
    és kiszűri a tolató pályákat (hacsak nincs kifejezetten engedélyezve a tolatás).
    """
    allow_reverse = getattr(robotconfig, "allow_reverse", False)
    
    admissible_list = []  # Ebben csak a "jó" párok lesznek
    
    for pair in pairstochoose(robotconfig, state):
        v = pair[0]
        w_L = pair[2]
        w_R = pair[3]
        
        # Előremeneti kényszer: ne válasszon tolatást vészmegoldásként
        if not allow_reverse and v < 0.0:
            continue
            
        if AdmissableVelocity(robotconfig, w_L, w_R, state, obstacle_list):
            admissible_list.append(pair)
                
    return admissible_list


################################################

############# optimalizáció #####################
def optimisation(robotconfig, state, goal, obstacle_list):
    # 1. Biztonságos sebességpárok lekérése
    safe_list = safepairs(robotconfig, state, obstacle_list)
    
    # Ha nincs biztonságos út (ÜRES A LISTA -> DEADLOCK)
    if not safe_list:
        # Visszaadunk egy speciális jelzést (None), hogy a főciklus tudja: Recovery kell
        return None, []

    best_score = -float('inf')
    best_pair = None
    
    dist_to_goal = math.hypot(goal.x - state.x, goal.y - state.y)
    v_max_robot = robotconfig.w_kerek_max * robotconfig.r_kerek
    
    # 2. Adaptív predikció: célhoz közeledve vagy éles szögeltérés esetén dinamikusan rövidül
    adaptive_predict_time = robotconfig.predict_time
    heading_to_goal = math.atan2(goal.y - state.y, goal.x - state.x)
    heading_error = abs(
        math.atan2(
            math.sin(heading_to_goal - state.irany),
            math.cos(heading_to_goal - state.irany),
        )
    )
    
    if dist_to_goal < 1.0:
        adaptive_predict_time = max(0.5, dist_to_goal * 2.0)
    
    alfa = robotconfig.Alfa      # Célra tartás súlya
    beta = robotconfig.Beta      # Akadálykerülés súlya
    gamma = robotconfig.Gamma    # Sebességszabályozás súlya

    for v, w, w_L, w_R in safe_list:  
        # Gyors szimuláció a jövőbeli állapot becsléséhez az adaptív időablak végéig
        temp_robot = robotstate(x=state.x, y=state.y, irany=state.irany, w_L=state.w_L, w_R=state.w_R)
        for _ in np.arange(0, adaptive_predict_time, robotconfig.dt):
            update(temp_robot, robotconfig, w_L, w_R, robotconfig.dt)
        
        # --- PONTOZÁSI LOGIKA ---

        # A: Heading score (Irányhiba normalizálva 0 és 1 közé, atan2 periodicitás-kezeléssel)
        angle_to_goal = getattr(goal, "heading", None)
        if angle_to_goal is None:
            angle_to_goal = math.atan2(goal.y - temp_robot.y, goal.x - temp_robot.x)
            
        error_angle = math.atan2(
            math.sin(angle_to_goal - temp_robot.irany), 
            math.cos(angle_to_goal - temp_robot.irany)
        )
        score_heading = (math.pi - abs(error_angle)) / math.pi
        
        # B: Dist score (Akadályoktól való távolság az ív mentén)
        score_dist = get_dist_on_trajectory(state, robotconfig, w_L, w_R, obstacle_list)
        
        # C: Velocity score (Szabad haladás esetén maximális tempó, cél közelében dinamikus lebegtetés)
        slow_down_distance = getattr(goal, "slow_down_distance", 0.8)
        if not getattr(goal, "slow_down", True) and dist_to_goal > slow_down_distance:
            score_vel = v / v_max_robot
        else:
            # Nem engedi a célsebességet 0-ra fulladni, dinamikusabban húz a cél felé
            v_target = min(v_max_robot, max(0.08, dist_to_goal * 1.4))
            score_vel = 1.0 - (abs(v_target - v) / v_max_robot)

        # Végső pontszám kiszámítása a költségfüggvény súlyaival
        score = (alfa * score_heading + 
                 beta * score_dist + 
                 gamma * score_vel)

        if score > best_score:
            best_score = score
            best_pair = [v, w, w_L, w_R]

    return best_pair, safe_list