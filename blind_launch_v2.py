from pymavlink import mavutil
import time
import sys
import subprocess

connection_string = 'tcp:127.0.0.1:5762'
master = mavutil.mavlink_connection(connection_string)
print("Sending Blind Commands V2...", flush=True)

# 1. Disable Failsafes
master.mav.param_set_send(master.target_system, master.target_component, b'ARMING_CHECK', 0, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
time.sleep(0.05)
master.mav.param_set_send(master.target_system, master.target_component, b'BATT_MONITOR', 0, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
time.sleep(0.05)

# 2. Arm
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0)
print(">> ARM SENT <<", flush=True)

# 3. Mode FBWA
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    master.mode_mapping()['FBWA'])

# 4. Throttle MAX
master.mav.rc_channels_override_send(
    master.target_system, master.target_component,
    1500, 1500, 2000, 0, 0, 0, 0, 0)
print(">> THRUST MAX SENT <<", flush=True)

# 5. CATAPULT LOOP (Manual Duration)
# Remove 'duration' field, use loop instead
svc = "/world/zephyr_runway/model/zephyr_with_ardupilot/link/base_link/apply_link_wrench"
msg = 'entity: {name: "zephyr_with_ardupilot", type: MODEL}, wrench: {force: {x: 0, y: 0, z: 2000}}'

print(">> FIRING CATAPULT (10x Impulse) <<", flush=True)
for i in range(10):
    subprocess.run([
        "gz", "service", "-s", svc,
        "--reqtype", "gz.msgs.EntityWrench",
        "--reptype", "gz.msgs.Boolean",
        "--timeout", "100",
        "--req", msg
    ])
    # time.sleep(0.05) # Delay not needed if service call is sync-ish

print(">> LAUNCH COMPLETE <<", flush=True)
