from dataclasses import dataclass

import day1
import day2
import day3
import day4
import day5
import day6
import day7
import day8
import day9
import day10
import day11
import day12
import day13
import day14
import day17


@dataclass
class Day:
    solution: __module__
    part1: str
    part2: str


days = [
    Day(day1, 72070, 211805),
    Day(day2, 14297, 10498),
    Day(day3, 7826, 2577),
    Day(day4, 424, 804),
    Day(day5, 'FJSRQCFTN', 'CJVLJQPHS'),
    Day(day6, 1912, 2122),
    Day(day7, 1307902, 7068748),
    Day(day8, 1700, 470596),
    Day(day9, 6081, 2487),
    Day(day10, 13740, day10.part2_answer),
    Day(day11, 61005, 20567144694),
    Day(day12, 412, 402),
    Day(day13, 6070, 20758),
    Day(day14, 979, 29044),
    Day(day17, 3114, 1540804597682),
]

total_errors = 0
for i, day in enumerate(days):
    errors = 0
    part1, part2 = day.solution.main()
    try:
        assert part1 == day.part1
    except AssertionError:
        errors += 1
        print(f'Day {i + 1} (part 1): Expected {day.part1} got {part1}')
    else:
        print(f'Day {i + 1} (part 1): OK')
    try:
        assert part2 == day.part2
    except AssertionError:
        errors += 1
        print(f'Day {i + 1} (part 2): Expected {day.part2} got {part2}')
    else:
        print(f'Day {i + 1} (part 2): OK')
    total_errors += errors

num_tests = len(days) * 2
print(f'Ran {num_tests}: {num_tests - total_errors} passed, {total_errors} failed.')
