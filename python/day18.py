from dataclasses import dataclass
from functools import cached_property

from utils import get_data

DELTAS = (
    (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (-1, 0, 0), (0, -1, 0), (0, 0, -1),
)


@dataclass
class LavaDroplet:
    cubes: set[tuple[int, int, int]]

    @cached_property
    def start(self):
        return min(min(point) for point in self.cubes) - 1

    @cached_property
    def end(self):
        return min(min(point) for point in self.cubes) - 1

    def get_neighbors(self, cube):
        x, y, z = cube
        return {c for dx, dy, dz in DELTAS if not self.out_of_bounds(c := (x + dx, y + dy, z + dz))}

    def out_of_bounds(self, cube):
        for n in cube:
            if not self.start < n < self.end:
                return False
        return True

    @cached_property
    def open_sides(self):
        sides = []
        for cube in self.cubes:
            sides.extend(
                [n for n in self.get_neighbors(cube) if n not in self.cubes]
            )
        return sides

    @cached_property
    def surface_area(self):
        return len(self.open_sides)


def main():
    lines = get_data(18)
    cubes = {tuple(([int(n) for n in line.split(',')])) for line in lines}
    droplet = LavaDroplet(cubes)
    return droplet.surface_area


if __name__ == '__main__':
    print(main())
