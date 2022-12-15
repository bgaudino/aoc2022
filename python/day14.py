from utils import get_data


class Cave:
    sand_start = (500, 0)
    _x_start = None
    _x_end = None
    _y_end = None

    def __init__(self, paths, has_infinite_floor=False):
        self.sand = set()
        self.rocks = self.add_rocks(paths)
        self.has_infinite_floor = has_infinite_floor
        if has_infinite_floor:
            self.add_infinite_floor()

    def print(self, current=None):
        x_start = self.x_start - 50 if self.has_infinite_floor else self.x_start
        x_end = self.x_end + 50 if self.has_infinite_floor else self.x_end
        for y in range(self.y_end):
            for x in range(x_start, x_end):
                if (x, y) == current:
                    print('*', end='')
                elif (x, y) == self.sand_start:
                    print('+', end='')
                elif (x, y) in self.rocks or self.on_floor((x, y)):
                    print('#', end='')
                elif (x, y) in self.sand:
                    print('o', end='')
                else:
                    print('.', end='')
            print()
        print()

    @property
    def x_start(self):
        if self._x_start is None:
            self._x_start = min({x for x, _ in self.rocks}) - 1
        return self._x_start

    @property
    def y_start(self):
        return 0

    @property
    def x_end(self):
        if self._x_end is None:
            self._x_end = max({x for x, _ in self.rocks}) + 1
        return self._x_end

    @property
    def y_end(self):
        if self._y_end is None:
            self._y_end = max({y for _, y in self.rocks}) + 1
        return self._y_end

    def on_floor(self, point):
        return self.has_infinite_floor and point[1] == self.y_end - 1

    def is_available(self, point):
        return not (point in self.rocks or point in self.sand or self.on_floor(point))

    def is_overflowed(self, x, y):
        return y >= self.y_end

    def fall(self):
        while self.add_sand():
            pass

    def add_sand(self):
        x, y = self.sand_start
        while True:
            # falls into the abyss
            if self.is_overflowed(x, y):
                return False

            # move down
            if self.is_available((x, y + 1)):
                y = y + 1

            # down and left
            elif self.is_available((x - 1, y + 1)):
                x, y = x - 1, y + 1

            # down and right
            elif self.is_available((x + 1, y + 1)):
                x, y = x + 1, y + 1

            # comes to rest or blocks start
            else:
                self.sand.add((x, y))
                return (x, y) != self.sand_start

    def add_rocks(self, paths):
        rocks = set()
        for p in paths:
            prev = None
            for x, y in p:
                rocks.add((x, y))
                if prev is None:
                    prev = (x, y)
                    continue

                xx, yy = prev
                if x == xx:
                    # vertical
                    start, stop = min(y, yy), max(y, yy)
                    while start < stop:
                        rocks.add((x, start))
                        start += 1

                if y == yy:
                    # horizontal
                    start, stop = min(x, xx), max(x, xx)
                    while start < stop:
                        rocks.add((start, y))
                        start += 1

                prev = (x, y)
        return rocks

    def add_infinite_floor(self):
        for x in range(self.x_start, self.x_end):
            self.rocks.add((x, self.y_end + 1))
        self._y_end = None


def main():
    paths = [parse_path(p) for p in get_data(14)]

    cave_with_abyss = Cave(paths)
    cave_with_abyss.fall()

    cave_with_infinite_floor = Cave(paths, has_infinite_floor=True)
    cave_with_infinite_floor.fall()

    return len(cave_with_abyss.sand), len(cave_with_infinite_floor.sand)


def parse_path(path):
    return [(int((r := p.split(','))[0]), int(r[1])) for p in path.split(' -> ')]


if __name__ == '__main__':
    print(main())
