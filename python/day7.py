from utils import get_data


class Directory:
    def __init__(self, parent=None):
        self.sizeOfFiles = 0
        self.parent = parent
        self.children = {}

    def dir_sizes(self):
        sizes = []

        def dir_size(dir):
            size = dir.size
            size += sum([dir_size(c) for c in dir.children.values()])
            sizes.append(size)
            return size

        return dir_size(self), sizes


def main():
    root = Directory()
    cursor = root
    for line in get_data(7):
        parts = line.split(' ')

        # directory
        if line.startswith('dir'):
            name = parts[-1]
            cursor.children[name] = Directory(parent=cursor)
            continue

        # file
        if not line.startswith('$'):
            size = int(parts[0])
            cursor.sizeOfFiles += size
            continue

        # ls
        if line.startswith('$ ls'):
            continue

        # cd
        pwd = parts[2]
        if pwd == "/":
            cursor = root
            continue
        if pwd == "..":
            cursor = cursor.parent
            continue
        cursor = cursor.children[pwd]

    total_size, sizes = root.dir_sizes()
    available_space = 70000000 - total_size
    space_to_free = 30000000 - available_space

    return sum([s for s in sizes if s <= 100000]), min([s for s in sizes if s >= space_to_free])


if __name__ == '__main__':
    print(main())
