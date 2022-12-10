from dataclasses import dataclass, field

from utils import get_data


class CRT:
    cycle = 1
    row_length = 40
    register = 1
    sum_of_significant_signals = 0

    def __init__(self):
        self.rows = [[]]

    def parse_instruction(self, instruction):
        parts = instruction.split(' ')
        if parts[0] == 'noop':
            return parts[0], 0
        return parts[0], int(parts[-1])

    def perform_cycle(self):
        if self.cycle % 40 == 20:
            self.sum_of_significant_signals += self.signal_strength
        self.draw()
        self.cycle += 1

    def draw(self):
        pixel = '#' if self.sprite_visible else '.'
        if len(self.rows[-1]) == self.row_length:
            self.rows.append([pixel])
        else:
            self.rows[-1].append(pixel)

    @property
    def signal_strength(self):
        return self.cycle * self.register

    @property
    def sprite_position(self):
        middle = self.register % 40
        return (middle - 1, middle, middle + 1)

    @property
    def sprite_visible(self):
        return len(self.rows[-1]) in self.sprite_position

    def print(self):
        for row in self.rows:
            print(''.join(row))


def main():
    crt = CRT()
    instructions = get_data(10)
    for instruction in instructions:
        crt.perform_cycle()

        operation, value = crt.parse_instruction(instruction)
        if operation == 'addx':
            crt.perform_cycle()
            crt.register += value

    crt.print()
    return crt.sum_of_significant_signals, crt.rows


if __name__ == '__main__':
    main()


part2_answer = [
    ['#', '#', '#', '#', '.', '#', '.', '.', '#', '.', '#', '#', '#', '.', '.', '#', '#', '#', '.', '.',
        '#', '#', '#', '#', '.', '#', '#', '#', '#', '.', '.', '#', '#', '.', '.', '#', '.', '.', '.', '.'],
    ['.', '.', '.', '#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '#', '.',
        '#', '.', '.', '.', '.', '#', '.', '.', '.', '.', '#', '.', '.', '#', '.', '#', '.', '.', '.', '.'],
    ['.', '.', '#', '.', '.', '#', '.', '.', '#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '#', '.',
        '#', '#', '#', '.', '.', '#', '#', '#', '.', '.', '#', '.', '.', '.', '.', '#', '.', '.', '.', '.'],
    [
        '.', '#', '.', '.', '.', '#', '.', '.', '#', '.', '#', '#', '#', '.', '.', '#', '#', '#', '.', '.', '#', '.', '.', '.', '.', '#', '.', '.', '.', '.', '#', '.', '.', '.', '.', '#', '.', '.', '.', '.'],
    ['#', '.', '.', '.', '.', '#', '.', '.', '#', '.', '#', '.', '.', '.', '.', '#', '.', '#', '.', '.',
        '#', '.', '.', '.', '.', '#', '.', '.', '.', '.', '#', '.', '.', '#', '.', '#', '.', '.', '.', '.'],
    ['.', '#', '#', '#', '.', '.', '#', '#', '.', '.', '#', '.', '.', '.', '.', '#', '.', '.', '#', '.',
        '#', '.', '.', '.', '.', '#', '#', '#', '#', '.', '.', '#', '#', '.', '.', '#', '#', '#', '#', '.']
]
