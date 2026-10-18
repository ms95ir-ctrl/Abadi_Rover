#!/usr/bin/env python3
"""Draft v0 floor plan: reusable robot carrier board, 100 x 100 mm.

Placement only. Nothing is routed and nothing here is for fabrication. Module sizes are the
common sizes for each part and still have to be checked against the real modules.
Run:  python3 floorplan_v0.py   (needs matplotlib)  ->  floorplan_v0_top.png, floorplan_v0_3d.png
"""
import math
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Circle, Polygon, Rectangle

OUT = os.path.dirname(os.path.abspath(__file__))
W = H = 100.0
HOLES = [(4.0, 4.0), (96.0, 4.0), (4.0, 96.0), (96.0, 96.0)]  # M3
HOLE_KEEPOUT = 3.2  # radius reserved around each M3 hole for the screw head
PITCH = 2.54
TERM_PITCH = 5.08
TERM_DEPTH = 8.0

# colours
BOARD = "#1f7a3a"
C_ESP = "#5b9bd5"
C_DRV = "#f4a261"
C_GYRO = "#b48ad9"
C_PWR = "#d95050"
C_MOTOR = "#3b6fd4"
C_CABLE = "#2b2b2b"
C_SOCKET = "#3a3a3a"

parts = []  # footprint rectangles used for the overlap check and the top view
boxes = []  # 3D boxes: (x0, y0, w, h, z0, z1, colour)


def add_part(name, x, y, w, h, colour, label, kind, z=10.0, pins=None, label_xy=None, size=7.0):
    parts.append(dict(name=name, x=x, y=y, w=w, h=h, colour=colour, label=label, kind=kind,
                      pins=pins or [], label_xy=label_xy, size=size))
    boxes.append((x, y, w, h, 0.0, z, colour))


def header(name, label, x, y, n, vertical=False, kind="cable", colour=C_CABLE, size=6.0, z=8.5,
           label_xy=None):
    """n-pin 2.54 mm header. (x, y) is the centre of pin 1."""
    pins = [(x, y + i * PITCH) if vertical else (x + i * PITCH, y) for i in range(n)]
    bx, by = x - PITCH / 2, y - PITCH / 2
    bw, bh = (PITCH, n * PITCH) if vertical else (n * PITCH, PITCH)
    add_part(name, bx, by, bw, bh, colour, label, kind, z=z, pins=pins, label_xy=label_xy, size=size)


def terminal(name, label, x, y, poles, vertical, colour, side):
    """Screw terminal block. (x, y) is the lower-left corner. side = edge the wires enter from."""
    bw, bh = (TERM_DEPTH, poles * TERM_PITCH) if vertical else (poles * TERM_PITCH, TERM_DEPTH)
    pins = []
    for i in range(poles):
        pins.append((x + TERM_DEPTH / 2, y + TERM_PITCH * (i + 0.5)) if vertical
                    else (x + TERM_PITCH * (i + 0.5), y + TERM_DEPTH / 2))
    add_part(name, x, y, bw, bh, colour, label, "terminal", z=10.0, pins=pins, size=5.6)
    parts[-1]["side"] = side


def cap(name, label, cx, cy, r, z):
    add_part(name, cx - r, cy - r, 2 * r, 2 * r, "#555555", label, "cap", z=z, size=5.0)


# ---------------------------------------------------------------- ESP32-S3 DevKit (dual USB-C)
ESP_X, ESP_Y, ESP_L, ESP_W = 26.0, 66.0, 69.6, 25.4
ROW_GAP = 22.86
esp_rows_y = (ESP_Y + (ESP_W - ROW_GAP) / 2, ESP_Y + (ESP_W + ROW_GAP) / 2)
esp_pin1_x = 31.0
esp_pins = [(esp_pin1_x + i * PITCH, ry) for ry in esp_rows_y for i in range(22)]
parts.append(dict(name="ESP32", x=ESP_X, y=ESP_Y, w=ESP_L, h=ESP_W, colour=C_ESP, kind="esp",
                  label="ESP32-S3 DevKit (dual USB-C)", pins=esp_pins, label_xy=None, size=8.0))
