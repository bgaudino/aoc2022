from utils import get_data

SNAFU_DIGITS = ['0', '1', '2', '=', '-']


def snafu_to_decimal(snafu):
    value = 0
    power = 1
    for i, digit in enumerate(reversed(snafu)):
        if i > 0:
            power *= 5
        if digit == '=':
            value += power * -2
        elif digit == '-':
            value += power * -1
        else:
            value += power * int(digit)
    return value


def decimal_to_snafu(decimal):
    if decimal == 0:
        return ''
    digit = SNAFU_DIGITS[decimal % 5]
    snafu = decimal_to_snafu(int((decimal + 2) / 5))
    return snafu + digit


def main():
    decimal = sum(snafu_to_decimal(line) for line in get_data(25))
    return decimal_to_snafu(decimal)


if __name__ == '__main__':
    print(main())
