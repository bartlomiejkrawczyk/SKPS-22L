import sys
from matplotlib import pyplot as plt


def main():
    times = [0.0]
    previous_time = 0.0
    previous_value = 0
    values = [previous_value]

    signal = [0.5]

    for line in sys.stdin:
        time, value = line.strip().split('\t')

        time = int(time) / 1e9
        value = int(value)

        times.append(time)
        times.append(times[-1])

        if previous_value == 1.0:
            signal.append(signal[-1] + time - previous_time)
        else:
            signal.append(signal[-1] - time + previous_time)

        values.append(previous_value)
        values.append(value)

        previous_value = value
        previous_time = time

    plt.plot(times, values)
    plt.plot(times[::2], signal, color='red')
    plt.show()


if __name__ == '__main__':
    main()
