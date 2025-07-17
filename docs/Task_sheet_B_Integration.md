# Task Sheet for Engineer B (Nam)

**Your Team:** Team Alpha - PC/Vision Squad  
**Your Role:** Application Integration Lead  
**Your Partner:** Engineer A (Vision Module Developer)  
**Special Responsibility:** Lead final system integration with Team Bravo

## 1. Your Mission

Build the main application that ties everything together. You'll create the user interface, manage the program flow, handle configuration, and integrate all modules into a polished, user-friendly application. As Integration Lead, you'll also coordinate the final system assembly.

## 2. Your Deliverables

1. **`main_app.py`** - Main application with GUI and integration logic
2. **`config.json`** - Configuration file with default settings
3. **`test_integration.py`** - Integration tests for the complete system
4. **`README.md`** - Quick start guide for users

## 3. Required Libraries

```python
opencv-python     # Install with: pip install opencv-python
numpy            # Installed with opencv
json             # Built-in Python library
sys              # Built-in Python library
time             # Built-in Python library
threading        # Built-in Python library
os               # Built-in Python library

# From your teammates:
vision_module    # From Engineer A
comms_module     # From Engineer D (Team Bravo)
```

## 4. Detailed Specifications

### 4.1 Main Application Structure (`main_app.py`)

```python
"""
main_app.py - Main application for Gest-LED system
Author: Engineer B
Date: [Current Date]
"""

import cv2
import json
import sys
import time
import threading
from datetime import datetime

# These will be imported after receiving from teammates
import vision_module
# import comms_module  # Uncomment after integration

class GestLEDApp:
    """Main application class for Gest-LED system"""
    
    def __init__(self, config_path='config.json'):
        """Initialize application with configuration"""
        pass
    
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        pass
    
    def initialize_camera(self):
        """Initialize webcam with config settings"""
        pass
    
    def initialize_serial(self):
        """Initialize serial communication"""
        pass
    
    def create_gui_window(self):
        """Create and configure OpenCV window"""
        pass
    
    def draw_ui_elements(self, frame, finger_count, fps, status):
        """Draw UI overlay on video frame"""
        pass
    
    def process_frame(self, frame):
        """Process single frame through vision module"""
        pass
    
    def send_to_hardware(self, finger_count):
        """Send finger count to ESP8266"""
        pass
    
    def calculate_fps(self):
        """Calculate and return current FPS"""
        pass
    
    def handle_errors(self, error_type, error_msg):
        """Central error handling with user feedback"""
        pass
    
    def run(self):
        """Main application loop"""
        pass
    
    def cleanup(self):
        """Clean shutdown of all resources"""
        pass
```

### 4.2 Configuration File (`config.json`)

```json
{
    "application": {
        "name": "Gest-LED Controller",
        "version": "1.0",
        "debug_mode": false
    },
    "serial": {
        "port": "auto",
        "baud_rate": 115200,
        "timeout": 2,
        "retry_attempts": 3
    },
    "camera": {
        "index": 0,
        "width": 640,
        "height": 480,
        "fps": 30,
        "flip_horizontal": true
    },
    "vision": {
        "detection_confidence": 0.7,
        "max_hands": 1,
        "smoothing_frames": 3
    },
    "ui": {
        "window_name": "Gest-LED Controller",
        "font_scale": 1.0,
        "colors": {
            "text": [0, 255, 0],
            "error": [0, 0, 255],
            "background": [50, 50, 50]
        }
    }
}
```

### 4.3 Required Methods Implementation Details

#### Method 1: `load_config(config_path)`
```python
def load_config(self, config_path):
    """
    Load and validate configuration file.
    
    Parameters:
    - config_path: Path to config.json
    
    Returns:
    - dict: Configuration dictionary
    
    Behavior:
    - Try to load config file
    - If file not found, create default config
    - Validate required keys exist
    - Store in self.config
    """
```

#### Method 2: `initialize_camera()`
```python
def initialize_camera(self):
    """
    Initialize webcam with error handling.
    
    Behavior:
    - Try primary camera index from config
    - If fails, try indices 0-3
    - Set camera properties (resolution, FPS)
    - Store VideoCapture object in self.cap
    - Raise exception if no camera found
    """
```

