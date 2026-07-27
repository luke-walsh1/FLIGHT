import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# ---------------------------------------------------------
# 1. Open File Selector
# ---------------------------------------------------------
root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)

file_path = filedialog.askopenfilename(
    title="Select Flight Log for Visualizer",
    filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
)

if not file_path:
    print("No file selected. Exiting...")
    exit()

print(f"Loading: {file_path}")

# ---------------------------------------------------------
# 2. Load & Clean Telemetry Data
# ---------------------------------------------------------
try:
    df = pd.read_csv(file_path, sep=r'\s+|,', engine='python')
    df.columns = df.columns.str.strip()

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna().reset_index(drop=True)

    # Split MCU reboots if present
    reboot_indices = df.index[df['Time_ms'].diff() < 0].tolist()
    if reboot_indices:
        df = df.iloc[reboot_indices[-1]:].reset_index(drop=True)

    df = df[df['Pressure_hPa'] > 500].reset_index(drop=True)
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

# Math Calculations
time_sec = (df['Time_ms'] - df['Time_ms'].iloc[0]) / 1000.0
df['Accel_Mag'] = np.sqrt(df['Accel_X']**2 + df['Accel_Y']**2 + df['Accel_Z']**2)

z_clamped = np.clip(df['Accel_Z'] / df['Accel_Mag'], -1.0, 1.0)
df['Tilt_Angle_deg'] = np.degrees(np.arccos(z_clamped))

df['Alt_Smooth'] = df['Altitude_m'].rolling(window=5, center=True, min_periods=1).mean()
df['Tilt_Smooth'] = df['Tilt_Angle_deg'].rolling(window=5, center=True, min_periods=1).mean()

# ---------------------------------------------------------
# 3. Calculate Peaks for Annotations
# ---------------------------------------------------------
max_alt_idx = df['Alt_Smooth'].idxmax()
max_alt_val = df['Alt_Smooth'].iloc[max_alt_idx]
max_alt_time = time_sec.iloc[max_alt_idx]

max_g_idx = df['Accel_Mag'].idxmax()
max_g_val = df['Accel_Mag'].iloc[max_g_idx]
max_g_time = time_sec.iloc[max_g_idx]

# ---------------------------------------------------------
# 4. Setup DARK THEME Dashboard Layout
# ---------------------------------------------------------
plt.style.use('dark_background')

fig = plt.figure(figsize=(14, 8), facecolor='#0f111a')
filename_only = os.path.basename(file_path)
fig.suptitle(f'Telemetry Analysis & 3D Playback — {filename_only}', fontsize=14, fontweight='bold', color='white')

# --- Left Column: 2D Graphs ---
ax1 = fig.add_subplot(3, 2, 1, facecolor='#181a24')
ax2 = fig.add_subplot(3, 2, 3, sharex=ax1, facecolor='#181a24')
ax3 = fig.add_subplot(3, 2, 5, sharex=ax1, facecolor='#181a24')

# Altitude Subplot (Neon Cyan)
ax1.plot(time_sec, df['Altitude_m'], color='#003366', alpha=0.5, label='Raw Alt')
ax1.plot(time_sec, df['Alt_Smooth'], color='#00f2ff', linewidth=2, label='Filtered Alt (m)')
ax1.set_ylabel('Altitude (m)', color='white')
ax1.legend(loc='upper left', facecolor='#181a24', edgecolor='none')
ax1.grid(True, color='#2e3245', linestyle=':')

# Annotate Max Altitude
ax1.scatter(max_alt_time, max_alt_val, color='#00f2ff', s=60, zorder=5)
ax1.annotate(
    f'Max Alt: {max_alt_val:.2f} m\n@{max_alt_time:.1f}s',
    xy=(max_alt_time, max_alt_val),
    xytext=(max_alt_time + (time_sec.max() * 0.05), max_alt_val * 0.85),
    arrowprops=dict(facecolor='#00f2ff', edgecolor='#00f2ff', arrowstyle='->', lw=1.5),
    bbox=dict(boxstyle='round,pad=0.3', facecolor='#181a24', edgecolor='#00f2ff', alpha=0.9),
    color='white', fontweight='bold', fontsize=9
)

# G-Force Subplot (Neon Green)
ax2.plot(time_sec, df['Accel_Mag'], color='#39ff14', linewidth=1.5, label='Total Accel (G)')
ax2.set_ylabel('Acceleration (G)', color='white')
ax2.legend(loc='upper left', facecolor='#181a24', edgecolor='none')
ax2.grid(True, color='#2e3245', linestyle=':')

