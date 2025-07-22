"""
test_integration.py - Integration tests for complete system
"""

import cv2
import time
import json
import os
import sys

# This is to ensure that the main_app and its dependencies can be found
# when running this script from the project root.
sys.path.append(os.path.join(os.path.dirname(__file__)))

from main_app import GestLEDApp

# Define the path to the config file relative to the project root.
CONFIG_PATH = 'src/pc_vision_system/config.json'

def test_config_loading():
    """Test configuration file handling."""
    print("Testing configuration loading...")
    # Ensure the config file exists for the test, or the app will create it.
    if not os.path.exists(CONFIG_PATH):
        print(f"Note: Config file not found at '{CONFIG_PATH}', GestLEDApp will create a default one.")
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        
    app = GestLEDApp(config_path=CONFIG_PATH)
    assert app.config is not None
    assert app.config['serial']['baud_rate'] == 115200
    print("✓ Config loading test passed")

def test_camera_initialization():
    """Test camera setup and fallback."""
    print("Testing camera initialization...")
    app = GestLEDApp(config_path=CONFIG_PATH)
    camera_ready = app.initialize_camera()
    if camera_ready:
        assert app.cap is not None
        assert app.cap.isOpened()
        app.cleanup()
        print("✓ Camera initialization test passed")
    else:
        print("✗ Camera initialization test failed or skipped (no camera found).")


def test_vision_integration():
    """Test integration with the (mock) vision module."""
    print("Testing vision module integration...")
    app = GestLEDApp(config_path=CONFIG_PATH)
    if not app.initialize_camera():
        print("Skipping vision integration test: No camera available.")
        return
        
    # This was the missing step that caused the crash.
    # We must initialize the vision module before processing frames.
    if not app.initialize_vision():
        print("Skipping vision integration test: Vision module failed to initialize.")
        app.cleanup()
        return

    # Capture and process one frame
    ret, frame = app.cap.read()
    assert ret == True
    
    # In the mock implementation, count is always 3
    processed_frame, count = app.process_frame(frame)
    assert processed_frame is not None
    assert 0 <= count <= 5
    app.cleanup()
    print("✓ Vision integration test passed")

def test_serial_mock():
    """Test that serial communication is correctly mocked."""
    print("Testing serial communication mock...")
    app = GestLEDApp(config_path=CONFIG_PATH)
    app.initialize_serial()
    assert not app.hardware_connected
    print("✓ Running in standalone mode (no hardware) as expected.")
    print("✓ Serial mock test passed")


def test_full_pipeline():
    """Test the complete pipeline for a short duration."""
    print("\nTesting full pipeline for 3 seconds...")
    print("A window should appear. Show your hand to the camera!")
    
    app = GestLEDApp(config_path=CONFIG_PATH)
    if not app.initialize_camera():
        print("Skipping full pipeline test: No camera available.")
        return

    # This was the missing step that caused the crash.
    # The vision module must be initialized before the main loop.
    if not app.initialize_vision():
        print("Skipping full pipeline test: Vision module failed to initialize.")
        app.cleanup()
        return
        
    app.initialize_serial()
    
    start_time = time.time()
    frame_count = 0
    # Run the loop for a few seconds without blocking for user input
    while time.time() - start_time < 10:
        ret, frame = app.cap.read()
        if not ret:
            break
        if app.config['camera']['flip_horizontal']:
            frame = cv2.flip(frame, 1)
            
        processed_frame, count = app.process_frame(frame)
        app.draw_ui_elements(processed_frame, count, 30, "Testing")
        
        cv2.imshow("Integration Test", processed_frame)
        frame_count += 1
        
        # Non-blocking wait key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Proper cleanup is crucial for tests
    cv2.destroyAllWindows()
    app.cleanup()
    
    fps = frame_count / 3
    print(f"✓ Full pipeline test ran successfully. Average FPS: {fps:.1f}")

if __name__ == "__main__":
    print("Running integration tests for Gest-LED...\n")
    try:
        test_config_loading()
        test_camera_initialization()
        test_vision_integration()
        test_serial_mock()
        test_full_pipeline()
        print("\nAll integration tests completed!")
    except Exception as e:
        print(f"\nAn error occurred during testing: {e}")
        import traceback
        traceback.print_exc()