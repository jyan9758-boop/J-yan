/**
 * @file communication.h
 * @brief Communication interface with computer vision module
 * @description UART communication protocol for CV module integration
 */

#ifndef COMMUNICATION_H
#define COMMUNICATION_H

#include <stdint.h>
#include <stdbool.h>

/* Communication protocol commands */
#define CMD_START_PATROL     0x01
#define CMD_STOP_PATROL      0x02
#define CMD_FIRE_DETECTED    0x03
#define CMD_STATUS_REQUEST   0x04
#define CMD_STATUS_RESPONSE  0x05
#define CMD_EMERGENCY_STOP   0x06
#define CMD_SENSOR_DATA      0x07
#define CMD_CV_RESULT        0x08

/* Communication packet structure */
typedef struct __attribute__((packed)) {
    uint8_t header;         /* Packet header (0xAA) */
    uint8_t command;        /* Command byte */
    uint8_t length;         /* Data length */
    uint8_t data[64];       /* Data payload */
    uint8_t checksum;       /* Checksum byte */
} CommPacket_t;

/**
 * @brief Initialize UART communication
 * @param baudrate UART baudrate
 * @return 0 on success, -1 on failure
 */
int comm_init(uint32_t baudrate);

/**
 * @brief Send packet to computer vision module
 * @param packet Pointer to packet structure
 * @return 0 on success, -1 on failure
 */
int comm_send_packet(const CommPacket_t *packet);

/**
 * @brief Receive packet from computer vision module
 * @param packet Pointer to packet structure
 * @param timeout_ms Timeout in milliseconds
 * @return 0 on success, -1 on failure
 */
int comm_receive_packet(CommPacket_t *packet, uint32_t timeout_ms);

/**
 * @brief Send sensor data to CV module
 * @param temp Temperature value
 * @param smoke Smoke level
 * @param flame Flame value
 * @return 0 on success, -1 on failure
 */
int comm_send_sensor_data(float temp, uint16_t smoke, uint16_t flame);

/**
 * @brief Process received command
 * @param command Command byte
 * @param data Data payload
 * @param length Data length
 */
void comm_process_command(uint8_t command, const uint8_t *data, uint8_t length);

/**
 * @brief Calculate checksum for packet
 * @param data Data to calculate checksum for
 * @param length Data length
 * @return Checksum byte
 */
uint8_t comm_calculate_checksum(const uint8_t *data, uint8_t length);

#endif /* COMMUNICATION_H */
