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
        return (
            min(x for x, _, _ in self.cubes) - 1,
            min(y for _, y, _ in self.cubes) - 1,
            min(z for _, _, z in self.cubes) - 1,
        )

    @cached_property
    def end(self):
        return (
            max(x for x, _, _ in self.cubes) + 1,
            max(y for _, y, _ in self.cubes) + 1,
            max(z for _, _, z in self.cubes) + 1,
        )

    def get_neighbors(self, cube):
        x, y, z = cube
        return {(x + dx, y + dy, z + dz) for dx, dy, dz in DELTAS}

    def out_of_bounds(self, cube):
        return any(n < self.start[i] or n > self.end[i] for i, n in enumerate(cube))

    @cached_property
    def open_sides(self):
        return [neighbor for cube in self.cubes for neighbor in self.get_neighbors(cube) if neighbor not in self.cubes]

    @cached_property
    def surface_area(self):
        return len(self.open_sides)

    @cached_property
    def outside_surface_area(self):
        outside_cubes = set()
        candidates = [self.start]
        while candidates:
            cube = candidates.pop()
            outside_cubes.add(cube)
            for neighbor in self.get_neighbors(cube):
                if self.out_of_bounds(neighbor):
                    continue
                if neighbor in self.cubes or neighbor in outside_cubes:
                    continue
                candidates.append(neighbor)
        return sum(
            neighbor in outside_cubes for cube in self.cubes for neighbor in self.get_neighbors(cube)
        )


def main():
    lines = get_data(18)
    cubes = {tuple(([int(n) for n in line.split(',')])) for line in lines}
    droplet = LavaDroplet(cubes)
    return droplet.surface_area, droplet.outside_surface_area


if __name__ == '__main__':
    print(main())
