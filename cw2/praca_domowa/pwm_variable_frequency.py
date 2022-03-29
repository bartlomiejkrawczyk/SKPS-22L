from pwm import generate_pwm
from random import randint


def main():
    generate_pwm(0.5, [randint(1, 99) for _ in range(50)])


if __name__ == '__main__':
    main()
