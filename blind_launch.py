from pymavlink import mavutil
import time
import sys
import subprocess

connection_string = 'tcp:127.0.0.1:5762'
master = mavutil.mavlink_connection(connection_string)
# master.wait_heartbeat(timeout=2) # Skip heartbeat wait
print("Sending Blind Commands...", flush=True)

# 1. Arm Force
master.mav.param_set_send(master.target_system, master.target_component, b'ARMING_CHECK', 0, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
time.sleep(0.1)
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0)
print(">> ARM SENT <<", flush=True)

# 2. Mode FBWA
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    master.mode_mapping()['FBWA'])
print(">> MODE FBWA SENT <<", flush=True)

# 3. Throttle MAX
master.mav.rc_channels_override_send(
    master.target_system, master.target_component,
    1500, 1500, 2000, 0, 0, 0, 0, 0)
print(">> THROT MAX SENT <<", flush=True)

# 4. Catapult Wrench
svc = "/world/zephyr_runway/model/zephyr_with_ardupilot/link/base_link/apply_link_wrench"
gz_cmd = [
    "gz", "service", "-s", svc,
    "--reqtype", "gz.msgs.EntityWrench",
    "--reptype", "gz.msgs.Boolean",
    "--timeout", "500",
    "--req", 'entity: {name: "zephyr_with_ardupilot", type: MODEL}, wrench: {force: {x: 0, y: 0, z: 2000}}, duration: {sec: 0, nsec: 500000000}'
]
# 2000 Newtons UP (Z)
subprocess.run(gz_cmd)
print(">> CATAPULT SENT <<", flush=True)
