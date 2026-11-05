#!/usr/bin/env python3
"""Draw the robot 2 (telepresence robot) wiring diagram. Usage: draw_wiring.py <out_dir>   (needs matplotlib)"""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
RED, BLK, GRN, BLU, GRY, ORG = "#d62828", "#111111", "#2a9d3f", "#1d5fbf", "#666666", "#d9822b"
fig = plt.figure(figsize=(20, 12.6), dpi=110)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 200); ax.set_ylim(0, 126); ax.axis("off")


def box(x0, y0, x1, y1, text="", fc="#f4f1e8", ec="#333", fs=9, bold=False, lw=1.5, z=3):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0,rounding_size=1.1", fc=fc, ec=ec, lw=lw, zorder=z))
    if text:
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, text, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal", zorder=6, linespacing=1.25)


def wire(pts, c, lw=3.0, z=4, ls="-"):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=c, lw=lw, solid_capstyle="round", solid_joinstyle="round", zorder=z, ls=ls)


def txt(x, y, t, fs=8, c="#222", ha="center", va="center", bold=False):
    ax.text(x, y, t, fontsize=fs, color=c, ha=ha, va=va, fontweight="bold" if bold else "normal", zorder=7, linespacing=1.2)


def stub(x, y, t="to − splice"):
    wire([(x, y), (x, y - 4.2)], BLK, 2.8)
    ax.add_patch(plt.Circle((x, y - 4.2), 0.65, color=BLK, zorder=6))
    txt(x + 1.3, y - 2.2, t, 7, ha="left")


txt(100, 123.4, "ABADI ROVER 2 (TELEPRESENCE ROBOT) - WIRING   |   motherboard v5 + Raspberry Pi 5 + 7 inch HDMI screen", 16, bold=True)
txt(100, 120.0, "red = plus (+)    black = minus (−)    blue = data / video cable    orange = servo / motor leads    thick bar = lever-connector splice (+)", 10.5, "#333")

# ---------- battery + splice ----------
box(2, 98, 32, 116, "2S BATTERY PACK\ncells + BMS + charger\n+ main switch\n(see battery-wiring.png)", fc="#f6e9c8", fs=8.6, bold=True)
wire([(32, 107), (36.8, 107)], RED)
ax.add_patch(Rectangle((36, 12), 1.6, 97, color=RED, zorder=4))
txt(36.8, 111.6, "SPLICE +\n(lever connector)", 8.4, RED, bold=True)

# ---------- three rails for the motherboard ----------
rows = [(95, "5 A fuse\nslow-blow", None, "BATT IN\n(motors)", ""),
        (76, "5 A fuse", "XL4016 module\nset to 5.0 V\n(servo power)", "SERVO 5V IN\n(pan/tilt servos)", ""),
        (57, "2 A fuse", "fixed 5 V buck\n1.8 A\n(clean 5 V)", "CLEAN 5V IN\n(ESP32, sonars)", "")]
box(104, 41, 156, 114, "", fc="#e9eef5", ec="#335", lw=2.2)
txt(130, 111.2, "MOTHERBOARD v5", 12, "#223", bold=True)
txt(130, 107.6, "ESP32-S3 · DRV8833 A · PCA9685 · GY-521", 8, "#334")
for y, fuse, buck, term, what in rows:
    wire([(37.6, y + 1.5), (46, y + 1.5)], RED)
    box(46, y - 3.6, 60, y + 4.4, fuse, fc="#fff3b0", fs=7.6, bold=True)
    box(105.5, y - 4.0, 121, y + 4.0, "", fc="#fff")
    txt(114.4, y, term, 7.6, "#111", bold=True)
    txt(106.6, y + 1.7, "+", 9, RED, bold=True, ha="left"); txt(106.6, y - 1.7, "−", 10, BLK, bold=True, ha="left")
    if buck:
        wire([(60, y + 1.5), (68, y + 1.5)], RED)
        box(68, y - 6.2, 92, y + 6.2, buck, fc="#e7f0fa", fs=8, bold=True)
        txt(69.4, y + 4.2, "IN+", 6.8, RED, ha="left", bold=True); txt(90.6, y + 4.2, "OUT+", 6.8, RED, ha="right", bold=True)
        txt(69.4, y - 4.2, "IN−", 6.8, BLK, ha="left", bold=True); txt(90.6, y - 4.2, "OUT−", 6.8, BLK, ha="right", bold=True)
        wire([(92, y + 1.5), (105.5, y + 1.5)], RED); wire([(92, y - 1.5), (105.5, y - 1.5)], BLK)
        stub(71, y - 6.2)
    else:
        wire([(60, y + 1.5), (105.5, y + 1.5)], RED)
        stub(108, y - 4.0)
box(105.5, 43.2, 121, 51.2, "", fc="#e0e0e0", ec="#999")
txt(113.2, 47.2, "3.3V IN (not used)", 7.2, "#777")

