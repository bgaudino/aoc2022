def get_data(day):
    filename = f'data/day{day}.txt'
    with open(filename, 'r') as file:
        return file.read().split('\n')
