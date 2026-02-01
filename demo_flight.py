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
master.mav.param_set_send(master.target_system, master.target_component, b'ARMING_CHECK', 0, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
time.sleep(0.5)
master.arducopter_arm()
master.motors_armed_wait()
print(">> ARMED <<", flush=True)

# 2. Mode FBWA
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    master.mode_mapping()['FBWA'])

# 3. Throttle Max
master.mav.rc_channels_override_send(
    master.target_system, master.target_component,
    1500, 1500, 2000, 0, 0, 0, 0, 0)
time.sleep(2)

print("✨ ATTEMPTING MAGIC LIFT...", flush=True)

# Try multiple potential service names (Garden convention vs Classic)
possible_services = [
    "/world/zephyr_runway/set_pose",
    "/world/default/set_pose", # Sometimes world name defaults
    "/set_pose"
]

target_entity = "zephyr_with_ardupilot"

success = False
for svc in possible_services:
    print(f"Trying service: {svc}...", flush=True)
    gz_cmd = [
        "gz", "service", "-s", svc,
        "--reqtype", "gz.msgs.Pose",
        "--reptype", "gz.msgs.Boolean",
        "--timeout", "1000",
        "--req", f'name: "{target_entity}", position: {{x: 0, y: 0, z: 20}}, orientation: {{x: 0, y: 0, z: 0, w: 1}}'
    ]
    
    # Run and check output
    result = subprocess.run(gz_cmd, capture_output=True, text=True)
    if "data: true" in result.stdout:
        print(f"SUCCESS on {svc}!", flush=True)
        success = True
        break
    else:
        print(f"Failed on {svc}: {result.stderr or result.stdout}", flush=True)

if not success:
    print("ALL LIFT ATTEMPTS FAILED.", flush=True)
else:
    print(">> AIRBORNE <<", flush=True)
    
print("Switching to CIRCLE logic...", flush=True)
