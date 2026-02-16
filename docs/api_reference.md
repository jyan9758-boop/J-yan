# API Reference

## STM32 Firmware API

### Motor Control API

#### `motor_control_init()`
Initialize motor control system.

**Returns:**
- `0` on success
- `-1` on failure

**Example:**
```c
if (motor_control_init() != 0) {
    // Handle initialization error
}
```

---

#### `motor_set_direction(direction, speed)`
Set motor direction and speed.

**Parameters:**
- `direction` (MotorDirection_t): Direction to move
  - `MOTOR_FORWARD`: Move forward
  - `MOTOR_BACKWARD`: Move backward
  - `MOTOR_LEFT`: Turn left
  - `MOTOR_RIGHT`: Turn right
  - `MOTOR_STOP`: Stop motors
- `speed` (uint8_t): Speed percentage (0-100)

**Example:**
```c
motor_set_direction(MOTOR_FORWARD, 70);  // Move forward at 70% speed
motor_set_direction(MOTOR_RIGHT, 50);    // Turn right at 50% speed
```

---

#### `motor_emergency_stop()`
Immediately stop all motors.

**Example:**
```c
if (fire_detected) {
    motor_emergency_stop();
}
```

---

#### `motor_get_speed()`
Get current motor speed.

**Returns:**
- Current speed percentage (0-100)

**Example:**
```c
uint8_t current_speed = motor_get_speed();
printf("Current speed: %d%%\n", current_speed);
```

---

### Sensor Interface API

#### `sensor_init()`
Initialize all sensors.

**Returns:**
- `0` on success
- `-1` on failure

**Example:**
```c
if (sensor_init() != 0) {
    // Handle initialization error
}
```

---

#### `sensor_read_all(data)`
Read all sensor data.

**Parameters:**
- `data` (SensorData_t*): Pointer to sensor data structure

**Returns:**
- `0` on success
- `-1` on failure

**Example:**
```c
SensorData_t sensor_data;
if (sensor_read_all(&sensor_data) == 0) {
    printf("Temperature: %.2f°C\n", sensor_data.temperature);
    printf("Smoke: %d ppm\n", sensor_data.smoke_level);
    printf("Flame: %d\n", sensor_data.flame_value);
    printf("Fire detected: %d\n", sensor_data.fire_detected);
}
```

---

#### `sensor_check_fire(data)`
Check if fire is detected based on sensor readings.

**Parameters:**
- `data` (const SensorData_t*): Pointer to sensor data

**Returns:**
- `true` if fire detected
- `false` otherwise

**Example:**
```c
SensorData_t data;
sensor_read_all(&data);
if (sensor_check_fire(&data)) {
    // Fire detected - take action
    motor_emergency_stop();
    trigger_alarm();
}
```

---

#### `sensor_read_temperature()`
Read temperature sensor.

**Returns:**
- Temperature in Celsius (float)

---

#### `sensor_read_smoke()`
Read smoke sensor.

**Returns:**
- Smoke level in PPM (uint16_t)

---

#### `sensor_read_flame()`
Read flame sensor.

**Returns:**
- Flame sensor value (uint16_t)

---

### Patrol Control API

#### `patrol_init(config)`
Initialize patrol control system.

**Parameters:**
- `config` (const PatrolConfig_t*): Patrol configuration parameters
  - Can be `NULL` to use default configuration

**Returns:**
- `0` on success
- `-1` on failure

**Example:**
```c
PatrolConfig_t config = {
    .forward_time_ms = 3000,
    .turn_time_ms = 1000,
    .scan_time_ms = 2000,
    .patrol_speed = 70,
    .obstacle_avoidance = true
};

if (patrol_init(&config) != 0) {
    // Handle error
}
```

---

#### `patrol_start()`
Start autonomous patrolling.

**Example:**
```c
patrol_start();
```

---

#### `patrol_stop()`
Stop patrolling.

**Example:**
```c
patrol_stop();
```

---

#### `patrol_update()`
Update patrol state machine. Should be called periodically (e.g., every 10ms).

**Example:**
```c
// In main loop
while (1) {
    patrol_update();
    HAL_Delay(10);
}
```

---

#### `patrol_get_state()`
Get current patrol state.

