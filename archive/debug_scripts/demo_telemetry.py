from pymavlink import mavutil
import time
import sys

# Connect
connection_string = 'tcp:127.0.0.1:5762'
print(f"Connecting to {connection_string}...", flush=True)
master = mavutil.mavlink_connection(connection_string)
master.wait_heartbeat(timeout=5)
print(f"Connected. System {master.target_system}", flush=True)

# Helper to set params
def set_param(param_id, value):
    master.mav.param_set_send(
        master.target_system, master.target_component,
        param_id.encode('utf-8'),
        value,
        mavutil.mavlink.MAV_PARAM_TYPE_REAL32
    )
    time.sleep(0.05)

# Disable Safety
set_param("ARMING_CHECK", 0)

# Arm
print("Arming...", flush=True)
master.arducopter_arm()
master.motors_armed_wait()
print(">> ARMED <<", flush=True)

# Set Mode FBWA
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    master.mode_mapping()['FBWA'])
print("Mode: FBWA", flush=True)

print("Applying MAX Power + Pitch INVERSE (1100)...", flush=True)
# Channel 1: Roll (1500)
# Channel 2: Pitch (1100) -> Trying Low for UP
# Channel 3: Throttle (2000)
master.mav.rc_channels_override_send(
    master.target_system, master.target_component,
    1500, # Roll
    1100, # Pitch LOW (Checking if this is Nose Up)
    2000, # Throttle
    0, 0, 0, 0, 0)

# Monitor Loop (10 seconds)
print("--- TELEMETRY LOG V2 ---", flush=True)
print("Time | ThrOut | Speed | Alt | Pitch | S1 | S2", flush=True)

start = time.time()
while time.time() - start < 15:
    # Request Data
    msg = master.recv_match(type=['VFR_HUD', 'ATTITUDE', 'SERVO_OUTPUT_RAW'], blocking=True, timeout=1)
    
    if msg:
        if msg.get_type() == 'VFR_HUD':
            spd = msg.groundspeed
            thr = msg.throttle
            alt = msg.alt
            print(f"HUD | Thr:{thr}% | Spd:{spd:.1f} | Alt:{alt:.2f}", flush=True)
            
        if msg.get_type() == 'ATTITUDE':
            pitch_deg = msg.pitch * 57.2958
            print(f"ATT | Pitch:{pitch_deg:.1f}", flush=True)

        if msg.get_type() == 'SERVO_OUTPUT_RAW':
            s1 = msg.servo1_raw
            s2 = msg.servo2_raw
            print(f"SRV | S1:{s1} | S2:{s2}", flush=True)

    time.sleep(0.5)

print("Test Complete", flush=True)
