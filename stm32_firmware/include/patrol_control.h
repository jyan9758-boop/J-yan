/**
 * @file patrol_control.h
 * @brief Patrolling and navigation control
 * @description Implements autonomous patrolling logic and navigation
 */

#ifndef PATROL_CONTROL_H
#define PATROL_CONTROL_H

#include <stdint.h>
#include <stdbool.h>

/* Patrol states */
typedef enum {
    PATROL_IDLE = 0,
    PATROL_FORWARD,
    PATROL_TURNING,
    PATROL_SCANNING,
    PATROL_FIRE_DETECTED,
    PATROL_EMERGENCY_STOP
} PatrolState_t;

/* Patrol parameters */
typedef struct {
    uint32_t forward_time_ms;     /* Time to move forward */
    uint32_t turn_time_ms;        /* Time to turn */
    uint32_t scan_time_ms;        /* Time to scan area */
    uint8_t patrol_speed;         /* Patrol speed (0-100) */
    bool obstacle_avoidance;      /* Enable obstacle avoidance */
} PatrolConfig_t;

/**
 * @brief Initialize patrol control system
 * @param config Patrol configuration parameters
 * @return 0 on success, -1 on failure
 */
int patrol_init(const PatrolConfig_t *config);

/**
 * @brief Start autonomous patrolling
 */
void patrol_start(void);

/**
 * @brief Stop patrolling
 */
void patrol_stop(void);

/**
 * @brief Update patrol state machine
 * @note Should be called periodically in main loop
 */
void patrol_update(void);

/**
 * @brief Get current patrol state
 * @return Current patrol state
 */
PatrolState_t patrol_get_state(void);

/**
 * @brief Handle fire detection event
 */
void patrol_handle_fire_detection(void);

/**
 * @brief Set patrol configuration
 * @param config New patrol configuration
 */
void patrol_set_config(const PatrolConfig_t *config);

#endif /* PATROL_CONTROL_H */
