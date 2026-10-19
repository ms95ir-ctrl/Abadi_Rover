#!/usr/bin/env python3
"""Choose which ESP32 pin carries which signal so every signal sits near what it connects to.

Reads a pcbnew dump (dump_board.py JSON) of a board built with the default pin map and writes pinmap.json.
Needs numpy + scipy. Only pins that are safe for general use are offered (no strapping, USB, UART0 or PSRAM pins).
"""
import json
import sys

import numpy as np
from scipy.optimize import linear_sum_assignment

dump, out = sys.argv[1], sys.argv[2]
d = json.load(open(dump))
SIGNALS = ["IN1A", "IN2A", "IN3A", "IN4A", "IN1B", "IN2B", "IN3B", "IN4B", "SDA", "SCL", "LCD_RST", "MOSI", "SCK",
           "CS_L", "CS_R", "LCD_DC", "RLY1", "RLY2", "RLY3", "TRIG", "ECHO1_3V", "ECHO2_3V"]
J1_PINS = ["3V3", "3V3", "RST", 4, 5, 6, 7, 15, 16, 17, 18, 8, 3, 46, 9, 10, 11, 12, 13, 14, "5V", "G"]
J3_PINS = ["G", 43, 44, 1, 2, 42, 41, 40, 39, 38, 37, 36, 35, 0, 45, 48, 47, 21, 20, 19, "G", "G"]
# GPIOs safe for general use: not USB (19/20), UART0 (43/44), boot (0), PSRAM (35-37), the RGB LED (38/48) or the
# boot-strapping pins (3, 45, 46). Anything left over is brought out on the spare header.
SAFE = {4, 5, 6, 7, 15, 16, 17, 18, 8, 9, 10, 11, 12, 13, 14, 1, 2, 42, 41, 40, 39, 47, 21}

pin_xy = {}
for ref, pins in (("J1", J1_PINS), ("J3", J3_PINS)):
    pads = sorted((p for p in d["pads"] if p["ref"] == ref), key=lambda p: int(p["n"]))
    for g, p in zip(pins, pads):
        if g in SAFE:
            pin_xy[g] = p["p"]
gpios = sorted(pin_xy)

target = {}
for s in SIGNALS:
    pts = [p["p"] for p in d["pads"] if p["net"] == s and p["ref"] not in ("J1", "J3")]
    # signals that share an ESP pin with something else (e.g. SDA: PCA, gyro, I2C header): use the centroid
    target[s] = np.mean(pts, axis=0)

cost = np.zeros((len(SIGNALS), len(gpios)))
for i, s in enumerate(SIGNALS):
    for j, g in enumerate(gpios):
        cost[i, j] = abs(pin_xy[g][0] - target[s][0]) + abs(pin_xy[g][1] - target[s][1])
r, c = linear_sum_assignment(cost)
mapping = {int(gpios[j]): SIGNALS[i] for i, j in zip(r, c)}
json.dump({str(k): v for k, v in sorted(mapping.items())}, open(out, "w"), indent=1)
print("total Manhattan length: %.0f mm; free safe pins: %s" % (cost[r, c].sum(), sorted(set(gpios) - set(mapping))))
for g in sorted(mapping):
    print("GPIO%-2d -> %s" % (g, mapping[g]))
