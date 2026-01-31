# Custom AI Vision UAV (LW-PLA 3D Printed)

## System Specifications
*   **Target Payload**: Jetson Nano (for AI Vision)
*   **Airframe Material**: LW-PLA (Polymaker)
*   **Printer**: Ender 3 Pro
*   **Compute (Ground Station)**: Dual NVIDIA RTX 3060 (24GB VRAM Total), 32GB RAM
*   **Storage**: 2TB SSD (Mounted at `/mnt/data`)

## Environment
*   **Docker**: Installed and verified
*   **NVIDIA Runtime**: Active (GPU acceleration enabled for containers)
*   **Workspace**: `/mnt/data/projects/moose_vision` (Need to rename to `custom_uav_vision` eventually)

## Status
*   [x] Hardware Verified
*   [x] Storage Mounted
*   [x] Workspace Structure Created
*   [ ] Airframe Design (CAD/Slicing)
*   [ ] Training Data Pipeline
*   [ ] YOLO Model Training
*   [ ] ArduPilot SITL Integration