for ry in esp_rows_y:  # the two 1x22 sockets under the board
    boxes.append((esp_pin1_x - PITCH / 2, ry - PITCH / 2, 22 * PITCH, PITCH, 0.0, 8.5, C_SOCKET))
boxes.append((ESP_X, ESP_Y, ESP_L, ESP_W, 8.5, 10.1, C_ESP))          # PCB of the dev board
boxes.append((ESP_X, ESP_Y, 18.0, ESP_W, 10.1, 13.3, "#b9bec7"))      # WROOM module + antenna end
for cy in (69.5, 80.5):                                              # two USB-C sockets
    boxes.append((ESP_X + ESP_L - 9.0, cy, 8.9, 7.35, 10.1, 13.4, "#9aa0aa"))
ANT = (ESP_X, ESP_Y, 18.0, ESP_W)

# ---------------------------------------------------------------- motor drivers (2x DRV8833)
DRV_W, DRV_H = 21.0, 18.0
for nm, x0 in (("DRV A", 30.0), ("DRV B", 56.0)):
    y0 = 28.0
    pins = [(x0 + 4.0 + i * PITCH, y0 + 1.5) for i in range(5)] + \
           [(x0 + 4.0 + i * PITCH, y0 + DRV_H - 1.5) for i in range(5)]
    parts.append(dict(name=nm, x=x0, y=y0, w=DRV_W, h=DRV_H, colour=C_DRV, kind="drv",
                      label=nm + "\nDRV8833", pins=pins, label_xy=None, size=7.5))
    for py in (y0 + 1.5, y0 + DRV_H - 1.5):
        boxes.append((x0 + 4.0 - PITCH / 2, py - PITCH / 2, 5 * PITCH, PITCH, 0.0, 8.5, C_SOCKET))
    boxes.append((x0, y0, DRV_W, DRV_H, 8.5, 10.1, C_DRV))
    boxes.append((x0 + 7, y0 + 5, 7, 8, 10.1, 11.4, "#222222"))

# ---------------------------------------------------------------- gyro GY-521
GX, GY, GW, GH = 8.0, 48.0, 21.2, 16.4
gyro_pins = [(GX + 1.4 + i * PITCH, GY + GH - 1.5) for i in range(8)]
parts.append(dict(name="GY-521", x=GX, y=GY, w=GW, h=GH, colour=C_GYRO, kind="gyro",
                  label="GY-521\ngyro", pins=gyro_pins, label_xy=None, size=7.0))
boxes.append((GX + 1.4 - PITCH / 2, GY + GH - 1.5 - PITCH / 2, 8 * PITCH, PITCH, 0.0, 8.5, C_SOCKET))
boxes.append((GX, GY, GW, GH, 8.5, 10.1, C_GYRO))
boxes.append((GX + 8, GY + 4, 4, 4, 10.1, 11.0, "#222222"))

# ---------------------------------------------------------------- cable headers (modules on wires)
header("SCREEN L", "SCREEN L\n1x7", 8.0, 72.0, 7, vertical=True, size=5.8, label_xy=(8.0, 90.5))
header("SCREEN R", "SCREEN R\n1x7", 14.5, 72.0, 7, vertical=True, size=5.8, label_xy=(15.0, 90.5))
strip1 = 61.0
header("RELAY A", "RELAY A\n1x4", 32.5, strip1, 4, label_xy=(36.3, strip1 - 3.3))
header("RELAY B", "RELAY B\n1x4", 44.56, strip1, 4, label_xy=(48.4, strip1 - 3.3))
header("SONAR", "SONAR\n1x4", 56.62, strip1, 4, label_xy=(60.4, strip1 - 3.3))
header("UART", "UART\n1x3", 68.68, strip1, 3, label_xy=(71.2, strip1 - 3.3))
header("I2C 1", "I2C 1\nservo board", 78.2, strip1, 4, label_xy=(82.0, strip1 - 3.3))
strip2 = 53.0
header("I2C 2", "I2C 2\nsensor", 32.5, strip2, 4, label_xy=(36.3, strip2 - 3.3))
header("I2C 3", "I2C 3\nsensor", 44.56, strip2, 4, label_xy=(48.4, strip2 - 3.3))
header("SPARE IO", "SPARE IO\n1x6", 56.62, strip2, 6, label_xy=(63.3, strip2 - 3.3))

