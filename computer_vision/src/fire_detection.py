"""
fire_detection.py
Computer Vision module for fire detection using OpenCV
"""

import cv2
import numpy as np
from typing import Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FireDetector:
    """Fire detection using color-based and motion analysis"""
    
    def __init__(self):
        """Initialize fire detector"""
        # Fire color range in HSV
        # Lower bound - orange/red colors
        self.lower_fire_hsv1 = np.array([0, 50, 50])
        self.upper_fire_hsv1 = np.array([35, 255, 255])
        
        # Upper bound - yellow colors
        self.lower_fire_hsv2 = np.array([35, 50, 50])
        self.upper_fire_hsv2 = np.array([65, 255, 255])
        
        # Minimum contour area to be considered as fire
        self.min_fire_area = 500
        
        # Confidence threshold
        self.confidence_threshold = 0.6
        
        logger.info("Fire detector initialized")
    
    def detect_fire(self, frame: np.ndarray) -> Tuple[bool, float, Optional[Tuple]]:
        """
        Detect fire in a video frame
        
        Args:
            frame: Input BGR image frame
            
        Returns:
            Tuple of (fire_detected, confidence, bounding_box)
            - fire_detected: Boolean indicating if fire is detected
            - confidence: Confidence score (0.0 to 1.0)
            - bounding_box: (x, y, w, h) of detected fire region or None
        """
        if frame is None or frame.size == 0:
            return False, 0.0, None
        
        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create masks for fire colors
        mask1 = cv2.inRange(hsv, self.lower_fire_hsv1, self.upper_fire_hsv1)
        mask2 = cv2.inRange(hsv, self.lower_fire_hsv2, self.upper_fire_hsv2)
        
        # Combine masks
        fire_mask = cv2.bitwise_or(mask1, mask2)
        
        # Apply morphological operations to reduce noise
        kernel = np.ones((5, 5), np.uint8)
        fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_CLOSE, kernel)
        fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_OPEN, kernel)
        
        # Apply Gaussian blur to smooth the mask
        fire_mask = cv2.GaussianBlur(fire_mask, (5, 5), 0)
        
        # Find contours
        contours, _ = cv2.findContours(fire_mask, cv2.RETR_EXTERNAL, 
                                       cv2.CHAIN_APPROX_SIMPLE)
        
        fire_detected = False
        max_area = 0
        best_bbox = None
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            if area > self.min_fire_area:
                fire_detected = True
                
                if area > max_area:
                    max_area = area
                    x, y, w, h = cv2.boundingRect(contour)
                    best_bbox = (x, y, w, h)
        
        # Calculate confidence based on area and color intensity
        if fire_detected and best_bbox:
            # Extract ROI
            x, y, w, h = best_bbox
            roi = hsv[y:y+h, x:x+w]
            
            # Calculate mean saturation and value
            mean_saturation = np.mean(roi[:, :, 1])
            mean_value = np.mean(roi[:, :, 2])
            
            # Confidence calculation
            area_confidence = min(max_area / (frame.shape[0] * frame.shape[1]), 1.0)
            color_confidence = (mean_saturation / 255.0 + mean_value / 255.0) / 2.0
            
            confidence = (area_confidence * 0.6 + color_confidence * 0.4)
        else:
            confidence = 0.0
        
        # Apply threshold
        fire_detected = fire_detected and (confidence >= self.confidence_threshold)
        
        return bool(fire_detected), confidence, best_bbox
    
    def detect_smoke(self, frame: np.ndarray) -> Tuple[bool, float]:
        """
        Detect smoke in a video frame
        
        Args:
            frame: Input BGR image frame
            
        Returns:
            Tuple of (smoke_detected, confidence)
        """
        if frame is None or frame.size == 0:
            return False, 0.0
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Smoke typically appears as a grayish region
        # Use adaptive thresholding to detect smoke-like regions
        blur = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # Calculate standard deviation in local regions
        mean, std = cv2.meanStdDev(blur)
        
        # Smoke has low texture (low std deviation) and medium brightness
        smoke_confidence = 0.0
        if 50 < mean[0][0] < 200 and std[0][0] < 30:
            smoke_confidence = 1.0 - (std[0][0] / 30.0)
        
        smoke_detected = smoke_confidence > 0.5
        
        return bool(smoke_detected), float(smoke_confidence)
    
    def annotate_frame(self, frame: np.ndarray, fire_detected: bool, 
                       confidence: float, bbox: Optional[Tuple]) -> np.ndarray:
        """
        Annotate frame with detection results
        
        Args:
            frame: Input BGR image frame
            fire_detected: Whether fire was detected
            confidence: Detection confidence
            bbox: Bounding box of detected fire
            
        Returns:
            Annotated frame
        """
        annotated = frame.copy()
        
        if fire_detected and bbox:
            x, y, w, h = bbox
            
            # Draw bounding box
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 0, 255), 2)
            
            # Add label
            label = f"FIRE: {confidence:.2f}"
            cv2.putText(annotated, label, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Add status text
        status = "FIRE DETECTED!" if fire_detected else "No Fire"
        color = (0, 0, 255) if fire_detected else (0, 255, 0)
        cv2.putText(annotated, status, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        return annotated


def process_video_stream(source: int = 0, display: bool = True) -> None:
    """
    Process video stream for fire detection
    
    Args:
        source: Video source (0 for webcam, or video file path)
        display: Whether to display the video feed
    """
    detector = FireDetector()
    cap = cv2.VideoCapture(source)
    
    if not cap.isOpened():
        logger.error(f"Failed to open video source: {source}")
        return
    
    logger.info("Starting fire detection...")
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                logger.warning("Failed to read frame")
                break
            
            # Detect fire
            fire_detected, confidence, bbox = detector.detect_fire(frame)
            
            # Detect smoke
            smoke_detected, smoke_conf = detector.detect_smoke(frame)
            
            if fire_detected:
                logger.warning(f"FIRE DETECTED! Confidence: {confidence:.2f}")
            
            if smoke_detected:
                logger.warning(f"SMOKE DETECTED! Confidence: {smoke_conf:.2f}")
            
            # Annotate frame
            if display:
                annotated = detector.annotate_frame(frame, fire_detected, 
                                                    confidence, bbox)
                cv2.imshow('Fire Detection', annotated)
                
                # Exit on 'q' key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    
    finally:
        cap.release()
        if display:
            cv2.destroyAllWindows()
        logger.info("Fire detection stopped")


if __name__ == "__main__":
    # Process webcam feed
    process_video_stream(source=0, display=True)