**Returns:**
- Current patrol state (PatrolState_t)
  - `PATROL_IDLE`: Not patrolling
  - `PATROL_FORWARD`: Moving forward
  - `PATROL_TURNING`: Turning
  - `PATROL_SCANNING`: Scanning area
  - `PATROL_FIRE_DETECTED`: Fire detected
  - `PATROL_EMERGENCY_STOP`: Emergency stop

**Example:**
```c
PatrolState_t state = patrol_get_state();
if (state == PATROL_FIRE_DETECTED) {
    // Handle fire detection
}
```

---

#### `patrol_handle_fire_detection()`
Handle fire detection event. Stops robot and transitions to fire detected state.

---

#### `patrol_set_config(config)`
Set patrol configuration.

**Parameters:**
- `config` (const PatrolConfig_t*): New patrol configuration

---

### Communication API

#### `comm_init(baudrate)`
Initialize UART communication.

**Parameters:**
- `baudrate` (uint32_t): UART baudrate (e.g., 115200)

**Returns:**
- `0` on success
- `-1` on failure

**Example:**
```c
if (comm_init(115200) != 0) {
    // Handle initialization error
}
```

---

#### `comm_send_packet(packet)`
Send packet to computer vision module.

**Parameters:**
- `packet` (const CommPacket_t*): Pointer to packet structure

**Returns:**
- `0` on success
- `-1` on failure

**Example:**
```c
CommPacket_t packet;
packet.header = 0xAA;
packet.command = CMD_START_PATROL;
packet.length = 0;
packet.checksum = 0;

if (comm_send_packet(&packet) != 0) {
    // Handle error
}
```

---

#### `comm_receive_packet(packet, timeout_ms)`
Receive packet from computer vision module.

**Parameters:**
- `packet` (CommPacket_t*): Pointer to packet structure to fill
- `timeout_ms` (uint32_t): Timeout in milliseconds

**Returns:**
- `0` on success
- `-1` on timeout or error

---

#### `comm_send_sensor_data(temp, smoke, flame)`
Send sensor data to CV module.

**Parameters:**
- `temp` (float): Temperature in Celsius
- `smoke` (uint16_t): Smoke level in PPM
- `flame` (uint16_t): Flame sensor value

**Returns:**
- `0` on success
- `-1` on failure

**Example:**
```c
comm_send_sensor_data(25.5, 100, 200);
```

---

#### `comm_process_command(command, data, length)`
Process received command.

**Parameters:**
- `command` (uint8_t): Command byte
- `data` (const uint8_t*): Data payload
- `length` (uint8_t): Data length

---

#### `comm_calculate_checksum(data, length)`
Calculate checksum for packet.

**Parameters:**
- `data` (const uint8_t*): Data to calculate checksum for
- `length` (uint8_t): Data length

**Returns:**
- Checksum byte (uint8_t)

---

## Python Computer Vision API

### FireDetector Class

#### `__init__()`
Initialize fire detector.

**Example:**
```python
detector = FireDetector()
```

---

#### `detect_fire(frame)`
Detect fire in a video frame.

**Parameters:**
- `frame` (np.ndarray): Input BGR image frame

**Returns:**
- Tuple of `(fire_detected, confidence, bounding_box)`
  - `fire_detected` (bool): Whether fire is detected
  - `confidence` (float): Confidence score (0.0 to 1.0)
  - `bounding_box` (tuple): `(x, y, w, h)` or `None`

**Example:**
```python
ret, frame = cap.read()
fire_detected, confidence, bbox = detector.detect_fire(frame)

if fire_detected:
    print(f"Fire detected with confidence: {confidence:.2f}")
    x, y, w, h = bbox
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
```

---

#### `detect_smoke(frame)`
Detect smoke in a video frame.

**Parameters:**
- `frame` (np.ndarray): Input BGR image frame

**Returns:**
- Tuple of `(smoke_detected, confidence)`
  - `smoke_detected` (bool): Whether smoke is detected
  - `confidence` (float): Confidence score (0.0 to 1.0)

**Example:**
```python
smoke_detected, confidence = detector.detect_smoke(frame)
if smoke_detected:
    print(f"Smoke detected: {confidence:.2f}")
```

