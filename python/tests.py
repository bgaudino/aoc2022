from dataclasses import dataclass

import day01
import day02
import day03
import day04
import day05
import day06
import day07
import day08
import day09
import day10
import day11
import day12
import day13
import day14
import day15
import day16
import day17
import day18
import day20
import day21
import day22
import day23
import day24


@dataclass
class Day:
    solution: __module__
    part1: str
    part2: str


days = [
    Day(day01, 72070, 211805),
    Day(day02, 14297, 10498),
    Day(day03, 7826, 2577),
    Day(day04, 424, 804),
    Day(day05, 'FJSRQCFTN', 'CJVLJQPHS'),
    Day(day06, 1912, 2122),
    Day(day07, 1307902, 7068748),
    Day(day08, 1700, 470596),
    Day(day09, 6081, 2487),
    Day(day10, 13740, day10.part2_answer),
    Day(day11, 61005, 20567144694),
    Day(day12, 412, 402),
    Day(day13, 6070, 20758),
    Day(day14, 979, 29044),
    Day(day15, 4582667, 10961118625406),
    Day(day16, 2056, 2513),
    Day(day17, 3114, 1540804597682),
    Day(day18, 4628, 2582),
    Day(day20, 11073, 11102539613040),
    Day(day21, 54703080378102, 3952673930912),
    Day(day22, 93226, 37415),
    Day(day23, 4172, 942),
    Day(day24, 230, 713),
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
