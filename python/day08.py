from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from math import prod

from utils import get_data


class Forest:
    def __init__(self, data):
        rows = []
        for i, line in enumerate(data):
            row = []
            for j, tree in enumerate(line):
                row.append(Tree(tree, (j, i), self))
            rows.append(row)
        self.grid = rows
        self._trees_visible_from_outside = 0
        self._scenic_score = 0

    def search_grid(self):
        trees_visible_from_outside = 0
        scenic_score = 0
        for row in self.grid:
            for tree in row:
                search = [
                    tree.is_visible_from_outside(Directions.NORTH.value),
                    tree.is_visible_from_outside(Directions.SOUTH.value),
                    tree.is_visible_from_outside(Directions.EAST.value),
                    tree.is_visible_from_outside(Directions.WEST.value),
                ]
                if len([t for t in search if t[0]]):
                    trees_visible_from_outside += 1
                scenic_score = max(scenic_score, prod([t[1] for t in search]))
        self._trees_visible_from_outside = trees_visible_from_outside
        self._scenic_score = scenic_score
        return trees_visible_from_outside, scenic_score

    @cached_property
    def trees_visible_from_outside(self):
        return self._trees_visible_from_outside or self.search_grid()[0]

    @cached_property
    def scenic_score(self):
        return self._scenic_score or self.search_grid()[1]

    @cached_property
    def height(self):
        return len(self.grid)

    @cached_property
    def width(self):
        return len(self.grid[0])


class Directions(Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)


@dataclass
class Tree:
    height: int
    coordinates: tuple[int, int]
    parent: Forest

    def is_visible_from_outside(self, direction: Directions):
        is_visible = True
        scenic_score = 0
        x, y = self.coordinates
        x += direction[0]
        y += direction[1]
        while 0 <= x < self.parent.width and 0 <= y < self.parent.height:
            scenic_score += 1
            if self.height <= self.parent.grid[y][x].height:
                is_visible = False
                break
            x += direction[0]
            y += direction[1]
        return is_visible, scenic_score


def main():
    forest = Forest(get_data(8))
    return forest.trees_visible_from_outside, forest.scenic_score


if __name__ == '__main__':
    print(main())
