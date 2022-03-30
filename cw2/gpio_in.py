from periphery import GPIO, sleep



def main():
        gpio_in = GPIO("/dev/gpiochip0", 17, "in", edge="both")
        gpio_out = GPIO("/dev/gpiochip0", 27, "out")
        value = False
        try:
                while True:
                        gpio_in.read_event()
                        value = not value
                        gpio_out.write(value)

        except KeyboardInterrupt:
                pass

        gpio_in.close()
        gpio_out.close()

if __name__ == '__main__':
        main()

