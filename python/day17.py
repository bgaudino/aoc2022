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
    rock_pattern = (HorizontalLine, Plus, L, VerticalLine, Square)
    width = 7
    start_x = 2
    start_y = 3
    rock_index = 0
    gas_jet = 0

    def __init__(self):
        self.taken = set()
        self.states = set()
        self.gas_jet_directions = ''.join(get_data(17))

    def get_rock(self):
        rock = self.rock_pattern[self.rock_index % len(self.rock_pattern)]()
        self.rock_index += 1
        return rock

    def get_instruction(self):
        direction = self.gas_jet_directions[self.gas_jet % len(
            self.gas_jet_directions)]
        self.gas_jet += 1
        return direction

    def is_taken(self, rock):
        if len(rock.coordinates.intersection(self.taken)):
            return True
        if len([y for _, y in rock.coordinates if y < 0]):
            return True
        if len([x for x, _ in rock.coordinates if x < 0 or x >= self.width]):
            return True
        return False

    def height(self):
        if not self.taken:
            return 0
        return max((y for _, y in self.taken)) + 1

    def fall(self):
        rock = self.get_rock()
        rock.right(self.start_x)
        rock.up(self.height() + self.start_y)

        while True:
            instruction = self.get_instruction()
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

    def print(self, rock=None):
        chamber = ['+-------+']

        for y in range(0, self.height() + 4):
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


tower = Tower()
for i in range(2022):
    tower.fall()
tower.print()
print(tower.height())