# ---------------------------------------------------------------- screw terminals
# left edge, wire entry facing left
for i, (nm, lb) in enumerate((("QUIET IN", "QUIET 5V\nIN"), ("NOISY IN", "NOISY 5V\nIN"),
                              ("SERVO PWR", "SERVO V+\nOUT"))):
    terminal(nm, lb, 1.5, 12.0 + i * 2 * TERM_PITCH, 2, True, C_PWR, "left")
# bottom edge, wire entry facing down
bx = 14.0
for nm, lb in (("BUCK IN", "TO 3V3\nBUCK"), ("3V3 IN", "FROM 3V3\nBUCK"), ("BOOST IN", "TO 7V\nBOOST"),
               ("7V IN", "FROM 7V\nBOOST"), ("FAN", "FAN")):
    terminal(nm, lb, bx, 1.5, 2, False, C_PWR, "bottom")
    bx += 2 * TERM_PITCH
terminal("PI GND", "PI\nGND", bx, 1.5, 1, False, C_PWR, "bottom")
# right edge, wire entry facing right: four motors
for i in range(4):
    terminal("MOTOR %d" % (i + 1), "M%d" % (i + 1), 90.0, 22.0 + i * 2 * TERM_PITCH, 2, True, C_MOTOR, "right")

# ---------------------------------------------------------------- capacitors (rail decoupling)
cap("C 3V3 bulk", "100uF", 76.0, 6.0, 3.15, 11.0)
cap("C 3V3 hf", "100nF", 83.0, 6.0, 2.0, 4.0)
cap("C 7V bulk", "100uF", 76.0, 14.0, 3.15, 11.0)
cap("C 7V hf", "100nF", 83.0, 14.0, 2.0, 4.0)


# ================================================================= checks
def rect_overlap(a, b, margin=0.0):
    return not (a["x"] + a["w"] + margin <= b["x"] or b["x"] + b["w"] + margin <= a["x"] or
                a["y"] + a["h"] + margin <= b["y"] or b["y"] + b["h"] + margin <= a["y"])


def circle_hits_rect(cx, cy, r, p):
    nx = min(max(cx, p["x"]), p["x"] + p["w"])
    ny = min(max(cy, p["y"]), p["y"] + p["h"])
    return math.hypot(cx - nx, cy - ny) < r


def run_checks():
    problems = []
    for p in parts:
        if p["x"] < 0.5 or p["y"] < 0.5 or p["x"] + p["w"] > W - 0.5 or p["y"] + p["h"] > H - 0.5:
            problems.append("outside board margin: " + p["name"])
        for cx, cy in HOLES:
            if circle_hits_rect(cx, cy, HOLE_KEEPOUT, p):
                problems.append("touches mounting hole at (%g,%g): %s" % (cx, cy, p["name"]))
    for i, a in enumerate(parts):
        for b in parts[i + 1:]:
            both_terminals = a["kind"] == "terminal" and b["kind"] == "terminal"
            if rect_overlap(a, b, margin=0.0 if both_terminals else 1.5):
                problems.append("closer than %s mm: %s / %s" % ("0" if both_terminals else "1.5", a["name"], b["name"]))
    return problems


