<p align="center">
<img width="1024" height="288" alt="image" src="https://github.com/user-attachments/assets/47de00de-d221-4449-ad99-10b25c82d9e1" />
</p>

## FLIGHT

FLIGHT is a custom, high-performance rocket flight computer designed around a Raspberry Pi Pico (RP2040) to track, log, and deploy parachutes using a servo.

## Disclaimer
### The provided code is tested and working with the hardware; however, the servo and arm button controls can be customized to suit your specific needs and are not implimented in the code:)

---

<img width="1918" height="978" alt="rasppico altimiter 1 7" src="https://github.com/user-attachments/assets/56ea261e-ac57-4084-998a-59d0bfa2c2f6" />

<img width="4000" height="3000" alt="20260807_190316 1" src="https://github.com/user-attachments/assets/eb9ac075-e5b2-4a20-8350-ed8eae75aca7" />


---


## Features

* Core Processing: Raspberry Pi Pico running custom data-logging, and control scripts.

* Integrated Sensors (GY-91): Combines an IMU (accelerometer/gyroscope) to measure high-G launch forces (± 16g) and orientation, alongside a precision barometer (BMP280) to calculate real-time altitude changes.

* Recovery: Dedicated PWM outputs to trigger a servo mechanism for physical parachute deployment at apogee or however you wish to use it. not implimented in code, challange for yourself :)

* Power & Protection Circuitry: Integrated TP4056 LiPo charging network backed by a comprehensive safety protection block (DW01A controller + FS8205A dual-MOSFET switch) to safely manage battery current and prevent over-discharge.

* Voltage Regulation (MT3608): A  DC-DC boost converter circuit to cleanly step up battery power to a stable $5\text{V}$ line for the onboard servo control.

  <img width="1918" height="978" alt="rasppico altimiter 1 7  back" src="https://github.com/user-attachments/assets/efae182b-e41b-45f9-a3a7-c6dcfaae92b5" />

<img width="4000" height="3000" alt="20260807_190732 1" src="https://github.com/user-attachments/assets/f362efde-2315-4cad-bd7f-0b7cd2dd6455" />


---

## Mechanical & Layout Design

* Developed on a dual-layer PCB with a massive Ground Plane optimized for low electrical noise and high signal integrity.
  
* Designed with wide, heavy-current traces ($0.8\text{mm} - 1.0\text{mm}$) on the critical power highway loops (+BATT and -BATT) to safely absorb massive amp spikes when the deployment servos actuate.
  
* Custom aerospace graphics and visual infographics directly on the silkscreen layer.


<p align="center">
 <img width="684" height="622" alt="image" src="https://github.com/user-attachments/assets/3d16875b-5594-4297-a442-23ff238c6d3a" />
</p>

# DATA

The goal is to log data. FLIGHT saves data in a format that looks like this:


<img width="484" height="393" alt="image" src="https://github.com/user-attachments/assets/19f1c8ff-7cb5-4e7a-a3df-67507a9c7efb" />

---

These numbers by themselves arent that helpfull however with the help of a python program we can graph this data and mark the max altitude and other data points.

---

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/96aa4529-f86c-4a71-b71f-c26158b87d6a" />


More on my YouTube and Stardance Profile:


https://stardance.hackclub.com/projects/18720


https://www.youtube.com/watch?v=rl3e3K6eBTs
