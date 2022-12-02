def main():
    calorie_totals = []
    elf_item_calories = []
    with open('../data/day1.txt', 'r') as file:
        for line in file:
            if line == '\n':
                calorie_totals.append(sum(elf_item_calories))
                elf_item_calories = []
            else:
                elf_item_calories.append(int(line))

    calorie_totals = sorted(calorie_totals, reverse=True)

    # Part one
    print(calorie_totals[0])

    # Part two
    print(sum(calorie_totals[:3]))


if __name__ == '__main__':
    main()
