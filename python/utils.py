from pathlib import Path


def get_data(day):
    path = Path(__file__).parent.parent
    filename = f'{path}/data/day{day}.txt'
    with open(filename, 'r') as file:
        return file.read().split('\n')
