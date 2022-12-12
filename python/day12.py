from dataclasses import dataclass
from queue import Queue

from utils import get_data


class Maze:
    directions = (
        (0, 1), (0, -1),
        (1, 0), (-1, 0),
    )

    def __init__(self, lines):
        self.map = []
        for y, line in enumerate(lines):
            row = []
            for x, character in enumerate(line):
                elevation = ord(character)
                if character == 'S':
                    self.start = (x, y)
                    elevation = ord('a')
                if character == 'E':
                    self.end = (x, y)
                    elevation = ord('z')
                row.append(elevation)
            self.map.append(row)

    def get_edges_from(self, x, y):
        edges = []
        for d in self.directions:
            xx, yy = x + d[0], y + d[1]
            if xx < 0 or yy < 0 or xx > len(self.map[0]) - 1 or yy > len(self.map) - 1:
                continue
            from_elevation, to_elevation = self.map[y][x], self.map[yy][xx]
            if to_elevation > from_elevation + 1:
                continue
            edges.append((xx, yy))
        return edges

    def starting_points(self):
        points = []
        for y, row in enumerate(self.map):
            for x, elevation in enumerate(row):
                if chr(elevation) == 'a':
                    points.append((x, y))
        return points

    def print(self, current, visited):
        for y, row in enumerate(self.map):
            for x, character in enumerate(row):
                if (x, y) == current:
                    print('*', end='')
                elif (x, y) in visited:
                    print('#', end='')
                else:
                    print(chr(character), end='')
            print()

    def bfs(self, start=None):
        if start is None:
            start = self.start

        visited = {start}
        queue = [start]
        parent = {start: None}

        found = False
        while queue:
            current = queue.pop(0)
            if current == maze.end:
                found = True
                break

            for edge in self.get_edges_from(*current):
                if edge not in visited:
                    visited.add(edge)
                    queue.append(edge)
                    parent[edge] = current

        path = []
        end = maze.end

        if not found:
            return 0
        path.append(end)

        while parent.get(end):
            path.append(parent[end])
            end = parent[end]

        path.reverse()

        return len(path) - 1


maze = Maze(get_data(12))

print(maze.bfs())
print(min([maze.bfs(s) for s in maze.starting_points()]))
