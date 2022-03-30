from periphery import GPIO, sleep

SOUND_VELOCITY = 340.3 # m/s

def distance(trigger: GPIO, echo: GPIO) -> float:
        trigger.write(True)
        sleep(1e-5)
        trigger.write(False)

        start = echo.read_event().timestamp
        end = echo.read_event().timestamp

        return SOUND_VELOCITY * (end - start) / 1e9



def main():
        echo = GPIO("/dev/gpiochip0", 21, "in", edge="both")
        trigger = GPIO("/dev/gpiochip0", 20, "out")

	try:
                while True:
                        print(f'Distance to obstacle: {distance(trigger, echo)}>
                        sleep(0.1)
        except KeyboardInterrupt:
                pass

        echo.close()
        trigger.close()


if __name__ == '__main__':
        main()