# Annotate Peak G-Force
ax2.scatter(max_g_time, max_g_val, color='#39ff14', s=60, zorder=5)
ax2.annotate(
    f'Peak Accel: {max_g_val:.2f} G\n@{max_g_time:.1f}s',
    xy=(max_g_time, max_g_val),
    xytext=(max_g_time + (time_sec.max() * 0.05), max_g_val * 0.8),
    arrowprops=dict(facecolor='#39ff14', edgecolor='#39ff14', arrowstyle='->', lw=1.5),
    bbox=dict(boxstyle='round,pad=0.3', facecolor='#181a24', edgecolor='#39ff14', alpha=0.9),
    color='white', fontweight='bold', fontsize=9
)

# Tilt Angle Subplot (Neon Yellow/Orange)
ax3.plot(time_sec, df['Tilt_Angle_deg'], color='#664400', alpha=0.5, label='Raw Tilt')
ax3.plot(time_sec, df['Tilt_Smooth'], color='#ffaa00', linewidth=2, label='Tilt Angle (°)')
ax3.set_ylabel('Tilt (°)', color='white')
ax3.set_xlabel('Time (seconds)', color='white')
ax3.legend(loc='upper left', facecolor='#181a24', edgecolor='none')
ax3.grid(True, color='#2e3245', linestyle=':')

# --- Right Side: 3D Video Viewport ---
ax_3d = fig.add_subplot(1, 2, 2, projection='3d', facecolor='#0f111a')
ax_3d.set_xlim([-1.5, 1.5])
ax_3d.set_ylim([-1.5, 1.5])
ax_3d.set_zlim([-1.5, 1.5])

ax_3d.xaxis.pane.set_facecolor('#181a24')
ax_3d.yaxis.pane.set_facecolor('#181a24')
ax_3d.zaxis.pane.set_facecolor('#181a24')
ax_3d.xaxis.pane.set_edgecolor('#2e3245')
ax_3d.yaxis.pane.set_edgecolor('#2e3245')
ax_3d.zaxis.pane.set_edgecolor('#2e3245')

ax_3d.set_xlabel('Accel X', color='white')
ax_3d.set_ylabel('Accel Y', color='white')
ax_3d.set_zlabel('Accel Z', color='white')

# Initial 3D Vector & Time Trackers
quiver = ax_3d.quiver(0, 0, 0, 0, 0, 1, color='#ff0055', linewidth=4)

line1 = ax1.axvline(x=0, color='#ff0055', linestyle='--', alpha=0.8)
line2 = ax2.axvline(x=0, color='#ff0055', linestyle='--', alpha=0.8)
line3 = ax3.axvline(x=0, color='#ff0055', linestyle='--', alpha=0.8)

title_3d = ax_3d.set_title('Live 3D Orientation Vector', fontsize=12, fontweight='bold', color='white')

# ---------------------------------------------------------
# 5. Animation Function
# ---------------------------------------------------------
def update_telemetry(frame):
    global quiver
    quiver.remove()
    
    ax_val = df['Accel_X'].iloc[frame]
    ay_val = df['Accel_Y'].iloc[frame]
    az_val = df['Accel_Z'].iloc[frame]
    
    mag = df['Accel_Mag'].iloc[frame]
    if mag == 0:
        mag = 1.0

    quiver = ax_3d.quiver(0, 0, 0, ax_val/mag, ay_val/mag, az_val/mag, color='#ff0055', linewidth=4)
    
    current_time = time_sec.iloc[frame]
    line1.set_xdata([current_time])
    line2.set_xdata([current_time])
    line3.set_xdata([current_time])
    
    alt = df['Altitude_m'].iloc[frame]
    tilt = df['Tilt_Angle_deg'].iloc[frame]
    title_3d.set_text(f'Time: {current_time:.1f}s | Alt: {alt:.2f}m | Tilt: {tilt:.1f}° | G: {mag:.2f}G')
    
    return quiver, line1, line2, line3

# Animate video playback
ani = animation.FuncAnimation(fig, update_telemetry, frames=len(df), interval=50, blit=False)

plt.tight_layout()

# Save image with annotations
output_png = os.path.splitext(file_path)[0] + "_annotated_dashboard.png"
plt.savefig(output_png, dpi=300, facecolor=fig.get_facecolor())
print(f"Saved annotated dark dashboard image to: {output_png}")

plt.show()