#### Method 3: `initialize_serial()`
```python
def initialize_serial(self):
    """
    Initialize serial connection with auto-detection.
    
    Behavior:
    - If config port is "auto", scan for ESP8266
    - Try to connect with handshake
    - Store serial object in self.serial_conn
    - Set self.hardware_connected flag
    - Handle gracefully if no hardware found
    """
```

#### Method 4: `draw_ui_elements(frame, finger_count, fps, status)`
```python
def draw_ui_elements(self, frame, finger_count, fps, status):
    """
    Draw informative UI overlay.
    
    Elements to draw:
    - Title bar with app name
    - Large finger count display
    - FPS counter
    - Connection status (Camera ✓ Serial ✓/✗)
    - Error messages if any
    - Instructions (Press 'q' to quit, 's' for settings)
    
    Returns:
    - Annotated frame
    """
```

#### Method 5: `process_frame(frame)`
```python
def process_frame(self, frame):
    """
    Process frame and handle finger count smoothing.
    
    Behavior:
    - Call vision_module.process_frame()
    - If hand detected, get finger count
    - Apply smoothing (average of last N frames)
    - Update self.current_finger_count
    - Return processed frame and count
    """
```

#### Method 6: `send_to_hardware(finger_count)`
```python
def send_to_hardware(self, finger_count):
    """
    Send finger count to hardware with error handling.
    
    Behavior:
    - Check if hardware connected
    - Send command using comms_module
    - Handle timeout/errors
    - Update status display
    - Don't crash if hardware disconnected
    """
```

#### Method 7: `run()`
```python
def run(self):
    """
    Main application loop with proper error handling.
    
    Structure:
    while self.running:
        try:
            - Read frame from camera
            - Process frame for finger detection
            - Update UI
            - Send to hardware (if connected)
            - Handle keyboard input
            - Calculate FPS
        except Exception as e:
            - Handle errors gracefully
            - Continue running if possible
    """
```

### 4.4 Integration Test Suite (`test_integration.py`)

```python
"""
test_integration.py - Integration tests for complete system
"""

import cv2
import time
import json
from main_app import GestLEDApp

def test_config_loading():
    """Test configuration file handling"""
    print("Testing configuration loading...")
    app = GestLEDApp('config.json')
    assert app.config is not None
    assert app.config['serial']['baud_rate'] == 115200
    print("✓ Config loading test passed")

def test_camera_initialization():
    """Test camera setup and fallback"""
    print("Testing camera initialization...")
    app = GestLEDApp('config.json')
    app.initialize_camera()
    assert app.cap is not None
    assert app.cap.isOpened()
    print("✓ Camera initialization test passed")

def test_vision_integration():
    """Test integration with vision module"""
    print("Testing vision module integration...")
    app = GestLEDApp('config.json')
    app.initialize_camera()
    
    # Capture and process one frame
    ret, frame = app.cap.read()
    assert ret == True
    
    processed_frame, count = app.process_frame(frame)
    assert processed_frame is not None
    assert 0 <= count <= 5
    print("✓ Vision integration test passed")

def test_serial_mock():
    """Test serial communication (mock if no hardware)"""
    print("Testing serial communication...")
    app = GestLEDApp('config.json')
    
    try:
        app.initialize_serial()
        if app.hardware_connected:
            print("✓ Hardware detected and connected")
        else:
            print("✓ Running in standalone mode (no hardware)")
    except Exception as e:
        print(f"✗ Serial initialization failed: {e}")

def test_full_pipeline():
    """Test complete pipeline for 5 seconds"""
    print("\nTesting full pipeline for 5 seconds...")
    print("Show your hand to the camera!")
    
    app = GestLEDApp('config.json')
    app.initialize_camera()
    app.initialize_serial()
    
    start_time = time.time()
    frame_count = 0
    
    while time.time() - start_time < 5:
        ret, frame = app.cap.read()
        if not ret:
            break
            
        processed_frame, count = app.process_frame(frame)
        app.draw_ui_elements(processed_frame, count, 30, "Testing")
        
        cv2.imshow("Integration Test", processed_frame)
        frame_count += 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    app.cleanup()
    
    fps = frame_count / 5
    print(f"✓ Full pipeline test passed. Average FPS: {fps:.1f}")

if __name__ == "__main__":
    print("Running integration tests...\n")
    test_config_loading()
    test_camera_initialization()
    test_vision_integration()
    test_serial_mock()
    test_full_pipeline()
    print("\nAll integration tests completed!")
```

