import re

from utils import get_data

SEARCH_AREA_SIZE = 4000000


def manhattan_distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def out_of_bounds(x, y):
    return x < 0 or y < 0 or x > SEARCH_AREA_SIZE or y > SEARCH_AREA_SIZE


def is_empty(position, sensors, beacons):
    if position in sensors or position in beacons:
        return False
    for sensor, beacon in sensors.items():
        if manhattan_distance(sensor, beacon) >= manhattan_distance(sensor, position):
            return False
    return True


def find_signal(sensors, beacons):
    for sensor, beacon in sensors.items():
        sx, sy = sensor
        distance = manhattan_distance(sensor, beacon) + 1
        for x in range(sx - 1, sx + distance + 1):
            offset = abs(x - sx)
            for position in ((x, sy - distance + offset), (x, sy + distance - offset)):
                if not out_of_bounds(*position) and is_empty(position, sensors, beacons):
                    return position
    raise Exception('Oops, no signal')


def tuning_frequency(x, y):
    return x * SEARCH_AREA_SIZE + y


def parse_coordinates(*coordinates):
    return tuple([
        int(s.split('=')[-1].replace(',', '').replace(':', '')) for s in coordinates
    ])


def main():
    beacons = set()
    sensors = dict()

    for line in get_data(15):
        _, _, sx, sy, *_, bx, by = line.split(' ')
        beacon = parse_coordinates(bx, by)
        sensor = parse_coordinates(sx, sy)
        sensors[sensor] = beacon
        beacons.add(beacon)

    target_row = 2000000
    sensor_range = set()
    for sensor, beacon in sensors.items():
        sx, sy = sensor
        distance_to_beacon = manhattan_distance(sensor, beacon)
        distance_to_row = manhattan_distance(sensor, (sx, target_row))
        if distance_to_row > distance_to_beacon:
            continue

        offset = abs(sy - target_row)
        column_range = (
            sx - distance_to_beacon + offset,
            sx + distance_to_beacon - offset
        )
        for x in range(*column_range):
            sensor_range.add(x)

    signal = find_signal(sensors, beacons)

    return len(sensor_range), tuning_frequency(*signal)


if __name__ == '__main__':
    print(main())
