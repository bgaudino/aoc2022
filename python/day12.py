from utils import get_data


class HeightMap:
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

    def bfs(self, start=None):
        visited = {start or self.start}
        queue = [(start or self.start, -1)]

        while queue:
            current, steps = queue.pop(0)
            steps += 1
            if current == self.end:
                return steps

            for edge in self.get_edges_from(*current):
                if edge not in visited:
                    visited.add(edge)
                    queue.append((edge, steps))

        return -1


def main():
    maze = HeightMap(get_data(12))
    return maze.bfs(), min(
        [steps for start in maze.starting_points() if (steps := maze.bfs(start)) >= 0]
    )


if __name__ == '__main__':
    print(main())
