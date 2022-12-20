from utils import get_data


def main():
    data = get_data(5)
    crate_mover_9000, crate_mover_9001 = CrateMover9000(
        data), CrateMover9001(data)
    crate_mover_9000.rearrange()
    crate_mover_9001.rearrange()
    return crate_mover_9000.top_of_each_stack, crate_mover_9001.top_of_each_stack


class CrateMover9000:
    def __init__(self, data):
        sep = data.index('')
        self.diagram, self.instructions = data[:sep], data[sep + 1:]
        stacks = {}
        for k, line in enumerate(reversed(self.diagram)):
            i = j = 1
            while i < len(line):
                crate = line[i].strip()
                if k == 0:
                    stacks[crate] = []
                elif crate:
                    stacks[str(j)].append(crate)
                i += 4
                j += 1
        self.stacks = stacks

    def rearrange(self):
        for instruction in self.instructions:
            _, quantity, _, from_stack, _, to_stack = instruction.split(' ')
            self.perform_move(int(quantity), from_stack, to_stack)

    def perform_move(self, quantity, from_stack, to_stack):
        for _ in range(quantity):
            self.stacks[to_stack].append(self.stacks[from_stack].pop())

    @property
    def top_of_each_stack(self):
        return ''.join([s[-1] for s in self.stacks.values() if len(s)])


class CrateMover9001(CrateMover9000):
    def perform_move(self, quantity, from_stack, to_stack):
        index = len(self.stacks[from_stack]) - quantity
        self.stacks[to_stack] += self.stacks[from_stack][index:]
        self.stacks[from_stack] = self.stacks[from_stack][:index]


if __name__ == '__main__':
    print(main())
