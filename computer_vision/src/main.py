"""
main.py
Main application integrating fire detection with STM32 communication
"""

import cv2
import logging
import time
from fire_detection import FireDetector
from communication_interface import CommunicationInterface

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FireInspectionRobot:
    """Main application for autonomous fire inspection robot"""
    
    def __init__(self, serial_port: str = '/dev/ttyUSB0', 
                 camera_source: int = 0):
        """
        Initialize fire inspection robot
        
        Args:
            serial_port: Serial port for STM32 communication
            camera_source: Camera source (0 for webcam)
        """
        self.fire_detector = FireDetector()
        self.comm = CommunicationInterface(serial_port, 115200)
        self.camera_source = camera_source
        self.running = False
        
        logger.info("Fire inspection robot initialized")
    
    def start(self) -> bool:
        """
        Start the fire inspection robot
        
        Returns:
            True if started successfully
        """
        # Connect to STM32
        if not self.comm.connect():
            logger.error("Failed to connect to STM32")
            return False
        
        # Open camera
        self.cap = cv2.VideoCapture(self.camera_source)
        if not self.cap.isOpened():
            logger.error("Failed to open camera")
            self.comm.disconnect()
            return False
        
        # Send start patrol command
        if not self.comm.send_start_patrol():
            logger.warning("Failed to send start patrol command")
        
        self.running = True
        logger.info("Fire inspection robot started")
        return True
    
    def stop(self) -> None:
        """Stop the fire inspection robot"""
        self.running = False
        
        # Send stop patrol command
        if self.comm.connected:
            self.comm.send_stop_patrol()
            self.comm.disconnect()
        
        # Release camera
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        
        cv2.destroyAllWindows()
        logger.info("Fire inspection robot stopped")
    
    def run(self, display: bool = True) -> None:
        """
        Main execution loop
        
        Args:
            display: Whether to display video feed
        """
        if not self.running:
            if not self.start():
                return
        
        frame_count = 0
        last_sensor_read = time.time()
        
        try:
            while self.running:
                # Read frame
                ret, frame = self.cap.read()
                if not ret:
                    logger.warning("Failed to read frame")
                    break
                
                # Process frame for fire detection
                fire_detected, confidence, bbox = self.fire_detector.detect_fire(frame)
                smoke_detected, smoke_conf = self.fire_detector.detect_smoke(frame)
                
                # Send CV results to STM32 every 10 frames
                if frame_count % 10 == 0:
                    self.comm.send_cv_result(fire_detected, confidence, smoke_detected)
                
                # Log detection
                if fire_detected:
                    logger.warning(f"FIRE DETECTED! Confidence: {confidence:.2f}")
                    # Could trigger emergency alert here
                
                if smoke_detected:
                    logger.warning(f"SMOKE DETECTED! Confidence: {smoke_conf:.2f}")
                
                # Receive sensor data from STM32
                current_time = time.time()
                if current_time - last_sensor_read > 1.0:  # Every second
                    sensor_data = self.comm.receive_sensor_data()
                    if sensor_data:
                        logger.info(f"Sensor: Temp={sensor_data.temperature:.1f}°C, "
                                  f"Smoke={sensor_data.smoke_level}ppm, "
                                  f"Flame={sensor_data.flame_value}")
                    last_sensor_read = current_time
                
                # Display frame
                if display:
                    annotated = self.fire_detector.annotate_frame(
                        frame, fire_detected, confidence, bbox
                    )
                    
                    # Add smoke detection status
                    if smoke_detected:
                        cv2.putText(annotated, f"Smoke: {smoke_conf:.2f}", 
                                  (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                                  0.7, (0, 165, 255), 2)
                    
                    cv2.imshow('Fire Inspection Robot', annotated)
                    
                    # Exit on 'q' key, emergency stop on 's'
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                    elif key == ord('s'):
                        logger.warning("EMERGENCY STOP triggered by user")
                        self.comm.send_emergency_stop()
                        break
                
                frame_count += 1
        
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        
        finally:
            self.stop()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Autonomous Fire Inspection and Patrolling Robot'
    )
    parser.add_argument('--port', type=str, default='/dev/ttyUSB0',
                       help='Serial port for STM32 (default: /dev/ttyUSB0)')
    parser.add_argument('--camera', type=int, default=0,
                       help='Camera source (default: 0 for webcam)')
    parser.add_argument('--no-display', action='store_true',
                       help='Disable video display')
    
    args = parser.parse_args()
    
    # Create and run robot
    robot = FireInspectionRobot(serial_port=args.port, camera_source=args.camera)
    robot.run(display=not args.no_display)


if __name__ == "__main__":
    main()
