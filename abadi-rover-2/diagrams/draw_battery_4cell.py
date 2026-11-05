#!/usr/bin/env python3
"""Draw the 4-cell (2S2P) battery sketch for robot 2: 4 cells + BMS + charger board.
Usage: draw_battery_4cell.py <out_dir>   (needs matplotlib)
Same simple style as ../../pcb/kicad/battery-wiring.png (which shows 2 cells and is locked)."""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
RED, BLK, GRN, GRY = "#d62828", "#111111", "#2a9d3f", "#666666"
PAD_FC, PAD_EC = "#e8c040", "#8a6d00"
fig = plt.figure(figsize=(18, 12.5), dpi=110)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 180); ax.set_ylim(0, 125); ax.axis("off")


def box(x0, y0, x1, y1, fc, ec="#333", lw=1.6, z=3, ls="-"):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0,rounding_size=1.2", fc=fc, ec=ec, lw=lw, zorder=z, ls=ls))


def txt(x, y, t, fs=8, c="#222", ha="center", va="center", bold=False):
    ax.text(x, y, t, fontsize=fs, color=c, ha=ha, va=va, fontweight="bold" if bold else "normal", zorder=7, linespacing=1.3)


def wire(pts, c, lw=4.0, z=4):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=c, lw=lw, solid_capstyle="round", solid_joinstyle="round", zorder=z)


def dot(x, y, c, r=1.1):
    ax.add_patch(plt.Circle((x, y), r, color=c, zorder=6))


def pad(x, y, s=3.0):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc=PAD_FC, ec=PAD_EC, lw=1.2, zorder=5))


txt(90, 120.5, "BATTERY WIRING:  4 cells (2S2P)  +  your BMS  +  your charger board", 17, bold=True)
txt(90, 116.0, "red = plus (+)      black = minus (−)      green = the junction between the two pairs (the BM wire goes here)", 10.5, "#333")

# ---------- USB adapter and charger ----------
box(2, 62, 20, 78, "#eee9dd")
txt(11, 70, "USB-C\nadapter\n5 V, 2 A", 8.6)
wire([(20, 70), (28, 70)], GRY, 3.4)
txt(24, 73.4, "USB\ncable", 6.6)
box(28, 52, 60, 92, "#e7f0fa")
txt(44, 87, "YOUR CHARGER", 9.6, bold=True)
txt(44, 83, "chip IP2326, USB-C input", 7.6)
txt(44, 77.6, "2S = 8.4 V by default", 7.6)
txt(44, 70.4, "(pads drawn as on your board:\nB− on top, B+ below)", 6.6, "#555")
txt(44, 56.6, "leave the NTC, VSET, VIN\nand GND pads alone", 6.6, "#555")
pad(60, 80); pad(60, 62)
txt(57.4, 80, "B−", 8.6, BLK, ha="right", bold=True)
txt(57.4, 62, "B+", 8.6, RED, ha="right", bold=True)

# ---------- BMS ----------
box(88, 40, 118, 100, "#dff0df")
txt(103, 94, "YOUR BMS", 9.6, bold=True)
txt(103, 90, "2S, balancing", 7.6)
txt(103, 44.5, "left side = output (P+, P−)\nright side = cells (B+, BM, B−)", 6.6, "#555")
for yy, name, c, side in [(96, "P+", RED, "L"), (50, "P−", BLK, "L"), (96, "B+", RED, "R"), (78, "BM", GRN, "R"), (50, "B−", BLK, "R")]:
    xx = 88 if side == "L" else 118
    pad(xx, yy)
    if side == "L":
        txt(xx + 2.6, yy, name, 8.6, c, ha="left", bold=True)
    else:
        txt(xx - 2.6, yy, name, 8.6, c, ha="right", bold=True)

# charger B+ -> P+ (red), charger B- -> P- (black, with a small hop over the red wire)
wire([(60, 62), (66, 62), (66, 96), (88, 96)], RED)
wire([(60, 80), (65.0, 80), (65.6, 81.5), (66.6, 81.5), (67.2, 80), (74, 80), (74, 50), (88, 50)], BLK)

# ---------- to the robot ----------
box(62, 104, 86, 113, "#fdebd0")
txt(74, 110.0, "TO THE ROBOT  +", 8.2, bold=True)
txt(74, 106.6, "(main switch, then fuses)", 7.2, bold=True)
wire([(78, 96), (78, 104)], RED)
dot(78, 96, RED)
box(62, 28, 86, 37, "#eeeeee")
txt(74, 34.0, "TO THE ROBOT  −", 8.2, bold=True)
txt(74, 30.6, "(the − lever connector)", 7.2, bold=True)
wire([(78, 50), (78, 37)], BLK)
dot(78, 50, BLK)

