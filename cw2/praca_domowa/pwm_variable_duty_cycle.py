from pwm import generate_pwm
from math import cos, pi


def main():
    generate_pwm([(cos(pi * n / 10) + 1) / 2 for n in range(50)], 10)


if __name__ == '__main__':
    main()
