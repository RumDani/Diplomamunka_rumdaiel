"""Egyszeru racsterkep az A* algoritmushoz."""

import math


class GridMap:
    """Negyzetes cellakbol allo, ketdimenzios terkep."""

    def __init__(
        self,
        width,
        height,
        resolution=0.1,
        origin_x=0.0,
        origin_y=0.0,
        unknown=False,
    ):
        if width <= 0 or height <= 0:
            raise ValueError("A terkep merete legyen pozitiv.")
        if resolution <= 0:
            raise ValueError("A felbontas legyen pozitiv.")

        self.width = width
        self.height = height
        self.resolution = resolution
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.grid = []

        initial_value = 2 if unknown else 0
        for _ in range(height):
            self.grid.append([initial_value] * width)

    def is_inside(self, row, column):
        """Megadja, hogy a cella a terkepen belul van-e."""
        return 0 <= row < self.height and 0 <= column < self.width

    def is_free(self, row, column):
        """Megadja, hogy a cella szabad-e."""
        return self.is_inside(row, column) and self.grid[row][column] == 0

    def world_to_grid(self, x, y):
        """Vilagkoordinatat (meterben) racskoordinatava alakit."""
        column = math.floor((x - self.origin_x) / self.resolution)
        row = math.floor((y - self.origin_y) / self.resolution)
        return row, column

    def grid_to_world(self, row, column):
        """A cella kozepontjat visszaadja vilagkoordinataban."""
        x = self.origin_x + (column + 0.5) * self.resolution
        y = self.origin_y + (row + 0.5) * self.resolution
        return x, y

    def add_obstacle(self, row, column):
        """Akadalykent megjelol egy cellat."""
        if not self.is_inside(row, column):
            raise ValueError("Az akadaly a terkepen kivul van.")
        self.grid[row][column] = 1

    def remove_obstacle(self, row, column):
        """Szabad cellava tesz egy cellat."""
        if not self.is_inside(row, column):
            raise ValueError("A cella a terkepen kivul van.")
        self.grid[row][column] = 0

    def mark_free(self, row, column):
        """A robot altal megvizsgalt cellat szabadnak jelol."""
        if not self.is_inside(row, column):
            raise ValueError("A cella a terkepen kivul van.")
        self.grid[row][column] = 0

    def add_obstacle_world(self, x, y, radius=0.0):
        """Vilagkoordinatas akadalyat egy vagy tobb cellaba ir."""
        center_row, center_column = self.world_to_grid(x, y)
        cell_radius = int(radius / self.resolution) + 1

        for row in range(center_row - cell_radius, center_row + cell_radius + 1):
            for column in range(
                center_column - cell_radius,
                center_column + cell_radius + 1,
            ):
                if not self.is_inside(row, column):
                    continue
                cell_x, cell_y = self.grid_to_world(row, column)
                distance = ((cell_x - x) ** 2 + (cell_y - y) ** 2) ** 0.5
                if distance <= radius + self.resolution:
                    self.add_obstacle(row, column)

    def update_from_obstacles(self, obstacles):
        """Szimulacios akadalyobjektumokbol frissiti a terkepet.

        Az objektumoknak ``x``, ``y`` es opcionisan ``radius`` attributummal
        kell rendelkezniuk, ahogy az onlabos DWA Obstacle osztalyanak.
        """
        for obstacle in obstacles:
            radius = getattr(obstacle, "radius", 0.0)
            self.add_obstacle_world(obstacle.x, obstacle.y, radius)

    def inflate_obstacles(self, radius):
        """Biztonsagi tavolsaggal kitagitja az akadalycellakat."""
        if radius < 0:
            raise ValueError("A biztonsagi sugar nem lehet negativ.")
        if radius == 0:
            return

        obstacle_cells = [
            (row, column)
            for row in range(self.height)
            for column in range(self.width)
            if self.grid[row][column] == 1
        ]
        cell_radius = math.ceil(radius / self.resolution)

        for obstacle_row, obstacle_column in obstacle_cells:
            for row in range(
                obstacle_row - cell_radius,
                obstacle_row + cell_radius + 1,
            ):
                for column in range(
                    obstacle_column - cell_radius,
                    obstacle_column + cell_radius + 1,
                ):
                    if self.is_inside(row, column):
                        self.grid[row][column] = 1

    def get_neighbors(self, row, column, diagonal=False):
        """Visszaadja a szabad szomszedos cellakat."""
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        if diagonal:
            directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        neighbors = []
        for row_change, column_change in directions:
            new_row = row + row_change
            new_column = column + column_change
            if self.is_free(new_row, new_column):
                is_diagonal = row_change != 0 and column_change != 0
                if is_diagonal:
                    if not self.is_free(row, new_column):
                        continue
                    if not self.is_free(new_row, column):
                        continue
                neighbors.append((new_row, new_column))

        return neighbors

    def print_map(self, start=None, goal=None):
        """Kiirja a terkepet: . szabad, # akadaly, ? ismeretlen."""
        for row in range(self.height):
            line = ""
            for column in range(self.width):
                position = (row, column)
                if position == start:
                    line += "S"
                elif position == goal:
                    line += "G"
                elif self.grid[row][column] == 1:
                    line += "#"
                elif self.grid[row][column] == 2:
                    line += "?"
                else:
                    line += "."
            print(line)


if __name__ == "__main__":
    example_map = GridMap(width=10, height=6)
    example_map.add_obstacle(2, 3)
    example_map.add_obstacle(2, 4)
    example_map.add_obstacle(2, 5)
    example_map.print_map(start=(0, 0), goal=(5, 9))
