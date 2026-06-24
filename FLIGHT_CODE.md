```
import machine

import time

import os



# ==========================================

# 1. HARDWARE PIN CONFIGURATION

# ==========================================

# Arming Button on GPIO 14 (Internal Pull-Up)

arm_button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)



# I2C Configuration for GY-91 (SDA=GPIO 4, SCL=GPIO 5)

i2c = machine.I2C(0, sda=machine.Pin(4), scl=machine.Pin(5), freq=400000)



# SPI Configuration for MicroSD Card Slot (MISO=16, CS=17, SCK=18, MOSI=19)

spi = machine.SPI(0, sck=machine.Pin(18), mosi=machine.Pin(19), miso=machine.Pin(16))

cs = machine.Pin(17, machine.Pin.OUT)



# ==========================================

# 2. STANDBY & INITIALIZATION PHASE

# ==========================================

print("FLIGHT Core: Powered On.")

print("STATUS: Standby Mode. Hold button for 3 seconds to ARM...")



# --- 3-Second Arming Button Check ---

while True:

    if arm_button.value() == 0:  # Button pressed (connected to GND)

        hold_counter = 0

        while arm_button.value() == 0:

            hold_counter += 1

            time.sleep(0.1)

            if hold_counter >= 30:  # 30 * 0.1s = 3 full seconds

                break

                

        if hold_counter >= 30:

            print("STATUS: System ARMED successfully!")

            break

    time.sleep(0.1)



# Initialize and Mount MicroSD Card

try:

    import sdcard

    sd = sdcard.SDCard(spi, cs)

    vfs = os.VfsFat(sd)

    os.mount(vfs, "/sd")

    print("Storage: MicroSD mounted successfully.")

    log_to_sd = True

except Exception as e:

    print("Storage Error: Failed to mount MicroSD!", e)

    log_to_sd = False



# Initialize Barometer (BMP280 inside GY-91 module)

try:

    from bmp280 import BMP280

    bmp = BMP280(i2c)

    bmp.use_case(BMP280.CASE_WEATHER)

    print("Sensors: Barometer (BMP280) online.")

    baro_ready = True

except Exception as e:

    print("Sensor Error: BMP280 Initialization Failed!", e)

    baro_ready = False



# Initialize IMU (MPU9250 inside GY-91 module)

try:

    from mpu9250 import MPU9250

    imu = MPU9250(i2c)

    print("Sensors: IMU G-Force/Gyro (MPU9250) online.")

    imu_ready = True

except Exception as e:

    print("Sensor Error: IMU Initialization Failed!", e)

    imu_ready = False



# Establish Launch Pad Baseline Pressure for Altitude Calculation

if baro_ready:

    print("Calibrating launch pad altitude baseline...")

    baseline_pressure = 0

    for _ in range(10):

        baseline_pressure += bmp.pressure

        time.sleep(0.1)

    baseline_pressure /= 10

    print(f"Calibration locked. Baseline: {baseline_pressure:.2f} Pa")



# ==========================================

# 3. ACTIVE FLIGHT RUNTIME LOGGING

# ==========================================

if baro_ready and imu_ready and log_to_sd:

    # Create the CSV file header with G-force columns added back

    with open("/sd/flight_log.csv", "a") as f:

        f.write("Timestamp(ms),Pressure(Pa),Temperature(C),Est_Altitude(m),Accel_X(g),Accel_Y(g),Accel_Z(g)\n")

    

    print("--- RUNTIME ACTIVE: LOGGING DATA + G-FORCE ---")

    start_time = time.ticks_ms()

    

    while True:

        try:

            # Calculate elapsed time in milliseconds

            current_time = time.ticks_diff(time.ticks_ms(), start_time)

            

            # Read environmental variables

            press = bmp.pressure

            temp = bmp.temperature

            

            # Hypsometric relative altitude calculation formula

            altitude = 44330 * (1.0 - (press / baseline_pressure) ** 0.1903)

            

            # Read G-forces from IMU accelerometer vector (returns x, y, z tuples)

            accel = imu.acceleration

            ax, ay, az = accel[0], accel[1], accel[2]

            

            # Print status to serial terminal for workbench debugging

            print(f"T+{current_time}ms | Alt: {altitude:.2f}m | G-Z: {az:.2f}g")

            

            # Write data row to the SD Card

            with open("/sd/flight_log.csv", "a") as f:

                f.write(f"{current_time},{press},{temp},{altitude:.2f},{ax:.2f},{ay:.2f},{az:.2f}\n")

            

            time.sleep(0.1)  # 10Hz Sample Rate

            

        except KeyboardInterrupt:

            print("FLIGHT Core: Logging stopped safely.")

            break

else:

    print("FATAL: Hardware initialization failed. Execution halted.")


```
