def main():
    calorie_totals = []
    elf_items = []
    with open('../data/day1.txt', 'r') as file:
        for line in file:
            if line == '\n':
                calorie_totals.append(sum(elf_items))
                elf_items = []
            else:
                elf_items.append(int(line))

    calories = sorted(calorie_totals, reverse=True)

    # Part one
    print(calories[0])

    # Part two
    print(sum(calories[:3]))


if __name__ == '__main__':
    main()
