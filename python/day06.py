from utils import get_data


def main():
    datastream = get_data(6)[0]
    packet_marker = message_marker = None
    for i in range(len(datastream) - 3):
        if packet_marker is None and len(set(datastream[i:i+4])) == 4:
            packet_marker = i + 4
        if message_marker is None and len(set(datastream[i:i+14])) == 14:
            message_marker = i + 14
        if not (packet_marker is None or message_marker is None):
            break
    return packet_marker, message_marker


if __name__ == '__main__':
    print(main())
