# TKEEB
---
So I've made a fully custom 88-key mechanical keyboard powered by the Raspberry Pi Pico (RP2040), running KMK Firmware.
The layout is a standard TKL-style matrix, and I added an EC11 Rotary Encoder for volume control, per-key RGB lighting, and a 0.96" SSD1306 I²C OLED display which will show the real-time clock + date.

## Hardware Overview

### Components
- Raspberry Pi Pico (RP2040)
- 88x Mechanical Switches (Kailh Hotswap Sockets)
- 1× EC11 Rotary Encoder (with Push Switch)
- 0.96" SSD1306 OLED (128×64, I²C)
- 88× WS2812B RGB LEDs (NeoPixels)
- 470µF Tantalum Capacitor (Case D) & 470Ω Resistor (for power stability)

> **Design Note:** I am currently upgrading the LED specification from the standard 5050 package to the compact **2020 form factor**. This optimization ensures superior mechanical clearance between the PCB surface and the hotswap sockets, allowing for a flush, high-density assembly without compromising RGB brightness.

### Schematic
<img width="1433" height="718" alt="Screenshot 2025-12-29 143902" src="https://github.com/user-attachments/assets/f1150196-3ae6-44e0-80bc-277647b045aa" />

### PCB
<img width="1127" height="457" alt="Screenshot 2025-12-29 143838" src="https://github.com/user-attachments/assets/9ec19b12-b288-444c-818f-3f42873d7acb" />

### 3D Render (Assembled)
<img width="1427" height="493" alt="Screenshot 2025-12-29 164352" src="https://github.com/user-attachments/assets/4e07bf1a-1e28-4802-99ad-476b196ff0a5" />

### 3D Render (without PCB)
<img width="1412" height="491" alt="Screenshot 2025-12-29 164414" src="https://github.com/user-attachments/assets/471ea1f5-f901-43e9-b69c-9579c34b5ff5" />

### 3D Render (Top Plate - Top)
<img width="1403" height="422" alt="Screenshot 2025-12-29 164917" src="https://github.com/user-attachments/assets/83cd2f4b-a222-442f-9f63-85622d3ac5e2" />

### 3D Render (Top Plate - Bottom)
<img width="1626" height="465" alt="Screenshot 2025-12-29 164942" src="https://github.com/user-attachments/assets/80e21a73-8bdf-438a-958e-bfc7287ba299" />

### 3D Render (Bottom Base)


## Firmware

The keyboard runs on **KMK Firmware**, which is a lightweight Python-based keyboard firmware stored directly on the device’s flash.
Because of the custom matrix routing used, the **keys will appear scrambled** when the keyboard is first plugged in. This is expected behavior.
I integrated **Vial** support (GUID: `8f2e4a1b-9c3d-4e5f-b6a7-0d9e8c7b6a51`) to handle this. You simply open [Vial.rocks](https://vial.rocks), use the Matrix Tester to identify the switches, and drag-and-drop the correct characters to remap them instantly without editing code.
