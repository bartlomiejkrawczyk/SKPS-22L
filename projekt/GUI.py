from matplotlib import pyplot as plt
from math import sin, cos, radians
import socket

HOST = ''
PORT = 8888

MAX_DEGREE = 180
MIN_DEGREE = 120
STEP = 10

VALUES = ((MAX_DEGREE - MIN_DEGREE) // STEP) + 1

MAX_DISTANCE = 100


def receive_measurement():
    global soc
    data = str(soc.recv(1024))

    angle, distance = data[2:-5].split(',')

    angle = int(angle)
    distance = int(distance)

    print(f'{angle=}')
    print(f'{distance=}')
    print()

    return angle, distance


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

figure.canvas.draw()
figure.canvas.flush_events()

# Setup Connection to RPI
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.connect((HOST, PORT))

# Initialize connection by sending message
soc.send(b"S")

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
