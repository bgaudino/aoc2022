import json
from dataclasses import dataclass
from itertools import zip_longest

from utils import get_data


@dataclass
class Packet:
    data: list[int | list[int]]

    def __str__(self):
        return str(self.data)

    def __lt__(self, next):
        return self.in_order(next)

    def __eq__(self, next):
        return compare(self.data, next.data) is None

    def in_order(left, right):
        result = compare(left.data, right.data)
        return result if result is not None else True


def main():
    packets = parse_packets()
    num_in_order = sum(
        [i for i, (l, r) in enumerate(packets, 1) if l.in_order(r)]
    )

    dividers = [Packet([[2]]), Packet([[6]])]
    packets = sorted(
        [p for pair in packets for p in pair] + dividers
    )

    decoder_key = 1
    first_divider_found = False
    for i, p in enumerate(packets, 1):
        if p in dividers:
            decoder_key *= i
            if first_divider_found:
                break
            else:
                first_divider_found = True

    return num_in_order, decoder_key


# Maybe I'll go back and manually parse this later
def parse_packets():
    lines = lines = get_data(13)
    pair, pairs = [], []
    for line in lines:
        if line:
            line = json.loads(line)
            pair.append(Packet(line))
        else:
            pairs.append(pair)
            pair = []
    pairs.append(pair)
    return pairs


def compare(left, right):
    # Left list ran out first
    if left is None:
        return True

    # Right list ran out first
    if right is None:
        return False

    # Both ints
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        if left > right:
            return False
        return None

    # Mixed types
    if isinstance(left, int):
        return compare([left], right)
    if isinstance(right, int):
        return compare(left, [right])

    # Both lists
    for l, r in zip_longest(left, right):
        result = compare(l, r)
        if result is not None:
            return result
    return None


if __name__ == '__main__':
    print(main())
