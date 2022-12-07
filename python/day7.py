from utils import get_data


class Directory:
    def __init__(self, parent=None):
        self.files = []
        self.parent = parent
        self.children = {}


def dir_sizes(directory):
    sizes = []

    def dir_size(dir):
        size = sum(dir.files)
        size += sum([dir_size(c) for c in dir.children.values()])
        sizes.append(size)
        return size

    return dir_size(directory), sizes


def main():
    root = Directory('/')
    cursor = root
    for line in get_data(7):
        parts = line.split(' ')
        if line.startswith('dir'):
            name = parts[-1]
            cursor.children[name] = Directory(parent=cursor)
            continue
        if not line.startswith('$'):
            size = int(parts[0])
            cursor.files.append(size)
            continue
        if line.startswith('$ ls'):
            continue
        if parts[2] == "/":
            cursor = root
            continue
        if parts[2] == "..":
            cursor = cursor.parent
            continue

        # cd
        name = parts[2]
        if d := cursor.children.get(name):
            cursor = d
            continue

        d = Directory(parent=cursor)
        cursor.children[name] = d
        cursor = d

    total_size, sizes = dir_sizes(root)
    available_space = 70000000 - total_size
    space_to_free = 30000000 - available_space

    return sum([s for s in sizes if s <= 100000]), min([s for s in sizes if s >= space_to_free])


if __name__ == '__main__':
    print(main())
