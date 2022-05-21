#include <unistd.h>

#include <fstream>
#include <iostream>
#include <random>
#include <string>

#include "vl53l0x_api.h"
#include "vl53l0x_platform.h"

#define MAX_DEGREE 360
#define MIN_DEGREE 10
#define STEP 5

#define MIN_DUTY_CYCLE 1'000'000
#define MAX_DUTY_CYCLE 2'000'000

#define PWM_CHIP "/sys/class/pwm/pwmchip1"
#define PWM_CHANNEL "/sys/class/pwm/pwmchip1/pwm0"

// Sensor Time Of Flight

#define FAKE_DEVICES

void check_sensor_status(VL53L0X_Error status) {
    if (status != VL53L0X_ERROR_NONE) {
        char buffer[VL53L0X_MAX_STRING_LENGTH];
        VL53L0X_GetPalErrorString(status, buffer);
        std::cerr << "Sensor: failed - " << buffer << std::endl;
        exit(EXIT_FAILURE);
    }
}

void initialize_sensor(VL53L0X_Dev_t &sensor) {
#ifndef FAKE_DEVICES
    VL53L0X_Error status;
    uint32_t ref_spad_count;
    uint8_t is_aperture_spads;
    uint8_t vhv_settings;
    uint8_t phase_cal;

    // Initialize Comms
    sensor.I2cDevAddr = 0x29;

    // choose between i2c-0 and i2c-1
    char i2c[] = "/dev/i2c-1";
    sensor.fd = VL53L0X_i2c_init(i2c, sensor.I2cDevAddr);
    if (sensor.fd < 0) {
        status = VL53L0X_ERROR_CONTROL_INTERFACE;
        std::cerr << "Sensor: failed to initialize" << std::endl;
        check_sensor_status(VL53L0X_ERROR_CONTROL_INTERFACE);
    }

    // Data initialization
    std::cout << "Sensor: Call of VL53L0X_DataInit" << std::endl;
    status = VL53L0X_DataInit(&sensor);
    check_sensor_status(status);

    // Device Initialization
    std::cout << "Sensor: Call of VL53L0X_StaticInit" << std::endl;
    status = VL53L0X_StaticInit(&sensor);
    check_sensor_status(status);

    // Device Initialization
    std::cout << "Sensor: Call of VL53L0X_PerformRefCalibration" << std::endl;
    status = VL53L0X_PerformRefCalibration(&sensor, &vhv_settings, &phase_cal);
    check_sensor_status(status);

    // Device Initialization
    std::cout << "Sensor: Call of VL53L0X_PerformRefSpadManagement" << std::endl;
    status = VL53L0X_PerformRefSpadManagement(&sensor, &ref_spad_count, &is_aperture_spads);
    std::cout << "Sensor: ref_spad_count = " << ref_spad_count
              << ", is_aperture_spads = " << is_aperture_spads << std::endl;
    check_sensor_status(status);

    // Setup in single ranging mode
    std::cout << "Sensor: Call of VL53L0X_SetDeviceMode" << std::endl;
    status = VL53L0X_SetDeviceMode(&sensor, VL53L0X_DEVICEMODE_SINGLE_RANGING);
    check_sensor_status(status);

    status = VL53L0X_SetLimitCheckEnable(&sensor, VL53L0X_CHECKENABLE_SIGMA_FINAL_RANGE, 1);
    check_sensor_status(status);

    status = VL53L0X_SetLimitCheckEnable(&sensor, VL53L0X_CHECKENABLE_SIGNAL_RATE_FINAL_RANGE, 1);
    check_sensor_status(status);

    status = VL53L0X_SetLimitCheckValue(&sensor, VL53L0X_CHECKENABLE_SIGNAL_RATE_FINAL_RANGE,
                                        (FixPoint1616_t)(0.1 * 65536));
    check_sensor_status(status);

    status = VL53L0X_SetLimitCheckValue(&sensor, VL53L0X_CHECKENABLE_SIGMA_FINAL_RANGE,
                                        (FixPoint1616_t)(60 * 65536));
    check_sensor_status(status);

    status = VL53L0X_SetMeasurementTimingBudgetMicroSeconds(&sensor, 33000);
    check_sensor_status(status);

    status = VL53L0X_SetVcselPulsePeriod(&sensor, VL53L0X_VCSEL_PERIOD_PRE_RANGE, 18);
    check_sensor_status(status);

    status = VL53L0X_SetVcselPulsePeriod(&sensor, VL53L0X_VCSEL_PERIOD_FINAL_RANGE, 14);
    check_sensor_status(status);
#else
    (void)sensor;
#endif
}

