# Fire Inspection Robot System

## Overview

An autonomous fire inspection and patrolling robot system based on the STM32 microcontroller and computer vision. The system combines embedded firmware control with advanced computer vision algorithms to detect and respond to fire hazards in real-time.

## System Architecture

### Components

1. **STM32 Firmware** (`stm32_firmware/`)
   - Motor control for autonomous navigation
   - Sensor interface (temperature, smoke, flame sensors)
   - Patrol control and navigation logic
   - Communication interface with computer vision module

2. **Computer Vision Module** (`computer_vision/`)
   - Fire detection using OpenCV
   - Smoke detection algorithms
   - Real-time video processing
   - UART communication with STM32

3. **Configuration** (`config/`)
   - System parameters and thresholds
   - Customizable detection settings

## Hardware Requirements

### STM32 Microcontroller Setup
- STM32 microcontroller (recommended: STM32F4 series or higher)
- Motor driver (L298N or similar)
- DC motors for robot movement
- Temperature sensor (LM35 or DHT22)
- Smoke sensor (MQ-2)
- Flame sensor (IR flame detector)
- UART interface for communication

### Computer Vision Hardware
- Computer/Raspberry Pi with Python support
- USB camera or webcam
- USB-to-UART adapter for STM32 communication

## Software Requirements

### STM32 Firmware
- STM32CubeIDE or Keil MDK
- STM32 HAL library
- ARM GCC toolchain

### Computer Vision Module
```bash
Python 3.8+
opencv-python >= 4.8.0
numpy >= 1.24.0
pyserial >= 3.5
```

## Installation

### 1. STM32 Firmware Setup

```bash
# Clone the repository
git clone https://github.com/jyan9758-boop/J-yan.git
cd J-yan/stm32_firmware

# Open project in STM32CubeIDE or your preferred IDE
# Configure GPIO pins according to your hardware setup
# Build and flash to STM32 microcontroller
```

### 2. Computer Vision Module Setup

```bash
# Navigate to computer vision directory
cd computer_vision

# Install Python dependencies
pip install -r requirements.txt
```

## Configuration

Edit `config/config.py` to customize:
- Camera settings
- Fire detection thresholds
- Serial port configuration
- Patrol parameters
- Sensor thresholds

## Usage

### Running the Computer Vision Module

Basic usage:
```bash
cd computer_vision/src
python main.py
```

With custom parameters:
```bash
python main.py --port /dev/ttyUSB0 --camera 0
```

Command line options:
- `--port`: Serial port for STM32 (default: /dev/ttyUSB0)
- `--camera`: Camera source (default: 0 for webcam)
- `--no-display`: Disable video display

### Keyboard Controls (when display is enabled)
- `q`: Quit application
- `s`: Emergency stop

### Running Fire Detection Only (Testing)
```bash
cd computer_vision/src
python fire_detection.py
```

## System Features

### Fire Detection
- Color-based fire detection using HSV color space
- Multi-threshold fire color detection (orange, red, yellow)
- Contour analysis for fire region identification
- Confidence scoring based on area and color intensity
- Real-time video processing

### Smoke Detection
- Grayscale analysis for smoke-like regions
- Texture analysis (low standard deviation)
- Brightness-based smoke identification

### Autonomous Patrolling
- State machine-based navigation
- Forward movement with periodic turns
- Area scanning at waypoints
- Automatic fire response behavior

### Sensor Integration
- Real-time temperature monitoring
- Smoke level detection
- Flame sensor input
- Multi-sensor fire confirmation

### Communication Protocol
- UART-based communication between STM32 and CV module
- Packet-based protocol with checksum verification
- Bidirectional data exchange
- Command and status reporting

## Communication Protocol

### Packet Structure
```
[Header] [Command] [Length] [Data...] [Checksum]
  0xAA     1 byte    1 byte   N bytes    1 byte
```

### Commands
- `0x01`: Start patrol
- `0x02`: Stop patrol
- `0x03`: Fire detected
- `0x04`: Status request
- `0x05`: Status response
- `0x06`: Emergency stop
- `0x07`: Sensor data
- `0x08`: Computer vision result

## Project Structure

```
J-yan/
├── stm32_firmware/
│   ├── include/
│   │   ├── motor_control.h
│   │   ├── sensor_interface.h
│   │   ├── patrol_control.h
│   │   └── communication.h
│   └── src/
│       ├── main.c
│       ├── motor_control.c
│       ├── sensor_interface.c
│       ├── patrol_control.c
│       └── communication.c
├── computer_vision/
│   ├── src/
│   │   ├── main.py
│   │   ├── fire_detection.py
│   │   └── communication_interface.py
│   └── requirements.txt
├── config/
│   └── config.py
├── docs/
│   ├── hardware_setup.md
│   ├── software_guide.md
│   └── api_reference.md
└── README.md
```

## Safety Features

1. **Emergency Stop**: Immediate motor shutdown on command
2. **Multi-sensor Verification**: Fire confirmation using multiple sensors
3. **Automatic Alert**: System stops and alerts when fire detected
4. **Watchdog Timer**: System reset on firmware hang
5. **Communication Timeout**: Safe state on communication loss

## Development

### Building STM32 Firmware
```bash
# Using STM32CubeIDE
# 1. Import project
# 2. Configure for your STM32 board
# 3. Build project
# 4. Flash to microcontroller
```

### Testing Computer Vision Module
```bash
# Run fire detection test
cd computer_vision/src
python fire_detection.py

# Run communication test
python communication_interface.py
```

## Troubleshooting

### Camera Not Detected
- Check camera connection
- Try different camera index: `python main.py --camera 1`
- Verify camera permissions

### Serial Port Connection Failed
- Check serial port name: `ls /dev/tty*`
- Verify permissions: `sudo chmod 666 /dev/ttyUSB0`
- Check STM32 connection

### Fire Detection Issues
- Adjust HSV color thresholds in config
- Improve lighting conditions
- Calibrate confidence threshold

## Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available for educational and research purposes.

## Acknowledgments

- OpenCV community for computer vision tools
- STM32 community for embedded resources
- Contributors and testers

## Contact

For questions or support, please open an issue on GitHub.

## Future Enhancements

- [ ] Deep learning-based fire detection
- [ ] Path planning with SLAM
- [ ] Multi-robot coordination
- [ ] Cloud integration for remote monitoring
- [ ] Mobile app for control and monitoring
- [ ] Advanced obstacle avoidance
- [ ] GPS navigation support
