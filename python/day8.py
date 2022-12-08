from math import prod
from utils import get_data


ROWS = get_data(8)
Y_LEN = len(ROWS)
X_LEN = len(ROWS[0])


def main():
    count = 0
    score = 0
    for y in range(Y_LEN):
        for x in range(X_LEN):
            height = ROWS[y][x]

            south_visible, south_count = search(height, y + 1, Y_LEN, 'y', x)
            north_visible, north_count = search(height,  y - 1, -1, 'y', x, -1)
            east_visible, east_count = search(height,  x + 1, Y_LEN, 'x', y)
            west_visible, west_count = search(height,  x - 1, -1, 'x', y, -1)

            if any((
                on_edge(x, y),
                north_visible,
                south_visible,
                east_visible,
                west_visible
            )):
                count += 1
            score = max(
                score, prod((north_count, south_count, east_count, west_count))
            )

    return count, score


def on_edge(*coordinates):
    for c in coordinates:
        if c == 0 or c == Y_LEN - 1:
            return True


def search(height, start, stop, axis, index, step=1):
    is_visible = False
    count = 0
    for i in range(start, stop, step):
        count += 1
        neighbor_height = ROWS[i][index] if axis == 'y' else ROWS[index][i]
        if height <= neighbor_height:
            break
    else:
        is_visible = True
    return is_visible, count


if __name__ == '__main__':
    print(main())
