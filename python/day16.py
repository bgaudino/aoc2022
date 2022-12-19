
import re
from dataclasses import dataclass
from functools import cached_property

from utils import get_data


@dataclass
class Tunnels:
    valves: dict
    edges: dict
    starting_valve = 'AA'
    time = 30

    @cached_property
    def distances(self):
        return {
            (f): {t: self._find_shortest_distance(f, t) for t in self.relevant_valves} for f in self.relevant_valves
        }

    @cached_property
    def relevant_valves(self):
        return [self.starting_valve] + list(self.valves.keys())

    def _find_shortest_distance(self, start, end):
        visited = {start}
        queue = [(start, -1)]

        while queue:
            current, steps = queue.pop(0)
            steps += 1
            if current == end:
                return steps

            for edge in self.edges[current]:
                if edge not in visited:
                    visited.add(edge)
                    queue.append((edge, steps))

        return -1

    def find_max_relief(self):
        max_relief = 0
        stack = [[0, 0, self.starting_valve]]  # distance, pressure, valves
        while stack:
            path = stack.pop(0)
            current = path[-1]
            paths = [
                path + [valve] for valve in self.valves if valve not in path
            ]
            for path in paths:
                elapsed_time, pressure, *_, next_valve = path
                remaining_valves = path[2:-1]
                distance = self.distances[current][next_valve] + 1

                if elapsed_time + distance >= self.time:
                    for valve in remaining_valves:
                        time_remaining = self.time - elapsed_time
                        pressure += self.valves.get(valve, 0) * time_remaining
                    path[0], path[1] = self.time, pressure
                    if pressure > max_relief:
                        max_relief = pressure
                    continue

                path[0] += distance
                for valve in remaining_valves:
                    path[1] += self.valves.get(valve, 0) * distance
                stack.append(path)

        return max_relief


def parse():
    valves = {}
    edges = {}
    for line in get_data(16):
        parts = line.split(' ')
        name = parts[1]
        rate = int(re.sub('[^0-9]', '', parts[4]))
        if rate > 0:
            valves[name] = rate
        edges[name] = [e.replace(',', '') for e in parts[9:]]
    return valves, edges


def main():
    return Tunnels(*parse()).find_max_relief()


if __name__ == '__main__':
    print(main())
