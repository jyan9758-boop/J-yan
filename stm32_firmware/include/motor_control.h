/**
 * @file motor_control.h
 * @brief Motor control interface for autonomous robot
 * @description Controls DC motors for robot movement and navigation
 */

#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

#include <stdint.h>

/* Motor directions */
typedef enum {
    MOTOR_FORWARD = 0,
    MOTOR_BACKWARD,
    MOTOR_LEFT,
    MOTOR_RIGHT,
    MOTOR_STOP
} MotorDirection_t;

/* Motor speed levels */
typedef enum {
    SPEED_STOP = 0,
    SPEED_SLOW = 40,
    SPEED_MEDIUM = 70,
    SPEED_FAST = 100
} MotorSpeed_t;

/**
 * @brief Initialize motor control system
 * @return 0 on success, -1 on failure
 */
int motor_control_init(void);

/**
 * @brief Set motor direction and speed
 * @param direction Direction to move
 * @param speed Speed percentage (0-100)
 */
void motor_set_direction(MotorDirection_t direction, uint8_t speed);

/**
 * @brief Stop all motors immediately
 */
void motor_emergency_stop(void);

/**
 * @brief Get current motor speed
 * @return Current speed percentage
 */
uint8_t motor_get_speed(void);

#endif /* MOTOR_CONTROL_H */