void check_measurement_status(VL53L0X_RangingMeasurementData_t &ranging_measurement_data) {
    /*
     * New Range Status: data is valid when ranging_measurement_data.RangeStatus = 0
     */

    uint8_t range_status = ranging_measurement_data.RangeStatus;

    if (range_status != 0) {
        std::cerr << "Sensor: measurement failed" << std::endl;

        char buffer[VL53L0X_MAX_STRING_LENGTH];
        VL53L0X_GetRangeStatusString(range_status, buffer);
        std::cerr << "Sensor: range_status - " << range_status << " : " << buffer << std::endl;
    }
}

uint16_t measure_distance(VL53L0X_Dev_t &sensor) {
#ifndef FAKE_DEVICES
    VL53L0X_RangingMeasurementData_t ranging_measurement_data;
    VL53L0X_Error status =
        VL53L0X_PerformSingleRangingMeasurement(&sensor, &ranging_measurement_data);

    check_sensor_status(status);
    check_measurement_status(ranging_measurement_data);

    return ranging_measurement_data.RangeMilliMeter;
#else
    (void)sensor;
    return random() % 10 + 90;
#endif
}

void close_sensor() {
#ifndef FAKE_DEVICES
    /*
     *  Disconnect comms - part of VL53L0X_platform.c
     */
    std::cout << "Sensor: close comms" << std::endl;
    VL53L0X_i2c_close();
#endif
}

// Servo

void write(const std::string &file_path, const std::string &text) {
#ifndef FAKE_DEVICES
    std::ofstream file;
    file.open(file_path);
    file << text << std::endl;
    file.close();
#else
    std::cout << file_path << std::endl;
    std::cout << text << std::endl;
    std::cout << std::endl;
#endif
}

void export_pwm() {
#ifndef FAKE_DEVICES
    write(PWM_CHIP "/export", "0");
#endif
}

void unexport_pwm() {
#ifndef FAKE_DEVICES
    write(PWM_CHIP "/unexport", "0");
#endif
}

void rotate_servo(uint16_t angle) {
    uint32_t duty_cycle = MIN_DUTY_CYCLE + (MAX_DUTY_CYCLE - MIN_DUTY_CYCLE) *
                                               (angle - MIN_DEGREE) / (MAX_DEGREE - MIN_DEGREE);
    write(PWM_CHANNEL "/period", "20000000");
    write(PWM_CHANNEL "/duty_cycle", std::to_string(duty_cycle));
    write(PWM_CHANNEL "/enable", "1");

    usleep(250000);
    write(PWM_CHANNEL "/enable", "0");
}

// Message Queue

void send_data(uint16_t angle, uint16_t distance) {
    std::cout << "angle = " << angle << std::endl;
    std::cout << "distance = " << distance << std::endl;
    std::cout << std::endl;
}

void clean_at_exit() {
    close_sensor();
    unexport_pwm();
}

int main() {
    srand(3141592);

    std::cout << "Hello, Main!" << std::endl;

    if (atexit(clean_at_exit)) {
        std::cerr << "Clean_at_exit: failed" << std::endl;
        return EXIT_FAILURE;
    }

    VL53L0X_Dev_t sensor;
    initialize_sensor(sensor);

    export_pwm();

    uint16_t angle = MIN_DEGREE;
    uint16_t distance = 0;
    int direction = 1;

    while (true) {
        rotate_servo(angle);
        distance = measure_distance(sensor);

        send_data(angle, distance);

        angle += direction * STEP;
        if (angle >= MAX_DEGREE) {
            angle = MAX_DEGREE;
            direction = -direction;
        } else if (angle <= MIN_DEGREE) {
            angle = MIN_DEGREE;
            direction = -direction;
        }
    }

    return 0;
}