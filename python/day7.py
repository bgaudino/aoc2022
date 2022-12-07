from utils import get_data


class FileSystem:
    def __init__(self):
        self.dirs = {'/': {}}
        self.cwd = '/'
        self.path = ['/']
        self.is_listing = False
        self.current_dir = {}

    def update_filesystem(self):
        fs = self.dirs
        for i, p in enumerate(self.path):
            if i == len(self.path) - 1:
                fs[p] = self.current_dir
                break
            fs = fs[p]

    def process_command(self, command):
        if command.startswith('$ cd'):
            if self.is_listing:
                self.update_filesystem()
            self.is_listing = False
            cwd = command.split(' ')[-1]
            self.cd(cwd)
            self.current_dir = {}

        if command.startswith('$ ls'):
            self.is_listing = True

    def cd(self, dir):
        if dir == '/':
            self.path = ['/']
        elif dir == '..':
            self.path.pop()
        else:
            self.path.append(dir)

    def add_item(self, data):
        if data.startswith('dir'):
            key = data.split(' ')[-1]
            if key not in self.current_dir:
                self.current_dir[key] = {}
        else:
            size, file = data.split(' ')
            self.current_dir[file] = int(size)

    def dir_sizes(self):
        sizes = []

        def dir_size(dir):
            size = sum([v for v in dir.values() if type(v) == int])
            size += sum(
                [dir_size(v) for v in dir.values() if type(v) == dict]
            )
            sizes.append(size)
            return size

        return dir_size(self.dirs['/']), sizes


def main():
    f = FileSystem()
    for line in get_data(7):
        if line.startswith('$'):
            f.process_command(line)
        else:
            f.add_item(line)
    if f.is_listing:
        f.update_filesystem()

    total_size, sizes = f.dir_sizes()
    available_space = 70000000 - total_size
    space_to_free = 30000000 - available_space

    return sum([s for s in sizes if s <= 100000]), min([s for s in sizes if s >= space_to_free])


if __name__ == '__main__':
    print(main())
