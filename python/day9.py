from utils import get_data


class Knot:
    def __init__(self, name, prev=None, next=None):
        self.name = name
        self.prev = prev
        self.next = next
        self.x = 0
        self.y = 0
        self.visited = set()

    def __str__(self):
        return f'({self.x}, {self.y})'

    @property
    def coordinates(self):
        return (self.x, self.y)

    def move_up(self):
        self.y += 1

    def move_down(self):
        self.y -= 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def is_touching(self):
        return self.prev.x - 1 <= self.x <= self.prev.x + 1 and self.prev.y - 1 <= self.y <= self.prev.y + 1

    def follow(self):
        if self.is_touching():
            return

        if self.is_in_column_of():
            self.move_down() if self.is_above() else self.move_up()
            return

        if self.is_in_row_of():
            self.move_right() if self.is_left_of() else self.move_left()
            return

        if self.is_below():
            self.move_up()
            self.move_left() if self.is_right_of() else self.move_right()
            return

        if self.is_above():
            self.move_down()
            self.move_left() if self.is_right_of() else self.move_right()
            return

    def is_in_row_of(self):
        return self.y == self.prev.y

    def is_in_column_of(self):
        return self.x == self.prev.x

    def is_left_of(self):
        return self.x < self.prev.x

    def is_right_of(self):
        return self.x > self.prev.x

    def is_above(self):
        return self.y > self.prev.y

    def is_below(self):
        return self.y < self.prev.y

    def add_coordinates(self):
        self.visited.add(self.coordinates)


class Rope:
    start = (0, 0)

    def __init__(self, length):
        self.head = Knot(name='H')
        knot = self.head
        for i in range(1, length):
            name = 'T' if i == length - 1 else str(i)
            knot.next = Knot(name=name, prev=knot)
            knot = knot.next

    def process_move(self, move):
        parts = move.split(' ')
        direction, distance = self.get_direction(parts[0]), int(parts[1])
        for _ in range(distance):
            direction()
            knot = self.head
            while knot.next is not None:
                knot.next.follow()
                knot.next.add_coordinates()
                knot = knot.next

    def get_direction(self, move):
        return {
            'U': self.head.move_up,
            'D': self.head.move_down,
            'L': self.head.move_left,
            'R': self.head.move_right,
        }[move]

    @property
    def tail(self):
        knot = self.head
        while knot.next is not None:
            knot = knot.next
        return knot


def main():
    moves = get_data(9)

    rope = Rope(2)
    for move in moves:
        rope.process_move(move)
    part1 = len(rope.tail.visited)

    rope = Rope(10)
    for move in moves:
        rope.process_move(move)
    part2 = len(rope.tail.visited)

    return part1, part2


if __name__ == '__main__':
    print(main())
