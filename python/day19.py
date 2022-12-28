import math

from utils import get_data

ORE, CLAY, OBSIDIAN, GEODE = 0, 1, 2, 3


def parse(line):
    robot_strings = line.split(': ')[1].split('. ')
    blueprint = []
    for i, string in enumerate(robot_strings):
        words = string.split(' ')
        costs = {ORE: int(words[4])}
        if i == 2:
            costs[CLAY] = int(words[7])
        if i == 3:
            costs[OBSIDIAN] = int(words[7])
        blueprint.append(costs)
    return tuple(blueprint)


def geode_potential(blueprint, robots, resources, time):
    new_robots = [0, 0, 0, 0]
    new_materials = [*resources]
    for _ in range(time):
        for i in range(4):
            new_materials[i] += robots[i] + new_robots[i]
        for costs in blueprint:
            if all(
                new_materials[material] >= cost *
                (new_robots[i] + 1) for material, cost in costs.items()
            ):
                new_robots[i] += 1
    return new_materials[GEODE]


def bfs(blueprint, time):
    queue = [((1, 0, 0, 0), (0, 0, 0, 0), time)]
    seen = set()
    max_geodes = 0
    max_robots = [
        max(costs.get(i, 0) for costs in blueprint) for i in range(4)
    ]

    i = 0
    while queue:
        state = queue.pop(0)
        robots, resources, time = state
        if geode_potential(blueprint, robots, resources, time) < max_geodes:
            continue
        max_geodes = max(max_geodes, resources[GEODE] + time * robots[GEODE])

        if state in seen:
            continue
        seen.add(state)

        for resource, robot in enumerate(blueprint):
            if resource != GEODE and robots[resource] >= max_robots[resource]:
                continue

            if any(robots[r] == 0 for r in robot):
                continue

            time_to_build = max(
                [
                    math.ceil((cost - resources[resource]) / robots[resource])
                    for resource, cost in robot.items()
                ] + [0]
            )
            if time - time_to_build - 1 <= 0:
                continue

            next_stuff = [
                resources[i] + (robots[i] * (time_to_build + 1)) - blueprint[resource].get(i, 0) for i in range(4)
            ]
            next_robots = list(robots)
            next_robots[resource] += 1

            for i in range(3):
                next_stuff[i] = min(
                    next_stuff[i], max_robots[i] * (time - time_to_build - 1)
                )

            queue.append((
                tuple(next_robots),
                tuple(next_stuff),
                (time - time_to_build - 1)
            ))
        i += 1

    return max_geodes


def main():
    blueprints = [parse(line) for line in get_data(19)]
    part1 = sum(i * bfs(bp, 24) for i, bp in enumerate(blueprints, 1))
    part2 = math.prod(bfs(bp, 32) for bp in blueprints[:3])

    return part1, part2


if __name__ == '__main__':
    print(main())
