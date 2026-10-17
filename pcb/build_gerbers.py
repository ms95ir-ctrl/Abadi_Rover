#!/usr/bin/env python3
"""Build a 2-layer Gerber zip of the Abadi Rover body board for a PCB quote."""

import math
import os
import zipfile
from collections import defaultdict

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_NAME = os.path.join(OUT_DIR, "abadi-rover-body.zip")

# Manufacturing numbers, in millimetres.
HEADER_DRILL = 1.0
HEADER_PAD = 1.8
VIA_DRILL = 0.45
VIA_PAD = 0.90
VIA_PITCH = 1.15
TRACE = 0.25
POWER_TRACE = 0.80
CLEARANCE = 0.20
LANE_GAP = 1.20
POWER_LANE_GAP = 1.70
PIN_PITCH = 2.54
LABEL_GAP = 3.0
EDGE_MARGIN = 5.0

POWER_NETS = {"QUIET5", "NOISY5", "RAILC", "VM7", "ESP3V3"}

# 5x7 stroke font. Coordinates are 0..4 across, 0..6 up.
FONT = {
    "A": [(0, 0, 0, 6), (0, 6, 4, 6), (4, 6, 4, 0), (0, 3, 4, 3)],
    "B": [(0, 0, 0, 6), (0, 6, 3, 6), (3, 6, 4, 5), (4, 5, 4, 4), (4, 4, 3, 3), (0, 3, 3, 3), (3, 3, 4, 2), (4, 2, 4, 1), (4, 1, 3, 0), (3, 0, 0, 0)],
    "C": [(4, 6, 0, 6), (0, 6, 0, 0), (0, 0, 4, 0)],
    "D": [(0, 0, 0, 6), (0, 6, 3, 6), (3, 6, 4, 4), (4, 4, 4, 2), (4, 2, 3, 0), (3, 0, 0, 0)],
    "E": [(4, 6, 0, 6), (0, 6, 0, 0), (0, 0, 4, 0), (0, 3, 3, 3)],
    "F": [(0, 0, 0, 6), (0, 6, 4, 6), (0, 3, 3, 3)],
    "G": [(4, 6, 0, 6), (0, 6, 0, 0), (0, 0, 4, 0), (4, 0, 4, 3), (4, 3, 2, 3)],
    "H": [(0, 0, 0, 6), (4, 0, 4, 6), (0, 3, 4, 3)],
    "I": [(1, 0, 3, 0), (2, 0, 2, 6), (1, 6, 3, 6)],
    "J": [(0, 1, 0, 0), (0, 0, 4, 0), (4, 0, 4, 6), (4, 6, 2, 6)],
    "K": [(0, 0, 0, 6), (4, 6, 0, 3), (0, 3, 4, 0)],
    "L": [(0, 6, 0, 0), (0, 0, 4, 0)],
    "M": [(0, 0, 0, 6), (0, 6, 2, 3), (2, 3, 4, 6), (4, 6, 4, 0)],
    "N": [(0, 0, 0, 6), (0, 6, 4, 0), (4, 0, 4, 6)],
    "O": [(0, 0, 0, 6), (0, 6, 4, 6), (4, 6, 4, 0), (4, 0, 0, 0)],
    "P": [(0, 0, 0, 6), (0, 6, 4, 6), (4, 6, 4, 3), (4, 3, 0, 3)],
    "Q": [(0, 1, 0, 6), (0, 6, 4, 6), (4, 6, 4, 1), (4, 1, 0, 1), (2, 2, 4, 0)],
    "R": [(0, 0, 0, 6), (0, 6, 4, 6), (4, 6, 4, 3), (4, 3, 0, 3), (2, 3, 4, 0)],
    "S": [(4, 6, 0, 6), (0, 6, 0, 3), (0, 3, 4, 3), (4, 3, 4, 0), (4, 0, 0, 0)],
    "T": [(0, 6, 4, 6), (2, 6, 2, 0)],
    "U": [(0, 6, 0, 0), (0, 0, 4, 0), (4, 0, 4, 6)],
    "V": [(0, 6, 2, 0), (2, 0, 4, 6)],
    "W": [(0, 6, 0, 0), (0, 0, 2, 3), (2, 3, 4, 0), (4, 0, 4, 6)],
    "X": [(0, 0, 4, 6), (0, 6, 4, 0)],
    "Y": [(0, 6, 2, 3), (4, 6, 2, 3), (2, 3, 2, 0)],
    "Z": [(0, 6, 4, 6), (4, 6, 0, 0), (0, 0, 4, 0)],
    "0": [(0, 0, 0, 6), (0, 6, 4, 6), (4, 6, 4, 0), (4, 0, 0, 0), (0, 0, 4, 6)],
    "1": [(1, 0, 3, 0), (2, 0, 2, 6), (2, 6, 1, 5)],
    "2": [(0, 6, 4, 6), (4, 6, 4, 3), (4, 3, 0, 0), (0, 0, 4, 0)],
    "3": [(0, 6, 4, 6), (4, 6, 4, 0), (4, 0, 0, 0), (0, 3, 4, 3)],
    "4": [(0, 6, 0, 3), (0, 3, 4, 3), (4, 6, 4, 0)],
    "5": [(4, 6, 0, 6), (0, 6, 0, 3), (0, 3, 4, 3), (4, 3, 4, 0), (4, 0, 0, 0)],
    "6": [(4, 6, 0, 6), (0, 6, 0, 0), (0, 0, 4, 0), (4, 0, 4, 3), (4, 3, 0, 3)],
    "7": [(0, 6, 4, 6), (4, 6, 1, 0)],
    "8": [(0, 0, 0, 6), (0, 6, 4, 6), (4, 6, 4, 0), (4, 0, 0, 0), (0, 3, 4, 3)],
    "9": [(0, 0, 4, 0), (4, 0, 4, 6), (4, 6, 0, 6), (0, 6, 0, 3), (0, 3, 4, 3)],
    "+": [(2, 1, 2, 5), (0, 3, 4, 3)],
    "-": [(0, 3, 4, 3)],
    ".": [(1.5, 0, 2.5, 0)],
    "/": [(0, 0, 4, 6)],
    " ": [],
}


