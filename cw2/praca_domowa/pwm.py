from itertools import repeat
import argparse
import time
import math

def generate_pwm(frequencies, duty_cycles):
    if isinstance(frequencies, int):
            frequencies = repeat(frequencies)
    if isinstance(duty_cycles, float):
        duty_cycles = repeat(duty_cycles)

    start = time.monotonic_ns()
    for frequency, duty_cycle in zip(frequencies, duty_cycles):
        up_time = 1 / frequency * duty_cycle
        down_time = 1 / frequency - up_time
        if up_time:
            timestamp = time.monotonic_ns() - start
            print(timestamp, "1", sep="\t")
            time.sleep(up_time)
        if down_time:
            timestamp = time.monotonic_ns() - start
            print(timestamp, "0", sep="\t")
            time.sleep(down_time)




def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-t", "--test", type=int, default=1, help="Select test:\n 0.Const cycle,\n1.Const frequency")
    args = arg_parser.parse_args()
    if args.test == 0:
        generate_pwm([1, 2, 3, 4, 5, 4, 3, 2, 1], .5)
    elif args.test == 1:
        generate_pwm(5, [math.sin(math.pi * i / 20) for i in range(20 + 1)])
    else:
        print("Invalid test number")


if __name__ == "__main__":
    main()