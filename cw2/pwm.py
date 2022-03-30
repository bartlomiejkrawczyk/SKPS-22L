from typing import Iterable, Union, Optional
from itertools import repeat

import time
from periphery import GPIO

def active_sleep(nanoseconds: int) -> None:
    end = time.monotonic_ns() + nanoseconds

    while time.monotonic_ns() < end:
        pass


def generate_pwm(duty_cycles: Union[Iterable[float], float],
                 frequencies: Union[Iterable[float], float],
                 output: GPIO,
                 max_time: Optional[float] = None) -> None:
    """
    Print to the standard output timestamp and value of pwm signal

	Args:
        duty_cycles (Union[Iterable[float], float]): Value of consequtive duty_cycles from range [0.0; 1.0]
        frequencies (Union[Iterable[float], float]): Value of consequtive frequencies in Hz
        output (GPIO): Pin to which we want to send the signal
        max_time (float): Maximal time through which we are to generate the signal (in seconds)
    """

    if isinstance(duty_cycles, float):
        duty_cycles = repeat(duty_cycles)

    if isinstance(frequencies, float) or isinstance(frequencies, int):
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
            print(current_time - start, 1, sep='\t');output.write(True)
            active_sleep(up_time)

        current_time = time.monotonic_ns()

        if down_time != 0:
            print(current_time - start, 0, sep='\t');output.write(False)
			active_sleep(down_time)

        current_time = time.monotonic_ns()

        if end and current_time > end:
            return




