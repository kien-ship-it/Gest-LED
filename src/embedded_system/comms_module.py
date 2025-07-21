"""
comms_module.py - Serial communication for Gest-LED
Author: Engineer D
"""

import serial
import serial.tools.list_ports


def find_esp_port():
    """Scans available serial ports and finds the ESP8266."""
    # Implementation: List ports, look for known identifiers,
    # or try sending "HELLO" to each and wait for "READY".
    # return serial port on success, -1 on fail
    com_device_list = serial.tools.list_ports.comports()
    for device in com_device_list:
        com_port = device.device
        esp_object = initialize_connection(com_port)
        if esp_object != None:
            return esp_object.port

    return -1


def initialize_connection(port, baud_rate=115200, timeout=2):
    """Establishes connection and performs handshake."""
    # Implementation: Open port, send "HELLO\n",
    # wait for "READY\n". Return serial object on success, None on fail.
    ser = None
    try:
        ser = serial.Serial(port, baud_rate, timeout=timeout, write_timeout=2)
        print(f"Port {port} opened")
        ser.write(b"HELLO\n")
        ser.flush()
        print("Sent HELLO")
        received_data = ser.readline().decode(errors="ignore").strip()
        print(f"Got: '{received_data}'")
        if received_data == "READY":
            return ser              # return serial object
        
    except serial.SerialTimeoutException:
        print(f"Write timeout on {port}")
    except Exception as e:
        print(f"Error on {port}: {e}")

    if ser and ser.is_open:
        ser.close()
    return None # fail


def send_command(serial_conn, finger_count):
    """Sends a finger count command and waits for acknowledgment."""
    # Implementation: Format command "C[count]\n", send it.
    # Read response. Return True if "OK\n" is received, False otherwise.

    message = f"C{finger_count}\n"

    try:
        serial_conn.write(message.encode())
        serial_conn.flush()
        print(f"Command Sent: {message.strip()}")
        received_data = serial_conn.readline().decode(errors="ignore").strip()
        print(f"Got: '{received_data}'")
        if received_data == "OK":
            return True

    except serial.SerialTimeoutException:
        print("Write timeout")
    except Exception as e:
        print(f"Error: {e}")
    return False


def close_connection(serial_conn):
    """Close the serial connection if open."""
    if serial_conn and serial_conn.is_open:
        serial_conn.close()