# ---------- peripherals on the motherboard ----------
per = [(104.0, "LEFT MOTOR\n(Pololu 25D 12 V)", "M1 (JST 2-pin)", "DRV A out 1+2"),
       (95.6, "RIGHT MOTOR\n(Pololu 25D 12 V)", "M2 (JST 2-pin)", "DRV A out 3+4"),
       (87.2, "PAN SERVO (turn)", "PCA9685 CH0", "3-pin servo plug"),
       (78.8, "TILT SERVO (nod)", "PCA9685 CH1", "3-pin servo plug"),
       (70.4, "2 x SONAR HC-SR04", "SONAR 1 + 2 headers", "5 V, 4-pin"),
       (62.0, "BATTERY MONITOR\nADS1115 + divider", "I2C SENSOR header", "3V3 GND SDA SCL"),
       (53.6, "2 x CLIFF SENSOR\n(IR, 3.3 V)", "SPARE IO header", "GND 3V3 GPIO 21, 3"),
       (45.2, "CAMERA LED (CH2)\n+ CALL BUTTON (GPIO45)", "PCA CH2 + SPARE IO", "LED + button")]
for y, name, port, note in per:
    box(166, y - 3.5, 199, y + 3.5, name, fc="#fdebd0" if "MOTOR" in name or "SERVO" in name else "#e6f4e6", fs=7.4, bold=True)
    wire([(156, y), (166, y)], ORG if ("MOTOR" in name or "SERVO" in name) else GRN, 3.2)
    txt(154.4, y, port, 7.2, "#223", ha="right")
    txt(161, y + 2.3, note, 5.4, "#555")

# ---------- SBC branch (bottom) ----------
y = 22
wire([(37.6, y + 1.5), (46, y + 1.5)], RED)
box(46, y - 3.6, 60, y + 4.4, "5 A fuse", fc="#fff3b0", fs=7.6, bold=True)
wire([(60, y + 1.5), (68, y + 1.5)], RED)
box(68, y - 6.2, 92, y + 6.2, "XL4016 module\nset to 5.1 V\n(Pi + screen)", fc="#e7f0fa", fs=8, bold=True)
txt(69.4, y + 4.2, "IN+", 6.8, RED, ha="left", bold=True); txt(90.6, y + 4.2, "OUT+", 6.8, RED, ha="right", bold=True)
txt(69.4, y - 4.2, "IN−", 6.8, BLK, ha="left", bold=True); txt(90.6, y - 4.2, "OUT−", 6.8, BLK, ha="right", bold=True)
stub(71, y - 6.2)
box(104, 6, 156, 35, "", fc="#efe6f5", ec="#538", lw=2.2)
txt(130, 31.4, "SINGLE BOARD COMPUTER (SBC)", 10.5, "#325", bold=True)
txt(130, 28.0, "Raspberry Pi 5 (2 GB) - why: sbc-selection.md", 8, "#435")
wire([(92, y + 1.5), (104, y + 1.5)], RED); wire([(92, y - 1.5), (104, y - 1.5)], BLK)
txt(94.6, y + 3.6, "5.1 V", 7, RED, bold=True)
txt(130, 21.0, "power in: USB-C pigtail from the 5.1 V buck\n+ 1000 uF capacitor at the Pi (mind polarity)", 7.4, "#325")
txt(130, 12.2, "4 USB ports: webcam, audio, ESP32 (data-only cable),\ntouch (data-only cable)", 7.0, "#325")
# branch for the screen power
ax.add_patch(plt.Circle((99.5, y + 1.5), 0.9, color=RED, zorder=7))
wire([(99.5, y + 1.5), (99.5, 38.6), (138.6, 38.6), (139.3, 40.0), (140.7, 40.0), (141.4, 38.6), (164.4, 38.6), (164.4, 34.0), (166, 34.0)], RED, 2.8)
box(146, 36.9, 158, 40.3, "1 A fuse", fc="#fff3b0", fs=7, bold=True, z=5)
txt(101.0, 36.7, "5.1 V for the screen", 7, RED, ha="left", bold=True)

# USB link SBC -> ESP32
wire([(140, 35), (140, 41)], BLU, 3.4)
txt(138.0, 36.7, "USB (data-only cable): Pi → ESP32 COM port", 7.2, BLU, ha="right", bold=True)

# SBC peripherals
spe = [(30.5, "7 INCH HDMI SCREEN\n(+ touch, own 5.1 V lead)", "HDMI + touch", BLU), (21.0, "USB WEBCAM + MICROPHONE", "USB 3 port", BLU), (12.0, "SPEAKER: USB AUDIO ADAPTER\n+ amp + 40 mm speaker", "USB 2 port", BLU)]
for yy, name, how, c in spe:
    box(166, yy - 3.8, 199, yy + 3.8, name, fc="#e7ecf7", fs=7.8, bold=True)
    wire([(156, yy), (166, yy)], c, 3.2)
    txt(161, yy + 2.5, how, 5.8, "#555")

# legend / rules
txt(76, 4.0, "Every black stub = a black wire back to the − lever connector (the screen's black wire too). All − pins on the motherboard are one ground.\nBattery-monitor divider (47k / 27k) is taken from the SPLICE +. The USB link to the ESP32 must have NO 5 V wire (the ESP32 is fed from CLEAN 5V IN). 3.3 V buck and DRV B not fitted.", 7.2, "#555", ha="center")
fig.savefig(OUT + "/wiring-robot2.png")
fig.savefig(OUT + "/wiring-robot2.svg")
print("saved")
