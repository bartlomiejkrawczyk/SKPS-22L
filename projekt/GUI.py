from matplotlib import pyplot as plt
from random import randint
from math import sin, cos, radians
import time


MAX_DEGREE = 360
MIN_DEGREE = 0
STEP = 5

VALUES = ((MAX_DEGREE - MIN_DEGREE) // STEP)

MAX_DISTANCE = 100


i = 0


def receive_measurement():
    """
    Mock function for generating angle, distance pairs
    TODO: Replace with the real function when ready
    """
    global i
    time.sleep(0.01)  # simulate taking the measurement
    i = (i + STEP) % (MAX_DEGREE - MIN_DEGREE)
    return i + MIN_DEGREE, randint(90, 100)


def calculate_coordinates(angle, radius):
    x = radius * sin(radians(angle))
    y = radius * cos(radians(angle))
    return x, y


# Enable interactive mode
plt.ion()

figure, ax = plt.subplots(figsize=(10, 8))

# Legend
plt.title("LIDAR", fontsize=20)
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

# Make sure aspect ratio is equal - plot is a square
plt.gca().set_aspect('equal', adjustable='box')

# Create separate line for every possible angle
# Every plot initialize with 0 distance
lines = [ax.plot([0, 0], [0, 0], '-o', color='red')[0] for _ in range(VALUES)]

# Make the plot fixed size
plt.xlim(-MAX_DISTANCE, MAX_DISTANCE)
plt.ylim(-MAX_DISTANCE, MAX_DISTANCE)

plt.show()

# Loop through the program until the window is closed
while plt.fignum_exists(figure.number):
    angle, distance = receive_measurement()

    # Map degree to an index
    idx = (angle - MIN_DEGREE) // STEP

    x, y = calculate_coordinates(angle, distance)

    # Update the line distance corresponding to received angle
    lines[idx].set_data([0, x], [0, y])

    figure.canvas.draw()
    figure.canvas.flush_events()
