"""
communication_interface.py
Communication interface between computer vision module and STM32
"""

import serial
import struct
import logging
from typing import Optional, Tuple
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Communication protocol commands
CMD_START_PATROL = 0x01
CMD_STOP_PATROL = 0x02
CMD_FIRE_DETECTED = 0x03
CMD_STATUS_REQUEST = 0x04
CMD_STATUS_RESPONSE = 0x05
CMD_EMERGENCY_STOP = 0x06
CMD_SENSOR_DATA = 0x07
CMD_CV_RESULT = 0x08

PACKET_HEADER = 0xAA


@dataclass
class SensorData:
    """Sensor data from STM32"""
    temperature: float
    smoke_level: int
    flame_value: int


@dataclass
class CVResult:
    """Computer vision detection result"""
    fire_detected: bool
    confidence: float
    smoke_detected: bool


class CommunicationInterface:
    """Interface for communicating with STM32 via UART"""
    
    def __init__(self, port: str = '/dev/ttyUSB0', baudrate: int = 115200):
        """
        Initialize communication interface
        
        Args:
            port: Serial port name
            baudrate: Communication baudrate
        """
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.connected = False
    
    def connect(self) -> bool:
        """
        Connect to STM32
        
        Returns:
            True if connected successfully
        """
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1.0
            )
            self.connected = True
            logger.info(f"Connected to {self.port} at {self.baudrate} baud")
            return True
        except serial.SerialException as e:
            logger.error(f"Failed to connect: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> None:
        """Disconnect from STM32"""
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.connected = False
            logger.info("Disconnected")
    
    def calculate_checksum(self, data: bytes) -> int:
        """
        Calculate XOR checksum
        
        Args:
            data: Data bytes
            
        Returns:
            Checksum byte
        """
        checksum = 0
        for byte in data:
            checksum ^= byte
        return checksum
    
    def send_packet(self, command: int, data: bytes = b'') -> bool:
        """
        Send packet to STM32
        
        Args:
            command: Command byte
            data: Data payload
            
        Returns:
            True if sent successfully
        """
        if not self.connected or not self.serial:
            logger.error("Not connected")
            return False
        
        try:
            length = len(data)
            checksum = self.calculate_checksum(data)
            
            # Build packet: header | command | length | data | checksum
            packet = struct.pack('BBB', PACKET_HEADER, command, length)
            packet += data
            packet += struct.pack('B', checksum)
            
            self.serial.write(packet)
            self.serial.flush()
            
            return True
        except Exception as e:
            logger.error(f"Failed to send packet: {e}")
            return False
    
    def receive_packet(self, timeout: float = 1.0) -> Optional[Tuple[int, bytes]]:
        """
        Receive packet from STM32
        
        Args:
            timeout: Receive timeout in seconds
            
        Returns:
            Tuple of (command, data) or None if failed
        """
        if not self.connected or not self.serial:
            return None
        
        try:
            self.serial.timeout = timeout
            
            # Read header
            header = self.serial.read(1)
            if len(header) == 0 or header[0] != PACKET_HEADER:
                return None
            
            # Read command and length
            cmd_len = self.serial.read(2)
            if len(cmd_len) < 2:
                return None
            
            command = cmd_len[0]
            length = cmd_len[1]
            
            # Read data
            data = self.serial.read(length)
            if len(data) < length:
                return None
            
            # Read checksum
            checksum_byte = self.serial.read(1)
            if len(checksum_byte) == 0:
                return None
            
            # Verify checksum
            expected_checksum = self.calculate_checksum(data)
            if checksum_byte[0] != expected_checksum:
                logger.warning("Checksum mismatch")
                return None
            
            return (command, data)
        
        except Exception as e:
            logger.error(f"Failed to receive packet: {e}")
            return None
    
    def send_cv_result(self, fire_detected: bool, confidence: float, 
                       smoke_detected: bool) -> bool:
        """
        Send computer vision result to STM32
        
        Args:
            fire_detected: Whether fire was detected
            confidence: Detection confidence
            smoke_detected: Whether smoke was detected
            
        Returns:
            True if sent successfully
        """
        # Pack data: fire_detected (1 byte) | confidence (4 bytes float) | smoke_detected (1 byte)
        data = struct.pack('Bf?', fire_detected, confidence, smoke_detected)
        return self.send_packet(CMD_CV_RESULT, data)
    
    def receive_sensor_data(self) -> Optional[SensorData]:
        """
        Receive sensor data from STM32
        
        Returns:
            SensorData object or None if failed
        """
        result = self.receive_packet(timeout=0.5)
        
        if result is None:
            return None
        
        command, data = result
        
        if command != CMD_SENSOR_DATA or len(data) < 8:
            return None
        
        # Unpack data: temperature (4 bytes float) | smoke (2 bytes) | flame (2 bytes)
        temperature, smoke_level, flame_value = struct.unpack('fHH', data[:8])
        
        return SensorData(
            temperature=temperature,
            smoke_level=smoke_level,
            flame_value=flame_value
        )
    
    def send_start_patrol(self) -> bool:
        """Send start patrol command"""
        return self.send_packet(CMD_START_PATROL)
    
    def send_stop_patrol(self) -> bool:
        """Send stop patrol command"""
        return self.send_packet(CMD_STOP_PATROL)
    
    def send_emergency_stop(self) -> bool:
        """Send emergency stop command"""
        return self.send_packet(CMD_EMERGENCY_STOP)


def main():
    """Test communication interface"""
    comm = CommunicationInterface('/dev/ttyUSB0', 115200)
    
    if not comm.connect():
        logger.error("Failed to connect to STM32")
        return
    
    try:
        # Send start patrol command
        comm.send_start_patrol()
        
        # Receive sensor data
        sensor_data = comm.receive_sensor_data()
        if sensor_data:
            logger.info(f"Sensor data: Temp={sensor_data.temperature}°C, "
                       f"Smoke={sensor_data.smoke_level}ppm, "
                       f"Flame={sensor_data.flame_value}")
        
        # Send CV result
        comm.send_cv_result(fire_detected=True, confidence=0.85, 
                           smoke_detected=False)
    
    finally:
        comm.disconnect()


if __name__ == "__main__":
    main()
