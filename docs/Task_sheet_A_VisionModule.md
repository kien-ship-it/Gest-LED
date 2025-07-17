# Task Sheet for Engineer A (Đăng)

**Your Team:** Team Alpha - PC/Vision Squad  
**Your Role:** Vision Module Developer  
**Your Partner:** Engineer B (Application Integration Lead)

## 1. Your Mission

Create the core vision processing engine that can analyze video frames, detect hands, and accurately count raised fingers. Your module will be the "brain" that interprets what the camera sees.

## 2. Your Deliverables

1. **`vision_module.py`** - Core vision processing module
2. **`test_vision.py`** - Unit tests for your module
3. **Sample test images** (optional but recommended)

## 3. Required Libraries

```python
opencv-python  # Install with: pip install opencv-python
cvzone         # Install with: pip install cvzone
mediapipe      # Installed automatically with cvzone
numpy          # Installed automatically with opencv
```

## 4. Detailed Function Specifications

### 4.1 Main Functions in `vision_module.py`

#### Function 1: `initialize_detector(detection_confidence=0.7, max_hands=1)`
```python
def initialize_detector(detection_confidence=0.7, max_hands=1):
    """
    Initialize and return a HandDetector object.
    
    Parameters:
    - detection_confidence (float): Minimum confidence for hand detection (0.0-1.0)
    - max_hands (int): Maximum number of hands to detect
    
    Returns:
    - HandDetector object from cvzone.HandTrackingModule
    
    Example:
        detector = initialize_detector(0.7, 1)
    """
```

#### Function 2: `process_frame(frame, detector)`
```python
def process_frame(frame, detector):
    """
    Process a single frame to detect hands and draw landmarks.
    
    Parameters:
    - frame: numpy array (OpenCV image/frame from webcam)
    - detector: Initialized HandDetector object
    
    Returns:
    - tuple: (hands_list, annotated_image)
        - hands_list: List of hand dictionaries (empty list if no hands)
        - annotated_image: Frame with hand landmarks drawn
    
    Example:
        hands, img = process_frame(frame, detector)
    """
```

#### Function 3: `count_fingers(hand_data)`
```python
def count_fingers(hand_data):
    """
    Count the number of raised fingers for a single hand.
    
    Parameters:
    - hand_data: Dictionary containing hand information from detector
                 Must contain 'lmList' (landmarks) and 'type' (Left/Right)
    
    Returns:
    - int: Number of raised fingers (0-5)
    
    Raises:
    - ValueError: If hand_data is None or missing required keys
    
    Example:
        if hands:
            count = count_fingers(hands[0])
    """
```

#### Function 4: `get_finger_status(hand_data)`
```python
def get_finger_status(hand_data):
    """
    Get the status of each finger (raised or lowered).
    
    Parameters:
    - hand_data: Dictionary containing hand information
    
    Returns:
    - dict: Status of each finger
        {
            'thumb': bool,
            'index': bool,
            'middle': bool,
            'ring': bool,
            'pinky': bool
        }
    
    Example:
        status = get_finger_status(hands[0])
        if status['index'] and status['middle']:
            print("Peace sign detected!")
    """
```

#### Function 5: `validate_hand_data(hand_data)`
```python
def validate_hand_data(hand_data):
    """
    Validate that hand_data contains all required information.
    
    Parameters:
    - hand_data: Dictionary to validate
    
    Returns:
    - bool: True if valid, False otherwise
    
    Example:
        if validate_hand_data(hand_data):
            count = count_fingers(hand_data)
    """
```

### 4.2 Error Handling Requirements

Your functions should handle these cases gracefully:
- Empty or None frame input
- No hands detected (return empty list)
- Invalid hand data structure
- Multiple hands (process first hand only)

### 4.3 Performance Requirements

- Process frame should complete in <50ms on average
- No memory leaks (proper cleanup of OpenCV resources)
- Thread-safe functions (no global state modification)

## 5. Implementation Guide

### 5.1 Basic Module Structure

```python
"""
vision_module.py - Hand detection and finger counting module
Author: Engineer A
Date: [Current Date]
"""

from cvzone.HandTrackingModule import HandDetector
import cv2

# Constants
THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12
RING_TIP = 16
PINKY_TIP = 20

def initialize_detector(detection_confidence=0.7, max_hands=1):
    # Your implementation here
    pass

def process_frame(frame, detector):
    # Your implementation here
    pass

def count_fingers(hand_data):
    # Your implementation here
    pass

def get_finger_status(hand_data):
    # Your implementation here
    pass

def validate_hand_data(hand_data):
    # Your implementation here
    pass
```

