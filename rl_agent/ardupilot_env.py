import gymnasium as gym
from gymnasium import spaces
import numpy as np
from pymavlink import mavutil
import time
import math

class ArduPilotEnv(gym.Env):
    """
    Custom Environment that follows gym interface.
    Connects to ArduPilot SITL via MAVLink.
    Target: Train a plane to land in crosswind.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self, connection_string='tcp:127.0.0.1:5762'):
        super(ArduPilotEnv, self).__init__()

        # Define Action Space:
        # 0: Aileron (-1 to 1)
        # 1: Elevator (-1 to 1)
        # 2: Throttle (0 to 1)
        self.action_space = spaces.Box(low=np.array([-1, -1, 0]), 
                                       high=np.array([1, 1, 1]), 
                                       dtype=np.float32)

        # Define Observation Space:
        # [Roll, Pitch, Yaw, Airspeed, Alt_Rel, Climb_Rate]
        # Normalized appropriately for cleaner training
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(6,), dtype=np.float32)

        self.conn_str = connection_string
        self.master = None
        self._connect()

    def _connect(self):
        print(f"Connecting to SITL at {self.conn_str}...")
        try:
            self.master = mavutil.mavlink_connection(self.conn_str)
            self.master.wait_heartbeat()
            print("Connected to ArduPilot!")
        except Exception as e:
            print(f"Connection failed: {e}")

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # Reset the Simulation (Position)
        # Note: We can use the 'reposition' command or reload the sim.
        # For SITL, sending a MAV_CMD_DO_REPOSITION is fastest.
        # Reset to 150m Alt, Random heading?
        # TODO: Implement robust reset logic. For now, assume externally reset or crude reposition.
        
        self._send_command(mavutil.mavlink.MAV_CMD_DO_REPOSITION, 0, -1, 0, 0, 0, 0, 150)
        
        # Stabilize briefly
        time.sleep(1)
        
        return self._get_obs(), {}

    def step(self, action):
        # 1. Apply Action
        # Map -1..1 to PWM 1000..2000
        aileron = int(np.interp(action[0], [-1, 1], [1100, 1900]))
        elevator = int(np.interp(action[1], [-1, 1], [1100, 1900]))
        throttle = int(np.interp(action[2], [0, 1], [1000, 2000]))
        
        # Send RC Override
        self.master.mav.rc_channels_override_send(
            self.master.target_system, self.master.target_component,
            aileron, elevator, throttle, 0, 0, 0, 0, 0)

        # 2. Step Time
        # Ideally we wait for the next tick, or sleep a fixed dt
        time.sleep(0.1) # 10Hz control loop

        # 3. Get Observation
        obs = self._get_obs()

        # 4. Calculate Reward
        reward = self._calculate_reward(obs)

        # 5. Check Done
        terminated = False
        truncated = False
        
        alt = obs[4]
        if alt <= 1.0: # Ground contact
            terminated = True
            if abs(obs[5]) < 1.0 and abs(obs[0]) < 0.1: # Soft landing (low sink, level roll)
                reward += 100
            else:
                reward -= 100 # Crash

        return obs, reward, terminated, truncated, {}

    def _get_obs(self):
        # Fetch latest data
        msg = self.master.recv_match(type='VFR_HUD', blocking=True, timeout=1)
        att = self.master.recv_match(type='ATTITUDE', blocking=True, timeout=1)
        
        if not msg or not att:
            return np.zeros(6, dtype=np.float32)

        roll = att.roll
        pitch = att.pitch
        yaw = att.yaw
        airspeed = msg.airspeed
        alt = msg.alt
        climb = msg.climb
        
        return np.array([roll, pitch, yaw, airspeed, alt, climb], dtype=np.float32)

    def _calculate_reward(self, obs):
        # Minimize sink rate (climb) when close to ground?
        # Minimize roll (keep wings level)
        # Minimize heading deviation (crosswind correction) - TODO: Need target heading
        
        roll_penalty = -abs(obs[0])
        return roll_penalty

    def _send_command(self, command, p1, p2, p3, p4, p5, p6, p7):
        self.master.mav.command_long_send(
            self.master.target_system, self.master.target_component,
            command, 0,
            p1, p2, p3, p4, p5, p6, p7)

    def close(self):
        if self.master:
            self.master.close()
