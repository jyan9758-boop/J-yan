# Software Guide

## Development Environment Setup

### STM32 Development

#### Option 1: STM32CubeIDE (Recommended)

1. **Download and Install**
   ```bash
   # Download from: https://www.st.com/en/development-tools/stm32cubeide.html
   # Install according to your OS
   ```

2. **Create New Project**
   - File -> New -> STM32 Project
   - Select your STM32 board (e.g., STM32F407VG)
   - Choose project name and location

3. **Configure Peripherals**
   - Open .ioc file in CubeMX
   - Configure GPIO pins for motor control
   - Configure ADC for sensors
   - Configure UART for communication
   - Configure timers for PWM
   - Generate code

4. **Import Source Files**
   ```bash
   # Copy files from this repository
   cp -r stm32_firmware/include/* Core/Inc/
   cp -r stm32_firmware/src/* Core/Src/
   ```

#### Option 2: Keil MDK

1. **Install Keil MDK**
   - Download from ARM website
   - Install STM32 device pack

2. **Create Project**
   - New Project -> Select STM32 device
   - Add source files from repository
   - Configure project settings

### Python Development

#### Install Python

```bash
# Linux/Mac
sudo apt-get install python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

#### Install Dependencies

```bash
cd computer_vision
pip3 install -r requirements.txt
```

#### Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Building and Flashing STM32 Firmware

### Using STM32CubeIDE

1. **Build Project**
   - Right-click project -> Build Project
   - Or press Ctrl+B
   - Check console for errors

2. **Flash to Board**
   - Connect ST-Link to board
   - Right-click project -> Debug As -> STM32 C/C++ Application
   - Or use Run -> Run As -> STM32 C/C++ Application

### Using Command Line

```bash
# Build using arm-none-eabi-gcc
cd stm32_firmware
make all

# Flash using st-flash
st-flash write build/firmware.bin 0x8000000

# Or using OpenOCD
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg \
  -c "program build/firmware.elf verify reset exit"
```

## Running the System

### 1. Start STM32 Firmware

```bash
# Power on the robot
# Firmware starts automatically on boot
# LED should indicate system ready
```

### 2. Connect Computer Vision Module

```bash
# Activate virtual environment (if using)
source venv/bin/activate

# Navigate to source directory
cd computer_vision/src

# Run with default settings
python3 main.py

# Or with custom settings
python3 main.py --port /dev/ttyUSB0 --camera 0
```

### 3. Monitor Operation

```bash
# View logs in terminal
# Watch video feed for fire detection
# Monitor sensor data from STM32
```

## Configuration

### STM32 Configuration

Edit configuration in firmware source files:

```c
// In patrol_control.c
PatrolConfig_t default_config = {
    .forward_time_ms = 3000,     // Adjust patrol forward time
    .turn_time_ms = 1000,        // Adjust turn duration
    .scan_time_ms = 2000,        // Adjust scan duration
    .patrol_speed = 70,          // Speed 0-100
    .obstacle_avoidance = true   // Enable/disable obstacle avoidance
};

// In sensor_interface.h
#define TEMP_THRESHOLD_CELSIUS    45.0f  // Temperature alarm threshold
#define SMOKE_THRESHOLD_PPM       150    // Smoke alarm threshold
#define FLAME_DETECTION_THRESHOLD 500    // Flame sensor threshold
```

### Python Configuration

Edit `config/config.py`:

```python
# Camera settings
CAMERA_CONFIG = {
    'source': 0,      # Camera index
    'width': 640,     # Frame width
    'height': 480,    # Frame height
    'fps': 30         # Frames per second
}

# Fire detection parameters
FIRE_DETECTION_CONFIG = {
    'min_fire_area': 500,            # Minimum fire area in pixels
    'confidence_threshold': 0.6,     # Detection confidence threshold
    # HSV color ranges for fire detection
    'hsv_lower_bound1': [0, 50, 50],
    'hsv_upper_bound1': [35, 255, 255],
}
```

## Debugging

### STM32 Debugging

#### Using ST-Link Debugger

```bash
# In STM32CubeIDE
# Set breakpoints in code
# Click Debug button (F11)
# Step through code
# Watch variables
# View peripheral registers
```

#### Serial Debug Output

```c
// Add debug UART output
#include <stdio.h>

// Redirect printf to UART
int _write(int file, char *ptr, int len) {
    HAL_UART_Transmit(&huart1, (uint8_t *)ptr, len, HAL_MAX_DELAY);
    return len;
}

// Use in code
printf("Temperature: %.2f\n", temperature);
printf("Fire detected: %d\n", fire_detected);
```

### Python Debugging

#### Enable Debug Logging

```python
import logging

# Set logging level to DEBUG
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

#### Debug Fire Detection

```python
# In fire_detection.py
# Visualize detection masks
cv2.imshow('Fire Mask', fire_mask)
cv2.imshow('HSV', hsv)

# Print detection values
print(f"Fire confidence: {confidence}")
print(f"Contour area: {area}")
```

## Testing

### Unit Testing

#### STM32 Unit Tests

```c
// Create test functions
void test_motor_control() {
    motor_control_init();
    motor_set_direction(MOTOR_FORWARD, 50);
    assert(motor_get_speed() == 50);
}

void test_sensor_read() {
    SensorData_t data;
    int result = sensor_read_all(&data);
    assert(result == 0);
}
```

