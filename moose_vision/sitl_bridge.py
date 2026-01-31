#!/usr/bin/env python3
"""
sitl_bridge.py - Bridge between ArduPilot SITL and YOLO Vision System
"""

import sys
import time
from pymavlink import mavutil

# Connection parameters for SITL (default port for first vehicle)
CONNECTION_STRING = "udp:127.0.0.1:14550"
BAUD_RATE = 115200

def connect_to_vehicle():
    """Establishes connection to the SITL vehicle."""
    print(f"Connecting to vehicle on {CONNECTION_STRING}...")
    try:
        # Create the connection
        master = mavutil.mavlink_connection(CONNECTION_STRING, baud=BAUD_RATE)
        
        # Wait for the first heartbeat
        print("Waiting for heartbeat...")
        master.wait_heartbeat()
        
        print(f"Heartbeat received from system (system {master.target_system} component {master.target_component})")
        return master
    except Exception as e:
        print(f"Error connecting: {e}")
        return None

def main():
    vehicle = connect_to_vehicle()
    if not vehicle:
        sys.exit(1)

    print("Listening for messages...")
    try:
        while True:
            # Monitor specific messages (e.g., ATTITUDE, GPS_RAW_INT)
            msg = vehicle.recv_match(type=['ATTITUDE', 'GPS_RAW_INT', 'STATUSTEXT'], blocking=True, timeout=1.0)
            
            if msg:
                if msg.get_type() == 'STATUSTEXT':
                    print(f"[ArduPilot]: {msg.text}")
                elif msg.get_type() == 'ATTITUDE':
                    # Rate limit print for high-frequency messages
                    pass
            
            # Request regular data streams if needed
            # vehicle.mav.request_data_stream_send(...)

    except KeyboardInterrupt:
        print("\nStopping bridge...")

if __name__ == "__main__":
    main()
