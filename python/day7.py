import re
from utils import get_data


class FileSystem:
    def __init__(self):
        self.dirs = {'/': {}}
        self.pwd = '/'
        self.path = ['/']

    def update_filesystem(self, data):
        fs = self.dirs
        for i, p in enumerate(self.path):
            if i == len(self.path) - 1:
                if p not in fs:
                    fs[p] = data
                else:
                    fs[p] = {**fs[p], **data}
                break
            fs = fs[p]

    def cd(self, dir):
        if dir == '/':
            self.path = ['/']
        elif dir == '..':
            self.path.pop()
        else:
            self.path.append(dir)


def main():
    filesystem = {'/': {}}
    pwd = '/'
    path = [pwd]
    dir = {}
    is_listing = False

    for line in get_data(7):
        if line.startswith('$ cd'):
            if is_listing:
                update_filesystem(filesystem, path, dir)
                is_listing = False

            pwd = line.split(' ')[-1]
            if pwd == '/':
                path = ['/']
            elif pwd == '..':
                path.pop()
            else:
                path.append(pwd)

            fs = filesystem
            for p in path:
                fs = fs[p]
            dir = fs
        elif line.startswith('$ ls'):
            is_listing = True
        elif line.startswith('dir'):
            key = line.split(' ')[-1]
            if key not in dir:
                dir[key] = {}
        else:
            size, file = line.split(' ')
            dir[file] = int(size)

    if is_listing:
        update_filesystem(filesystem, path, dir)

    sizes = {}

    def dir_size(dir, key):
        size = sum([v for v in dir.values() if type(v) == int])
        size += sum(
            [dir_size(v, k) for k, v in dir.items() if type(v) == dict]
        )
        sizes[key] = size
        print(sizes)
        return size
    fs = filesystem['/']
    dir_size(fs, '/')
    from pprint import pprint
    pprint(sizes)
    return sum(s for s in sizes.values() if s <= 100000)


def update_filesystem(filesystem, path, dir):
    fs = filesystem
    for i, p in enumerate(path):
        if i == len(path) - 1:
            if p not in fs:
                fs[p] = dir
            else:
                fs[p] = {**fs[p], **dir}
            break
        fs = fs[p]
    return filesystem


if __name__ == '__main__':
    print(main())


with open('data/day7.txt') as input_data:
    input_data = [line.strip('\n') for line in input_data.readlines()]
    current_dir = [r'/']
    dirs = {}
    for line in input_data[1:]:
        current_dir = current_dir

        if line.startswith('$ cd'):
            if not line.endswith('..'):
                current_dir.append(line[5:])
            else:
                current_dir.pop()

        if line[0].isdigit():
            for i in range(1, len(current_dir)+1):
                try:
                    dirs[current_dir[-i]].append(line)
                except KeyError:
                    dirs[current_dir[-i]] = []
                    dirs[current_dir[-i]].append(line)


totals = []
for dir, files in dirs.items():
    sizes = [z.split(' ')[0] for z in files]
    total_size = sum(int(x) for x in sizes)
    dirs[dir] = total_size
    totals.append(total_size)

totals = [a for a in totals if a <= 100000]
print(sum(totals))


with open('data/day7.txt') as input_data:
    input_data = [line.strip('\n') for line in input_data.readlines()]
    current_dir = [r'/']
    dirs = {}
    for line in input_data[1:]:
        current_dir = current_dir

        if line.startswith('$ cd'):
            if not line.endswith('..'):
                current_dir.append(line[5:])
            else:
                current_dir.pop()

        if line[0].isdigit():
            for i in range(1, len(current_dir)+1):
                try:
                    dirs[current_dir[-i]].append(line)
                except KeyError:
                    dirs[current_dir[-i]] = []
                    dirs[current_dir[-i]].append(line)


totals = []
for dir, files in dirs.items():
    sizes = [z.split(' ')[0] for z in files]
    total_size = sum(int(x) for x in sizes)
    dirs[dir] = total_size
    totals.append(total_size)

totals = [a for a in totals if a <= 100000]
print(sum(totals))
