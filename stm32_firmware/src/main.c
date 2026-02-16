/**
 * @file main.c
 * @brief Main application for fire inspection robot
 * @description STM32 firmware main application integrating all modules
 * 
 * @note This is a template implementation. Hardware initialization and HAL-specific
 *       functions should be implemented according to your STM32 board configuration.
 */

#include "motor_control.h"
#include "sensor_interface.h"
#include "patrol_control.h"
#include "communication.h"

/* System status */
typedef struct {
    bool system_initialized;
    bool patrol_active;
    bool fire_detected;
    uint32_t uptime_seconds;
} SystemStatus_t;

static SystemStatus_t system_status = {0};

/**
 * @brief System initialization
 */
int system_init(void) {
    /* Initialize hardware */
    /* Configure system clock */
    /* Initialize GPIO */
    /* Initialize timers */
    
    /* Initialize modules */
    if (motor_control_init() != 0) {
        return -1;
    }
    
    if (sensor_init() != 0) {
        return -1;
    }
    
    PatrolConfig_t patrol_cfg = {
        .forward_time_ms = 3000,
        .turn_time_ms = 1000,
        .scan_time_ms = 2000,
        .patrol_speed = SPEED_MEDIUM,
        .obstacle_avoidance = true
    };
    
    if (patrol_init(&patrol_cfg) != 0) {
        return -1;
    }
    
    if (comm_init(115200) != 0) {
        return -1;
    }
    
    system_status.system_initialized = true;
    system_status.patrol_active = false;
    system_status.fire_detected = false;
    system_status.uptime_seconds = 0;
    
    return 0;
}

/**
 * @brief Main application loop
 */
void main_loop(void) {
    static uint32_t sensor_read_counter = 0;
    static uint32_t comm_update_counter = 0;
    
    /* Update patrol control (called every 10ms) */
    patrol_update();
    
    /* Read sensors every 100ms */
    sensor_read_counter++;
    if (sensor_read_counter >= 10) {
        sensor_read_counter = 0;
        
        SensorData_t sensor_data;
        if (sensor_read_all(&sensor_data) == 0) {
            system_status.fire_detected = sensor_data.fire_detected;
            
            /* Send sensor data to CV module every 500ms */
            comm_update_counter++;
            if (comm_update_counter >= 5) {
                comm_update_counter = 0;
                comm_send_sensor_data(
                    sensor_data.temperature,
                    sensor_data.smoke_level,
                    sensor_data.flame_value
                );
            }
        }
    }
    
    /* Check for incoming commands */
    CommPacket_t rx_packet;
    if (comm_receive_packet(&rx_packet, 10) == 0) {
        comm_process_command(rx_packet.command, rx_packet.data, rx_packet.length);
    }
}

/**
 * @brief Main function
 */
int main(void) {
    /* Initialize system */
    if (system_init() != 0) {
        /* Initialization failed - halt */
        while (1) {
            /* Error indication */
        }
    }
    
    /* Start autonomous patrolling */
    patrol_start();
    system_status.patrol_active = true;
    
    /* Main loop */
    while (1) {
        main_loop();
        
        /* Delay 10ms */
        /* HAL_Delay(10); */
    }
    
    return 0;
}