# ================================================================= top view
def top_view(path):
    fig, ax = plt.subplots(figsize=(15, 13.2), dpi=100)
    ax.set_xlim(-14, 114)
    ax.set_ylim(-16, 108)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), W, H, fc=BOARD, ec="#0b2a14", lw=2.5, zorder=1))
    for cx, cy in HOLES:
        ax.add_patch(Circle((cx, cy), HOLE_KEEPOUT, fc="none", ec="#cde9d4", lw=0.7, ls=":", zorder=2))
        ax.add_patch(Circle((cx, cy), 1.6, fc="#f3f1e9", ec="#222", lw=0.8, zorder=3))
    # antenna keep-out
    ax.add_patch(Rectangle(ANT[:2], ANT[2], ANT[3], fc="none", ec="#ffd54f", lw=1.0, hatch="////", zorder=3))
    for p in parts:
        ax.add_patch(Rectangle((p["x"], p["y"]), p["w"], p["h"], fc=p["colour"], ec="#111", lw=0.9,
                               alpha=0.55 if p["kind"] in ("esp", "drv", "gyro") else 0.95, zorder=4))
        for (px, py) in p["pins"]:
            if p["kind"] == "terminal":
                ax.add_patch(Circle((px, py), 1.2, fc="#d8d8d8", ec="#111", lw=0.5, zorder=6))
            elif p["kind"] != "cap":
                ax.add_patch(Rectangle((px - 0.5, py - 0.5), 1.0, 1.0, fc="#f2c94c", ec="#222", lw=0.3, zorder=6))
        if p["kind"] == "esp":
            for cy in (69.5, 80.5):
                ax.add_patch(Rectangle((p["x"] + p["w"] - 9.0, cy), 8.9, 7.35, fc="#9aa0aa", ec="#111",
                                       lw=0.8, zorder=5))
            ax.text(p["x"] + p["w"] - 4.6, 76.0, "USB-C x2", ha="center", va="center", rotation=90,
                    fontsize=6.5, zorder=8)
            ax.text(ESP_X + 9, ESP_Y + ESP_W / 2, "ANTENNA END\nno copper here", ha="center", va="center",
                    fontsize=6.8, color="#5a4300", zorder=8, fontweight="bold")
            ax.text(p["x"] + 37, ESP_Y + ESP_W / 2, "ESP32-S3 DevKit (dual USB-C)\n2 x 22-pin sockets",
                    ha="center", va="center", fontsize=9, fontweight="bold", color="#06223f", zorder=8)
            continue
        cx, cy = p["x"] + p["w"] / 2, p["y"] + p["h"] / 2
        if p["label_xy"]:
            cx, cy = p["label_xy"]
        if p["kind"] == "terminal":
            lx = p["x"] + p["w"] / 2
            ly = p["y"] + p["h"] / 2
            if p["side"] == "left":
                ax.text(p["x"] + p["w"] + 1.2, ly, p["label"], ha="left", va="center", fontsize=p["size"], zorder=8,
                        color="white", fontweight="bold")
            elif p["side"] == "right":
                ax.text(p["x"] - 1.2, ly, p["label"], ha="right", va="center", fontsize=p["size"], zorder=8,
                        color="white", fontweight="bold")
            else:                                     # bottom edge
                ax.text(lx, p["y"] + p["h"] + 1.4, p["label"], ha="center", va="bottom", fontsize=p["size"],
                        zorder=8, color="white", fontweight="bold")
            continue
        col = "white" if p["kind"] in ("cable", "cap") else "#111"
        ax.text(cx, cy, p["label"], ha="center", va="center", fontsize=p["size"], zorder=8, color=col,
                fontweight="bold" if p["kind"] in ("drv", "gyro") else "normal")
    # dimensions
    ax.annotate("", xy=(0, -6), xytext=(W, -6), arrowprops=dict(arrowstyle="<->", lw=1.2))
    ax.text(W / 2, -9.2, "100 mm", ha="center", fontsize=10)
    ax.annotate("", xy=(-6, 0), xytext=(-6, H), arrowprops=dict(arrowstyle="<->", lw=1.2))
    ax.text(-8.2, H / 2, "100 mm", ha="center", va="center", rotation=90, fontsize=10)
    ax.text(0, 104.5, "DRAFT v0  -  robot carrier board, 100 x 100 mm, to scale (top view)",
            fontsize=14, fontweight="bold", ha="left")
    ax.text(0, 101.0, "Placement only: nothing routed yet. Module sizes are the common ones and must be checked "
            "against your real parts.", fontsize=8.5, ha="left", color="#444")
    # zone notes
    ax.text(103, 91, "USB cables\nexit this side", fontsize=7.5, ha="left", va="center", color="#333")
    ax.text(103, 44, "MOTOR terminals\nM1, M2 = DRV A\nM3, M4 = DRV B", fontsize=7.5, ha="left", va="center", color="#333")
    ax.text(50, -12.6, "POWER terminals along the bottom and left edges  |  dark squares = headers for cables to "
            "modules (screens, relays, sonar, servo board, sensors)", fontsize=7.8, ha="center", color="#333")
    fig.savefig(path, bbox_inches="tight", facecolor="#f8f6f0")
    plt.close(fig)


