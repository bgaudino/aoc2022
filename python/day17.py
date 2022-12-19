from utils import get_data


class Rock:
    coordinates = {()}

    def left(self, num=1):
        self.coordinates = {(x - num, y) for x, y in self.coordinates}

    def right(self, num=1):
        self.coordinates = {(x + num, y) for x, y in self.coordinates}

    def up(self, num=1):
        self.coordinates = {(x, y + num) for x, y in self.coordinates}

    def down(self, num=1):
        self.coordinates = {(x, y - num) for x, y in self.coordinates}


class HorizontalLine(Rock):
    coordinates = {(0, 0), (1, 0), (2, 0), (3, 0)}


class Plus(Rock):
    coordinates = {
                (1, 2),
        (0, 1), (1, 1), (2, 1),
                (1, 0),
    }


class L(Rock):
    coordinates = {
                        (2, 2),
                        (2, 1),
        (0, 0), (1, 0), (2, 0),
    }


class VerticalLine(Rock):
    coordinates = {
        (0, 3),
        (0, 2),
        (0, 1),
        (0, 0),
    }


class Square(Rock):
    coordinates = {
        (0, 1), (1, 1),
        (0, 0), (1, 0),
    }


class Tower:
    rocks = (HorizontalLine, Plus, L, VerticalLine, Square)
    width = 7
    start_x = 2
    start_y = 3
    rock_count = 0
    jet_count = 0

    def __init__(self):
        self.taken = set()
        self.states = {}
        self.jet_directions = ''.join(get_data(17))

    @property
    def rock_index(self):
        return self.rock_count % len(self.rocks)

    @property
    def jet_index(self):
        return self.jet_count % len(self.jet_directions)

    def get_rock(self):
        rock = self.rocks[self.rock_index]()
        self.rock_count += 1
        return rock

    def get_jet_instruction(self):
        direction = self.jet_directions[self.jet_index]
        self.jet_count += 1
        return direction

    def is_taken(self, rock):
        if len(rock.coordinates.intersection(self.taken)):
            return True
        if len([y for _, y in rock.coordinates if y < 0]):
            return True
        if len([x for x, _ in rock.coordinates if x < 0 or x >= self.width]):
            return True
        return False

    @property
    def height(self):
        if not self.taken:
            return 0
        return max((y for _, y in self.taken)) + 1

    @property
    def surface_profile(self):
        profile = []
        for x in range(self.width):
            y = self.height
            while (x, y) not in self.taken:
                y -= 1
                if y < 0:
                    break
            profile.append(self.height - (y + 1))
        return tuple(profile)

    def fall(self):
        rock = self.get_rock()
        rock.right(self.start_x)
        rock.up(self.height + self.start_y)

        while True:
            instruction = self.get_jet_instruction()
            if instruction == '>':
                rock.right()
                if self.is_taken(rock):
                    rock.left()

            if instruction == '<':
                rock.left()
                if self.is_taken(rock):
                    rock.right()

            rock.down()
            if self.is_taken(rock):
                rock.up()
                self.taken = self.taken.union(rock.coordinates)
                break

        return (
            self.surface_profile,
            self.rock_index,
            self.jet_index,
        )

    def print(self, rock=None):
        chamber = ['+-------+']

        for y in range(0, self.height + 4):
            row = ['|']
            for x in range(self.width):
                if rock and (x, y) in rock.coordinates:
                    row.append('@')
                elif (x, y) in self.taken:
                    row.append('#')
                else:
                    row.append('.')
            row.append('|')
            chamber.append(row)

        chamber.reverse()
        for row in chamber:
            print(''.join(row))


def drop_rocks(iterations):
    tower = Tower()

    # Find cycle
    for i in range(iterations):
        state = tower.fall()
        if state in tower.states:
            cycle_start, pre_cycle_height = tower.states[state]
            cycle_length = i - cycle_start
            cycle_height = tower.height - pre_cycle_height
            break
        tower.states[state] = (i, tower.height)
    else:
        # If no cycle return height
        return tower.height

    # Get height after last cycle
    remainder = (iterations - cycle_start) % cycle_length - 1
    for i in range(remainder):
        tower.fall()
    remainder_height = tower.height - pre_cycle_height - cycle_height

    num_cycles = (iterations - cycle_start) // cycle_length
    return pre_cycle_height + (cycle_height * num_cycles) + remainder_height


def main():
    return drop_rocks(2022), drop_rocks(1000000000000)


if __name__ == '__main__':
    print(main())
