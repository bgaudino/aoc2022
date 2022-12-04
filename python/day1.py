from utils import get_data


def main():
    calorie_totals = []
    elf_item_calories = []
    for line in get_data(1):
        if line:
            elf_item_calories.append(int(line))
        else:
            calorie_totals.append(sum(elf_item_calories))
            elf_item_calories = []
        calorie_totals = sorted(calorie_totals, reverse=True)
    return calorie_totals[0], sum(calorie_totals[:3])


if __name__ == '__main__':
    print(main())
