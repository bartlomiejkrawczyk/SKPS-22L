from matplotlib import pyplot as plt
from random import randint
from math import sin, cos, radians
import numpy as np
import time

MAX_DEGREE = 360
MIN_DEGREE = 0

plt.ion()
figure, ax = plt.subplots(figsize=(10, 8))
plt.title("LIDAR", fontsize=20)
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

data = [(i, 0) for i in range(MAX_DEGREE - MIN_DEGREE)]
i = 0
while True:
    data[i] = (i, randint(1,10))
    x = data[i][1] * sin(radians(data[i][0]))
    y = data[i][1] * cos(radians(data[i][0]))
    plt.plot([0, x], [0, y], "-o", color="red")

    plt.xlim([-10,10])
    plt.ylim([-10,10])
    figure.canvas.draw()
    figure.canvas.flush_events()
    # time.sleep(0.01)

    i = (i + 1) % (MAX_DEGREE - MIN_DEGREE)
    if i == MIN_DEGREE or i == MAX_DEGREE:
        plt.clf()
