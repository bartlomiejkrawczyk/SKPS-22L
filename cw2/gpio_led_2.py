from periphery import GPIO
from pwm import generate_pwm
from math import cos, pi


def main():
    output = GPIO("/dev/gpiochip0", 27, "out")

    generate_pwm([
        (cos(pi * n / 100) + 1) / 2
        for n in range(10_000)
    ], 50, output, 10)

    output.close()


if __name__ == '__main__':
    main()
