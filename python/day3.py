class Item(str):
    @property
    def points(self):
        c = self[0]
        if c.lower() == c:
            return ord(c) - 96
        if c.upper() == c:
            return ord(c) - 38
        return 0


class Rucksack:
    def __init__(self, items):
        self.items = set([Item(i) for i in items])


class Group(list):
    @property
    def badge(self):
        items = set(self[0].items)
        for i in range(1, len(self)):
            items = items.intersection(self[i].items)
        return items.pop()


part_1_total = 0
part_2_total = 0
with open('data/day3.txt', 'r') as file:
    group = Group()
    for line in file:
        line = line.strip()
        middle = len(line) // 2

        # part1
        left, right = Rucksack(line[:middle]), Rucksack(line[middle:])
        part_1_total += left.items.intersection(right.items).pop().points

        # part2
        rucksack = Rucksack(left.items.union(right.items))
        group.append(rucksack)
        if len(group) == 3:
            part_2_total += group.badge.points
            group = Group()

print(part_1_total)
print(part_2_total)
