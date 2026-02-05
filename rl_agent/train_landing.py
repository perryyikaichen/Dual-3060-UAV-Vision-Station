from stable_baselines3 import PPO
from ardupilot_env import ArduPilotEnv
import os
import time

def main():
    # Ensure logs exist
    log_dir = "/mnt/data/logs/ppo_landing"
    os.makedirs(log_dir, exist_ok=True)

    print("Initializing ArduPilot Environment...")
    # Note: Inside the container, we might need a specific IP if using docker networking.
    # For now, assuming host networking or mapped ports.
    # If simulated on host, use host.docker.internal or 172.17.0.1 if Linux support allows, 
    # but strictly --net=host is easiest for mavlink.
    env = ArduPilotEnv(connection_string='tcp:127.0.0.1:5762')

    print("Creating PPO Agent...")
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_dir)

    print("Starting Training Loop (10,000 timesteps)...")
    try:
        model.learn(total_timesteps=10000)
        model.save("ppo_landing_v1")
        print("Model Saved: ppo_landing_v1.zip")
    except Exception as e:
        print(f"Training interrupted: {e}")
        # Save emergency checkpoint
        model.save("ppo_landing_emergency")
    finally:
        env.close()

if __name__ == "__main__":
    main()
