from pymavlink import mavutil
import time
import sys

# Connect
connection_string = 'tcp:127.0.0.1:5762'
print(f"Connecting to {connection_string}...", flush=True)
master = mavutil.mavlink_connection(connection_string)
master.wait_heartbeat(timeout=5)
print("Connected.", flush=True)

# 1. Arm
master.mav.param_set_send(master.target_system, master.target_component, b'ARMING_CHECK', 0, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
time.sleep(0.5)
master.arducopter_arm()
master.motors_armed_wait()
print(">> ARMED <<", flush=True)

# 2. REPOSITION (Magic Move)
print("Sending REPOSITION Command (Alt 100m)...", flush=True)
# MAV_CMD_DO_REPOSITION
# Param 1: Speed (m/s) - -1 for default
# Param 4: Yaw (deg) - NaN for unchanged
# Param 5: Lat (deg * 1e7)
# Param 6: Lon (deg * 1e7)
# Param 7: Alt (m)
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_DO_REPOSITION,
    0,
    -1, # Speed
    mavutil.mavlink.MAV_DO_REPOSITION_FLAGS_CHANGE_MODE, # Flags
    0, # Radius
    0, # Yaw
    0, 0, 100) # Lat/Lon ignored if 0? Or maybe we need current pos.

# Let's try RELATIVE move if possible? No.
# Let's just try sending a SET_POSITION_TARGET_LOCAL_NED? 
# Usually REPOSITION works best for SITL.

# 3. THRUST
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    master.mode_mapping()['FBWA'])

master.mav.rc_channels_override_send(
    master.target_system, master.target_component,
    1500, 1500, 2000, 0, 0, 0, 0, 0)
    
print(">> BURST POWER <<", flush=True)
print("Monitoring Altitude...", flush=True)

for i in range(10):
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=1)
    if msg:
        alt = msg.relative_alt / 1000.0
        print(f"Alt: {alt:.1f}m", flush=True)
    time.sleep(0.5)