#### Python Unit Tests

```python
# Create tests/test_fire_detection.py
import unittest
from fire_detection import FireDetector

class TestFireDetection(unittest.TestCase):
    def setUp(self):
        self.detector = FireDetector()
    
    def test_detector_init(self):
        self.assertIsNotNone(self.detector)
    
    def test_fire_detection(self):
        # Load test image
        frame = cv2.imread('test_fire.jpg')
        fire_detected, confidence, bbox = self.detector.detect_fire(frame)
        self.assertTrue(fire_detected)
        self.assertGreater(confidence, 0.6)

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing

```bash
# Test complete system
# 1. Start firmware
# 2. Start Python application
# 3. Test patrol mode
# 4. Test fire detection with controlled fire source
# 5. Test emergency stop
# 6. Test sensor data transmission
```

### Performance Testing

```python
# Measure detection latency
import time

start = time.time()
fire_detected, confidence, bbox = detector.detect_fire(frame)
latency = time.time() - start
print(f"Detection latency: {latency*1000:.2f}ms")

# Monitor FPS
frame_count = 0
start_time = time.time()
while True:
    ret, frame = cap.read()
    detector.detect_fire(frame)
    frame_count += 1
    
    if time.time() - start_time >= 1.0:
        fps = frame_count / (time.time() - start_time)
        print(f"FPS: {fps:.2f}")
        frame_count = 0
        start_time = time.time()
```

## Common Issues and Solutions

### Build Issues

**Issue**: Compilation errors in STM32CubeIDE
```
Solution:
- Check include paths
- Verify HAL library version
- Update compiler settings
- Clean and rebuild project
```

**Issue**: Python import errors
```bash
Solution:
pip install --upgrade opencv-python numpy pyserial
# Or reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Runtime Issues

**Issue**: Camera not opening
```python
Solution:
# Try different camera indices
cap = cv2.VideoCapture(0)  # Try 0, 1, 2...
# Check permissions
sudo chmod 666 /dev/video0
```

**Issue**: Serial port access denied
```bash
Solution:
# Add user to dialout group (Linux)
sudo usermod -a -G dialout $USER
# Logout and login again

# Or change permissions temporarily
sudo chmod 666 /dev/ttyUSB0
```

**Issue**: Fire detection not working
```
Solution:
1. Check lighting conditions
2. Adjust HSV thresholds
3. Test with controlled fire source
4. Verify camera is working
5. Check confidence threshold
```

## Best Practices

### Code Organization
- Keep modular structure
- Use meaningful variable names
- Comment complex logic
- Follow coding standards (MISRA-C for embedded)

### Version Control
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial implementation"

# Create branches for features
git checkout -b feature/obstacle-avoidance
```

### Documentation
- Document all functions
- Keep README updated
- Add inline comments for complex code
- Document configuration changes

### Safety
- Always test with low-speed settings first
- Use emergency stop during development
- Test fire detection with controlled sources
- Keep fire extinguisher nearby

## Performance Optimization

### STM32 Optimization

```c
// Use compiler optimization flags
// -O2 or -O3 in project settings

// Optimize loops
for (int i = 0; i < 100; i++) {
    // Use loop unrolling for critical paths
}

// Use DMA for UART to reduce CPU load
HAL_UART_Transmit_DMA(&huart1, data, length);
```

### Python Optimization

```python
# Use NumPy operations instead of loops
# BAD:
for i in range(height):
    for j in range(width):
        result[i, j] = image[i, j] * 2

# GOOD:
result = image * 2

# Reduce frame size if needed
frame = cv2.resize(frame, (320, 240))

# Skip frames for processing
if frame_count % 3 == 0:  # Process every 3rd frame
    detect_fire(frame)
```

## Deployment

### Production Setup

1. **Optimize Configuration**
   - Tune detection thresholds
   - Set appropriate patrol parameters
   - Configure fail-safe behaviors

2. **Create Startup Scripts**
```bash
#!/bin/bash
# startup.sh
cd /home/robot/J-yan/computer_vision/src
source /home/robot/venv/bin/activate
python3 main.py --port /dev/ttyUSB0 --camera 0 --no-display
```

3. **Set Up Auto-Start**
```bash
# Create systemd service (Linux)
sudo nano /etc/systemd/system/fire-robot.service

[Unit]
Description=Fire Inspection Robot
After=network.target

[Service]
User=robot
WorkingDirectory=/home/robot/J-yan
ExecStart=/home/robot/J-yan/startup.sh
Restart=always

[Install]
WantedBy=multi-user.target

# Enable service
sudo systemctl enable fire-robot.service
sudo systemctl start fire-robot.service
```

4. **Monitor System**
```bash
# Check service status
sudo systemctl status fire-robot.service

# View logs
sudo journalctl -u fire-robot.service -f
```

## Additional Resources

- [STM32 HAL Documentation](https://www.st.com/en/development-tools/stm32cubeide.html)
- [OpenCV Python Documentation](https://docs.opencv.org/)
- [PySerial Documentation](https://pyserial.readthedocs.io/)
- [STM32 Community Forum](https://community.st.com/)
