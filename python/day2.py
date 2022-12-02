codes = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}
outcome_codes = {'X': 0, 'Y': 3, 'Z': 6}


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


part1 = []
part2 = []
with open('data/day2.txt', 'r') as file:
    for line in file:
        elf_code, my_code = line.strip().split(' ')
        elf, me = codes[elf_code], codes[my_code]
        part1.append(me + get_outcome(elf, me))

        my_outcome = outcome_codes[my_code]
        part2.append(my_outcome + get_shape(elf, my_outcome))

print(sum(part1))
print(sum(part2))
