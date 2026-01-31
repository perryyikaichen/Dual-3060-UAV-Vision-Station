# 🦅 Dual-3060 UAV Vision Station
**AI-Powered Autonomous Landing System**

## 📖 Project Overview
This project builds an autonomous UAV capability to land fixed-wing aircraft using computer vision (YOLO) and simulation (ArduPilot SITL). The system is designed to run on a dual-GPU workstation (2x RTX 3060), separating the "Brain" (Vision Processing) from the "World" (Simulation/Rendering).

### 🛠️ Tech Stack
*   **Simulation**: ArduPilot SITL + Gazebo (Dockerized)
*   **Vision**: YOLOv8 (Ultralytics)
*   **Control**: MAVLink (Python Bridge)
*   **Hardware Target**: Jetson Nano (Airborne), Dual RTX 3060 (Ground Station)
*   **Airframe**: Custom LW-PLA Design (Ender 3 Pro)

## 🚀 Getting Started

### 1. Prerequisites
*   Ubuntu 22.04 LTS
*   Docker + NVIDIA Container Runtime
*   Python 3.10+

### 2. Run the Simulation
We use a Docker container to run the physics engine without polluting the host OS.
```bash
# Build the simulator
docker build -t ardupilot-sitl:latest ./docker_sitl

# Run the simulation (detached)
docker run -rm -d --name ardupilot-sim -p 14550:14550 -p 14551:14551 ardupilot-sitl:latest
```

### 3. Connect the Vision Bridge
Start the Python bridge to talk to the flight controller.
```bash
python3 moose_vision/sitl_bridge.py
```

### 4. Visualizer
Launch QGroundControl (via the wrapper script to fix library dependencies):
```bash
bash run_qgc.sh
```

## 📂 Project Structure
*   `docker_sitl/`: Dockerfile and scripts for the ArduPilot environment.
*   `moose_vision/`: Python code for YOLO and MAVLink control.
*   `daily_logs/`: Engineering logs tracking the development journey.
*   `assets/`: Screenshots and media.

## 📝 Latest Status (Day 1)
*   ✅ **Simulation**: Active (Dockerized ArduPlane).
*   ✅ **Bridge**: Connected (Heartbeat confirmed).
*   🚧 **Vision**: Setting up Gazebo for 3D camera data.
