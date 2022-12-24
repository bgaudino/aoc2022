import math
from dataclasses import dataclass

from utils import get_data

N, NE, E, SE = (0, -1), (1, -1), (1, 0), (1, 1)
S, SW, W, NW = (0, 1), (-1, 1), (-1, 0), (-1, -1)
DIRECTIONS = (N, NE, E, SE, S, SW, W, NW)


@dataclass
class Proposal:
    move: tuple[int, int]
    if_empty: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]


@dataclass
class Crater:
    elves: set[tuple[int, int]]
    proposals = [
        Proposal(N, (N, NE, NW)),
        Proposal(S, (S, SE, SW)),
        Proposal(W, (W, NW, SW)),
        Proposal(E, (E, NE, SE)),
    ]

    def perform_round(self):
        elf_proposals = {}
        move_count = {}
        for elf in self.elves:
            for proposal in self.proposals:
                if move := self.propose(elf, proposal):
                    elf_proposals.setdefault(elf, move)
                    if move in move_count:
                        move_count[move] += 1
                    else:
                        move_count[move] = 1
                    break
        self.elves = {
            proposal if move_count.get((proposal := elf_proposals.get(elf))) == 1 else elf for elf in self.elves
        }
        self.proposals.append(self.proposals.pop(0))
        return len(elf_proposals) == 0

    def propose(self, elf, proposal):
        if not self.needs_to_move(elf):
            return None
        moves = {(elf[0] + d[0], elf[1] + d[1])for d in proposal.if_empty}
        if moves.intersection(self.elves):
            return None
        return (elf[0] + proposal.move[0], elf[1] + proposal.move[1])

    def needs_to_move(self, elf):
        moves = {(elf[0] + d[0], elf[1] + d[1]) for d in DIRECTIONS}
        return bool(moves.intersection(self.elves))

    def bounds(self):
        min_x, max_x = math.inf, -math.inf
        min_y, max_y = math.inf, -math.inf
        for y in range(-100, 100):
            for x in range(-100, 100):
                if (x, y) in self.elves:
                    min_x, max_x = min(x, min_x), max(x, max_x)
                    min_y, max_y = min(y, min_y), max(y, max_y)
        return min_x, max_x + 1, min_y, max_y + 1

    def empty_spaces(self):
        min_x, max_x, min_y, max_y = self.bounds()
        return (max_x - min_x) * (max_y - min_y) - len(self.elves)

    def print(self):
        min_x, max_x, min_y, max_y = self.bounds()
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                if (x, y) in self.elves:
                    print('#', end='')
                else:
                    print('.', end='')
            print()
        print()


def main():
    elves = {
        (x, y) for y, line in enumerate(get_data(23)) for x, c in enumerate(line) if c == '#'
    }
    crater = Crater(elves)

    round = 1
    progress = 0
    while True:
        done = crater.perform_round()
        if round == 10:
            progress = crater.empty_spaces()
        if done:
            break
        round += 1

    return progress, round


if __name__ == '__main__':
    print(main())
