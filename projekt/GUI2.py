from matplotlib import pyplot as plt
from random import randint
from math import sin, cos, radians

MAX_DEGREE = 360
MIN_DEGREE = 0

plt.ion()
figure, ax = plt.subplots(figsize=(10, 8))
plt.title("LIDAR", fontsize=20)
plt.xlabel("X-axis")
plt.ylabel("Y-axis")


while True:
    data = [(i, randint(5, 10)) for i in range(MAX_DEGREE - MIN_DEGREE)]
    points = []
    for a, d in data:
        points.append((d * sin(radians(a)), d * cos(radians(a))))

    plt.clf()
    for x, y in points:
        plt.plot([0, x], [0, y], "-o", color="red")

    figure.canvas.draw()
    figure.canvas.flush_events()
    plt.xlim([-10,10])
    plt.ylim([-10,10])