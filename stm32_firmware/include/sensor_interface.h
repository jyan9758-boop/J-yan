/**
 * @file sensor_interface.h
 * @brief Sensor interface for fire detection
 * @description Interfaces with temperature, smoke, and flame sensors
 */

#ifndef SENSOR_INTERFACE_H
#define SENSOR_INTERFACE_H

#include <stdint.h>
#include <stdbool.h>

/* Sensor thresholds */
#define TEMP_THRESHOLD_CELSIUS    45.0f
#define SMOKE_THRESHOLD_PPM       150
#define FLAME_DETECTION_THRESHOLD 500

/* Sensor data structure */
typedef struct {
    float temperature;      /* Temperature in Celsius */
    uint16_t smoke_level;   /* Smoke level in PPM */
    uint16_t flame_value;   /* Flame sensor analog value */
    bool fire_detected;     /* Fire detection flag */
} SensorData_t;

/**
 * @brief Initialize all sensors
 * @return 0 on success, -1 on failure
 */
int sensor_init(void);

/**
 * @brief Read all sensor data
 * @param data Pointer to sensor data structure
 * @return 0 on success, -1 on failure
 */
int sensor_read_all(SensorData_t *data);

/**
 * @brief Check if fire is detected based on sensor readings
 * @param data Pointer to sensor data
 * @return true if fire detected, false otherwise
 */
bool sensor_check_fire(const SensorData_t *data);

/**
 * @brief Read temperature sensor
 * @return Temperature in Celsius
 */
float sensor_read_temperature(void);

/**
 * @brief Read smoke sensor
 * @return Smoke level in PPM
 */
uint16_t sensor_read_smoke(void);

/**
 * @brief Read flame sensor
 * @return Flame sensor value
 */
uint16_t sensor_read_flame(void);

#endif /* SENSOR_INTERFACE_H */