---

#### `annotate_frame(frame, fire_detected, confidence, bbox)`
Annotate frame with detection results.

**Parameters:**
- `frame` (np.ndarray): Input BGR image frame
- `fire_detected` (bool): Whether fire was detected
- `confidence` (float): Detection confidence
- `bbox` (tuple): Bounding box `(x, y, w, h)` or `None`

**Returns:**
- Annotated frame (np.ndarray)

**Example:**
```python
annotated = detector.annotate_frame(frame, fire_detected, confidence, bbox)
cv2.imshow('Fire Detection', annotated)
```

---

### CommunicationInterface Class

#### `__init__(port, baudrate)`
Initialize communication interface.

**Parameters:**
- `port` (str): Serial port name (e.g., '/dev/ttyUSB0')
- `baudrate` (int): Communication baudrate (default: 115200)

**Example:**
```python
comm = CommunicationInterface('/dev/ttyUSB0', 115200)
```

---

#### `connect()`
Connect to STM32.

**Returns:**
- `True` if connected successfully
- `False` otherwise

**Example:**
```python
if not comm.connect():
    print("Failed to connect to STM32")
    exit(1)
```

---

#### `disconnect()`
Disconnect from STM32.

**Example:**
```python
comm.disconnect()
```

---

#### `send_cv_result(fire_detected, confidence, smoke_detected)`
Send computer vision result to STM32.

**Parameters:**
- `fire_detected` (bool): Whether fire was detected
- `confidence` (float): Detection confidence
- `smoke_detected` (bool): Whether smoke was detected

**Returns:**
- `True` if sent successfully
- `False` otherwise

**Example:**
```python
comm.send_cv_result(
    fire_detected=True,
    confidence=0.85,
    smoke_detected=False
)
```

---

#### `receive_sensor_data()`
Receive sensor data from STM32.

**Returns:**
- `SensorData` object or `None` if failed

**Example:**
```python
sensor_data = comm.receive_sensor_data()
if sensor_data:
    print(f"Temperature: {sensor_data.temperature}°C")
    print(f"Smoke: {sensor_data.smoke_level} ppm")
    print(f"Flame: {sensor_data.flame_value}")
```

---

#### `send_start_patrol()`
Send start patrol command.

**Returns:**
- `True` if sent successfully

---

#### `send_stop_patrol()`
Send stop patrol command.

**Returns:**
- `True` if sent successfully

---

#### `send_emergency_stop()`
Send emergency stop command.

**Returns:**
- `True` if sent successfully

**Example:**
```python
if fire_detected:
    comm.send_emergency_stop()
```

---

### FireInspectionRobot Class

#### `__init__(serial_port, camera_source)`
Initialize fire inspection robot.

**Parameters:**
- `serial_port` (str): Serial port for STM32 communication
- `camera_source` (int): Camera source (0 for webcam)

**Example:**
```python
robot = FireInspectionRobot('/dev/ttyUSB0', 0)
```

---

#### `start()`
Start the fire inspection robot.

**Returns:**
- `True` if started successfully
- `False` otherwise

---

#### `stop()`
Stop the fire inspection robot.

---

#### `run(display)`
Main execution loop.

**Parameters:**
- `display` (bool): Whether to display video feed (default: True)

**Example:**
```python
robot = FireInspectionRobot('/dev/ttyUSB0', 0)
robot.run(display=True)
```

---

## Data Structures

### STM32 Structures

#### `MotorDirection_t` (enum)
```c
typedef enum {
    MOTOR_FORWARD = 0,
    MOTOR_BACKWARD,
    MOTOR_LEFT,
    MOTOR_RIGHT,
    MOTOR_STOP
} MotorDirection_t;
```

#### `SensorData_t` (struct)
```c
typedef struct {
    float temperature;      /* Temperature in Celsius */
    uint16_t smoke_level;   /* Smoke level in PPM */
    uint16_t flame_value;   /* Flame sensor analog value */
    bool fire_detected;     /* Fire detection flag */
} SensorData_t;
```

#### `PatrolState_t` (enum)
```c
typedef enum {
    PATROL_IDLE = 0,
    PATROL_FORWARD,
    PATROL_TURNING,
    PATROL_SCANNING,
    PATROL_FIRE_DETECTED,
    PATROL_EMERGENCY_STOP
} PatrolState_t;
```

