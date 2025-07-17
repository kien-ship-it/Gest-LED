# Task Sheet for Engineer D (Vinh)

**Your Team:** Team Bravo - Embedded/Hardware Squad
**Your Role:** Firmware Developer
**Your Partner:** Engineer C (Hardware Engineer)

## 1. Your Mission

You are responsible for writing the software that runs on the ESP8266 microcontroller and the Python module that allows the PC to talk to it. Your code is the critical bridge between the vision system and the physical hardware. You will implement the communication protocol, control the LEDs, and provide a simple, reliable Python interface for Team Alpha.

## 2. Your Deliverables

1.  **`ESP_Firmware.ino`** - The primary Arduino sketch for the ESP8266.
2.  **`comms_module.py`** - The Python module for PC-side serial communication. This is a key deliverable for Team Alpha.
3.  **`test_comms.py`** - A Python script to test and validate your firmware and communication module together.

## 3. Required Software & Libraries

*   **Arduino IDE:** With ESP8266 board support installed.
*   **Python 3.x:** For developing the communication module.
*   **pyserial:** Python library for serial communication. Install with: `pip install pyserial`

## 4. Detailed Specifications

### 4.1 Integration with Hardware (from Engineer C)

You will receive the following file from Engineer C. Your firmware **MUST** use it without modification.

*   **`config.h`**: This file defines the hardware layout, including the baud rate and the specific GPIO pins for each of the 5 LEDs.
    ```c
    // Example content of config.h
    #define BAUD_RATE 115200
    #define LED_COUNT 5
    const int LED_PINS[LED_COUNT] = {5, 4, 14, 12, 13}; // D1, D2, D5, D6, D7
    ```

### 4.2 Firmware Logic (`ESP_Firmware.ino`)

Your firmware must strictly follow the communication protocol defined in the project plan.

**`setup()` function:**
1.  Initialize all LED pins defined in `LED_PINS` as `OUTPUT`.
2.  Turn all LEDs off.
3.  Start serial communication at the `BAUD_RATE` from `config.h`.
4.  Wait for the "HELLO\n" command from the PC.
5.  Upon receiving "HELLO\n", respond with "READY\n".

**`loop()` function:**
1.  Continuously check if there is data available on the serial port.
2.  Read incoming data until a newline character (`\n`) is received.
3.  Parse the received command string.
4.  **If the command is valid** (e.g., "C3\n"):
    *   Extract the number (3 in this case).
    *   Call a helper function to update the LEDs (light up 3 LEDs).
    *   Send the confirmation response "OK\n".
5.  **If the command is invalid** (e.g., "C9\n", "hello\n"):
    *   Send the error response "ERROR\n".
6.  The firmware should be non-blocking; do not use long `delay()` calls in the main loop.

**Helper Function `update_leds(int count)`:**
*   This function takes an integer from 0 to 5.
*   It should iterate from `i = 0` to `LED_COUNT - 1`.
*   If `i` is less than `count`, turn `LED_PINS[i]` ON.
*   Otherwise, turn `LED_PINS[i]` OFF.

### 4.3 Python Communication Module (`comms_module.py`)

This module will be used by Engineer B to integrate with the main PC application.

**`comms_module.py` Structure:**

```python
"""
comms_module.py - Serial communication for Gest-LED
Author: Engineer D
"""
import serial
import serial.tools.list_ports
import time

def find_esp_port():
    """Scans available serial ports and finds the ESP8266."""
    # Implementation: List ports, look for known identifiers,
    # or try sending "HELLO" to each and wait for "READY".
    pass

def initialize_connection(port, baud_rate=115200, timeout=2):
    """Establishes connection and performs handshake."""
    # Implementation: Open port, send "HELLO\n",
    # wait for "READY\n". Return serial object on success, None on fail.
    pass

def send_command(serial_conn, finger_count):
    """Sends a finger count command and waits for acknowledgment."""
    # Implementation: Format command "C[count]\n", send it.
    # Read response. Return True if "OK\n" is received, False otherwise.
    pass

def close_connection(serial_conn):
    """Closes the serial connection."""
    if serial_conn and serial_conn.is_open:
        serial_conn.close()
```

