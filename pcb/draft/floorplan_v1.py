#!/usr/bin/env python3
"""Draft v1 floor plan: reusable robot carrier board, 100 x 100 mm.

Placement only. Nothing is routed and nothing here is for fabrication. Module sizes are the
common sizes for each part and still have to be checked against the real modules.
Run:  python3 floorplan_v0.py   (needs matplotlib)  ->  floorplan_v1_top.png, floorplan_v1_3d.png
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
C_PCA = "#6cc3a0"
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


def terminal(name, label, x, y, poles, vertical, colour, side, pitch=TERM_PITCH, depth=TERM_DEPTH):
    """Screw terminal block. (x, y) is the lower-left corner. side = edge the wires enter from."""
    bw, bh = (depth, poles * pitch) if vertical else (poles * pitch, depth)
    pins = []
    for i in range(poles):
        pins.append((x + depth / 2, y + pitch * (i + 0.5)) if vertical
                    else (x + pitch * (i + 0.5), y + depth / 2))
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
for ry in esp_rows_y:
    boxes.append((esp_pin1_x - PITCH / 2, ry - PITCH / 2, 22 * PITCH, PITCH, 0.0, 8.5, C_SOCKET))
boxes.append((ESP_X, ESP_Y, ESP_L, ESP_W, 8.5, 10.1, C_ESP))
boxes.append((ESP_X, ESP_Y, 18.0, ESP_W, 10.1, 13.3, "#b9bec7"))
for cy in (69.5, 80.5):
    boxes.append((ESP_X + ESP_L - 9.0, cy, 8.9, 7.35, 10.1, 13.4, "#9aa0aa"))
ANT = (ESP_X, ESP_Y, 18.0, ESP_W)

# ---------------------------------------------------------------- PCA9685 servo board, on the board
PX, PY, PL, PW = 11.0, 2.0, 62.5, 25.4
pca_ctrl = [(PX + 12.0 + i * PITCH, PY + PW - 1.5) for i in range(6)]
pca_servo = [(PX + 8.0 + c * PITCH, PY + 1.5 + r * PITCH) for c in range(16) for r in range(3)]
parts.append(dict(name="PCA9685", x=PX, y=PY, w=PL, h=PW, colour=C_PCA, kind="pca",
                  label="PCA9685 16-channel servo board\n(1x6 socket + 2 standoffs; servo plugs face the bottom edge)",
                  pins=pca_ctrl + pca_servo, label_xy=(PX + PL / 2, PY + 15.5), size=7.5))
boxes.append((PX + 12.0 - PITCH / 2, PY + PW - 1.5 - PITCH / 2, 6 * PITCH, PITCH, 0.0, 8.5, C_SOCKET))
boxes.append((PX, PY, PL, PW, 8.5, 10.1, C_PCA))
boxes.append((PX + 8.0 - 1.27, PY + 1.5 - 1.27, 16 * PITCH, 3 * PITCH, 10.1, 18.6, "#2b2b2b"))
boxes.append((PX, PY + 6.0, 8.0, 13.0, 10.1, 20.0, "#2e8b57"))  # its own power terminal

# ---------------------------------------------------------------- motor drivers (2x DRV8833)
DRV_W, DRV_H = 21.0, 18.0
for nm, x0 in (("DRV A", 34.0), ("DRV B", 60.0)):
    y0 = 29.5
    pins = [(x0 + 4.0 + i * PITCH, y0 + 1.5) for i in range(5)] + \
           [(x0 + 4.0 + i * PITCH, y0 + DRV_H - 1.5) for i in range(5)]
    parts.append(dict(name=nm, x=x0, y=y0, w=DRV_W, h=DRV_H, colour=C_DRV, kind="drv",
                      label=nm + "\nDRV8833", pins=pins, label_xy=None, size=7.5))
    for py in (y0 + 1.5, y0 + DRV_H - 1.5):
        boxes.append((x0 + 4.0 - PITCH / 2, py - PITCH / 2, 5 * PITCH, PITCH, 0.0, 8.5, C_SOCKET))
    boxes.append((x0, y0, DRV_W, DRV_H, 8.5, 10.1, C_DRV))
    boxes.append((x0 + 7, y0 + 5, 7, 8, 10.1, 11.4, "#222222"))

# ---------------------------------------------------------------- gyro GY-521
GX, GY, GW, GH = 11.0, 48.0, 21.2, 16.4
gyro_pins = [(GX + 1.4 + i * PITCH, GY + GH - 1.5) for i in range(8)]
parts.append(dict(name="GY-521", x=GX, y=GY, w=GW, h=GH, colour=C_GYRO, kind="gyro",
                  label="GY-521\ngyro", pins=gyro_pins, label_xy=None, size=7.0))
boxes.append((GX + 1.4 - PITCH / 2, GY + GH - 1.5 - PITCH / 2, 8 * PITCH, PITCH, 0.0, 8.5, C_SOCKET))
boxes.append((GX, GY, GW, GH, 8.5, 10.1, C_GYRO))
boxes.append((GX + 8, GY + 4, 4, 4, 10.1, 11.0, "#222222"))

# ---------------------------------------------------------------- cable headers
header("SCREEN L", "SCREEN L\n1x7", 8.0, 72.0, 7, vertical=True, size=5.8, label_xy=(8.0, 90.5))
header("SCREEN R", "SCREEN R\n1x7", 14.5, 72.0, 7, vertical=True, size=5.8, label_xy=(14.5, 90.5))
header("SPARE IO", "SPARE\nIO 1x6", 21.0, 72.0, 6, vertical=True, size=5.8, label_xy=(21.0, 88.5))
S1, S2, X0 = 61.0, 54.5, 35.0
def strip(y, items):
    x = X0
    for nm, lb, n in items:
        header(nm, lb, x, y, n, label_xy=(x + (n - 1) * PITCH / 2, y - 3.4))
        x += n * PITCH + 1.9
strip(S1, [("RELAY 1", "RELAY 1\n1x3", 3), ("RELAY 2", "RELAY 2\n1x3", 3), ("RELAY 3", "RELAY 3\n1x3", 3),
           ("SONAR 1", "SONAR 1\n1x4", 4), ("SONAR 2", "SONAR 2\n1x4", 4)])
strip(S2, [("I2C SENSOR", "I2C sensor\n1x4", 4), ("UART", "UART\n1x3", 3),
           ("TOUCH 1", "TOUCH 1\n1x3", 3), ("TOUCH 2", "TOUCH 2\n1x3", 3)])

# ---------------------------------------------------------------- screw terminals
# left edge (5.08 pitch, wires enter from the left): battery in, then three feeds out to the bucks.
# The servo buck's output goes straight to the PCA9685's own screw terminal, right next to it.
for i, (nm, lb) in enumerate((("BATT IN", "BATT IN\n2S pack"), ("TO BUCK 1", "TO BUCK 1\nservo 5V"),
                              ("TO BUCK 2", "TO BUCK 2\nclean 5V"), ("TO BUCK 3", "TO BUCK 3\n3.3V"))):
    terminal(nm, lb, 1.5, 10.0 + i * 2 * TERM_PITCH, 2, True, C_PWR, "left")
# right edge (3.5 pitch, wires enter from the right): clean 5V in, 3.3V in, then four motors
y = 12.0
for nm, lb in (("5V IN", "CLEAN 5V\nIN"), ("3V3 IN", "3.3V IN")):
    terminal(nm, lb, 91.0, y, 2, True, C_PWR, "right", pitch=3.5, depth=7.0)
    y += 7.0
for i in range(4):
    terminal("MOTOR %d" % (i + 1), "M%d" % (i + 1), 91.0, y, 2, True, C_MOTOR, "right", pitch=3.5, depth=7.0)
    y += 7.0

# ---------------------------------------------------------------- capacitors and the ESP32 5V diode
cap("C 3V3 bulk", "100uF\n3.3V", 79.5, 6.0, 3.15, 11.0)
cap("C 3V3 hf", "100nF", 87.0, 4.0, 2.0, 4.0)
cap("C pack bulk", "470uF\npack", 79.5, 15.0, 4.0, 13.0)
cap("C pack hf", "100nF", 87.0, 9.5, 2.0, 4.0)
add_part("D ESP 5V", 60.0, 93.0, 6.0, 2.6, "#444444", "Schottky\nESP 5V pin", "diode", z=4.0, size=5.0)


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
                               alpha=0.55 if p["kind"] in ("esp", "drv", "gyro", "pca") else 0.95, zorder=4))
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
    ax.text(0, 104.5, "DRAFT v1  -  robot carrier board, 100 x 100 mm, to scale (top view)",
            fontsize=14, fontweight="bold", ha="left")
    ax.text(0, 101.0, "Placement only: nothing routed yet. Module sizes are the common ones and must be checked "
            "against your real parts.", fontsize=8.5, ha="left", color="#444")
    # zone notes
    ax.text(103, 91, "USB cables\nexit this side", fontsize=7.5, ha="left", va="center", color="#333")
    ax.text(103, 44, "M1, M2 = DRV A\nM3, M4 = DRV B\n(red = buck returns)", fontsize=7.5, ha="left", va="center", color="#333")
    ax.text(50, -12.6, "Left edge: battery in + feeds to the 3 bucks  |  right edge: buck returns + motors  |  dark squares = headers for cables to "
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
            ("GY-521", 18.5, 54, 12.0), ("battery / buck\nterminals", 4, 30, 11.5), ("PCA9685\nservo board", 42, 14, 20.5),
            ("motor\nterminals", 94, 44, 11.5), ("screen / relay / sonar /\nI2C headers", 53, 57, 9.5),
            ("screen\nheaders", 11, 80, 9.5)]
    for txt, x, y, z in tags:
        u, v = proj(x, y, z)
        ax.text(u, v + 1.0, txt, ha="center", va="bottom", fontsize=9, fontweight="bold", path_effects=halo, zorder=9)
    us = [proj(x, y, 0)[0] for x in (0, W) for y in (0, H)]
    vs = [proj(x, y, z)[1] for x in (0, W) for y in (0, H) for z in (-1.6, 14)]
    ax.set_xlim(min(us) - 4, max(us) + 4)
    ax.set_ylim(min(vs) - 4, max(vs) + 14)
    ax.text(min(us), max(vs) + 9, "DRAFT v1  -  3D-style view (heights are real, mm-accurate)", fontsize=14,
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
    top_view(os.path.join(OUT, "floorplan_v1_top.png"))
    iso_view(os.path.join(OUT, "floorplan_v1_3d.png"))
    sys.exit(1 if problems else 0)