def dist_point_seg(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    length2 = dx * dx + dy * dy
    if length2 == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / length2))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))


def seg_distance(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return min(
        dist_point_seg(ax1, ay1, bx1, by1, bx2, by2),
        dist_point_seg(ax2, ay2, bx1, by1, bx2, by2),
        dist_point_seg(bx1, by1, ax1, ay1, ax2, ay2),
        dist_point_seg(bx2, by2, ax1, ay1, ax2, ay2),
    )


class Board:
    def __init__(self):
        self.pads = []
        self.vias = []
        self.traces = []  # x1,y1,x2,y2,width,net,layer
        self.silk = []  # strokes and text records
        self.headers = []
        self.errors = []

    def add_pad(self, x, y, drill, dia, net, name, kind="header"):
        self.pads.append(
            {"x": x, "y": y, "drill": drill, "dia": dia, "net": net, "name": name, "kind": kind}
        )
        return self.pads[-1]

    def add_header(self, title, x, y0, pins):
        """pins: list of (name, net) from bottom to top. net None means GND."""
        placed = []
        for i, (name, net) in enumerate(pins):
            y = y0 + i * PIN_PITCH
            actual_net = "GND" if net is None else net
            pad = self.add_pad(x, y, HEADER_DRILL, HEADER_PAD, actual_net, name)
            placed.append(pad)
        self.headers.append({"title": title, "x": x, "pads": placed})
        return placed

    def add_pair(self, x, y, name_a, net_a, name_b, net_b, drill, dia, pitch=5.0):
        self.add_pad(x, y, drill, dia, net_a, name_a, "screw")
        self.add_pad(x + pitch, y, drill, dia, net_b, name_b, "screw")


def build():
    b = Board()
    y0 = 72.0
    x = 36.0

    def column(title, pins):
        nonlocal x
        # Leave room for the previous fanout; the first column uses the left margin.
        pads = b.add_header(title, x, y0, pins)
        fan_width = max(0, (len(pins) - 1) * VIA_PITCH)
        x = x + 3.2 + fan_width + LABEL_GAP
        return pads

    column(
        "ESP32-S3",
        [
            ("GND", None),
            ("GPIO4", "IN1A"),
            ("GPIO5", "IN2A"),
            ("GPIO6", "IN3A"),
            ("GPIO7", "IN4A"),
            ("GPIO15", "IN1B"),
            ("GPIO16", "IN2B"),
            ("GPIO17", "IN3B"),
            ("GPIO18", "IN4B"),
            ("GPIO8", "SDA"),
            ("GPIO9", "SCL"),
            ("GPIO1", "RLY1"),
            ("GPIO2", "RLY2"),
            ("GPIO38", "RLY3"),
            ("GPIO39", "RLY4"),
            ("GPIO13", "CSL"),
            ("GPIO14", "CSR"),
            ("GPIO21", "DC"),
            ("GPIO10", "RST"),
            ("GPIO11", "MOSI"),
            ("GPIO12", "SCK"),
            ("GPIO41", "TRIG"),
            ("GPIO42", "ECHO3"),
            ("GPIO40", "SPARE"),
            ("3V3", "ESP3V3"),
            ("GND", None),
        ],
    )
    column(
        "DRV8833 TRACKS",
        [
            ("IN1", "IN1A"),
            ("IN2", "IN2A"),
            ("IN3", "IN3A"),
            ("IN4", "IN4A"),
            ("VM", "VM7"),
            ("OUT1", "ML1"),
            ("OUT2", "ML2"),
            ("OUT3", "MR1"),
            ("OUT4", "MR2"),
            ("GND", None),
        ],
    )
    column(
        "DRV8833 SPARE",
        [
            ("IN1", "IN1B"),
            ("IN2", "IN2B"),
            ("IN3", "IN3B"),
            ("IN4", "IN4B"),
            ("VM", "VM7"),
            ("OUT1", "MS1"),
            ("OUT2", "MS2"),
            ("OUT3", "MS3"),
            ("OUT4", "MS4"),
            ("GND", None),
        ],
    )
    column(
        "PCA9685",
        [
            ("VCC", "ESP3V3"),
            ("SDA", "SDA"),
            ("SCL", "SCL"),
            ("V+", "NOISY5"),
            ("GND", None),
        ],
    )
    column(
        "GYRO",
        [
            ("VCC", "ESP3V3"),
            ("SDA", "SDA"),
            ("SCL", "SCL"),
            ("GND", None),
        ],
    )
    column(
        "RELAY A",
        [
            ("VCC", "RAILC"),
            ("IN1", "RLY1"),
            ("IN2", "RLY2"),
            ("COM", "RAILC"),
            ("NO1", "NO1"),
            ("NO2", "NO2"),
            ("GND", None),
        ],
    )
    column(
        "RELAY B",
        [
            ("VCC", "RAILC"),
            ("IN1", "RLY3"),
            ("IN2", "RLY4"),
            ("COM", "RAILC"),
            ("NO1", "NO3"),
            ("NO2", "NO4"),
            ("GND", None),
        ],
    )
    column(
        "SCREEN L",
        [
            ("VCC", "RAILC"),
            ("GND", None),
            ("CS", "CSL"),
            ("RST", "RST"),
            ("DC", "DC"),
            ("SDA", "MOSI"),
            ("SCL", "SCK"),
        ],
    )
    column(
        "SCREEN R",
        [
            ("VCC", "RAILC"),
            ("GND", None),
            ("CS", "CSR"),
            ("RST", "RST"),
            ("DC", "DC"),
            ("SDA", "MOSI"),
            ("SCL", "SCK"),
        ],
    )
    column(
        "SONAR",
        [
            ("VCC", "QUIET5"),
            ("GND", None),
            ("TRIG", "TRIG"),
            ("ECHO", "ECHO5"),
        ],
    )

    # One column of small parts. The fanout runs into empty space on the right.
    rx = x + 6
    ry = y0

    def vpart(name_a, net_a, name_b, net_b, yy, drill, dia):
        b.add_pad(rx, yy, drill, dia, net_a, name_a, "part")
        b.add_pad(rx, yy + 3.6, drill, dia, net_b, name_b, "part")

    vpart("10R-1", "NO1", "LAMP1", "LAMP1", ry, 0.8, 1.6)
    vpart("10R-2", "NO2", "LAMP2", "LAMP2", ry + 8, 0.8, 1.6)
    vpart("10R-3", "NO3", "LAMP3", "LAMP3", ry + 16, 0.8, 1.6)
    vpart("10R-4", "NO4", "LAMP4", "LAMP4", ry + 24, 0.8, 1.6)
    vpart("1K", "ECHO5", "ECHO3", "ECHO3", ry + 34, 0.8, 1.6)
    vpart("2K", "ECHO3", "GND", "GND", ry + 42, 0.8, 1.6)
    vpart("100U-3V", "RAILC", "GND", "GND", ry + 52, 0.9, 1.9)
    vpart("100N-3V", "RAILC", "GND", "GND", ry + 60, 0.8, 1.5)
    vpart("100U-7V", "VM7", "GND", "GND", ry + 68, 0.9, 1.9)
    vpart("100N-7V", "VM7", "GND", "GND", ry + 76, 0.8, 1.5)

    board_w = rx + 3.4 + 20 * VIA_PITCH + EDGE_MARGIN

    # Screw row along the bottom.
    sx = 40.0
    pitch = 7.0
    gap = 4.0
    row_y = {"power": 56.0, "motor": 42.0}

    def screw_pair(row, label_net_pos, label_net_neg):
        nonlocal sx
        yy = row_y[row]
        b.add_pad(sx, yy, 1.3, 2.6, label_net_pos[1], label_net_pos[0], "screw")
        b.add_pad(sx + pitch, yy, 1.3, 2.6, label_net_neg[1], label_net_neg[0], "screw")
        sx += pitch + gap + pitch

    def screw_one(row, label, net):
        nonlocal sx
        b.add_pad(sx, row_y[row], 1.3, 2.6, net, label, "screw")
        sx += pitch + gap

    screw_pair("power", ("QUIET+", "QUIET5"), ("QUIET-", "GND"))
    screw_pair("power", ("NOISY+", "NOISY5"), ("NOISY-", "GND"))
    screw_pair("power", ("BUCKIN+", "QUIET5"), ("BUCKIN-", "GND"))
    screw_pair("power", ("3V3OUT+", "RAILC"), ("3V3OUT-", "GND"))
    screw_pair("power", ("BOOSTIN+", "NOISY5"), ("BOOSTIN-", "GND"))
    screw_pair("power", ("7VOUT+", "VM7"), ("7VOUT-", "GND"))
    screw_pair("power", ("FAN+", "NOISY5"), ("FAN-", "GND"))
    screw_one("power", "PI GND", "GND")
    power_end = sx
    sx = 44.0
    screw_pair("motor", ("LEFT1", "ML1"), ("LEFT2", "ML2"))
    screw_pair("motor", ("RIGHT1", "MR1"), ("RIGHT2", "MR2"))
    screw_pair("motor", ("SPR1", "MS1"), ("SPR2", "MS2"))
    screw_pair("motor", ("SPR3", "MS3"), ("SPR4", "MS4"))
    screw_pair("motor", ("LAMP1+", "LAMP1"), ("LAMP1-", "GND"))
    screw_pair("motor", ("LAMP2+", "LAMP2"), ("LAMP2-", "GND"))
    screw_pair("motor", ("LAMP3+", "LAMP3"), ("LAMP3-", "GND"))
    screw_pair("motor", ("LAMP4+", "LAMP4"), ("LAMP4-", "GND"))
    sx = max(sx, power_end)

    board_w = max(board_w, sx + EDGE_MARGIN)

    # Fanout vias. Every pad that shares a net with another pad gets a unique via x.
    # GND pads stay on the ground plane and are not fanned out.
    # Single-pin nets (SPARE) are not fanned out.
    net_members = defaultdict(list)
    for p in b.pads:
        if p["net"] != "GND":
            net_members[p["net"]].append(p)
    routed_pads = []
    for net, members in net_members.items():
        if len(members) >= 2:
            routed_pads.extend(members)

    # Group routed pads by header x so each column fans out to its right.
    columns = defaultdict(list)
    for p in routed_pads:
        columns[round(p["x"], 3)].append(p)

    for col_x, pads in columns.items():
        pads.sort(key=lambda p: p["y"])
        # Screws fan upward so the sideways fanout does not run into the next screw.
        others = [p for p in pads if p["kind"] != "screw"]
        start = col_x + 3.4
        for i, p in enumerate(others):
            vx = start + i * VIA_PITCH
            via = {"x": vx, "y": p["y"], "drill": VIA_DRILL, "dia": VIA_PAD, "net": p["net"], "name": "via"}
            b.vias.append(via)
            p["via"] = via
            width = POWER_TRACE if p["net"] in POWER_NETS else TRACE
            b.traces.append((p["x"], p["y"], vx, p["y"], width, p["net"], "top"))

    # Lanes at the top, one per routed net. Power nets get a wider lane.
    header_top = max(p["y"] for p in b.pads if p["kind"] not in ("screw", "mount"))
    lane_y = header_top + 6.0
    nets_in_order = []
    for p in routed_pads:
        if p["net"] not in nets_in_order:
            nets_in_order.append(p["net"])
    lane_of = {}
    for net in nets_in_order:
        gap = POWER_LANE_GAP if net in POWER_NETS else LANE_GAP
        width = POWER_TRACE if net in POWER_NETS else TRACE
        lane_of[net] = (lane_y, width)
        members = [p for p in routed_pads if p["net"] == net and p.get("via")]
        xs = [p["via"]["x"] for p in members]
        y_lane = lane_y
        # Bottom vertical from each via up to the lane, then a top horizontal.
        for p in members:
            vx = p["via"]["x"]
            b.traces.append((vx, p["y"], vx, y_lane, width, net, "bot"))
            street_via = {"x": vx, "y": y_lane, "drill": VIA_DRILL, "dia": VIA_PAD, "net": net, "name": "lane"}
            b.vias.append(street_via)
        if len(xs) >= 2:
            b.traces.append((min(xs), y_lane, max(xs), y_lane, width, net, "top"))
        lane_y += gap

    # Screws escape downward into free lanes, then up the left edge to the matching lane.
    screws_by_net = defaultdict(list)
    for p in b.pads:
        if p["kind"] == "screw" and p["net"] != "GND":
            screws_by_net[p["net"]].append(p)
    bus_x = 6.0
    escape_y = 4.0
    for net, pads in screws_by_net.items():
        if net not in lane_of:
            b.errors.append(f"screw net {net} has nowhere to connect")
            continue
        width = POWER_TRACE if net in POWER_NETS else TRACE
        y_lane, _ = lane_of[net]
        for p in pads:
            b.traces.append((p["x"], p["y"], p["x"], escape_y, width, net, "top"))
            b.vias.append({"x": p["x"], "y": escape_y, "drill": VIA_DRILL, "dia": VIA_PAD, "net": net, "name": "esc"})
        left = min(p["x"] for p in pads)
        b.traces.append((left, escape_y, bus_x, escape_y, width, net, "bot"))
        b.traces.append((bus_x, escape_y, bus_x, y_lane, width, net, "bot"))
        b.vias.append({"x": bus_x, "y": y_lane, "drill": VIA_DRILL, "dia": VIA_PAD, "net": net, "name": "bus"})
        b.traces.append((bus_x, y_lane, min(p["via"]["x"] for p in b.pads if p.get("via") and p["net"] == net), y_lane, width, net, "top"))
        bus_x += 1.40
        escape_y += 1.40

    board_h = lane_y + EDGE_MARGIN

    # Mounting holes, kept off the copper features.
    holes = [
        (3.2, 70.0),
        (board_w - 3.2, 70.0),
        (3.2, board_h - 6.0),
        (board_w - 3.2, board_h - 6.0),
    ]
    for hx, hy in holes:
        b.add_pad(hx, hy, 3.2, 3.2, "MOUNT", "M3", "mount")

    # Silkscreen titles and pin names.
    b.silk.append(("text", 6, board_h - 4.5, "ABADI ROVER BODY  REV A", 1.3))
    b.silk.append(("text", 6, board_h - 7.2, "2 LAYERS  1.6 MM", 1.1))
    for h in b.headers:
        top = h["pads"][-1]["y"]
        b.silk.append(("text", h["x"] - 1.5, top + 3.2, h["title"], 1.0))
        for p in h["pads"]:
            b.silk.append(("text", p["x"] - 1.2, p["y"] - 0.7, p["name"], 0.85, "right"))
        # Pin 1 dot at the bottom pin.
        p1 = h["pads"][0]
        b.silk.append(("dot", p1["x"] - 1.6, p1["y"]))
    # Screw labels above the holes would hit headers, so put them below.
    for p in b.pads:
        if p["kind"] == "screw":
            b.silk.append(("text", p["x"] - 1.0, 2.2, p["name"], 0.7, "right"))
    b.silk.append(("text", rx + 2.2, ry, "10 OHM LAMPS", 0.9))
    b.silk.append(("text", rx + 2.2, ry + 34, "1K THEN 2K ECHO", 0.9))
    b.silk.append(("text", rx + 2.2, ry + 52, "100UF AND 100NF ON 3V3", 0.9))
    b.silk.append(("text", rx + 2.2, ry + 68, "100UF AND 100NF ON 7V", 0.9))
    b.silk.append(("text", 16, 14.5, "PIN 1 IS THE BOTTOM PIN OF EACH HEADER", 1.0))
    b.silk.append(("text", 16, 12.2, "BUCK 3V3 DOES NOT CONNECT TO ESP 3V3", 1.0))

    drc(b)
    return b, board_w, board_h


def drc(b):
    features = []
    for t in b.traces:
        x1, y1, x2, y2, w, net, layer = t
        features.append(("seg", layer, net, w, (x1, y1, x2, y2)))
    for v in b.vias:
        features.append(("pad", "top", v["net"], v["dia"], (v["x"], v["y"])))
        features.append(("pad", "bot", v["net"], v["dia"], (v["x"], v["y"])))
    for p in b.pads:
        features.append(("pad", "top", p["net"], p["dia"], (p["x"], p["y"])))
        if p["net"] != "GND":
            features.append(("pad", "bot", p["net"], p["dia"], (p["x"], p["y"])))

    by_layer = defaultdict(list)
    for f in features:
        by_layer[f[1]].append(f)

    for layer, items in by_layer.items():
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                a, c = items[i], items[j]
                if a[2] == c[2]:
                    continue
                gap = _gap(a, c)
                need = CLEARANCE
                if gap < need - 0.01:
                    b.errors.append(
                        f"{layer} {a[2]} vs {c[2]} gap {gap:.3f} at { _where(a) }"
                    )


def _where(item):
    if item[0] == "pad":
        return f"{item[4][0]:.1f},{item[4][1]:.1f}"
    x1, y1, x2, y2 = item[4]
    return f"{x1:.1f},{y1:.1f}-{x2:.1f},{y2:.1f}"


def _gap(a, c):
    if a[0] == "pad" and c[0] == "pad":
        return math.hypot(a[4][0] - c[4][0], a[4][1] - c[4][1]) - a[3] / 2 - c[3] / 2
    if a[0] == "seg" and c[0] == "seg":
        return seg_distance(a[4], c[4]) - a[3] / 2 - c[3] / 2
    if a[0] == "pad":
        pad, seg = a, c
    else:
        pad, seg = c, a
    x1, y1, x2, y2 = seg[4]
    return dist_point_seg(pad[4][0], pad[4][1], x1, y1, x2, y2) - pad[3] / 2 - seg[3] / 2


def gerber_num(v):
    return str(int(round(v * 1_000_000)))


def header():
    return "\n".join(
        [
            "G04 Abadi Rover body rev A*",
            "%TF.GenerationSoftware,Abadi,build_gerbers,1.0*%",
            "%FSLAX46Y46*%",
            "%MOMM*%",
            "%LPD*%",
        ]
    )


def aperture(code, diameter):
    return f"%ADD{code}C,{diameter:.4f}*%"


def flash(ap, x, y):
    return f"{ap}\nX{gerber_num(x)}Y{gerber_num(y)}D03*"


def draw(ap, x1, y1, x2, y2):
    return (
        f"{ap}\nX{gerber_num(x1)}Y{gerber_num(y1)}D02*\n"
        f"X{gerber_num(x2)}Y{gerber_num(y2)}D01*"
    )


def rect_region(x0, y0, x1, y1):
    return "\n".join(
        [
            "G36*",
            f"X{gerber_num(x0)}Y{gerber_num(y0)}D02*",
            f"X{gerber_num(x1)}Y{gerber_num(y0)}D01*",
            f"X{gerber_num(x1)}Y{gerber_num(y1)}D01*",
            f"X{gerber_num(x0)}Y{gerber_num(y1)}D01*",
            f"X{gerber_num(x0)}Y{gerber_num(y0)}D01*",
            "G37*",
        ]
    )


def text_strokes(text, x, y, height, align="left"):
    """Return list of (x1,y1,x2,y2) in mm."""
    char_w = height * 0.7
    gap = height * 0.18
    advance = char_w + gap
    total = max(0, len(text) * advance - gap)
    if align == "right":
        x = x - total
    strokes = []
    scale_x = char_w / 4.0
    scale_y = height / 6.0
    cursor = x
    for ch in text.upper():
        for seg in FONT.get(ch, FONT.get(" ", [])):
            x1, y1, x2, y2 = seg
            strokes.append(
                (
                    cursor + x1 * scale_x,
                    y + y1 * scale_y,
                    cursor + x2 * scale_x,
                    y + y2 * scale_y,
                )
            )
        cursor += advance
    return strokes


def write_layers(b, width, height):
    files = {}

    def copper(layer, function):
        lines = [
            header(),
            f"%TF.FileFunction,Copper,{function}*%",
            aperture(10, HEADER_PAD),
            aperture(11, 2.6),
            aperture(12, 1.6),
            aperture(13, 1.9),
            aperture(14, 1.5),
            aperture(15, VIA_PAD),
            aperture(16, TRACE),
            aperture(17, POWER_TRACE),
            aperture(18, TRACE + 2 * CLEARANCE),
            aperture(19, POWER_TRACE + 2 * CLEARANCE),
            aperture(20, VIA_PAD + 2 * CLEARANCE),
            aperture(21, HEADER_PAD + 2 * CLEARANCE),
            aperture(22, 2.6 + 2 * CLEARANCE),
            aperture(23, 1.6 + 2 * CLEARANCE),
            aperture(24, 1.9 + 2 * CLEARANCE),
            aperture(25, 1.5 + 2 * CLEARANCE),
            aperture(26, 5.2),
        ]
        if layer == "bot":
            lines.append("%LPD*%")
            lines.append(rect_region(0.5, 0.5, width - 0.5, height - 0.5))
            lines.append("%LPC*%")
            # Clear the plane around every non-ground feature, then redraw it.
            for p in b.pads:
                if p["net"] in ("GND",):
                    continue
                dia_ap = {1.0: "D21*", 1.3: "D22*", 0.8: "D23*", 0.9: "D24*"}.get(round(p["drill"], 1), "D21*")
                # Mounting holes are cleared wider.
                if p["net"] == "MOUNT":
                    lines.append(f"D26*\nX{gerber_num(p['x'])}Y{gerber_num(p['y'])}D03*")
                else:
                    lines.append(flash(dia_ap, p["x"], p["y"]))
            for v in b.vias:
                lines.append(flash("D20*", v["x"], v["y"]))
            for t in b.traces:
                if t[6] != "bot":
                    continue
                ap = "D19*" if t[4] >= POWER_TRACE - 0.01 else "D18*"
                lines.append(draw(ap, t[0], t[1], t[2], t[3]))
            lines.append("%LPD*%")
        # Pads and traces.
        for p in b.pads:
            if p["net"] == "MOUNT":
                continue
            if layer == "bot" and p["net"] == "GND":
                # Ground holes are already in the plane. Add a pad for soldering.
                pass
            ap = {1.0: "D10*", 1.3: "D11*", 0.8: "D12*", 0.9: "D13*"}.get(round(p["drill"], 1), "D10*")
            if abs(p["dia"] - 1.5) < 0.05:
                ap = "D14*"
            lines.append(flash(ap, p["x"], p["y"]))
        for v in b.vias:
            lines.append(flash("D15*", v["x"], v["y"]))
        for t in b.traces:
            if t[6] != layer:
                continue
            ap = "D17*" if t[4] >= POWER_TRACE - 0.01 else "D16*"
            lines.append(draw(ap, t[0], t[1], t[2], t[3]))
        lines.append("M02*")
        return "\n".join(lines) + "\n"

    def mask():
        lines = [
            header(),
            "%TF.FileFunction,Soldermask,Top*%",
            aperture(10, HEADER_PAD + 0.15),
            aperture(11, 2.75),
            aperture(12, 1.75),
            aperture(13, 2.05),
            aperture(14, 1.65),
            aperture(15, VIA_PAD + 0.1),
            aperture(16, 3.6),
        ]
        for p in b.pads:
            if p["net"] == "MOUNT":
                lines.append(flash("D16*", p["x"], p["y"]))
                continue
            ap = {1.0: "D10*", 1.3: "D11*", 0.8: "D12*", 0.9: "D13*"}.get(round(p["drill"], 1), "D10*")
            if abs(p["dia"] - 1.5) < 0.05:
                ap = "D14*"
            lines.append(flash(ap, p["x"], p["y"]))
        for v in b.vias:
            lines.append(flash("D15*", v["x"], v["y"]))
        lines.append("M02*")
        return "\n".join(lines) + "\n"

    def silk():
        lines = [header(), "%TF.FileFunction,Legend,Top*%", aperture(10, 0.12), aperture(11, 0.6)]
        pen = "D10*"
        for item in b.silk:
            if item[0] == "dot":
                lines.append(flash("D11*", item[1], item[2]))
                continue
            _, x, y, text, height = item[:5]
            align = item[5] if len(item) > 5 else "left"
            for x1, y1, x2, y2 in text_strokes(text, x, y, height, align):
                lines.append(draw(pen, x1, y1, x2, y2))
        lines.append("M02*")
        return "\n".join(lines) + "\n"

    def edge():
        lines = [
            header(),
            "%TF.FileFunction,Profile,NP*%",
            aperture(10, 0.10),
            draw("D10*", 0, 0, width, 0),
            draw("D10*", width, 0, width, height),
            draw("D10*", width, height, 0, height),
            draw("D10*", 0, height, 0, 0),
            "M02*",
        ]
        return "\n".join(lines) + "\n"

    files["abadi-F_Cu.gtl"] = copper("top", "L1,Top")
    files["abadi-B_Cu.gbl"] = copper("bot", "L2,Bot")
    files["abadi-F_Mask.gts"] = mask().replace("Soldermask,Top", "Soldermask,Top")
    bot_mask = mask().replace("Soldermask,Top", "Soldermask,Bot")
    files["abadi-B_Mask.gbs"] = bot_mask
    files["abadi-F_Silkscreen.gto"] = silk()
    files["abadi-B_Silkscreen.gbo"] = "\n".join(
        [header(), "%TF.FileFunction,Legend,Bot*%", aperture(10, 0.15), "M02*"]
    ) + "\n"
    files["abadi-Edge_Cuts.gko"] = edge()
    files["abadi.drl"] = drill_file(b)
    return files


def drill_file(b):
    tools = {}
    hits = defaultdict(list)

    def tool_for(diameter):
        key = round(diameter, 2)
        if key not in tools:
            tools[key] = len(tools) + 1
        return tools[key]

    for p in b.pads:
        hits[tool_for(p["drill"])].append((p["x"], p["y"]))
    for v in b.vias:
        hits[tool_for(v["drill"])].append((v["x"], v["y"]))
    lines = ["M48", "; Abadi Rover body rev A", "METRIC,TZ", "FMAT,2"]
    for dia, num in sorted(tools.items(), key=lambda kv: kv[1]):
        lines.append(f"T{num:02d}C{dia:.3f}")
    lines.append("%")
    for num, points in sorted(hits.items()):
        lines.append(f"T{num:02d}")
        for x, y in points:
            lines.append(f"X{x:.3f}Y{y:.3f}")
    lines.append("M30")
    return "\n".join(lines) + "\n"


def write_preview(b, width, height, path):
    def sc(v):
        return v * 8

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{sc(width):.0f}" height="{sc(height):.0f}" viewBox="0 0 {width:.2f} {height:.2f}">',
        f'<rect x="0" y="0" width="{width:.2f}" height="{height:.2f}" fill="#1f7a3a"/>',
        '<g transform="scale(1,-1) translate(0,-{h:.2f})">'.format(h=height),
    ]
    # bottom traces
    for t in b.traces:
        if t[6] != "bot":
            continue
        parts.append(
            f'<line x1="{t[0]:.3f}" y1="{t[1]:.3f}" x2="{t[2]:.3f}" y2="{t[3]:.3f}" stroke="#6eb5ff" stroke-width="{t[4]:.3f}" stroke-linecap="round"/>'
        )
    for t in b.traces:
        if t[6] != "top":
            continue
        parts.append(
            f'<line x1="{t[0]:.3f}" y1="{t[1]:.3f}" x2="{t[2]:.3f}" y2="{t[3]:.3f}" stroke="#ffd0d0" stroke-width="{t[4]:.3f}" stroke-linecap="round"/>'
        )
    for p in b.pads:
        color = "#f4c430" if p["net"] == "GND" else "#ffffff"
        if p["net"] == "MOUNT":
            color = "#333333"
        r = p["dia"] / 2
        parts.append(f'<circle cx="{p["x"]:.3f}" cy="{p["y"]:.3f}" r="{r:.3f}" fill="{color}"/>')
        parts.append(f'<circle cx="{p["x"]:.3f}" cy="{p["y"]:.3f}" r="{p["drill"]/2:.3f}" fill="#1f7a3a"/>')
    for v in b.vias:
        parts.append(f'<circle cx="{v["x"]:.3f}" cy="{v["y"]:.3f}" r="{v["dia"]/2:.3f}" fill="#cccccc"/>')
    parts.append("</g></svg>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))


def main():
    b, width, height = build()
    print(f"Board size: {width:.1f} mm x {height:.1f} mm")
    print(f"Pads: {len(b.pads)}  vias: {len(b.vias)}  traces: {len(b.traces)}")
    if b.errors:
        print(f"DRC errors: {len(b.errors)}")
        for err in b.errors[:40]:
            print(" ", err)
        raise SystemExit(1)
    print("DRC clean")
    files = write_layers(b, width, height)
    gerber_dir = os.path.join(OUT_DIR, "gerber")
    os.makedirs(gerber_dir, exist_ok=True)
    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)
    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in files.items():
            path = os.path.join(gerber_dir, name)
            with open(path, "w", encoding="ascii") as f:
                f.write(data)
            zf.write(path, arcname=name)
    write_preview(b, width, height, os.path.join(OUT_DIR, "gerber-preview.svg"))
    print("Wrote", ZIP_NAME)


if __name__ == "__main__":
    main()
