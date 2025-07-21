
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