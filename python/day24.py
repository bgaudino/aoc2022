from dataclasses import dataclass
from functools import cached_property

from utils import get_data

DIRECTIONS = {
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
    '^': (0, -1),
    '.': (0, 0),
}


@dataclass
class Basin:
    wall: set[tuple[int, int]]
    blizzards: set[tuple[int, int]]

    def __post_init__(self):
        self.location = self.start

    @cached_property
    def start(self):
        for x in range(self.width):
            if (x, 0) not in self.wall:
                return (x, 0)

    @cached_property
    def goal(self):
        for x in range(self.width):
            if (x, self.height - 1) not in self.wall:
                return (x, self.height - 1)

    def is_blocked(self, location, blizzards):
        return location in self.wall or location in blizzards or location[1] < 0 or location[1] >= self.height

    def edges(self, location, blizzards):
        neighbors = [
            (location[0] + d[0], location[1] + d[1])
            for d in DIRECTIONS.values()
        ]
        return [n for n in neighbors if not self.is_blocked(n, blizzards)]

    @cached_property
    def height(self):
        return max(y for _, y in self.wall) + 1

    @cached_property
    def width(self):
        return max(x for x, _ in self.wall) + 1

    def print_map(self, location=None, blizzards=None):
        if location is None:
            location = self.location
        if blizzards is None:
            blizzards = self.blizzards
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == location:
                    print('E', end='')
                elif (x, y) in self.blizzards:
                    if len(self.blizzards[(x, y)]) == 1:
                        print(self.blizzards[(x, y)][0], end='')
                    else:
                        print(len(self.blizzards[(x, y)]), end='')
                elif (x, y) in self.wall:
                    print('#', end='')
                else:
                    print('.', end='')
            print()
        print()

    def move_blizzards(self, blizzards):
        new_blizzards = {}
        for location, blizzards in blizzards.items():
            for blizzard in blizzards:
                x, y = location
                dx, dy = DIRECTIONS[blizzard]
                next_space = (x + dx, y + dy)
                if next_space in self.wall:
                    match blizzard:
                        case '>':
                            next_space = (1, y)
                        case 'v':
                            next_space = (x, 1)
                        case '<':
                            next_space = (self.width - 2, y)
                        case '^':
                            next_space = (x, self.height - 2)
                if next_space in new_blizzards:
                    new_blizzards[next_space].append(blizzard)
                else:
                    new_blizzards[next_space] = [blizzard]
        return new_blizzards

    def distance_to_goal(self, location):
        return abs(location[0] - self.goal[0]) + abs(location[1] - self.goal[1])

    def bfs(self, blizzards=None, reverse=False):
        start = self.start if not reverse else self.goal
        goal = self.goal if not reverse else self.start
        blizzards_list = [blizzards or self.blizzards]
        visited = {(start, 0)}
        queue = [(start, 0)]
        while queue:
            current, minutes = queue.pop(0)
            try:
                blizzards = blizzards_list[minutes]
            except IndexError:
                blizzards_list.append(self.move_blizzards(blizzards_list[-1]))
                blizzards = blizzards_list[-1]
            for edge in self.edges(current, blizzards):
                if edge == goal:
                    return minutes, blizzards
                if (edge, minutes + 1) not in visited:
                    queue.append((edge, minutes + 1))
                    visited.add((edge, minutes + 1))
            queue.sort(key=lambda x: (x[1], self.distance_to_goal(x[0])))
        return -1


def parse():
    wall = set()
    blizzards = dict()
    lines = get_data(24)
    for y, line in enumerate(lines):
        for x, space in enumerate(line):
            if space == '.':
                continue
            if space == '#':
                wall.add((x, y))
            else:
                blizzards[(x, y)] = [space]
    return wall, blizzards


def main():
    basin = Basin(*parse())
    trip1, blizzards = basin.bfs()
    trip2, blizzards = basin.bfs(reverse=True, blizzards=blizzards)
    trip3, blizzards = basin.bfs(blizzards=blizzards)
    return trip1, trip1 + trip2 + trip3


if __name__ == '__main__':
    print(main())
