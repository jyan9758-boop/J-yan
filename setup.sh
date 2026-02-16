#!/bin/bash

# Setup script for Fire Inspection Robot

echo "================================================"
echo "Fire Inspection Robot - Setup Script"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed"
    exit 1
fi
echo "✓ Python 3 is installed"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
cd computer_vision
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi
cd ..
echo "✓ Dependencies installed"
echo ""

# Run tests
echo "Running tests..."
python3 tests/test_fire_detection.py
if [ $? -eq 0 ]; then
    echo "✓ Tests passed"
else
    echo "⚠ Some tests failed"
fi
echo ""

# Check for camera
echo "Checking for camera..."
if [ -e /dev/video0 ]; then
    echo "✓ Camera detected at /dev/video0"
else
    echo "⚠ No camera detected at /dev/video0"
    echo "  You may need to specify a different camera index"
fi
echo ""

# Check for serial port
echo "Checking for serial ports..."
if ls /dev/ttyUSB* 1> /dev/null 2>&1; then
    echo "✓ Serial ports found:"
    ls /dev/ttyUSB*
else
    echo "⚠ No USB serial ports detected"
    echo "  Connect STM32 board via USB"
fi
echo ""

echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "To run the system:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Navigate to computer_vision/src"
echo "  3. Run: python3 main.py"
echo ""
echo "For more information, see README.md"
echo ""
