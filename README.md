# FLIGHT
A custom, high-performance rocket flight computer designed around a Raspberry Pi Pico (RP2040) to track, log, and deploy parachutes using a servo.

Core Processing: Raspberry Pi Pico running custom telemetry, data-logging, and control scripts.
Integrated Sensors (GY-91): Combines an IMU (accelerometer/gyroscope) to measure high-G launch forces and orientation, alongside a precision barometer (BMP280) to calculate real-time altitude changes.Actuation / 
Recovery: Dedicated PWM outputs to trigger a servo mechanism for physical parachute deployment at apogee.
Power & Protection Circuitry: Integrated TP4056 LiPo charging network backed by a comprehensive safety protection block (DW01A controller + FS8205A dual-MOSFET switch) to safely manage battery current and prevent over-discharge.
Voltage Regulation (MT3608): A $1.2\text{ MHz}$ high-frequency DC-DC boost converter circuit to cleanly step up battery power to a stable $5\text{V}$ line for the onboard sensors and servos.