### 5.2 Testing Requirements

Create `test_vision.py` with these test cases:

```python
"""
test_vision.py - Unit tests for vision module
"""

import cv2
import vision_module

def test_detector_initialization():
    """Test that detector initializes correctly"""
    detector = vision_module.initialize_detector()
    assert detector is not None
    print("✓ Detector initialization test passed")

def test_with_sample_image():
    """Test with a sample image file"""
    # Load a test image
    img = cv2.imread('test_hand.jpg')  # You can create this
    detector = vision_module.initialize_detector()
    
    hands, annotated = vision_module.process_frame(img, detector)
    assert annotated is not None
    print("✓ Sample image processing test passed")

def test_finger_counting():
    """Test finger counting with mock data"""
    # Create mock hand data
    mock_hand = {
        'lmList': [[0, 100, 200]] * 21,  # Simplified landmarks
        'type': 'Right',
        'bbox': [100, 100, 200, 200]
    }
    
    count = vision_module.count_fingers(mock_hand)
    assert 0 <= count <= 5
    print("✓ Finger counting test passed")

def test_webcam_integration():
    """Test with live webcam (interactive test)"""
    cap = cv2.VideoCapture(0)
    detector = vision_module.initialize_detector()
    
    print("Show your hand to the camera. Press 'q' to quit.")
    test_passed = False
    
    while True:
        success, frame = cap.read()
        if not success:
            break
            
        hands, img = vision_module.process_frame(frame, detector)
        
        if hands:
            count = vision_module.count_fingers(hands[0])
            cv2.putText(img, f"Fingers: {count}", (10, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            test_passed = True
        
        cv2.imshow("Test Vision Module", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if test_passed:
        print("✓ Webcam integration test passed")
    else:
        print("✗ No hand detected during test")

if __name__ == "__main__":
    print("Running vision module tests...\n")
    test_detector_initialization()
    test_finger_counting()
    test_webcam_integration()
    print("\nAll tests completed!")
```

## 6. Definition of Done

Your module is complete when:

- [ ] All 5 functions are implemented in `vision_module.py`
- [ ] Each function has proper error handling
- [ ] All functions have docstrings with examples
- [ ] `test_vision.py` runs without errors
- [ ] Webcam test shows correct finger count for 0-5 fingers
- [ ] Code follows PEP 8 style guidelines
- [ ] No hardcoded values (use constants)
- [ ] Module can be imported without side effects

## 7. Integration Notes for Engineer B

When Engineer B integrates your module, they will use it like this:

```python
import vision_module

# In their initialization
detector = vision_module.initialize_detector()

# In their main loop
hands, annotated_frame = vision_module.process_frame(frame, detector)
if hands:
    finger_count = vision_module.count_fingers(hands[0])
    # Send finger_count to serial communication
```

## 8. Tips and Best Practices

1. **Hand Detection Tips:**
   - cvzone's HandDetector already handles most complexity
   - The detector returns a list of hands, each as a dictionary
   - Each hand dict contains 'lmList' (21 landmarks), 'bbox', 'type', etc.

2. **Finger Counting Logic:**
   - Thumb: Compare x-coordinates (different from other fingers)
   - Other fingers: Compare y-coordinates of tip vs pip joint
   - Account for both left and right hands

3. **Performance Tips:**
   - Don't create new detector objects repeatedly
   - Avoid unnecessary image copies
   - Use detector's built-in drawing functions

4. **Debugging Tips:**
   - Print the structure of hand_data to understand it
   - Visualize landmark points on the image
   - Test with different hand orientations

## 9. Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| No hands detected | Check lighting, try different backgrounds |
| Wrong finger count | Verify landmark indices, check hand orientation |
| Slow performance | Reduce image size, check confidence threshold |
| Import errors | Ensure all packages installed correctly |

## 10. Resources

- cvzone documentation: https://github.com/cvzone/cvzone
- MediaPipe hands: https://google.github.io/mediapipe/solutions/hands
- OpenCV Python tutorials: https://docs.opencv.org/master/d6/d00/tutorial_py_root.html

Remember: Your module is the foundation of the entire system. Take time to test thoroughly, especially edge cases like partially visible hands or unusual hand positions. Good luck!
