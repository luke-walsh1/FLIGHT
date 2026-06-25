<p align="center">
<img width="220" height="220" alt="FLIGHT AVIONICS" src="https://github.com/user-attachments/assets/ad5a8aaf-a48c-42e4-bcc5-ee30d990d3c7" />
</p>

## FLIGHT

FLIGHT is a custom, high-performance rocket flight computer designed around a Raspberry Pi Pico (RP2040) to track, log, and deploy parachutes using a servo.

### this project is WIP and i do not guarantee that everything is working yet.

<img width="1918" height="978" alt="rasppico altimiter 1 7" src="https://github.com/user-attachments/assets/56ea261e-ac57-4084-998a-59d0bfa2c2f6" />

---


## Features

* Core Processing: Raspberry Pi Pico running custom data-logging, and control scripts.

* Integrated Sensors (GY-91): Combines an IMU (accelerometer/gyroscope) to measure high-G launch forces (± 16g) and orientation, alongside a precision barometer (BMP280) to calculate real-time altitude changes.

* Actuation / Recovery: Dedicated PWM outputs to trigger a servo mechanism for physical parachute deployment at apogee or however you wish to use it. not implimented in code, challange for yourself :)

* Power & Protection Circuitry: Integrated TP4056 LiPo charging network backed by a comprehensive safety protection block (DW01A controller + FS8205A dual-MOSFET switch) to safely manage battery current and prevent over-discharge.

* Voltage Regulation (MT3608): A  DC-DC boost converter circuit to cleanly step up battery power to a stable $5\text{V}$ line for the onboard servo control.

  <img width="1918" height="978" alt="rasppico altimiter 1 7  back" src="https://github.com/user-attachments/assets/efae182b-e41b-45f9-a3a7-c6dcfaae92b5" />

---

## Mechanical & Layout Design

* Developed on a dual-layer PCB with a massive Ground Plane optimized for low electrical noise and high signal integrity.
  
* Designed with wide, heavy-current traces ($0.8\text{mm} - 1.0\text{mm}$) on the critical power highway loops (+BATT and -BATT) to safely absorb massive amp spikes when the deployment servos actuate.
  
* Custom aerospace graphics and visual infographics directly on the silkscreen layer.


<p align="center">
 <img width="684" height="622" alt="image" src="https://github.com/user-attachments/assets/3d16875b-5594-4297-a442-23ff238c6d3a" />
</p>


