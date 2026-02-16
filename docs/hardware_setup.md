# Hardware Setup Guide

## Components List

### STM32 Microcontroller System

#### Main Controller
- **STM32F407VGT6** or similar (recommended)
  - 168 MHz ARM Cortex-M4
  - 1MB Flash, 192KB RAM
  - Multiple GPIO, UART, ADC interfaces

#### Motor System
- **L298N Motor Driver Module**
  - Dual H-Bridge motor driver
  - 5V-35V voltage range
  - Up to 2A per channel
- **2x DC Motors** (6V or 12V)
  - Geared DC motors recommended for torque
  - Encoder optional for precise control

#### Sensors

1. **Temperature Sensor**
   - **LM35** or **DHT22**
   - Range: -55°C to 150°C (LM35)
   - Accuracy: ±0.5°C

2. **Smoke Sensor**
   - **MQ-2 Gas Sensor**
   - Detects LPG, Propane, Methane, Alcohol, Smoke
   - Operating voltage: 5V
   - Heating voltage: 5V

3. **Flame Sensor**
   - **IR Flame Detector**
   - Detection range: 760nm-1100nm
   - Detection angle: ~60 degrees
   - Operating voltage: 3.3V-5V

#### Power Supply
- **7.4V LiPo Battery** (2S) or **12V Battery Pack**
- **5V Voltage Regulator** (LM7805 or DC-DC converter)
- **3.3V Voltage Regulator** for STM32

#### Additional Components
- **USB-to-UART Module** (CP2102 or FT232)
- PCB or Breadboard
- Jumper wires
- Robot chassis

### Computer Vision System

#### Computing Platform (Choose One)
1. **Laptop/Desktop Computer**
   - Intel i5 or better
   - 8GB+ RAM
   - USB ports for camera and UART

2. **Raspberry Pi 4**
   - 4GB or 8GB RAM model
   - USB camera compatible
   - GPIO UART available

#### Camera
- **USB Webcam** (720p or higher)
- **Raspberry Pi Camera Module V2** (if using RPi)
- Minimum 30 FPS for smooth detection

## Wiring Diagram

### STM32 Connections

#### Motor Driver (L298N)
```
STM32          L298N
------         -----
PA0  -------> IN1 (Left Motor Forward)
PA1  -------> IN2 (Left Motor Backward)
PA2  -------> IN3 (Right Motor Forward)
PA3  -------> IN4 (Right Motor Backward)
TIM2_CH1 ---> ENA (Left Motor Speed - PWM)
TIM2_CH2 ---> ENB (Right Motor Speed - PWM)

L298N OUT1, OUT2 -> Left Motor
L298N OUT3, OUT4 -> Right Motor
```

#### Sensors
```
STM32          Sensors
------         -------
PA4 (ADC)  --> LM35 Output
PA5 (ADC)  --> MQ-2 Analog Output
PA6 (ADC)  --> Flame Sensor Analog Output

3.3V -------> Sensor VCC (or 5V depending on sensor)
GND  -------> Sensor GND
```

#### UART Communication
```
STM32          USB-UART
------         ---------
PA9 (TX)  ---> RX
PA10 (RX) ---> TX
GND --------> GND
```

### Power Distribution
```
Battery (+) --> L298N 12V Input
             --> 5V Regulator Input
             
5V Regulator --> MQ-2 VCC
              --> Flame Sensor VCC
              --> 3.3V Regulator Input
              
3.3V Regulator --> STM32 VDD
                --> LM35 VCC (optional, can use 5V)
                
GND (Common Ground for all components)
```

## Assembly Instructions

### Step 1: Prepare Robot Chassis
1. Mount DC motors to chassis
2. Attach wheels to motor shafts
3. Install battery holder
4. Create mounting plate for electronics

### Step 2: Install Motor Driver
1. Mount L298N to chassis
2. Connect motors to output terminals
3. Connect power supply to motor driver input

### Step 3: Install STM32 Board
1. Mount STM32 development board to chassis
2. Ensure it's accessible for programming
3. Connect to motor driver control pins

### Step 4: Install Sensors
1. **Temperature Sensor**: Mount in ventilated area
2. **Smoke Sensor**: Mount at elevated position (heat rises)
3. **Flame Sensor**: Mount facing forward, clear view
4. Wire all sensors to STM32 ADC pins

### Step 5: Connect UART Module
1. Mount USB-UART adapter
2. Connect TX/RX to STM32
3. USB cable will connect to computer

### Step 6: Power Connections
1. Connect battery to distribution system
2. Install voltage regulators
3. Double-check all voltage levels
4. **Test power before connecting STM32**

### Step 7: Cable Management
1. Use zip ties for cable organization
2. Ensure no cables interfere with wheels
3. Label all connections
4. Use heat shrink tubing for protection

## Testing Procedure

### 1. Power System Test
```
□ Verify 5V rail voltage
□ Verify 3.3V rail voltage
□ Check for shorts
□ Test battery voltage under load
```

### 2. Motor Test
```
□ Test each motor individually
□ Verify direction control
□ Test PWM speed control
□ Check for smooth operation
```

### 3. Sensor Test
```
□ Read temperature sensor values
□ Test smoke sensor response (safe test environment)
□ Test flame sensor with lighter (from safe distance)
□ Verify ADC readings are stable
```

### 4. Communication Test
```
□ Connect USB-UART to computer
□ Verify serial port detection
□ Test bidirectional communication
□ Check packet integrity
```

## Safety Precautions

### Electrical Safety
- Always disconnect power before making changes
- Use appropriate wire gauge for current
- Add fuse protection to battery
- Insulate all connections properly

### Testing Safety
- Test in open, clear area
- Keep fire extinguisher nearby when testing fire detection
- Use controlled fire sources (candles, lighters)
- Never leave robot unattended during testing

### Sensor Calibration
- Smoke sensor requires 24-48 hour burn-in period
- Temperature sensor needs thermal equilibrium
- Flame sensor should be tested at various distances

## Troubleshooting

### Motor Issues
- **Motors don't move**: Check power supply, driver connections
- **Motors run in wrong direction**: Swap motor wire polarity
- **Motors are weak**: Check PWM settings, battery voltage

### Sensor Issues
- **No sensor readings**: Verify ADC configuration, check wiring
- **Erratic readings**: Add filtering capacitors, check ground connections
- **Sensor won't detect**: Verify sensor power, check orientation

### Communication Issues
- **No serial connection**: Check TX/RX swap, verify baudrate
- **Corrupted data**: Add ground connection, check cable length
- **Timeouts**: Verify both devices configured for same baudrate

## Maintenance

### Regular Checks
- Battery charge level
- Motor condition and lubrication
- Sensor cleanliness
- Wire connection integrity
- Firmware updates

### Calibration Schedule
- Temperature sensor: Monthly
- Smoke sensor: Weekly during heavy use
- Flame sensor: Before each operation
- Motor speeds: As needed

## Upgrades and Modifications

### Optional Additions
- **Ultrasonic sensors** for obstacle detection
- **GPS module** for outdoor navigation
- **Buzzer/LED indicators** for alerts
- **Battery monitoring** circuit
- **IMU sensor** for orientation tracking
- **WiFi/Bluetooth** for wireless control

### Performance Improvements
- Higher capacity battery
- More powerful motors
- Additional sensors for redundancy
- Better camera resolution
- Cooling fans for electronics
