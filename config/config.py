"""
Configuration file for fire inspection robot
"""

# Camera configuration
CAMERA_CONFIG = {
    'source': 0,  # 0 for default webcam
    'width': 640,
    'height': 480,
    'fps': 30
}

# Fire detection parameters
FIRE_DETECTION_CONFIG = {
    'min_fire_area': 500,
    'confidence_threshold': 0.6,
    'hsv_lower_bound1': [0, 50, 50],
    'hsv_upper_bound1': [35, 255, 255],
    'hsv_lower_bound2': [35, 50, 50],
    'hsv_upper_bound2': [65, 255, 255]
}

# Communication configuration
COMM_CONFIG = {
    'port': '/dev/ttyUSB0',
    'baudrate': 115200,
    'timeout': 1.0
}

# Patrol configuration
PATROL_CONFIG = {
    'forward_time_ms': 3000,
    'turn_time_ms': 1000,
    'scan_time_ms': 2000,
    'patrol_speed': 70,  # 0-100
    'obstacle_avoidance': True
}

# Sensor thresholds
SENSOR_THRESHOLDS = {
    'temperature_celsius': 45.0,
    'smoke_ppm': 150,
    'flame_threshold': 500
}

# System configuration
SYSTEM_CONFIG = {
    'log_level': 'INFO',
    'enable_display': True,
    'frame_process_interval': 10,
    'sensor_read_interval_sec': 1.0
}
