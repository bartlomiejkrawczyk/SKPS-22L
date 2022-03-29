from typing import Iterable, Union, Optional
from itertools import repeat

import time


def active_sleep(nanoseconds: int) -> None:
    end = time.monotonic_ns() + nanoseconds

    while time.monotonic_ns() < end:
        pass


def generate_pwm(duty_cycles: Union[Iterable[float], float],
                 frequencies: Union[Iterable[int], int],
                 max_time: Optional[float] = None) -> None:
    """
    Print to the standard output timestamp and value of pwm signal

    Args:
        duty_cycles (Union[Iterable[float], float]): Value of consequtive duty_cycles from range [0.0; 1.0]
        frequencies (Union[Iterable[int], int]): Value of consequtive frequencies in Hz
        max_time (float): Maximal time through which we are to generate the signal (in seconds)
    """

    if isinstance(duty_cycles, float):
        duty_cycles = repeat(duty_cycles)

    if isinstance(frequencies, int):
        frequencies = repeat(frequencies)

    start = time.monotonic_ns()
    end = None

    if max_time:
        max_time = int(max_time * 1e9)
        end = start + max_time

    current_time = time.monotonic_ns()

    for duty_cycle, frequency in zip(duty_cycles, frequencies):
        period_ns = int(1e9 / frequency)

        up_time = int(period_ns * duty_cycle)
        down_time = period_ns - up_time

        if up_time != 0:
            print(current_time - start, 1, sep='\t')
            active_sleep(up_time)

        current_time = time.monotonic_ns()

        if down_time != 0:
            print(current_time - start, 0, sep='\t')
            active_sleep(down_time)

        current_time = time.monotonic_ns()

        if end and current_time > end:
            return


def main():
    generate_pwm(0.75, 10, 0.5)


if __name__ == '__main__':
    main()
