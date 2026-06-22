
# FLIGHT

A custom, high-performance rocket flight computer designed around a Raspberry Pi Pico (RP2040) to track, log, and deploy parachutes using a servo.
This project is WIP and i do not guarantee that everything is working yet.

<img width="1724" height="978" alt="FRONT V1 5" src="https://github.com/user-attachments/assets/0b3ee80c-a42b-4f35-8d4f-f71571c01024" />

---

<p align="center">
  <img width="695" height="629" alt="pcb sdasdas" src="https://github.com/user-attachments/assets/108bbe89-a8d1-4833-ac66-d728aba80cc3" />
</p>

---

## Features

* Core Processing: Raspberry Pi Pico running custom data-logging, and control scripts.

* Integrated Sensors (GY-91): Combines an IMU (accelerometer/gyroscope) to measure high-G launch forces (± 16g) and orientation, alongside a precision barometer (BMP280) to calculate real-time altitude changes.

* Actuation / Recovery: Dedicated PWM outputs to trigger a servo mechanism for physical parachute deployment at apogee or however you wish to use it.

* Power & Protection Circuitry: Integrated TP4056 LiPo charging network backed by a comprehensive safety protection block (DW01A controller + FS8205A dual-MOSFET switch) to safely manage battery current and prevent over-discharge.

* Voltage Regulation (MT3608): A $1.2\text{ MHz}$ high-frequency DC-DC boost converter circuit to cleanly step up battery power to a stable $5\text{V}$ line for the onboard servo control.

---

## Mechanical & Layout Design

* Developed on a dual-layer PCB with a massive Ground Plane optimized for low electrical noise and high signal integrity.
  
* Designed with wide, heavy-current traces ($0.8\text{mm} - 1.0\text{mm}$) on the critical power highway loops (+BATT and -BATT) to safely absorb massive amp spikes when the deployment servos actuate.
  
* Custom aerospace graphics and visual infographics directly on the silkscreen layer.

<img width="1724" height="978" alt="BACK V1 5" src="https://github.com/user-attachments/assets/bf229743-d62b-423e-bfd4-7f5e11ce3cbf" />
