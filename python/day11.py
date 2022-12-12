from dataclasses import dataclass
from functools import cached_property
from math import prod, lcm
from typing import Callable

from utils import get_data


@dataclass
class Monkey:
    items: list[int] = None
    operation: Callable[[int], int] = lambda x: x
    modulus: int = 1
    if_true: int = 0
    if_false: int = 0
    inspection_count: int = 0

    def __post_init__(self):
        self.items = []

    def inspect(self):
        self.items[0] = self.operation(self.items[0])
        self.inspection_count += 1

    def get_bored(self):
        self.items[0] //= 3

    def test(self):
        return self.items[0] % self.modulus == 0

    def to_monkey_index(self):
        return self.if_true if self.test() else self.if_false

    def throw(self):
        return self.items.pop(0)

    def catch(self, item):
        self.items.append(item)


class Troop:
    def __init__(self, data):
        monkeys = []
        monkey = Monkey()
        for line in data:
            if line == '':
                continue
            part1, part2 = line.strip().split(':')
            match part1:
                case 'Starting items':
                    monkey.items = [int(i.strip()) for i in part2.split(',')]
                case 'Operation':
                    monkey.operation = get_operation(part2)
                case 'Test':
                    monkey.modulus = int(part2.split(' ')[-1])
                case 'If true':
                    monkey.if_true = int(part2.split(' ')[-1])
                case 'If false':
                    monkey.if_false = int(part2.split(' ')[-1])
                    monkeys.append(monkey)
                    monkey = Monkey()
        self.monkeys = monkeys

    def complete_round(self, relief=True):
        for monkey in self.monkeys:
            while monkey.items:
                monkey.inspect()
                if relief:
                    monkey.get_bored()
                else:
                    monkey.items[0] = self.reduce_worry(monkey.items[0])
                self.monkeys[monkey.to_monkey_index()].catch(monkey.throw())

    @cached_property
    def lcm(self):
        return lcm(*[m.modulus for m in self.monkeys])

    def reduce_worry(self, worry):
        return worry % self.lcm

    def get_monkey_business(self):
        return prod(sorted([m.inspection_count for m in self.monkeys], reverse=True)[:2])


def get_operation(line):
    *_, operation, value = line.split(' ')
    if operation == '+':
        return lambda x: x + (int(value) if value != "old" else x)
    if operation == '*':
        return lambda x: x * (int(value) if value != "old" else x)


def main():
    data = get_data(11)

    troop1 = Troop(data)
    for _ in range(20):
        troop1.complete_round()

    troop2 = Troop(data)
    for _ in range(10000):
        troop2.complete_round(relief=False)

    return troop1.get_monkey_business(), troop2.get_monkey_business()


if __name__ == '__main__':
    print(main())