### 4.4 Test Script (`test_comms.py`)

This script is crucial for verifying your work before handoff.

**Functionality:**
1.  Use `comms_module.find_esp_port()` to locate the device.
2.  Use `comms_module.initialize_connection()` to connect and handshake.
3.  If connection is successful:
    *   Loop from `i = 0` to `5`.
    *   Call `comms_module.send_command(conn, i)`.
    *   Print a message asking the user to verify that `i` LEDs are lit.
    *   Wait for 2 seconds.
    *   After the loop, send an invalid command like `C9` and verify it fails correctly.
4.  Use `comms_module.close_connection()` to shut down cleanly.
5.  Print success or failure messages for each step.

## 5. Development Timeline

### Phase 1: Firmware Development (Day 1-2)
1.  Receive `config.h` from Engineer C.
2.  Develop `ESP_Firmware.ino` based on the specifications.
3.  Test the firmware using the Arduino IDE's Serial Monitor. Manually type commands like `HELLO` and `C3` to verify the responses (`READY`, `OK`) and LED behavior.

### Phase 2: Python Module Development (Day 2)
1.  Create `comms_module.py` with all required functions.
2.  Start by hardcoding the serial port before implementing the `find_esp_port()` function.

### Phase 3: Sub-Team Integration & Testing (Day 3)
1.  Work with Engineer C to test the complete embedded system.
2.  Create `test_comms.py` to automate the testing process.
3.  Run `test_comms.py` and confirm that the hardware (from Engineer C), firmware (from you), and comms module (from you) all work together perfectly.
4.  Refine the `find_esp_port()` function for robustness.

### Phase 4: Handoff (Day 4)
1.  Provide the final, tested `comms_module.py` to Team Alpha (Engineer B).
2.  Be available to assist Engineer B with any integration questions related to serial communication.

## 6. Definition of Done

Your task is complete when:
*   [ ] `ESP_Firmware.ino` is uploaded to the ESP8266 and running.
*   [ ] The firmware correctly controls 0-5 LEDs based on serial commands `C0` through `C5`.
*   [ ] The firmware correctly handles the `HELLO`/`READY` handshake and `ERROR` responses.
*   [ ] `comms_module.py` is fully implemented with robust error handling (e.g., timeouts, connection failures).
*   [ ] `test_comms.py` runs from start to finish without errors, and the physical LEDs match the commands sent.
*   [ ] `comms_module.py` has been delivered to Engineer B.

## 7. Code Quality Checklist

*   [ ] All functions in both Arduino and Python have comments explaining their purpose.
*   [ ] No hardcoded pin numbers in the firmware; all values are from `config.h`.
*   [ ] Python code is PEP 8 compliant.
*   [ ] The serial connection is always closed properly, even if errors occur.
*   [ ] Your code handles the case where the ESP8266 is suddenly disconnected.

## 8. Troubleshooting Tips

| Issue | Solution |
|---|---|
| **Garbled text in Serial Monitor** | Ensure the baud rate is set to 115200 in both the code and the monitor. |
| **Python script can't find port** | Check Device Manager (Windows) or `ls /dev/tty.*` (Mac/Linux) to see the correct port name. Ensure drivers for the ESP8266's USB-to-serial chip (CP2102 or CH340) are installed. |
| **Handshake fails (no "READY")** | Check that the ESP has fully booted. Add a small delay in your Python script after opening the port and before sending "HELLO". Verify the ESP is waiting for "HELLO\n" (with the newline).|
| **Commands time out** | Ensure the ESP's main loop is not blocked. The `loop()` function must run quickly and frequently to check for serial data. |

Remember, your modules are the glue holding the software and hardware together. A robust and well-documented communication system is key to the project's success. Good luck