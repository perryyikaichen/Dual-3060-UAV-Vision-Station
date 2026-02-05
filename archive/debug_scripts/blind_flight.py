from pymavlink import mavutil
import time
import sys

connection_string = 'tcp:127.0.0.1:5762'

print("Connecting...", flush=True)
# Loop to connect aggressively
while True:
    try:
        master = mavutil.mavlink_connection(connection_string)
        master.mav.ping_send(int(time.time() * 1000000), 0, 0, 0)
        break
    except:
        time.sleep(0.5)

print(">> CONNECTED. SENDING COMMANDS <<", flush=True)

# Loop commands to ensure they stick
for i in range(20): # Send for 2 seconds
    # 1. Disable Checks
    master.mav.param_set_send(master.target_system, master.target_component, b'ARMING_CHECK', 0, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
    
    # 2. Arm
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        1, 0, 0, 0, 0, 0, 0)
        
    # 3. Mode FBWA
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        master.mode_mapping()['FBWA'])
        
    # 4. Throttle MAX
    master.mav.rc_channels_override_send(
        master.target_system, master.target_component,
        1500, 1500, 2000, 0, 0, 0, 0, 0)

    time.sleep(0.1)

print(">> IN FLIGHT (HOPEFULLY) <<", flush=True)

# Keep link alive and monitor
while True:
    master.mav.rc_channels_override_send(
        master.target_system, master.target_component,
        1500, 1500, 2000, 0, 0, 0, 0, 0)
    time.sleep(1)
