from periphery import sleep, GPIO
from pwm import generate_pwm

FREQUENCIES = [
    261.63,
    293.66,
    329.63,
    349.23,
    392.00,
    440.00,
    493.88,
    523.25,
    587.33,
    659.25,
    698.46,
    783.99,
    880.00,
    987.77,
    1046.50
]


def main():
    gpio_out = GPIO("/dev/gpiochip0", 18, "out")

    for frequency in FREQUENCIES:
        generate_pwm(0.5, frequency, gpio_out, 0.3)

    gpio_out.close()


if __name__ == '__main__':
    main()