# ================================================================= isometric view
def iso_view(path):
    c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))

    def proj(x, y, z):
        return ((x - y) * c30, (x + y) * s30 + z)

    def shade(hexcol, f):
        hexcol = hexcol.lstrip("#")
        r, g, b = (int(hexcol[i:i + 2], 16) for i in (0, 2, 4))
        return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))

    fig, ax = plt.subplots(figsize=(15, 11), dpi=100)
    ax.set_aspect("equal")
    ax.axis("off")
    slab = (0.0, 0.0, W, H, -1.6, 0.0, BOARD)
    # slab first, then everything else far-to-near
    rest = sorted(boxes, key=lambda b: (-(b[0] + b[2] / 2 + b[1] + b[3] / 2), b[4]))
    for (x, y, w, h, z0, z1, col) in [slab] + rest:
        x1, y1 = x + w, y + h
        top = [proj(x, y, z1), proj(x1, y, z1), proj(x1, y1, z1), proj(x, y1, z1)]
        fy = [proj(x, y, z0), proj(x1, y, z0), proj(x1, y, z1), proj(x, y, z1)]
        fx = [proj(x, y, z0), proj(x, y1, z0), proj(x, y1, z1), proj(x, y, z1)]
        ax.add_patch(Polygon(fx, fc=shade(col, 0.62), ec="#111", lw=0.35, zorder=2))
        ax.add_patch(Polygon(fy, fc=shade(col, 0.8), ec="#111", lw=0.35, zorder=2))
        ax.add_patch(Polygon(top, fc=col, ec="#111", lw=0.35, zorder=2))
    halo = [pe.withStroke(linewidth=2.4, foreground="white")]
    tags = [("ESP32-S3", 62, 80, 14.5), ("DRV A", 40.5, 37, 12.5), ("DRV B", 66.5, 37, 12.5),
            ("GY-521", 18.5, 54, 12.0), ("power\nterminals", 40, 5, 11.0),
            ("motor\nterminals", 94, 44, 11.5), ("screen / relay / sonar /\nI2C headers", 53, 57, 9.5),
            ("screen\nheaders", 11, 80, 9.5)]
    for txt, x, y, z in tags:
        u, v = proj(x, y, z)
        ax.text(u, v + 1.0, txt, ha="center", va="bottom", fontsize=9, fontweight="bold", path_effects=halo, zorder=9)
    us = [proj(x, y, 0)[0] for x in (0, W) for y in (0, H)]
    vs = [proj(x, y, z)[1] for x in (0, W) for y in (0, H) for z in (-1.6, 14)]
    ax.set_xlim(min(us) - 4, max(us) + 4)
    ax.set_ylim(min(vs) - 4, max(vs) + 14)
    ax.text(min(us), max(vs) + 9, "DRAFT v0  -  3D-style view (heights are real, mm-accurate)", fontsize=14,
            fontweight="bold", ha="left")
    fig.savefig(path, bbox_inches="tight", facecolor="#f8f6f0")
    plt.close(fig)


if __name__ == "__main__":
    problems = run_checks()
    print("Parts placed:", len(parts))
    print("Placement check:", "OK, no overlaps, nothing outside the board or on a mounting hole"
          if not problems else "")
    for pr in problems:
        print("  PROBLEM:", pr)
    top_view(os.path.join(OUT, "floorplan_v0_top.png"))
    iso_view(os.path.join(OUT, "floorplan_v0_3d.png"))
    sys.exit(1 if problems else 0)
