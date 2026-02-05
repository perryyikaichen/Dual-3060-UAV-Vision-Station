# 🛠️ UAV Hardware Inventory & Constraints
**Project**: Dual-3060 AI Vision UAV
**Strategy**: Bottom-Up Design (Payload First)

## 🧠 Mission Computer (The Payload)
| Component | Model | Weight (g) | Dimensions (mm) | Voltage | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| AI Computer | **NVIDIA Jetson Nano (Ref)** | ~140g (Module+Heatsink) | 100 x 80 x 29 | 5V (4A) | Needs active cooling airflow |
| Camera | **CSI Camera (IMX219)** | ~3g | - | - | Forward facing |

## ✈️ Flight Electronics (The Heart)
*Existing FPV Inventory (To Be Verified)*

| Category | Component | Spec/Model | Weight (g) | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Flight Controller** | *TBD* | *e.g., Matek F405 / Pixhawk* | - | ❓ |
| **ESC** | *TBD* | *e.g., 4-in-1 or Individual* | - | ❓ |
| **Motor** | *TBD* | *e.g., 2207 2400KV / 2806 1300KV* | - | ❓ |
| **Propeller** | *TBD* | *e.g., 7 inch, 8 inch?* | - | ❓ |
| **Battery** | *TBD* | *e.g., LiPo 4S 1500mAh / LiIon 4S* | - | ❓ |
| **Receiver** | *TBD* | *e.g., ELRS / Crossfire* | - | ❓ |
| **GPS** | *TBD* | *e.g., BN-880* | - | ❓ |
| **Servos** | *TBD* | *e.g., 9g Metal Gear* | - | ❓ |

## 🧱 Digital Clones (CAD Assets)
- [ ] Jetson Nano Case/Mount
- [ ] Flight Controller Mount (30.5x30.5 / 20x20)
- [ ] Motor Mount Pattern (16x16 / 19x19)
- [ ] Battery Tray Volume

## 💨 Design Constraints
1.  **Fuselage Width**: Must accommodate Jetson Nano (100mm) + Wiring.
2.  **Cooling**: Intake vents aligned with Jetson Heatsink.
3.  **CG Balance**: Battery placement must counter-weight the front-mounted AI computer.