#### `PatrolConfig_t` (struct)
```c
typedef struct {
    uint32_t forward_time_ms;
    uint32_t turn_time_ms;
    uint32_t scan_time_ms;
    uint8_t patrol_speed;
    bool obstacle_avoidance;
} PatrolConfig_t;
```

#### `CommPacket_t` (struct)
```c
typedef struct __attribute__((packed)) {
    uint8_t header;         /* Packet header (0xAA) */
    uint8_t command;        /* Command byte */
    uint8_t length;         /* Data length */
    uint8_t data[64];       /* Data payload */
    uint8_t checksum;       /* Checksum byte */
} CommPacket_t;
```

### Python Data Classes

#### `SensorData`
```python
@dataclass
class SensorData:
    temperature: float
    smoke_level: int
    flame_value: int
```

#### `CVResult`
```python
@dataclass
class CVResult:
    fire_detected: bool
    confidence: float
    smoke_detected: bool
```

---

## Constants

### Command Codes
```c
#define CMD_START_PATROL     0x01
#define CMD_STOP_PATROL      0x02
#define CMD_FIRE_DETECTED    0x03
#define CMD_STATUS_REQUEST   0x04
#define CMD_STATUS_RESPONSE  0x05
#define CMD_EMERGENCY_STOP   0x06
#define CMD_SENSOR_DATA      0x07
#define CMD_CV_RESULT        0x08
```

### Sensor Thresholds
```c
#define TEMP_THRESHOLD_CELSIUS    45.0f
#define SMOKE_THRESHOLD_PPM       150
#define FLAME_DETECTION_THRESHOLD 500
```

### Protocol Constants
```c
#define PACKET_HEADER 0xAA
```

---

## Usage Examples

### Complete STM32 Example
```c
#include "motor_control.h"
#include "sensor_interface.h"
#include "patrol_control.h"
#include "communication.h"

int main(void) {
    // Initialize system
    HAL_Init();
    SystemClock_Config();
    
    // Initialize modules
    motor_control_init();
    sensor_init();
    
    PatrolConfig_t config = {
        .forward_time_ms = 3000,
        .turn_time_ms = 1000,
        .scan_time_ms = 2000,
        .patrol_speed = 70,
        .obstacle_avoidance = true
    };
    patrol_init(&config);
    comm_init(115200);
    
    // Start patrolling
    patrol_start();
    
    // Main loop
    while (1) {
        // Update patrol
        patrol_update();
        
        // Read sensors
        SensorData_t sensor_data;
        sensor_read_all(&sensor_data);
        
        // Send sensor data
        comm_send_sensor_data(
            sensor_data.temperature,
            sensor_data.smoke_level,
            sensor_data.flame_value
        );
        
        // Check for fire
        if (sensor_data.fire_detected) {
            patrol_handle_fire_detection();
        }
        
        HAL_Delay(10);
    }
}
```

### Complete Python Example
```python
from fire_detection import FireDetector
from communication_interface import CommunicationInterface
import cv2

# Initialize components
detector = FireDetector()
comm = CommunicationInterface('/dev/ttyUSB0', 115200)
cap = cv2.VideoCapture(0)

# Connect to STM32
if not comm.connect():
    print("Failed to connect")
    exit(1)

# Start patrol
comm.send_start_patrol()

# Main loop
try:
    while True:
        # Read frame
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect fire
        fire_detected, confidence, bbox = detector.detect_fire(frame)
        smoke_detected, smoke_conf = detector.detect_smoke(frame)
        
        # Send results to STM32
        comm.send_cv_result(fire_detected, confidence, smoke_detected)
        
        # Receive sensor data
        sensor_data = comm.receive_sensor_data()
        if sensor_data:
            print(f"Temp: {sensor_data.temperature}°C")
        
        # Display
        annotated = detector.annotate_frame(frame, fire_detected, 
                                           confidence, bbox)
        cv2.imshow('Fire Detection', annotated)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    comm.send_stop_patrol()
    comm.disconnect()
    cap.release()
    cv2.destroyAllWindows()
```
