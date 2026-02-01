# 🦅 Dual-3060 UAV Vision Station
**AI-Powered Autonomous Landing System**

## 📖 Project Overview
This project builds an autonomous UAV capability to land fixed-wing aircraft using computer vision (YOLO) and simulation (ArduPilot SITL). The system is designed to run on a dual-GPU workstation (2x RTX 3060), separating the "Brain" (Vision Processing) from the "World" (Simulation/Rendering).

### 🛠️ Tech Stack
*   **Simulation**: ArduPilot SITL + Gazebo Garden (Dockerized)
*   **Vision**: YOLOv8 (Ultralytics)
*   **Control**: MAVLink (pymavlink Bridge)
*   **Hardware Target**: Jetson Nano (Airborne), Dual RTX 3060 (Ground Station)
*   **Airframe**: Custom LW-PLA Design (Ender 3 Pro)

## 🚀 Getting Started

### 1. Prerequisites
*   Ubuntu 22.04 LTS
*   Docker + NVIDIA Container Runtime
*   Python 3.10+

### 2. Run the 3D Simulation
We use a Docker container to run ArduPilot and Gazebo in a unified graphic environment.

```bash
# Build the simulator
docker build -t ardupilot-sitl:latest ./docker_sitl

# Run the simulation (detached)
# The container will auto-launch Gazebo and ArduPlane
docker run --rm -d \
    --name ardupilot-sim \
    --net=host \
    --env DISPLAY=$DISPLAY \
    --volume /tmp/.X11-unix:/tmp/.X11-unix \
    --volume $(pwd):/home/ardupilot/project \
    ardupilot-sitl:latest
```

### 3. Flight Automation
We have developed scripts to bypass simulation quirks (ground friction) and automate testing.

```bash
# "The Gravity Glider" (Air Spawn + Blind Launch)
# 1. Spawns plane at 150m
# 2. Ignites throttle immediately
docker cp blind_flight.py ardupilot-sim:/home/ardupilot/
docker exec ardupilot-sim python3 /home/ardupilot/blind_flight.py
```

### 4. Connect Visualizer
Launch QGroundControl on the host machine to monitor telemetry.
```bash
bash run_qgc.sh
```

## 📂 Project Structure
*   `docker_sitl/`: Dockerfile and scripts for the ArduPilot environment.
*   `moose_vision/`: Python code for YOLO and MAVLink control.
*   `daily_logs/`: Engineering logs tracking the development journey.
*   `*_flight.py`: Various test scripts for automated maneuvers.

## 📝 Latest Status (Day 2)
*   ✅ **Simulation**: Active (ArduPlane + Gazebo Garden).
*   ✅ **Protocol**: Fixed `JSON` backend for Gazebo communication.
*   ✅ **Automation**: "Blind Launch" scripts operational.
*   🚧 **Vision**: Camera sensor verification pending.
