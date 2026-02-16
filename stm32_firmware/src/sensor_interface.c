/**
 * @file sensor_interface.c
 * @brief Sensor interface implementation for fire detection
 */

#include "sensor_interface.h"

/* Global sensor data */
static SensorData_t sensor_data = {0};

/**
 * @brief Initialize all sensors
 */
int sensor_init(void) {
    /* Initialize ADC for analog sensors */
    /* Initialize I2C for digital sensors if needed */
    /* Configure GPIO for sensor inputs */
    
    sensor_data.temperature = 0.0f;
    sensor_data.smoke_level = 0;
    sensor_data.flame_value = 0;
    sensor_data.fire_detected = false;
    
    return 0;
}

/**
 * @brief Read all sensor data
 */
int sensor_read_all(SensorData_t *data) {
    if (data == NULL) {
        return -1;
    }
    
    /* Read temperature sensor */
    data->temperature = sensor_read_temperature();
    
    /* Read smoke sensor */
    data->smoke_level = sensor_read_smoke();
    
    /* Read flame sensor */
    data->flame_value = sensor_read_flame();
    
    /* Check for fire condition */
    data->fire_detected = sensor_check_fire(data);
    
    /* Update global sensor data */
    sensor_data = *data;
    
    return 0;
}

/**
 * @brief Check if fire is detected based on sensor readings
 */
bool sensor_check_fire(const SensorData_t *data) {
    if (data == NULL) {
        return false;
    }
    
    /* Fire detected if any condition is met */
    bool temp_alarm = (data->temperature > TEMP_THRESHOLD_CELSIUS);
    bool smoke_alarm = (data->smoke_level > SMOKE_THRESHOLD_PPM);
    bool flame_alarm = (data->flame_value > FLAME_DETECTION_THRESHOLD);
    
    return (temp_alarm || smoke_alarm || flame_alarm);
}

/**
 * @brief Read temperature sensor
 */
float sensor_read_temperature(void) {
    /* Read ADC channel for temperature sensor */
    /* Convert ADC value to temperature using sensor calibration */
    /* Example: LM35 gives 10mV per degree Celsius */
    
    uint16_t adc_value = 0;  /* Read from ADC */
    float voltage = (adc_value / 4095.0f) * 3.3f;  /* Assuming 12-bit ADC, 3.3V ref */
    float temperature = voltage * 100.0f;  /* For LM35: 10mV/°C */
    
    return temperature;
}

/**
 * @brief Read smoke sensor
 */
uint16_t sensor_read_smoke(void) {
    /* Read ADC channel for MQ-2 smoke sensor */
    /* Convert ADC value to PPM using sensor characteristics */
    
    uint16_t adc_value = 0;  /* Read from ADC */
    float voltage = (adc_value / 4095.0f) * 3.3f;
    
    /* Simplified conversion - actual conversion depends on sensor calibration */
    uint16_t ppm = (uint16_t)(voltage * 100.0f);
    
    return ppm;
}

/**
 * @brief Read flame sensor
 */
uint16_t sensor_read_flame(void) {
    /* Read ADC channel for flame sensor */
    /* IR flame sensor gives higher voltage when flame detected */
    
    uint16_t adc_value = 0;  /* Read from ADC */
    
    return adc_value;
}