## 5. User Interface Design

### 5.1 Main Window Layout

```
┌─────────────────────────────────────────┐
│  Gest-LED Controller v1.0         [FPS: 30] │
├─────────────────────────────────────────┤
│                                         │
│                                         │
│         [Camera Feed with               │
│          Hand Landmarks]                │
│                                         │
│         Fingers: 3                      │
│         ████████████                    │
│                                         │
├─────────────────────────────────────────┤
│ Status: Camera ✓  Serial ✓  LED ✓       │
│ Press 'q' to quit, 's' for settings     │
└─────────────────────────────────────────┘
```

### 5.2 Error Display Examples

- No camera: "Camera not found. Please check connection."
- No serial: "Running in demo mode. Connect ESP8266 for full functionality."
- Serial timeout: "Hardware not responding. Check connection."

## 6. Integration Timeline

### Phase 1: Standalone Development (Day 1-2)
1. Create main_app.py with camera functionality
2. Integrate vision_module from Engineer A
3. Create config.json with all settings
4. Build complete UI with mock serial

### Phase 2: Team Alpha Integration (Day 3)
1. Get vision_module.py from Engineer A
2. Run integration tests together
3. Fine-tune finger detection parameters
4. Ensure smooth operation at 30+ FPS

### Phase 3: Full System Integration (Day 4)
1. Receive comms_module.py from Team Bravo
2. Add serial communication to main_app.py
3. Test with actual hardware
4. Handle all edge cases

### Your Integration Lead Responsibilities:
- Coordinate file exchange between teams
- Run final system tests
- Debug integration issues
- Ensure smooth handoff to end users

## 7. Definition of Done

Your application is complete when:

- [ ] main_app.py runs without any imports from Team Bravo
- [ ] Camera feed displays with hand landmarks
- [ ] Finger count shows correctly on screen
- [ ] UI is clean and informative
- [ ] All errors handled gracefully
- [ ] Config file allows easy customization
- [ ] FPS stays above 25 on average hardware
- [ ] Integration with comms_module takes <30 minutes
- [ ] README.md helps new users get started

## 8. Quick Start Guide Template (README.md)

```markdown
# Gest-LED Controller

Control LEDs with hand gestures using computer vision!

## Installation

1. Install Python 3.7+
2. Install requirements:
   ```
   pip install opencv-python cvzone pyserial
   ```

## Hardware Setup

1. Connect ESP8266 with 5 LEDs to USB port
2. Note the COM port (or use "auto" in config)

## Usage

1. Run the application:
   ```
   python main_app.py
   ```

2. Show your hand to the camera
3. Raise 0-5 fingers to control LEDs

## Configuration

Edit `config.json` to customize:
- Camera settings
- Serial port
- UI preferences

## Troubleshooting

- **No camera found**: Try different camera index in config
- **Serial error**: Check COM port in Device Manager
- **Low FPS**: Reduce camera resolution

## Keyboard Shortcuts

- `q`: Quit application
- `s`: Show settings (future feature)
- `r`: Reset connection
```

## 9. Code Quality Checklist

- [ ] All functions have docstrings
- [ ] Error handling doesn't show stack traces to user
- [ ] No hardcoded values (use config.json)
- [ ] Thread-safe serial communication
- [ ] Memory efficient (no leaks in main loop)
- [ ] Clean shutdown (camera and serial released)
- [ ] PEP 8 compliant code style
- [ ] Meaningful variable names

## 10. Tips for Success

1. **Start Simple**: Get camera + vision working first, add serial later
2. **Mock Serial**: Create a fake send_to_hardware() that just prints
3. **Smooth Counts**: Average last 3 frames to reduce flicker
4. **User Feedback**: Always show status, never freeze silently
5. **Test Often**: Run integration tests after each major change

Remember: You're the integration lead! Your code brings everyone's work together into a polished product. Make it robust, user-friendly, and easy to understand. Good luck!