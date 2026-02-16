/**
 * @file patrol_control.c
 * @brief Patrolling and navigation control implementation
 */

#include "patrol_control.h"
#include "motor_control.h"
#include "sensor_interface.h"
#include <string.h>

/* Global variables */
static PatrolState_t patrol_state = PATROL_IDLE;
static PatrolConfig_t patrol_config;
static uint32_t state_timer = 0;
static bool patrol_active = false;

/**
 * @brief Initialize patrol control system
 */
int patrol_init(const PatrolConfig_t *config) {
    if (config == NULL) {
        /* Use default configuration */
        patrol_config.forward_time_ms = 3000;
        patrol_config.turn_time_ms = 1000;
        patrol_config.scan_time_ms = 2000;
        patrol_config.patrol_speed = SPEED_MEDIUM;
        patrol_config.obstacle_avoidance = true;
    } else {
        memcpy(&patrol_config, config, sizeof(PatrolConfig_t));
    }
    
    patrol_state = PATROL_IDLE;
    state_timer = 0;
    patrol_active = false;
    
    return 0;
}

/**
 * @brief Start autonomous patrolling
 */
void patrol_start(void) {
    patrol_active = true;
    patrol_state = PATROL_FORWARD;
    state_timer = 0;
    
    /* Start moving forward */
    motor_set_direction(MOTOR_FORWARD, patrol_config.patrol_speed);
}

/**
 * @brief Stop patrolling
 */
void patrol_stop(void) {
    patrol_active = false;
    patrol_state = PATROL_IDLE;
    motor_emergency_stop();
}

/**
 * @brief Update patrol state machine
 */
void patrol_update(void) {
    if (!patrol_active) {
        return;
    }
    
    /* Check for fire detection */
    SensorData_t sensor_data;
    sensor_read_all(&sensor_data);
    
    if (sensor_data.fire_detected) {
        patrol_handle_fire_detection();
        return;
    }
    
    /* Update state timer (assuming this is called every 10ms) */
    state_timer += 10;
    
    /* State machine */
    switch (patrol_state) {
        case PATROL_FORWARD:
            if (state_timer >= patrol_config.forward_time_ms) {
                /* Transition to turning */
                patrol_state = PATROL_TURNING;
                state_timer = 0;
                motor_set_direction(MOTOR_RIGHT, patrol_config.patrol_speed);
            }
            break;
            
        case PATROL_TURNING:
            if (state_timer >= patrol_config.turn_time_ms) {
                /* Transition to scanning */
                patrol_state = PATROL_SCANNING;
                state_timer = 0;
                motor_set_direction(MOTOR_STOP, 0);
            }
            break;
            
        case PATROL_SCANNING:
            if (state_timer >= patrol_config.scan_time_ms) {
                /* Transition back to forward */
                patrol_state = PATROL_FORWARD;
                state_timer = 0;
                motor_set_direction(MOTOR_FORWARD, patrol_config.patrol_speed);
            }
            break;
            
        case PATROL_FIRE_DETECTED:
            /* Stay in this state until manually reset */
            motor_emergency_stop();
            break;
            
        case PATROL_EMERGENCY_STOP:
            motor_emergency_stop();
            break;
            
        default:
            patrol_state = PATROL_IDLE;
            break;
    }
}

/**
 * @brief Get current patrol state
 */
PatrolState_t patrol_get_state(void) {
    return patrol_state;
}

/**
 * @brief Handle fire detection event
 */
void patrol_handle_fire_detection(void) {
    patrol_state = PATROL_FIRE_DETECTED;
    motor_emergency_stop();
    
    /* Trigger alarm/notification */
    /* Send alert to control station */
}

/**
 * @brief Set patrol configuration
 */
void patrol_set_config(const PatrolConfig_t *config) {
    if (config != NULL) {
        memcpy(&patrol_config, config, sizeof(PatrolConfig_t));
    }
}
