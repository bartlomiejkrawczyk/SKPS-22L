from periphery import GPIO, sleep

gpio_out = GPIO("/dev/gpiochip0", 27, "out")

for _ in range(10):
        gpio_out.write(True)
        sleep(0.1)
        gpio_out.write(False)
        sleep(0.1)

gpio_out.close()
