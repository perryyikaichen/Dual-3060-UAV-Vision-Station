# Daily Engineering Log: 2026-01-31 🚁
## *Theme: The Protocol Mismatch & The Blind Agent's Struggle*
*(Bilingual / ZH-EN Style for NotebookLM)*

### 1. The Goal (Initial mission)
**Target**: Deploy the 3D Simulator (ArduPilot + Gazebo) and launch the "Zephyr" flying wing.
**Context**: We need a physics playground to train our Moose Vision AI safely before crashing real hardware.
**Pivot**: The day quickly turned into a battle against "Invisible Walls" (Protocol Errors) and "Invisible Windows" (GUI Failures).

### 2. The "Magic" Commands (What we actually did)
We spent the day wrestling with Docker and Network Ports. Here are the key moves:

*   **The Breakthrough Fix**:
    `sim_vehicle.py ... --model JSON`
    *   *Why?* The new `ardupilot_gazebo` plugin speaks a modern binary dialect. The default ArduPilot SITL speaks "Legacy Float". They were shouting at each other in different languages until we forced the translation mode (**JSON**). This fixed the `Incorrect protocol magic` error that stalled us yesterday.

*   **The "Side Door" Hack**:
    `mavutil.mavlink_connection('tcp:127.0.0.1:5762')`
    *   *Why?* Port 5760 was clogged by QGroundControl. We wrote scripts (`demo_flight.py`) to sneak commands into the Autopilot via the secondary TCP port (5762), allowing us to script flight maneuvers autonomously.

*   **The "Time Travel" Teleport**:
    `gz service -s .../set_pose ... z: 150.0`
    *   *Why?* The plane kept sticking to the runway (friction physics). We decided to cheat physics by teleporting the plane 150 meters into the sky to force an "Air Spawn".

### 3. Technical Logic (Why it got messy)
**The Problem**: **Feedback Loops**.
I (the Agent) am blind to the GUI. I can send commands (`gz sim`), but I cannot *see* if the window actually opened or if it froze.
*   We tried to automate this by reading logs (`grep "pose"`), but logs are often delayed or misleading.
*   We got stuck in a loop of "Restarting Window" -> "Permission Denied" -> "User sees nothing" because I wasn't aggressively checking the *PID status* of the graphical processes.

### 4. Project State (Health Check)
*   **Simulator**: **Functional (Backend)**. ArduPilot and Gazebo are talking. The physics engine works.
*   **Visuals**: **Unstable**. The GUI process is prone to freezing and requires manual intervention to restart reliably.
*   **Automation**: **Weak**. Our "Blind Flight" scripts rely on timing rather than sensor confirmation.

### 5. Future Strategy (Overcoming the Obstacle)
**User Feedback**: "We need better self-diagnosis."
**The Fix for Tomorrow**:
Instead of assuming a command worked, we will build **Observation Tools** verified by the system:
1.  **Screenshot Verification**: I will use a tool to take a screenshot of the X11 window to *prove* the window is open before asking you to look.
2.  **Telemetry Handshakes**: Scripts will not just "Send" commands; they will poll for `ARMED` status and `ALTITUDE > 10m` before declaring success.
3.  **Process Watchdogs**: I will write a wrapper to monitor the `gz sim` PID and auto-kill it if it hangs, rather than waiting for you to report it.

### 6. NotebookLM Hook (The Story)
"Imagine trying to fly a plane by mail. You send a letter saying 'Pull Up!', but you don't know if the pilot got it until you hear the crash. That was us today. We built a sophisticated translator so the Plane (ArduPilot) could talk to the World (Gazebo), and they finally shook hands! But then we spent hours trying to find a working TV screen to watch the flight. We learned that an AI Agent needs 'eyes'—not just code—to be a true pilot. Next time? We build the eyes."

"试想一下，如果你只能通过寄信来开飞机，那会是什么样？你寄出一封信写着‘拉升！’，但直到听到坠毁的声音，你才知道飞行员有没有收到信。这就是我们今天的情况。我们建立了一个复杂的翻译器，让飞机（ArduPilot）和世界（Gazebo）终于能对话了！但我们却花了几个小时找一个能用的电视屏幕来通过看这一场飞行。我们学到了一课：AI 代理需要的不仅仅是代码，它需要‘眼睛’才能成为真正的飞行员。下一次？我们要给它装上眼睛。"
