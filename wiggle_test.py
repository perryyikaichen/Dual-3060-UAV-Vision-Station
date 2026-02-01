from pymavlink import mavutil
import time
import sys

connection_string = 'tcp:127.0.0.1:5762'
print(f"Connecting to {connection_string}...", flush=True)
master = mavutil.mavlink_connection(connection_string)
master.wait_heartbeat(timeout=5)
print("Connected.", flush=True)

# Arm
print("Arming...", flush=True)
master.arducopter_arm()
master.motors_armed_wait()
print(">> ARMED <<", flush=True)

master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    master.mode_mapping()['MANUAL'])
print("Mode: MANUAL (Surfaces Direct Control)", flush=True)

print("--- WIGGLE TEST (EXTENDED) ---")
print("Look at the wings!", flush=True)
time.sleep(2)

for i in range(10): # Run for longer
    print(f"[{i+1}/10] PITCH UP (Stick Back / PWM 1900)", flush=True)
    master.mav.rc_channels_override_send(
        master.target_system, master.target_component,
        1500, 1900, 1000, 0, 0, 0, 0, 0)
    time.sleep(3)

    print(f"[{i+1}/10] PITCH DOWN (Stick Fwd / PWM 1100)", flush=True)
    master.mav.rc_channels_override_send(
        master.target_system, master.target_component,
        1500, 1100, 1000, 0, 0, 0, 0, 0)
    time.sleep(3)

print("Test Complete.", flush=True)
