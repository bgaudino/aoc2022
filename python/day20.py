from utils import get_data


def mix(nums, rounds=1, decryption_key=None):
    if decryption_key is not None:
        nums = [(n * decryption_key, i) for n, i in nums]

    mixed = list(nums)
    for _ in range(rounds):
        for num, index in nums:
            if num == 0:
                continue
            from_index = mixed.index((num, index))
            offset = abs(num) % (len(nums) - 1)
            if num < 0:
                offset = 0 - offset
            to_index = from_index + offset
            if to_index == 0:
                to_index = len(nums) - 1
            elif to_index >= len(nums):
                to_index = to_index % (len(nums) - 1)
            mixed.insert(to_index, mixed.pop(from_index))

    for i in range(len(mixed)):
        if mixed[i][0] == 0:
            zero_index = i
            break

    return sum(
        mixed[(zero_index + i) % len(mixed)][0] for i in range(1000, 3001, 1000)
    )


def main():
    nums = [(int(line), i) for i, line in enumerate(get_data(20))]
    return mix(nums), mix(nums, 10, 811589153)


if __name__ == '__main__':
    print(main())
