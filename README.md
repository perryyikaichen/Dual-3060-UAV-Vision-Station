# 🦅 Dual-3060 UAV Vision Station
**AI-Powered Autonomous Landing System**

## 📖 Project Overview
This project builds an autonomous UAV capability to land fixed-wing aircraft using computer vision (YOLO) and simulation (ArduPilot SITL). The system is designed to run on a dual-GPU workstation (2x RTX 3060), separating the "Brain" (Vision Processing) from the "World" (Simulation/Rendering).

### 🛠️ Tech Stack
*   **Simulation**: ArduPilot SITL + Gazebo Garden (Dockerized)
*   **AI**: PyTorch + Stable Baselines3 (PPO)
*   **Hardware Target**: Matek F405 WTE (Real), Dual RTX 3060 (Training)
*   **Airframe**: Custom LW-PLA Design (Ender 3 Pro)

## 🚀 Getting Started

### 1. Prerequisites
*   Ubuntu 22.04 LTS
*   Docker + NVIDIA Container Runtime
*   Python 3.10+

### 2. Run the Training Environment
We use a Docker container to run the RL Agent (PyTorch) separate from the Simulator.

```bash
# Build the training agent
docker build -t rl-agent -f docker_sitl/Dockerfile.training docker_sitl

# Run Training (Mounts local code)
docker run --rm -it --net=host \
    -v $(pwd)/rl_agent:/home/agent/rl_ws \
    -v $(pwd)/logs:/mnt/data/logs \
    rl-agent python3 train_landing.py
```

### 3. Run the Simulator (Headless or GUI)
```bash
docker run --rm -d --net=host --name ardupilot-sim ardupilot-sitl:latest
```

## 📂 Project Structure
*   `docker_sitl/`: Dockerfiles for Simulation and Training.
*   `rl_agent/`: Reinforcement Learning code (Gym Wrapper + PPO).
*   `daily_logs/`: Engineering logs.
*   `archive/`: Legacy Vision/Jetson code.

## 📝 Latest Status (Day 3 - Strategic Pivot)
*   ✅ **Pivot**: Shifted from Edge Vision to Server-Side RL.
*   ✅ **Clean Up**: Archived legacy vision code.
*   🚧 **Training**: Building PyTorch Environment...
