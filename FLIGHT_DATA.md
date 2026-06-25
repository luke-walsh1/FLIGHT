```
import os
from tkinter import Tk, filedialog
import matplotlib.pyplot as plt
import pandas as pd

# =============================================================================
# 1. DATA LOADING & ENVIRONMENT SETUP
# =============================================================================
print("Opening file selector popup... Look for it on your taskbar!")
root = Tk()
root.withdraw()  # Hide the main blank Tkinter window
root.attributes("-topmost", True)  # Bring the file selection popup to the front

# Open standard OS file explorer dialog
file_path = filedialog.askopenfilename(
    title="Select your flight_log.csv data file",
    filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")],
)

if not file_path:
    print("Error: No file was selected. Exiting script.")
    exit()

print(f"Successfully loading file from: {file_path}")

# Read the CSV-formatted log file into a Pandas DataFrame
df = pd.read_csv(file_path)

# Convert Time from milliseconds to seconds for cleaner graph visualization
df["Time(s)"] = df["Timestamp(ms)"] / 1000.0
total_flight_time = df["Time(s)"].max()

# =============================================================================
# 2. PLOT CANVAS CONFIGURATION
# =============================================================================
# Set up 3 stacked subplots sharing the same X-axis (Time)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
fig.suptitle(
    "FLIGHT Rev 1.1 - Post-Flight Mission Analysis",
    fontsize=16,
    fontweight="bold",
    y=0.96,
)

# -----------------------------------------------------------------------------
# CHART 1: BAROMETRIC ALTITUDE PROFILE
# -----------------------------------------------------------------------------
ax1.plot(
    df["Time(s)"],
    df["Est_Altitude(m)"],
    color="darkblue",
    linewidth=2.5,
    label="Relative Altitude",
)

# Dynamic Apogee Detection
apogee_idx = df["Est_Altitude(m)"].idxmax()
apogee_time = df["Time(s)"].iloc[apogee_idx]
apogee_val = df["Est_Altitude(m)"].iloc[apogee_idx]

ax1.scatter(apogee_time, apogee_val, color="gold", s=100, zorder=5, edgecolor="black")
ax1.annotate(
    f"Apogee: {apogee_val:.1f}m\nat {apogee_time:.2f}s",
    xy=(apogee_time, apogee_val),
    xytext=(apogee_time + (total_flight_time * 0.04), apogee_val - (apogee_val * 0.15)),
    arrowprops=dict(facecolor="black", shrink=0.05, width=1, headwidth=6),
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3),
)

ax1.set_ylabel("Altitude (meters)", fontsize=11)
ax1.grid(True, linestyle=":", alpha=0.6)
ax1.legend(loc="upper left")
ax1.set_title("1. Barometric Altitude Tracking (BMP280)")

# -----------------------------------------------------------------------------
# CHART 2: INERTIAL ACCELERATION (G-FORCE PROFILE)
# -----------------------------------------------------------------------------
# Plotting all 3 axes so you can see vibrations/wobble vs vertical push
ax2.plot(df["Time(s)"], df["Accel_X(g)"], color="gray", alpha=0.5, label="X Axis (Lateral)")
ax2.plot(df["Time(s)"], df["Accel_Y(g)"], color="lightgray", alpha=0.5, label="Y Axis (Lateral)")
ax2.plot(df["Time(s)"], df["Accel_Z(g)"], color="crimson", linewidth=2, label="Z Axis (Vertical)")

ax2.axhline(1.0, color="black", linestyle="--", alpha=0.3, label="1G Static Gravity Baseline")

# Dynamic Max Thrust Detection (Peak vertical G-force)
max_g_idx = df["Accel_Z(g)"].idxmax()
burnout_time = df["Time(s)"].iloc[max_g_idx]
burnout_g = df["Accel_Z(g)"].iloc[max_g_idx]

ax2.annotate(
    f"Max Thrust ({burnout_g:.1f}g)",
    xy=(burnout_time, burnout_g),
    xytext=(burnout_time + (total_flight_time * 0.04), burnout_g - (burnout_g * 0.2)),
    arrowprops=dict(facecolor="black", shrink=0.08, width=1, headwidth=6),
    fontweight="bold",
)

# Dynamic Parachute Deployment Shock Detection (Deepest negative structural force on Z)
min_g_idx = df["Accel_Z(g)"].idxmin()
chute_time = df["Time(s)"].iloc[min_g_idx]
chute_g = df["Accel_Z(g)"].iloc[min_g_idx]

ax2.annotate(
    f"Chute Shock ({chute_g:.1f}g)",
    xy=(chute_time, chute_g),
    xytext=(chute_time + (total_flight_time * 0.04), chute_g + 1.0),
    arrowprops=dict(facecolor="black", shrink=0.08, width=1, headwidth=6),
    fontweight="bold",
)

ax2.set_ylabel("Structural Load (g)", fontsize=11)
ax2.grid(True, linestyle=":", alpha=0.6)
ax2.legend(loc="upper right")
ax2.set_title("2. IMU 3-Axis Structural Acceleration Profile (MPU9250)")

# -----------------------------------------------------------------------------
# CHART 3: AMBIENT TEMPERATURE GRADIENT
# -----------------------------------------------------------------------------
ax3.plot(
    df["Time(s)"],
    df["Temperature(C)"],
    color="teal",
    linewidth=2,
    label="Internal Temperature",
)
ax3.set_xlabel("Mission Elapsed Time (seconds)", fontsize=12)
ax3.set_ylabel("Temperature (°C)", fontsize=11)
ax3.grid(True, linestyle=":", alpha=0.6)
ax3.legend(loc="upper right")
ax3.set_title("3. Ambient Flight Temperature Gradient")

# =============================================================================
# 3. RENDER CLEANUP
# =============================================================================
plt.tight_layout(rect=[0, 0.03, 1, 0.93])
plt.show()
