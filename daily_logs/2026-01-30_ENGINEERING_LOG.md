# 🚁 Engineering Log: Day 1 (The Foundation)
**Date**: 2026-01-30
**Topic**: Building the "Matrix" for our Drone

## 🎯 The Goal
We needed to create a safe, crash-proof environment to train our AI Pilot. We couldn't risk crashing physical hardware (or messing up the main computer's operating system), so we had to build a purely digital world where the drone's "Brain" (Python/YOLO) could talk to its "Body" (ArduPilot) without even knowing it was in a simulation.

## 🧠 Technical Logic
*   **Docker (The Container)**: We wrapped the ArduPilot simulation (SITL) in a Docker container. This acts like a "Virtual Machine" but lighter. It prevents the simulation's messy dependencies from conflicting with our AI tools.
*   **MAVLink (The Language)**: We used the MAVLink protocol to create a bridge (`sitl_bridge.py`). This allows our modern Python AI code to send commands to the flight controller, which speaks a much older embedded language.
*   **Library Hacking (The Fix)**: The visualizer (QGroundControl) refused to launch because of missing system libraries (`libSDL2`, `libxcb`). Instead of installing them system-wide (risky), we "stole" them from the Docker container and tricked the app into using them via `LD_LIBRARY_PATH`.

## 🪄 The 'Magic' Commands
1.  **`docker build -t ardupilot-sitl .`**
    *   *What it did*: Cooked the "Takeout Box". It downloaded Ubuntu, ArduPilot, and all the compilers, then baked them into a single file we can run anywhere.
2.  **`export LD_LIBRARY_PATH=.../QGC_Extracted/usr/lib...`**
    *   *What it did*: The "Jedi Mind Trick". It told the QGroundControl app: "Don't look at the system libraries; look in *this specific folder* instead." This fixed the crash.
3.  **`python3 sitl_bridge.py`**
    *   *What it did*: The "Handshake". It opened a UDP port and successfully heard the heartbeat of the virtual plane.

## 🩺 Project State
**Status**: 🟢 **Healthy but Blind**
*   **Physics**: ✅ Working (The plane flies in the math world).
*   **Control**: ✅ Working (We can send commands).
*   **Vision**: ❌ Blind (We have a 2D map, but no 3D camera feed yet).
*   **Next Step**: Install Gazebo (The 3D Engine) to give the AI "eyes".

## 🎙️ NotebookLM Hook (Storytime)
(Imagine a Podcast Host voice / 想像一下 Podcast 主持人的聲音)

"So, imagine you want to teach a robot to land a plane. You *could* just throw it off a cliff and hope it learns before it hits the ground... but that gets expensive fast. (這太燒錢了吧！)

Instead, Perry decided to build 'The Matrix' (`Docker Container`). We constructed a digital reality where the laws of physics exist (ArduPilot), but the consequences don't. Yesterday was all about building this digital cage.

The funniest part? The visualization tool (`QGroundControl`) threw a tantrum and refused to open. It was like buying a 4K TV but losing the remote. Perry's AI Assistant had to literally perform surgery on the startup script—injecting 'stolen' libraries from the simulation itself—to force it to work. Talk about a hack! (這真的是硬核破解！)

Now the brain is alive, the heart is beating, but... it has no eyes. It's flying blind. That's what we fix today."
