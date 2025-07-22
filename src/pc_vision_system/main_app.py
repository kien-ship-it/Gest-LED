"""
main_app.py - Main application for Gest-LED system
Author: Engineer B
Date: 2023-10-27
"""

import cv2
import json
import sys
import time
import threading
import os
from datetime import datetime
from collections import deque

# --- Robust Import Support ---
# To enable robust imports from parent directories, add the project's 'src'
# directory to the system path. This allows us to import modules from 'embedded_system'.
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)
# --- End Robust Import Support ---

import vision_module

# Attempt to import the real comms module for integration,
# but allow standalone operation if it's not found.
try:
    from embedded_system import comms_module
except ImportError:
    print("WARNING: 'comms_module' from embedded_system not found. Serial communication will be mocked.")
    comms_module = None

class GestLEDApp:
    """Main application class for Gest-LED system."""
    
    def __init__(self, config_path='src/pc_vision_system/config.json'):
        """Initialize application with configuration."""
        self.config = self.load_config(config_path)
        self.running = True
        
        # Camera and vision
        self.cap = None
        self.detector = None  # This will hold the hand detector instance
        self.current_finger_count = 0
        self.last_counts = deque(maxlen=self.config['vision']['smoothing_frames'])
        
        # Serial hardware
        self.hardware_connected = False
        self.serial_conn = None # This would be the comms_module object later
        
        # UI and performance
        self.window_name = self.config['ui']['window_name']
        self.status = "Initializing..."
        self.error_message = None
        self.fps = 0
        self.frame_count = 0
        self.fps_start_time = time.time()
        
    def load_config(self, config_path):
        """Load configuration from JSON file. If not found, create a default."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: '{config_path}' not found. Creating default config.")
            default_config = {
                "application": {"name": "Gest-LED Controller", "version": "1.0", "debug_mode": False},
                "serial": {"port": "auto", "baud_rate": 115200, "timeout": 2, "retry_attempts": 3},
                "camera": {"index": 0, "width": 640, "height": 480, "fps": 30, "flip_horizontal": True},
                "vision": {"detection_confidence": 0.7, "max_hands": 1, "smoothing_frames": 3},
                "ui": {"window_name": "Gest-LED Controller", "font_scale": 1.0, "colors": {"text": [0, 255, 0], "error": [0, 0, 255], "background": [50, 50, 50]}}
            }
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config

    def initialize_camera(self):
        """Initialize webcam, trying multiple indices if the primary fails."""
        primary_index = self.config['camera']['index']
        
        # Try primary camera index first
        self.cap = cv2.VideoCapture(primary_index)
        if self.cap.isOpened():
            print(f"Camera found at index {primary_index}")
        else:
            # If primary fails, try indices 0 to 3
            print(f"Camera at index {primary_index} failed. Scanning other indices...")
            for i in range(4):
                self.cap = cv2.VideoCapture(i)
                if self.cap.isOpened():
                    print(f"Found camera at fallback index {i}")
                    self.config['camera']['index'] = i
                    break
            if not self.cap.isOpened():
                self.handle_errors("fatal", "No camera found. Please check connection.")
                return False

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config['camera']['width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config['camera']['height'])
        self.cap.set(cv2.CAP_PROP_FPS, self.config['camera']['fps'])
        return True

    def initialize_vision(self):
        """Initializes the hand detector from the vision module."""
        try:
            self.detector = vision_module.initialize_detector(
                detection_confidence=self.config['vision']['detection_confidence'],
                max_hands=self.config['vision']['max_hands']
            )
            print("Vision module initialized successfully.")
            return True
        except Exception as e:
            self.handle_errors("fatal", f"Failed to initialize vision module: {e}")
            return False

    def initialize_serial(self):
        """
        Initialize serial connection with auto-detection.
        Uses the real comms_module if available, otherwise mocks.
        """
        if comms_module:
            try:
                port = comms_module.find_esp_port()
                if port:
                    self.serial_conn = comms_module.connect_to_esp(port, self.config['serial']['baud_rate'])
                    self.hardware_connected = True
                    self.status = "Hardware Connected"
                    print(f"Successfully connected to hardware on port {port}.")
                else:
                    self.handle_errors("warning", "Hardware not found. Running in demo mode.")
            except Exception as e:
                self.handle_errors("warning", f"Serial connection failed: {e}. Running in demo mode.")
        else:
            # Mock implementation
            self.status = "Hardware not connected. Running in demo mode."
            self.hardware_connected = False
            print("INFO: Skipping hardware initialization for standalone mode.")

    def create_gui_window(self):
        """Create and configure the OpenCV window."""
        cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)

    def draw_ui_elements(self, frame, finger_count, fps, status):
        """Draw UI overlay on the video frame."""
        h, w, _ = frame.shape
        ui_color = self.config['ui']['colors']['text']
        err_color = self.config['ui']['colors']['error']

        # Status bar
        cv2.rectangle(frame, (0, h - 30), (w, h), (50, 50, 50), -1)
        cv2.putText(frame, f"Status: {status}", (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, ui_color, 1)

        # FPS counter
        cv2.putText(frame, f"FPS: {fps:.1f}", (w - 100, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, ui_color, 2)
        
        # Finger count
        cv2.putText(frame, f"Fingers: {finger_count}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, ui_color, 2)

        # Quit instructions
        cv2.putText(frame, "Press 'q' to quit", (w - 150, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, ui_color, 1)

        if self.error_message:
            cv2.putText(frame, self.error_message, (10, h // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, err_color, 2)

        return frame

    def process_frame(self, frame):
        """Process a single frame to detect hands, count fingers, and apply smoothing."""
        # Use the detector to find hands in the frame
        hands, processed_frame = vision_module.process_frame(frame, self.detector)
        
        count = 0
        if hands:
            # Process the first detected hand
            try:
                count = vision_module.count_fingers(hands[0])
            except (ValueError, IndexError) as e:
                if self.config['application']['debug_mode']:
                    print(f"Debug: Could not count fingers - {e}")
                # Keep previous count if hand is visible but fingers aren't clear
                count = self.last_counts[-1] if self.last_counts else 0

        # Apply smoothing to the count
        self.last_counts.append(count)
        if self.last_counts:
            # Use the most frequent count in the recent buffer for stability
            smoothed_count = max(set(self.last_counts), key=self.last_counts.count)
        else:
            smoothed_count = 0
            
        return processed_frame, smoothed_count

    def send_to_hardware(self, finger_count):
        """Send finger count to ESP8266 using the comms_module."""
        if self.hardware_connected and self.serial_conn:
            try:
                success = comms_module.send_command(self.serial_conn, f"C{finger_count}")
                if not success:
                    # Implement retry logic or connection reset if needed
                    self.handle_errors("warning", "Command to hardware failed.")
            except Exception as e:
                self.handle_errors("warning", f"Error sending to hardware: {e}")
                self.hardware_connected = False
        elif self.config['application']['debug_mode']:
            # Log for debugging when not connected
            print(f"Debug: Would send command 'C{finger_count}' to hardware.")

    def calculate_fps(self):
        """Calculate and return the current FPS."""
        self.frame_count += 1
        elapsed = time.time() - self.fps_start_time
        if elapsed >= 1:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.fps_start_time = time.time()
        return self.fps

    def handle_errors(self, error_type, error_msg):
        """Central error handling."""
        print(f"ERROR ({error_type}): {error_msg}")
        self.error_message = error_msg
        if error_type == "fatal":
            self.running = False

    def run(self):
        """Main application loop."""
        if not self.initialize_camera():
            return # Exit if no camera
        
        if not self.initialize_vision():
            return # Exit if vision module fails to load

        self.initialize_serial()
        self.create_gui_window()

        last_sent_count = -1

        while self.running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    self.handle_errors("fatal", "Failed to grab frame from camera.")
                    break
                
                if self.config['camera']['flip_horizontal']:
                    frame = cv2.flip(frame, 1)

                processed_frame, finger_count = self.process_frame(frame.copy())
                self.current_finger_count = finger_count
                
                # Only send data if the count has changed
                if self.current_finger_count != last_sent_count:
                    self.send_to_hardware(self.current_finger_count)
                    last_sent_count = self.current_finger_count

                # Update UI elements
                current_fps = self.calculate_fps()
                status_text = "Hardware Connected" if self.hardware_connected else "Demo Mode"
                ui_frame = self.draw_ui_elements(processed_frame, self.current_finger_count, current_fps, status_text)

                cv2.imshow(self.window_name, ui_frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("'q' pressed. Shutting down.")
                    self.running = False

            except Exception as e:
                self.handle_errors("runtime", f"An error occurred: {e}")
                time.sleep(1) # Pause to prevent rapid-fire errors

        self.cleanup()

    def cleanup(self):
        """Cleanly shut down all resources."""
        print("Cleaning up resources...")
        if self.cap:
            self.cap.release()
        if self.hardware_connected and self.serial_conn:
            comms_module.close_connection(self.serial_conn)
            print("Hardware connection closed.")
        cv2.destroyAllWindows()
        print("Shutdown complete.")

if __name__ == '__main__':
    # Ensure the script can find other modules in its directory
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    app = GestLEDApp()
    app.run()
