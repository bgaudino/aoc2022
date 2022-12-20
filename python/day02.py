from utils import get_data


def main():
    codes = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}
    outcome_codes = {'X': 0, 'Y': 3, 'Z': 6}
    part1 = []
    part2 = []

    for line in get_data(2):
        elf_code, my_code = line.strip().split(' ')
        elf, me = codes[elf_code], codes[my_code]
        part1.append(me + get_outcome(elf, me))

        my_outcome = outcome_codes[my_code]
        part2.append(my_outcome + get_shape(elf, my_outcome))

    return sum(part1), sum(part2)


def get_outcome(elf, me):
    if elf == me:
        return 3
    if elf == me % 3 + 1:
        return 0
    return 6


def get_shape(elf, outcome):
    if outcome == 3:
        return elf
    if outcome == 6:
        return elf % 3 + 1
    return 3 if elf - 1 == 0 else elf - 1


if __name__ == '__main__':
    print(main())
