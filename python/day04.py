from utils import get_data


def main():
    full_overlap_count = 0
    partial_overlap_count = 0
    for line in get_data(4):
        elf_ranges = [get_range(e) for e in line.split(',')]
        if fully_overlaps(*elf_ranges):
            full_overlap_count += 1
            partial_overlap_count += 1
        elif partially_overlaps(*elf_ranges):
            partial_overlap_count += 1
    return full_overlap_count, partial_overlap_count


def get_range(elf):
    return [int(n) for n in elf.split('-')]


def fully_overlaps(a, b):
    for x, y in ((a, b), (b, a)):
        if x[0] <= y[0] and x[1] >= y[1]:
            return True
    return False


def partially_overlaps(a, b):
    for x, y in ((a, b), (b, a)):
        if x[0] <= y[0] <= x[1] or x[0] <= y[1] <= x[1]:
            return True
    return False


if __name__ == '__main__':
    print(main())
