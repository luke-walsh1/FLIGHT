<p align="center">
<img width="1024" height="288" alt="image" src="https://github.com/user-attachments/assets/47de00de-d221-4449-ad99-10b25c82d9e1" />
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

# DATA

The goal is to log data. FLIGHT saves data in a format that looks like this:

```
Timestamp(ms),Pressure(Pa),Temperature(C),Est_Altitude(m),Accel_X(g),Accel_Y(g),Accel_Z(g)
0,101325.00,21.50,0.00,0.02,-0.01,1.01
100,101324.80,21.50,0.02,0.01,0.00,1.00
200,101325.10,21.48,-0.01,-0.01,-0.02,1.02
300,101310.20,21.45,1.23,0.15,0.08,2.45
400,101215.50,21.40,9.10,-0.32,0.45,5.12
500,101010.00,21.35,26.21,0.85,-0.92,7.89
600,100650.30,21.28,55.80,-1.10,1.20,6.54
700,100110.00,21.20,100.95,0.45,-0.32,0.12
800,99520.40,21.12,150.32,0.12,0.11,-0.15
900,99100.10,21.05,185.71,-0.05,0.02,-0.22
1000,98950.00,20.98,198.40,0.01,-0.02,-0.05
1100,98962.20,20.99,197.38,-0.12,0.15,-1.95
1200,99120.50,21.02,184.02,0.22,-0.18,-0.85

```
These numbers by themselves arent that helpfull however with the help of a python program we can graph this data and mark the max altitude and other data points.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a8c05150-00b3-4c91-8d45-b3b0f63e7ba1" />

More on my YouTube and Stardance Profile:

https://stardance.hackclub.com/projects/18720

https://www.youtube.com/watch?v=rl3e3K6eBTs
