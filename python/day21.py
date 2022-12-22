from dataclasses import dataclass
from sys import maxsize

from utils import get_data


@dataclass
class Monkey:
    value: int | list[str, str, str]

    def yell(self, troop):
        if isinstance(self.value, int):
            return self.value
        left, operation, right = self.value
        x = troop.get(left).yell(troop)
        y = troop.get(right).yell(troop)
        match operation:
            case '+':
                return x + y
            case '-':
                return x - y
            case '*':
                return x * y
            case '/':
                return x / y

    def test_equality(self, troop, human=1):
        _troop = {**troop, 'humn': Monkey(value=human)}
        if isinstance(self.value, int):
            return True, False, False
        left, _, right = self.value
        left_value = _troop.get(left).yell(_troop)
        right_value = _troop.get(right).yell(_troop)
        return left_value - right_value


def find_human_value(troop, reverse=False):
    root = troop['root']
    start = 0
    stop = maxsize
    while start <= stop:
        human = (start + stop) // 2
        diff = root.test_equality(troop, human)
        if diff == 0:
            return human
        if diff > 0:
            if reverse:
                stop = human
            else:
                start = human
        else:
            if reverse:
                start = human
            else:
                stop = human
    return None


def main():
    troop = {}
    for line in get_data(21):
        name, value = line.split(':')
        try:
            troop[name] = Monkey(value=int(value.strip()))
        except ValueError:
            troop[name] = Monkey(value=(value.strip().split(' ')))

    root = troop['root']
    human = find_human_value(troop)
    if human is None:
        human = find_human_value(troop, True)

    return int(root.yell(troop)), find_human_value(troop)


if __name__ == '__main__':
    print(main())