# ---------- the four cells ----------
cells = [("A2", 128, 84), ("B2", 150, 84), ("A1", 128, 56), ("B1", 150, 56)]
for name, x0, y0 in cells:
    box(x0, y0, x0 + 18, y0 + 16, "#f5e9c8")
    txt(x0 + 9, y0 + 8, "CELL %s\n18650" % name, 9, bold=True)
    txt(x0 + 3.0, y0 + 17.8, "+", 10, RED, bold=True)
    txt(x0 + 3.0, y0 - 1.9, "−", 11, BLK, bold=True)
cx = [137, 159]
# plus bus of pair 2 (A2 + B2, plus to plus) and the wire to BMS B+
wire([(118, 96), (124, 96), (124, 106), (cx[1], 106)], RED)
for x in cx:
    wire([(x, 100), (x, 106)], RED)
    dot(x, 106, RED)
# junction bus: pair 2 minus = pair 1 plus, and the BM wire
wire([(118, 78), (cx[1], 78)], GRN)
for x in cx:
    wire([(x, 84), (x, 72)], GRN)
    dot(x, 78, GRN)
# minus bus of pair 1 (A1 -, B1 -, minus to minus) and the wire to BMS B-
wire([(118, 50), (cx[1], 50)], BLK)
for x in cx:
    wire([(x, 56), (x, 50)], BLK)
    dot(x, 50, BLK)

txt(170.5, 92, "PAIR 2", 8.6, "#553", ha="left", bold=True)
txt(170.5, 88.4, "A2 + B2\nin parallel", 6.8, "#553", ha="left")
txt(170.5, 64, "PAIR 1", 8.6, "#553", ha="left", bold=True)
txt(170.5, 60.4, "A1 + B1\nin parallel", 6.8, "#553", ha="left")
txt(161.6, 78, "series link:\npair 1 + to\npair 2 −", 7.0, GRN, ha="left", bold=True)

# ---------- order ----------
box(2, 1, 60, 45, "#fff8e1", ec="#b8860b", lw=2.0)
txt(4.5, 42, "ORDER  (one wire at a time, tape every bare end)", 8.4, "#8a5a00", ha="left", bold=True)
steps = ["1. All 4 cells: same batch, same model. Measure each alone:",
         "    all within 0.05 V, or charge the low ones first.",
         "2. Pair 1: join A1 + B1 (plus to plus, minus to minus).",
         "    Pair 2: join A2 + B2 the same way.",
         "3. Join pair 1 + to pair 2 − (the series link).",
         "4. BMS wires: B− first (pair 1 −), then BM (series",
         "    link), then B+ (pair 2 +).",
         "5. Measure P+ to P−: 7.4 to 8.4 V.",
         "6. USB unplugged: charger B+ to P+, B− to P−.",
         "7. Plug in the USB adapter. Watch the voltage:",
         "    it must stop rising at 8.4 V.",
         "8. Robot wires go on the SAME P+ and P− pads as",
         "    the charger wires, never on B−."]
for i, s in enumerate(steps):
    txt(4.5, 38.2 - i * 2.85, s, 7.3, "#333", ha="left")

# ---------- rules ----------
box(92, 1, 178, 36, "#f1dcdc", ec="#a33", lw=2.0)
txt(94.5, 33, "RULES FOR FOUR CELLS", 8.6, "#a02020", ha="left", bold=True)
rules = ["• Same batch and same model for all 4 cells. No damaged cells. Never join cells of different charge.",
         "• Bring ALL cells to the same voltage, within 0.05 V, BEFORE the first joint. Never \"equalise\" by joining them.",
         "• One BMS only. NO fuse between the pairs. The BMS limit (10 A) and the 5 A branch fuses stay as they are.",
         "• Reach every cell end and the middle point: 4 single-cell holders, or two 2-cell holders with a middle wire.",
         "• The wires inside the pack have no fuse: keep them short, AWG 18 or thicker, bare ends taped.",
         "• Before anything else is connected: B+ to B− reads 7.4 to 8.4 V; B+ to BM and BM to B− read about",
         "    3.0 to 4.2 V each. Charger B+ to B− must read about 8.4 V (2S); 12 V or more = set to 3S: do NOT connect it.",
         "• The robot weighs about 3.2 kg with 4 cells; about 2.2 to 2.8 hours of calling (ASSUMED, measure in Stage 3)."]
for i, s in enumerate(rules):
    txt(94.5, 29.2 - i * 3.3, s, 7.1, "#333", ha="left")

fig.savefig(OUT + "/battery-4cell.png")
fig.savefig(OUT + "/battery-4cell.svg")
print("saved")
