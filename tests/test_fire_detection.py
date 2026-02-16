"""
Test suite for fire detection module
"""

import unittest
import numpy as np
import cv2
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'computer_vision', 'src'))

from fire_detection import FireDetector


class TestFireDetector(unittest.TestCase):
    """Test cases for FireDetector class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = FireDetector()
    
    def test_detector_initialization(self):
        """Test detector initializes correctly"""
        self.assertIsNotNone(self.detector)
        self.assertEqual(self.detector.min_fire_area, 500)
        self.assertEqual(self.detector.confidence_threshold, 0.6)
    
    def test_detect_fire_with_black_frame(self):
        """Test fire detection on black frame (no fire)"""
        # Create black frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        fire_detected, confidence, bbox = self.detector.detect_fire(frame)
        
        self.assertFalse(fire_detected)
        self.assertEqual(confidence, 0.0)
        self.assertIsNone(bbox)
    
    def test_detect_fire_with_white_frame(self):
        """Test fire detection on white frame (no fire)"""
        # Create white frame
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
        
        fire_detected, confidence, bbox = self.detector.detect_fire(frame)
        
        self.assertFalse(fire_detected)
    
    def test_detect_fire_with_red_region(self):
        """Test fire detection with red region (potential fire)"""
        # Create frame with red region
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Add large red region (fire-like color)
        frame[100:300, 200:400] = [0, 0, 255]  # BGR red
        
        fire_detected, confidence, bbox = self.detector.detect_fire(frame)
        
        # Red alone might not trigger (depends on HSV conversion)
        # This tests the function runs without error
        self.assertIsInstance(fire_detected, bool)
        self.assertIsInstance(confidence, float)
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
    
    def test_detect_fire_with_orange_region(self):
        """Test fire detection with orange region (fire color)"""
        # Create frame with orange region
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Add large orange region (typical fire color)
        frame[100:300, 200:400] = [0, 165, 255]  # BGR orange
        
        fire_detected, confidence, bbox = self.detector.detect_fire(frame)
        
        # This should have higher confidence than pure red
        self.assertIsInstance(fire_detected, bool)
        self.assertIsInstance(confidence, float)
    
    def test_detect_smoke_with_black_frame(self):
        """Test smoke detection on black frame"""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        smoke_detected, confidence = self.detector.detect_smoke(frame)
        
        self.assertIsInstance(smoke_detected, bool)
        self.assertIsInstance(confidence, float)
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
    
    def test_detect_smoke_with_gray_frame(self):
        """Test smoke detection on gray frame (smoke-like)"""
        # Create gray frame (smoke-like appearance)
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128
        
        smoke_detected, confidence = self.detector.detect_smoke(frame)
        
        self.assertIsInstance(smoke_detected, bool)
        self.assertIsInstance(confidence, float)
    
    def test_annotate_frame_no_fire(self):
        """Test frame annotation with no fire"""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        annotated = self.detector.annotate_frame(frame, False, 0.0, None)
        
        self.assertIsNotNone(annotated)
        self.assertEqual(annotated.shape, frame.shape)
    
    def test_annotate_frame_with_fire(self):
        """Test frame annotation with fire detection"""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        bbox = (100, 100, 200, 200)
        
        annotated = self.detector.annotate_frame(frame, True, 0.85, bbox)
        
        self.assertIsNotNone(annotated)
        self.assertEqual(annotated.shape, frame.shape)
        # Check that annotation modified the frame
        self.assertFalse(np.array_equal(annotated, frame))
    
    def test_detect_fire_with_none_frame(self):
        """Test fire detection handles None frame gracefully"""
        fire_detected, confidence, bbox = self.detector.detect_fire(None)
        
        self.assertFalse(fire_detected)
        self.assertEqual(confidence, 0.0)
        self.assertIsNone(bbox)
    
    def test_detect_fire_with_empty_frame(self):
        """Test fire detection handles empty frame gracefully"""
        frame = np.array([])
        
        fire_detected, confidence, bbox = self.detector.detect_fire(frame)
        
        self.assertFalse(fire_detected)
        self.assertEqual(confidence, 0.0)
        self.assertIsNone(bbox)


class TestFireDetectorConfiguration(unittest.TestCase):
    """Test configuration of FireDetector"""
    
    def test_threshold_configuration(self):
        """Test that thresholds can be configured"""
        detector = FireDetector()
        
        # Test default values
        self.assertEqual(detector.min_fire_area, 500)
        self.assertEqual(detector.confidence_threshold, 0.6)
        
        # Modify configuration
        detector.min_fire_area = 1000
        detector.confidence_threshold = 0.8
        
        self.assertEqual(detector.min_fire_area, 1000)
        self.assertEqual(detector.confidence_threshold, 0.8)
    
    def test_hsv_bounds_configuration(self):
        """Test HSV color bounds are properly set"""
        detector = FireDetector()
        
        # Check bounds are NumPy arrays
        self.assertIsInstance(detector.lower_fire_hsv1, np.ndarray)
        self.assertIsInstance(detector.upper_fire_hsv1, np.ndarray)
        self.assertIsInstance(detector.lower_fire_hsv2, np.ndarray)
        self.assertIsInstance(detector.upper_fire_hsv2, np.ndarray)
        
        # Check bounds have correct shape
        self.assertEqual(detector.lower_fire_hsv1.shape, (3,))
        self.assertEqual(detector.upper_fire_hsv1.shape, (3,))


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestFireDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestFireDetectorConfiguration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
