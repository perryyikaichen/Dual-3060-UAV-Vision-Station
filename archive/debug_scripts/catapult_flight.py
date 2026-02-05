from pymavlink import mavutil
import time
import sys
import subprocess

connection_string = 'tcp:127.0.0.1:5762'
print(f"Connecting to {connection_string}...", flush=True)
master = mavutil.mavlink_connection(connection_string)
master.wait_heartbeat(timeout=5)
print("Connected.", flush=True)

# 1. Arm
print("Arming...", flush=True)
master.mav.param_set_send(master.target_system, master.target_component, b'ARMING_CHECK', 0, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
master.arducopter_arm()
master.motors_armed_wait()
print(">> ARMED <<", flush=True)

# 2. Mode FBWA (Stabilize)
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    master.mode_mapping()['FBWA'])

# 3. Throttle MAX
master.mav.rc_channels_override_send(
    master.target_system, master.target_component,
    1500, 1500, 2000, 0, 0, 0, 0, 0)
print(">> THRUST SET TO MAX <<", flush=True)

time.sleep(1)

# 4. THE CATAPULT (Gazebo Wrench)
# Applying force to the 'base_link' of 'zephyr_with_ardupilot'
# World path: /world/zephyr_runway/model/zephyr_with_ardupilot/link/base_link/apply_link_wrench
# Force: 100 Newtons Forward (Body Frame?) No, Wrench is usually world frame or link frame.
# Let's try applying 500N in Z-axis (Up) and 200N in X-axis (Forward).

svc = "/world/zephyr_runway/model/zephyr_with_ardupilot/link/base_link/apply_link_wrench"
print(f"Applying CATAPULT FORCE {svc}...", flush=True)

# Force Duration: 1 second
gz_cmd = [
    "gz", "service", "-s", svc,
    "--reqtype", "gz.msgs.EntityWrench",
    "--reptype", "gz.msgs.Boolean",
    "--timeout", "2000",
    "--req", 'entity: {name: "zephyr_with_ardupilot", type: MODEL}, wrench: {force: {x: 0, y: 0, z: 1000}}, duration: {sec: 0, nsec: 500000000}'
]
# Note: Z=1000 is UP in World Frame (Garden is ENU usually). 
# If plane is vertical, we want to shoot it UP (World Z).

try:
    result = subprocess.run(gz_cmd, capture_output=True, text=True)
    if "data: true" in result.stdout:
        print(">> CATAPULT FIRED (1000N UP) <<", flush=True)
    else:
        print(f"Catapult Misfire: {result.stderr or result.stdout}", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)

print("Monitoring Flight...", flush=True)
for i in range(10):
    val = master.recv_match(type='VFR_HUD', blocking=True).groundspeed
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    alt = msg.relative_alt / 1000.0 if msg else 0
    print(f"Spd: {val:.1f} m/s | Alt: {alt:.1f}m", flush=True)
    time.sleep(0.5)

print("Switching to CIRCLE...", flush=True)
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    master.mode_mapping()['CIRCLE'])
