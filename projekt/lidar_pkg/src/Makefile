CC = g++

CFLAGS += -Wall -Wextra -Wpedantic

all: lidar connection

libVL53L0X_Rasp.a:
	API_DIR=../VL53L0X_API $(MAKE) -C VL53L0X_rasp


lidar: main.cpp libVL53L0X_Rasp.a
	$(CC) -I VL53L0X_rasp/platform/inc -I VL53L0X_API/Api/core/inc $(CFLAGS) -o main main.cpp -LVL53L0X_rasp/bin -lVL53L0X_Rasp


connection: connection.cpp
	$(CC) $(CFLAGS) -o connection connection.cpp


clean:
	rm main connection