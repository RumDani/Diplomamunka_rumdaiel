"""Grid-based A* planner."""

import heapq
import math


class Grid:
    def __init__(self, width, height, resolution, origin_x, origin_y):
        self.width, self.height = width, height
        self.resolution = resolution
        self.origin_x, self.origin_y = origin_x, origin_y
        self.cells = [[False] * width for _ in range(height)]

    def in_bounds(self, row, column):
        return 0 <= row < self.height and 0 <= column < self.width

    def free(self, row, column):
        return self.in_bounds(row, column) and not self.cells[row][column]

    def world_to_grid(self, x, y):
        return (math.floor((y - self.origin_y) / self.resolution),
                math.floor((x - self.origin_x) / self.resolution))

    def grid_to_world(self, row, column):
        return (self.origin_x + (column + 0.5) * self.resolution,
                self.origin_y + (row + 0.5) * self.resolution)

    def add_obstacle(self, x, y, radius):
        center = self.world_to_grid(x, y)
        cells = math.ceil(radius / self.resolution)
        for row in range(center[0] - cells, center[0] + cells + 1):
            for column in range(center[1] - cells, center[1] + cells + 1):
                if self.in_bounds(row, column):
                    cx, cy = self.grid_to_world(row, column)
                    if math.hypot(cx - x, cy - y) <= radius + self.resolution:
                        self.cells[row][column] = True


def astar(grid, start, goal, diagonal=True):
    if not grid.free(*start) or not grid.free(*goal):
        return []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if diagonal:
        directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def heuristic(cell):
        return math.hypot(goal[0] - cell[0], goal[1] - cell[1])

    queue = [(heuristic(start), 0.0, start)]
    parents, costs = {}, {start: 0.0}
    while queue:
        _, current_cost, current = heapq.heappop(queue)
        if current_cost > costs[current]:
            continue
        if current == goal:
            path = [current]
            while current in parents:
                current = parents[current]
                path.append(current)
            return list(reversed(path))
        for dr, dc in directions:
            neighbor = current[0] + dr, current[1] + dc
            if not grid.free(*neighbor):
                continue
            if dr and dc and (not grid.free(current[0] + dr, current[1])
                              or not grid.free(current[0], current[1] + dc)):
                continue
            cost = current_cost + (math.sqrt(2) if dr and dc else 1.0)
            if cost < costs.get(neighbor, math.inf):
                costs[neighbor] = cost
                parents[neighbor] = current
                heapq.heappush(queue, (cost + heuristic(neighbor), cost, neighbor))
    return []
