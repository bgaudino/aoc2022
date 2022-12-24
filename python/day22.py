import math
from functools import cached_property

from utils import get_data

DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
SYMBOLS = ('>', 'v', '<', '^')


class Board:
    facing = 0
    move_index = 0

    def __init__(self, data):
        index = data.index('')
        board, instructions = data[:index], data[index + 1:][0]
        width = max(len(row) for row in board)
        grid = []
        for row in board:
            spaces = []
            for i in range(width):
                if i < len(row):
                    spaces.append(row[i])
                else:
                    spaces.append(' ')
            grid.append(spaces)
        self.grid = grid

        found = False
        for y, row in enumerate(grid):
            if found:
                break
            for x, space in enumerate(row):
                if space == '.':
                    self.start = (x, y)
                    self.location = (x, y)
                    found = True
                    break

        moves = []
        number_string = ''
        for char in instructions:
            if char in ('L', 'R'):
                moves.append(int(number_string))
                moves.append(char)
                number_string = ''
            else:
                number_string += char
        if number_string:
            moves.append(int(number_string))
        self.moves = moves
        self.states = {self.location: SYMBOLS[self.facing]}

    @property
    def current_move(self):
        return self.moves[self.move_index]

    def take_step(self):
        x, y = self.location
        dx, dy = DIRECTIONS[self.facing]
        # tx, ty = (x + dx) % len(self.grid[y]), (y + dy) % len(self.grid) # part 1?
        tx, ty = x + dx, y + dy
        try:
            return self.grid[ty][tx], (tx, ty)
        except IndexError:
            return ' ', self.location

    def rotate_clockwise(self):
        self.facing = (self.facing + 1) % 4

    def rotate_counter_clockwise(self):
        self.facing = (self.facing - 1) % 4

    def wrap_3d(self):
        side, x, y = self._on_side()
        # {from_side: {from_facing: (to_side, to_facing, new_x, new_y)}}
        side_map = {
            0: {
                2: (3, 0, 0, self.invert_coordinates(y)),
                3: (5, 0, 0, x),
            },
            1: {
                0:  (4, 2, self.side_length - 1, self.invert_coordinates(y)),
                1:  (2, 2, self.side_length - 1, x),
                3:  (5, 3, self.invert_coordinates(x), self.side_length - 1),
            },
            2: {
                0: (1, 1, y, self.side_length - 1),
                2: (3, 1, y, 0),
            },
            3: {
                2: (0, 0, 0, self.invert_coordinates(y)),
                3: (2, 0, 0, x),
            },
            4: {
                0: (1, 2, self.side_length - 1, self.invert_coordinates(y)),
                1: (5, 2, self.side_length - 1, x),
            },
            5: {
                0: (4, 3, y, self.side_length - 1),
                1: (1, 3, self.invert_coordinates(x), self.side_length - 1),
                2: (0, 3, y, 0),
            }
        }
        new_side, new_facing, xx, yy = side_map[side][self.facing]
        new_location = self.sides[new_side][yy][xx]
        can_wrap = self._can_wrap(
            self.grid[new_location[1]][new_location[0]]
        )
        self.location = new_location if can_wrap else self.location
        self.facing = new_facing if can_wrap else self.facing
        return can_wrap

    def invert_coordinates(self, n):
        i, j = 0, self.side_length - 1
        inverted = {}
        while i < self.side_length and j >= 0:
            inverted[i] = j
            i += 1
            j -= 1
        return inverted[n]

    def wrap_2d(self):
        if self.facing in [0, 2]:
            return self._wrap_horizontal()
        return self._wrap_vertical()

    def _wrap_vertical(self):
        x, _ = self.location
        if self.facing == 1:
            _range = range(len(self.grid))
        else:
            _range = range(len(self.grid) - 1, -1, -1)
        for y in _range:
            can_wrap = self._can_wrap(self.grid[y][x])
            if can_wrap is not None:
                self.location = (x, y) if can_wrap else self.location
                return can_wrap
        raise Exception('No spaces found in this row')

    def _wrap_horizontal(self):
        _, y = self.location
        row = self.grid[y]
        if self.facing == 0:
            _range = range(len(row))
        else:
            _range = range(len(row) - 1, -1, -1)
        for x in _range:
            can_wrap = self._can_wrap(self.grid[y][x])
            if can_wrap is not None:
                self.location = (x, y) if can_wrap else self.location
                return can_wrap
        raise Exception('No spaces found in this column')

    def _can_wrap(self, space):
        if space == '.':
            return True
        if space == '#':
            return False
        return None

    @cached_property
    def side_length(self):
        num_spaces = sum(
            len([c for c in row if c != ' ']) for row in self.grid
        )
        cube_size = num_spaces / 6
        return int(math.sqrt(cube_size))

    @cached_property
    def sides(self):
        sides = []
        for y in range(0, len(self.grid), self.side_length):
            row = self.grid[y]
            for x in range(0, len(row), self.side_length):
                if row[x] != ' ':
                    side = []
                    for yy in range(y, y + self.side_length):
                        side_row = []
                        for xx in range(x, x + self.side_length):
                            side_row.append((xx, yy))
                        side.append(side_row)
                    sides.append(side)
        return sides

    def add_state(self):
        x, y = self.location
        if self.grid[y][x] == ' ':
            self.print()
            raise Exception('Foo')
        self.states[self.location] = SYMBOLS[self.facing]

    def process_move(self, is_3d=False):
        if isinstance(self.current_move, int):
            for _ in range(self.current_move):
                space, new_location = self.take_step()
                if space == '.':
                    self.location = new_location
                    self.add_state()
                elif space == ' ':
                    success = self.wrap_3d() if is_3d else self.wrap_2d()
                    self.add_state()
                    if not success:
                        break
                elif space == '#':
                    break
                else:
                    raise Exception(space)
        elif self.current_move == 'L':
            self.rotate_counter_clockwise()
        elif self.current_move == 'R':
            self.rotate_clockwise()
        self.move_index += 1
        self.add_state()

    @property
    def password(self):
        leading_spaces = 0
        for space in self.grid[self.location[1]]:
            if space == ' ':
                leading_spaces += 1
            else:
                break
        row = self.location[1] + 1
        column = self.location[0] + 1
        return 1000 * row + 4 * column + self.facing

    def reset(self):
        self.location = self.start
        self.facing = 0
        self.move_index = 0
        self.states = {self.start: self.facing}

    def print(self):
        for y, row in enumerate(self.grid):
            for x, space in enumerate(row):
                print(self.states.get((x, y), space), end='')
            print()
        print()

    def print_sides(self):
        for y in range(len(self.grid)):
            row = self.grid[y]
            for x in range(len(row)):
                side = self._on_side((x, y))
                if side is None:
                    print(' ', end='')
                else:
                    print(side[0], end='')
            print()

    def _on_side(self, location=None):
        if not location:
            location = self.location
        for i, side in enumerate(self.sides):
            for y, row in enumerate(side):
                for x, space in enumerate(row):
                    if space == location:
                        return i, x, y
        return None


def main():
    board = Board(get_data(22))
    for _ in range(len(board.moves)):
        board.process_move()
    password1 = board.password

    board.reset()
    board.location = board.start
    for _ in range(len(board.moves)):
        board.process_move(is_3d=True)
    password2 = board.password

    return password1, password2


if __name__ == '__main__':
    print(main())
