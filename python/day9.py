from utils import get_data


class Knot:
    def __init__(self, prev=None, next=None):
        self.prev = prev
        self.next = next
        self.x = 0
        self.y = 0
        self.visited = set()

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

        if not self.is_in_column_of():
            self.move_left() if self.is_right_of() else self.move_right()

        if not self.is_in_row_of():
            self.move_down() if self.is_above() else self.move_up()

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
        self.visited.add((self.x, self.y))


class Rope:
    start = (0, 0)

    def __init__(self, length):
        self.head = Knot()
        knot = self.head
        for _ in range(1, length):
            knot.next = Knot(prev=knot)
            knot = knot.next

    def process_move(self, move):
        direction, distance = move.split(' ')
        for _ in range(int(distance)):
            match direction:
                case 'U':
                    self.head.move_up()
                case 'D':
                    self.head.move_down()
                case 'L':
                    self.head.move_left()
                case 'R':
                    self.head.move_right()
            knot = self.head
            while knot.next is not None:
                knot.next.follow()
                knot.next.add_coordinates()
                knot = knot.next

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
