from pymavlink import mavutil
import time
import sys

# Connect
connection_string = 'tcp:127.0.0.1:5762'
print(f"Connecting to {connection_string}...", flush=True)

# Loop until connected (Sim might be restarting)
while True:
    try:
        master = mavutil.mavlink_connection(connection_string)
        master.wait_heartbeat(timeout=2)
        print("Connected.", flush=True)
        break
    except:
        print("Waiting for Sim...", flush=True)
        time.sleep(1)

print("!!! CATCHING PLANE !!!", flush=True)

# 1. Arm Force
master.mav.param_set_send(master.target_system, master.target_component, b'ARMING_CHECK', 0, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
master.arducopter_arm()
master.motors_armed_wait()
print(">> ARMED <<", flush=True)

# 2. Mode FBWA
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    master.mode_mapping()['FBWA'])

# 3. THRUST MAX
master.mav.rc_channels_override_send(
    master.target_system, master.target_component,
    1500, 1500, 2000, 0, 0, 0, 0, 0)
    
print(">> THROTTLE SET TO 100% <<", flush=True)
print("Plane should be recovering from 50m drop.", flush=True)

while True:
    time.sleep(1)
