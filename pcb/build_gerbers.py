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
VIA_DRILL = 0.30
VIA_PAD = 0.60
TRACE = 0.25
POWER_TRACE = 0.80
CLEARANCE = 0.20
PIN_PITCH = 2.54
SIG_PITCH = 0.70
PWR_PITCH = 1.16
MOTOR_PITCH = 1.12

POWER_NETS = {"QUIET5", "NOISY5", "RAILC", "VM7", "ESP3V3"}
MOTOR_NETS = {"ML1", "ML2", "MR1", "MR2", "MS1", "MS2", "MS3", "MS4"}
WIDE_NETS = POWER_NETS | MOTOR_NETS

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


def _orient(px, py, qx, qy, rx, ry):
    return (qx - px) * (ry - py) - (qy - py) * (rx - px)


def _on_seg(px, py, qx, qy, rx, ry):
    return (
        min(px, rx) - 1e-6 <= qx <= max(px, rx) + 1e-6
        and min(py, ry) - 1e-6 <= qy <= max(py, ry) + 1e-6
    )


def segments_intersect(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    o1 = _orient(ax1, ay1, ax2, ay2, bx1, by1)
    o2 = _orient(ax1, ay1, ax2, ay2, bx2, by2)
    o3 = _orient(bx1, by1, bx2, by2, ax1, ay1)
    o4 = _orient(bx1, by1, bx2, by2, ax2, ay2)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    if abs(o1) < 1e-6 and _on_seg(ax1, ay1, bx1, by1, ax2, ay2):
        return True
    if abs(o2) < 1e-6 and _on_seg(ax1, ay1, bx2, by2, ax2, ay2):
        return True
    if abs(o3) < 1e-6 and _on_seg(bx1, by1, ax1, ay1, bx2, by2):
        return True
    if abs(o4) < 1e-6 and _on_seg(bx1, by1, ax2, ay2, bx2, by2):
        return True
    return False


def seg_distance(a, b):
    if segments_intersect(a, b):
        return 0.0
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
    """Compact body board. Target: smaller than the 150 x 95 mm perfboard."""
    b = Board()

    def tw(net):
        if net in WIDE_NETS:
            return POWER_TRACE
        if str(net).startswith("LAMP") or str(net).startswith("NO"):
            return 0.50
        return TRACE

    def add_trace(x1, y1, x2, y2, width, net, layer):
        if abs(x1 - x2) < 1e-6 and abs(y1 - y2) < 1e-6:
            return
        b.traces.append((x1, y1, x2, y2, width, net, layer))

    def add_via(x, y, net):
        b.vias.append(
            {"x": x, "y": y, "drill": VIA_DRILL, "dia": VIA_PAD, "net": net, "name": "via"}
        )

    def vstub(pad, y, net):
        add_trace(pad["x"], pad["y"], pad["x"], y, tw(net), net, "bot")
        add_via(pad["x"], y, net)

    def place_groups(groups, y, x_start, role):
        x = x_start
        for title, pins in groups:
            pads = []
            origin = x
            for name, net in pins:
                actual = "GND" if net is None else net
                pad = b.add_pad(x, y, HEADER_DRILL, HEADER_PAD, actual, name, "header")
                pad["role"] = role
                pads.append(pad)
                x += PIN_PITCH
            b.headers.append({"title": title, "x": origin, "y": y, "pads": pads})
        return x - PIN_PITCH

    def place_pairs(y, x0, pairs):
        x = x0
        out = []
        for pos, neg in pairs:
            a = b.add_pad(x, y, 1.3, 2.6, pos[1], pos[0], "screw")
            a["role"] = "screw"
            c = b.add_pad(x + 5.08, y, 1.3, 2.6, neg[1], neg[0], "screw")
            c["role"] = "screw"
            out.append((a, c))
            x += 8.40
        return out

    # Rows, bottom to top. Numbers are the minimum gap that still clears a
    # 0.60 mm via and a 0.80 mm power trace.
    y_motor = 10.0
    motor_pitch = MOTOR_PITCH
    lamp_pitch = 0.76
    motor_track0 = y_motor + 1.92
    motor_tracks = [motor_track0 + i * motor_pitch for i in range(8)]
    lamp_track0 = motor_tracks[-1] + 0.92
    lamp_tracks = [lamp_track0 + i * lamp_pitch for i in range(4)]

    y_power = lamp_tracks[-1] + 1.92
    power_names = ["QUIET5", "NOISY5", "RAILC", "VM7", "ESP3V3"]
    power_track0 = y_power + 1.92
    power_tracks = {name: power_track0 + i * PWR_PITCH for i, name in enumerate(power_names)}

    y_esp = power_tracks["ESP3V3"] + 1.78
    direct_nets = [
        "IN1A", "IN2A", "IN3A", "IN4A",
        "IN1B", "IN2B", "IN3B", "IN4B",
        "SDA", "SCL",
    ]
    m2_sig_nets = [
        "RLY1", "RLY2", "RLY3", "RLY4",
        "CSL", "CSR", "DC", "RST", "MOSI", "SCK",
        "TRIG", "ECHO3",
    ]
    channel_nets = direct_nets + m2_sig_nets
    ch0 = y_esp + 1.66
    channel = {net: ch0 + i * SIG_PITCH for i, net in enumerate(channel_nets)}

    motor_nets = ["ML1", "ML2", "MR1", "MR2", "MS1", "MS2", "MS3", "MS4"]
    alley0 = channel[channel_nets[-1]] + 1.00
    alley = {net: alley0 + i * motor_pitch for i, net in enumerate(motor_nets)}

    y_m1 = alley[motor_nets[-1]] + 1.78
    m1_power_names = ["VM7", "NOISY5", "ESP3V3"]
    m1p0 = y_m1 + 1.80
    m1_power = {name: m1p0 + i * PWR_PITCH for i, name in enumerate(m1_power_names)}

    y_m2 = m1_power["ESP3V3"] + 1.80
    part_lo = y_m2 + 3.35
    part_hi = part_lo + 3.35

    lamp_nets = ["LAMP1", "LAMP2", "LAMP3", "LAMP4"]
    escape_nets = m2_sig_nets + lamp_nets
    esc0 = part_hi + 1.28
    escape = {}
    esc_y = esc0
    for i, net in enumerate(escape_nets):
        escape[net] = esc_y
        if i + 1 < len(escape_nets):
            nxt = escape_nets[i + 1]
            # Lamp traces are wider, so the via beside them needs a bigger step.
            esc_y += 0.84 if (net.startswith("LAMP") or nxt.startswith("LAMP")) else SIG_PITCH

    m2_power_names = ["RAILC", "QUIET5"]
    m2p0 = escape[escape_nets[-1]] + 0.98
    m2_power = {name: m2p0 + i * PWR_PITCH for i, name in enumerate(m2_power_names)}
    top_copper = m2_power["QUIET5"] + 0.55
    board_h = top_copper + 5.5

    # ---- headers ----
    x0 = 9.0
    place_groups(
        [("ESP32-S3", [
            ("GND", None),
            ("GPIO4", "IN1A"), ("GPIO5", "IN2A"), ("GPIO6", "IN3A"), ("GPIO7", "IN4A"),
            ("GPIO15", "IN1B"), ("GPIO16", "IN2B"), ("GPIO17", "IN3B"), ("GPIO18", "IN4B"),
            ("GPIO8", "SDA"), ("GPIO9", "SCL"),
            ("GPIO1", "RLY1"), ("GPIO2", "RLY2"), ("GPIO38", "RLY3"), ("GPIO39", "RLY4"),
            ("GPIO13", "CSL"), ("GPIO14", "CSR"), ("GPIO21", "DC"), ("GPIO10", "RST"),
            ("GPIO11", "MOSI"), ("GPIO12", "SCK"),
            ("GPIO41", "TRIG"), ("GPIO42", "ECHO3"),
            ("GPIO40", "SPARE"),
            ("3V3", "ESP3V3"),
            ("GND", None),
        ])],
        y_esp, x0, "esp",
    )
    place_groups(
        [
            ("DRV A  TRACKS", [
                ("IN1", "IN1A"), ("IN2", "IN2A"), ("IN3", "IN3A"), ("IN4", "IN4A"),
                ("VM", "VM7"),
                ("OUT1", "ML1"), ("OUT2", "ML2"), ("OUT3", "MR1"), ("OUT4", "MR2"),
                ("GND", None),
            ]),
            ("DRV B  SPARE", [
                ("IN1", "IN1B"), ("IN2", "IN2B"), ("IN3", "IN3B"), ("IN4", "IN4B"),
                ("VM", "VM7"),
                ("OUT1", "MS1"), ("OUT2", "MS2"), ("OUT3", "MS3"), ("OUT4", "MS4"),
                ("GND", None),
            ]),
            ("PCA9685", [
                ("VCC", "ESP3V3"), ("SDA", "SDA"), ("SCL", "SCL"), ("V+", "NOISY5"), ("GND", None),
            ]),
            ("GYRO", [
                ("VCC", "ESP3V3"), ("SDA", "SDA"), ("SCL", "SCL"), ("GND", None),
            ]),
        ],
        y_m1, x0 + 1.27, "m1",
    )
    place_groups(
        [
            ("RELAY A", [
                ("VCC", "RAILC"), ("IN1", "RLY1"), ("IN2", "RLY2"), ("COM", "RAILC"),
                ("NO1", "NO1"), ("NO2", "NO2"), ("GND", None),
            ]),
            ("RELAY B", [
                ("VCC", "RAILC"), ("IN1", "RLY3"), ("IN2", "RLY4"), ("COM", "RAILC"),
                ("NO1", "NO3"), ("NO2", "NO4"), ("GND", None),
            ]),
            ("SCREEN L", [
                ("VCC", "RAILC"), ("GND", None), ("CS", "CSL"), ("RST", "RST"),
                ("DC", "DC"), ("SDA", "MOSI"), ("SCL", "SCK"),
            ]),
            ("SCREEN R", [
                ("VCC", "RAILC"), ("GND", None), ("CS", "CSR"), ("RST", "RST"),
                ("DC", "DC"), ("SDA", "MOSI"), ("SCL", "SCK"),
            ]),
            ("SONAR", [
                ("VCC", "QUIET5"), ("GND", None), ("TRIG", "TRIG"), ("ECHO", "ECHO5"),
            ]),
        ],
        y_m2, x0, "m2",
    )

    # 10 ohm lamp resistors above the relay NO pins.
    no_to_lamp = {"NO1": "LAMP1", "NO2": "LAMP2", "NO3": "LAMP3", "NO4": "LAMP4"}
    for pad in list(b.pads):
        lamp = no_to_lamp.get(pad["net"])
        if lamp and pad.get("role") == "m2":
            lo = b.add_pad(pad["x"], part_lo, 0.8, 1.6, pad["net"], pad["net"], "part")
            lo["role"] = "local"
            hi = b.add_pad(pad["x"], part_hi, 0.8, 1.6, lamp, lamp, "part")
            hi["role"] = "escape"
            add_trace(pad["x"], pad["y"], lo["x"], lo["y"], 0.50, pad["net"], "bot")

    # Echo divider to the right of the sonar ECHO pin.
    echo_pin = next(p for p in b.pads if p.get("role") == "m2" and p["name"] == "ECHO")
    ex = echo_pin["x"]
    e5 = b.add_pad(ex, part_lo, 0.8, 1.6, "ECHO5", "1K", "part")
    e5["role"] = "local"
    e3a = b.add_pad(ex + 3.4, part_lo, 0.8, 1.6, "ECHO3", "1K", "part")
    e3a["role"] = "join"
    e3b = b.add_pad(ex + 3.4, part_hi, 0.8, 1.6, "ECHO3", "2K", "part")
    e3b["role"] = "escape"
    g2 = b.add_pad(ex + 6.8, part_hi, 0.8, 1.6, "GND", "2K", "part")
    g2["role"] = "gnd"
    add_trace(echo_pin["x"], echo_pin["y"], e5["x"], e5["y"], TRACE, "ECHO5", "bot")
    add_trace(e3a["x"], e3a["y"], e3b["x"], e3b["y"], TRACE, "ECHO3", "bot")

    # Screw rows. Power row is shifted half a step so its stubs miss the motor stubs.
    place_pairs(y_motor, 12.0, [
        (("LEFT1", "ML1"), ("LEFT2", "ML2")),
        (("RIGHT1", "MR1"), ("RIGHT2", "MR2")),
        (("SPR1", "MS1"), ("SPR2", "MS2")),
        (("SPR3", "MS3"), ("SPR4", "MS4")),
        (("LAMP1+", "LAMP1"), ("LAMP1-", "GND")),
        (("LAMP2+", "LAMP2"), ("LAMP2-", "GND")),
        (("LAMP3+", "LAMP3"), ("LAMP3-", "GND")),
        (("LAMP4+", "LAMP4"), ("LAMP4-", "GND")),
    ])
    place_pairs(y_power, 16.2, [
        (("QUIET+", "QUIET5"), ("QUIET-", "GND")),
        (("NOISY+", "NOISY5"), ("NOISY-", "GND")),
        (("BUCK+", "QUIET5"), ("BUCK-", "GND")),
        (("3V3+", "RAILC"), ("3V3-", "GND")),
        (("BOOST+", "NOISY5"), ("BOOST-", "GND")),
        (("7V+", "VM7"), ("7V-", "GND")),
        (("FAN+", "NOISY5"), ("FAN-", "GND")),
    ])
    pi = b.add_pad(16.2 + 7 * 8.40, y_power, 1.3, 2.6, "GND", "PI GND", "screw")
    pi["role"] = "screw"

    # One column per rail so the two caps on that rail share a trace.
    for name, net, drill, dia, xx, yy in (
        ("100U", "RAILC", 0.9, 1.9, 80.0, 7.3),
        ("100N", "RAILC", 0.8, 1.6, 80.0, 10.0),
        ("100U", "VM7", 0.9, 1.9, 88.5, 7.3),
        ("100N", "VM7", 0.8, 1.6, 88.5, 10.0),
    ):
        hot = b.add_pad(xx, yy, drill, dia, net, name, "part")
        hot["role"] = "cap"
        gnd = b.add_pad(xx + 3.3, yy, drill, dia, "GND", "GND", "part")
        gnd["role"] = "gnd"

    right = max(p["x"] for p in b.pads)
    bus = right + 2.8
    bus_x = {}
    for net in m2_sig_nets + lamp_nets:
        bus_x[net] = bus
        bus += 0.88
    bus += 0.40
    for net in motor_nets:
        bus_x[net] = bus
        bus += 1.10
    bus += 0.40
    for net in power_names:
        bus_x[net] = bus
        bus += 1.20
    board_w = bus + 6.2

    routed = set()

    def route_direct(net):
        pads = [p for p in b.pads if p["net"] == net and p.get("role") in ("esp", "m1")]
        y = channel[net]
        for p in pads:
            vstub(p, y, net)
        xs = [p["x"] for p in pads]
        add_trace(min(xs), y, max(xs), y, TRACE, net, "top")
        routed.add(net)

    def route_m2_signal(net):
        esp = [p for p in b.pads if p["net"] == net and p.get("role") == "esp"]
        mods = [p for p in b.pads if p["net"] == net and p.get("role") in ("m2", "escape")]
        if not esp or not mods:
            b.errors.append("missing pads for " + net)
            return
        y = channel[net]
        ey = escape[net]
        bx = bus_x[net]
        w = TRACE
        for p in esp:
            vstub(p, y, net)
        for p in mods:
            vstub(p, ey, net)
        add_trace(min(p["x"] for p in esp), y, bx, y, w, net, "top")
        add_via(bx, y, net)
        add_trace(min(p["x"] for p in mods), ey, bx, ey, w, net, "top")
        add_via(bx, ey, net)
        add_trace(bx, y, bx, ey, w, net, "bot")
        routed.add(net)

    def route_motor(net):
        src = [p for p in b.pads if p["net"] == net and p.get("role") == "m1"]
        dst = [p for p in b.pads if p["net"] == net and p.get("role") == "screw"]
        if len(src) != 1 or len(dst) != 1:
            b.errors.append("motor pads " + net)
            return
        y = alley[net]
        ly = motor_tracks[motor_nets.index(net)]
        bx = bus_x[net]
        w = POWER_TRACE
        vstub(src[0], y, net)
        add_trace(src[0]["x"], y, bx, y, w, net, "top")
        add_via(bx, y, net)
        add_trace(bx, y, bx, ly, w, net, "bot")
        add_via(bx, ly, net)
        add_trace(min(dst[0]["x"], bx), ly, max(dst[0]["x"], bx), ly, w, net, "top")
        add_via(dst[0]["x"], ly, net)
        add_trace(dst[0]["x"], ly, dst[0]["x"], dst[0]["y"], w, net, "bot")
        routed.add(net)

    def route_lamp(net):
        src = [p for p in b.pads if p["net"] == net and p.get("role") == "escape"]
        dst = [p for p in b.pads if p["net"] == net and p.get("role") == "screw"]
        if len(src) != 1 or len(dst) != 1:
            b.errors.append("lamp pads " + net)
            return
        ey = escape[net]
        ly = lamp_tracks[lamp_nets.index(net)]
        bx = bus_x[net]
        w = 0.50
        vstub(src[0], ey, net)
        add_trace(src[0]["x"], ey, bx, ey, w, net, "top")
        add_via(bx, ey, net)
        add_trace(bx, ey, bx, ly, w, net, "bot")
        add_via(bx, ly, net)
        add_trace(min(dst[0]["x"], bx), ly, max(dst[0]["x"], bx), ly, w, net, "top")
        add_via(dst[0]["x"], ly, net)
        add_trace(dst[0]["x"], ly, dst[0]["x"], dst[0]["y"], w, net, "bot")
        routed.add(net)

    def route_power(net):
        w = POWER_TRACE
        bx = bus_x[net]
        groups = []
        low = [p for p in b.pads if p["net"] == net and p.get("role") in ("screw", "cap")]
        if net == "ESP3V3":
            low += [p for p in b.pads if p["net"] == net and p.get("role") == "esp"]
        m1 = [p for p in b.pads if p["net"] == net and p.get("role") == "m1"]
        m2 = [p for p in b.pads if p["net"] == net and p.get("role") == "m2"]
        if low:
            groups.append((low, power_tracks[net]))
        if m1:
            groups.append((m1, m1_power[net]))
        if m2:
            groups.append((m2, m2_power[net]))
        ys = []
        for pads, y in groups:
            for p in pads:
                vstub(p, y, net)
            xs = [p["x"] for p in pads] + [bx]
            add_trace(min(xs), y, max(xs), y, w, net, "top")
            add_via(bx, y, net)
            ys.append(y)
        if len(ys) >= 2:
            add_trace(bx, min(ys), bx, max(ys), w, net, "bot")
        routed.add(net)

    for net in direct_nets:
        route_direct(net)
    for net in m2_sig_nets:
        route_m2_signal(net)
    for net in motor_nets:
        route_motor(net)
    for net in lamp_nets:
        route_lamp(net)
    for net in power_names:
        route_power(net)
    for net in ("NO1", "NO2", "NO3", "NO4", "ECHO5"):
        routed.add(net)

    seen = {}
    for p in b.pads:
        if p["net"] in ("GND", "MOUNT"):
            continue
        seen.setdefault(p["net"], 0)
        seen[p["net"]] += 1
    for net, count in seen.items():
        if net == "SPARE":
            continue
        if net not in routed:
            b.errors.append("unrouted " + net)
        if count < 2:
            b.errors.append("single pad " + net)

    # Mounting holes in the four corners, clear of the copper bands.
    inset = 3.6
    for hx, hy in (
        (inset, inset),
        (board_w - inset, inset),
        (inset, board_h - inset),
        (board_w - inset, board_h - inset),
    ):
        b.add_pad(hx, hy, 3.2, 3.2, "MOUNT", "M3", "mount")

    b.silk.append(("text", 8, board_h - 3.6, "ABADI ROVER BODY", 1.15))
    b.silk.append((
        "text", 8, board_h - 5.3,
        "{:.0f} MM X {:.0f} MM   2 LAYERS   1.6 MM".format(board_w, board_h),
        0.85,
    ))
    for h in b.headers:
        cx = (h["pads"][0]["x"] + h["pads"][-1]["x"]) / 2.0
        b.silk.append(("text", cx, h["y"] - 2.05, h["title"], 0.72, "center"))
        p1 = h["pads"][0]
        b.silk.append(("dot", p1["x"], p1["y"] - 1.35))
    for p in b.pads:
        if p["kind"] == "screw":
            b.silk.append(("text", p["x"], p["y"] - 2.15, p["name"], 0.48, "center"))
    b.silk.append(("text", 12, 4.6, "PIN 1 IS THE LEFT HOLE.  BUCK 3V3 DOES NOT JOIN ESP 3V3.", 0.62))
    b.silk.append(("text", ex, part_hi + 0.3, "ECHO 1K 2K", 0.55))

    if board_w >= 150 or board_h >= 95:
        b.errors.append("SIZE {:.1f} x {:.1f}".format(board_w, board_h))

    b.meta = {"motor_y": y_motor, "power_y": y_power, "esp_y": y_esp, "m1_y": y_m1, "m2_y": y_m2}
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
    if align == "center":
        x = x - total / 2.0
    elif align == "right":
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


def write_layout_png(b, width, height, path):
    """To-scale picture of the real board, with a pin list beside it."""
    from PIL import Image, ImageDraw, ImageFont

    scale = 16
    left_m, top_m, bot_m = 14.0, 18.0, 12.0
    panel = 86.0
    img_w = int((left_m + width + 6 + panel) * scale)
    img_h = int((top_m + height + bot_m) * scale) + 520
    img = Image.new("RGBA", (img_w, img_h), (248, 246, 240, 255))
    draw = ImageDraw.Draw(img)
    regular = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"
    bold = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
    title_f = ImageFont.truetype(bold, 32)
    sub_f = ImageFont.truetype(regular, 18)
    head_f = ImageFont.truetype(bold, 15)
    name_f = ImageFont.truetype(bold, 11)
    pin_f = ImageFont.truetype(regular, 11)
    list_f = ImageFont.truetype(regular, 13)
    list_b = ImageFont.truetype(bold, 14)

    def X(x):
        return int((left_m + x) * scale)

    def Y(y):
        return int((top_m + height - y) * scale)

    draw.text((18, 10), "ABADI ROVER BODY", font=title_f, fill=(20, 20, 20, 255))
    draw.text(
        (18, 48),
        "{:.0f} mm wide  x  {:.0f} mm tall.   Smaller than the 150 x 95 mm perfboard.".format(width, height),
        font=sub_f,
        fill=(150, 30, 30, 255),
    )
    draw.text(
        (18, 74),
        "Previous file was 224 x 218 mm. This picture is the real board, to scale. Pin 1 is the left hole.",
        font=sub_f,
        fill=(40, 40, 40, 255),
    )

    draw.rectangle([X(0), Y(height), X(width), Y(0)], fill=(31, 122, 58, 255), outline=(12, 40, 18, 255), width=4)

    tint = {
        "ESP32-S3": (214, 230, 255, 230),
        "DRV A  TRACKS": (255, 196, 140, 230),
        "DRV B  SPARE": (255, 214, 170, 230),
        "PCA9685": (220, 200, 255, 230),
        "GYRO": (220, 200, 255, 230),
        "RELAY A": (255, 230, 120, 230),
        "RELAY B": (255, 230, 120, 230),
        "SCREEN L": (176, 224, 176, 230),
        "SCREEN R": (176, 224, 176, 230),
        "SONAR": (170, 230, 230, 230),
    }
    for h in b.headers:
        col = tint.get(h["title"], (255, 255, 255, 220))
        x1 = h["pads"][0]["x"] - 1.15
        x2 = h["pads"][-1]["x"] + 1.15
        draw.rectangle([X(x1), Y(h["y"] + 1.35), X(x2), Y(h["y"] - 1.35)], fill=col)
        draw.text((X(h["pads"][0]["x"] - 1.0), Y(h["y"] + 3.5)), h["title"], font=head_f, fill=(10, 10, 10, 255))

    for t in b.traces:
        color = (255, 186, 186, 255) if t[6] == "top" else (170, 205, 255, 255)
        draw.line(
            [(X(t[0]), Y(t[1])), (X(t[2]), Y(t[3]))],
            fill=color,
            width=max(1, int(round(t[4] * scale * 0.55))),
        )

    def paste_up(text, x_mm, y_mm, font, fill):
        bbox = font.getbbox(text)
        tw, th = bbox[2] - bbox[0] + 2, bbox[3] - bbox[1] + 2
        chip = Image.new("RGBA", (tw + 2, th + 2), (0, 0, 0, 0))
        ImageDraw.Draw(chip).text((1, 0), text, font=font, fill=fill)
        rot = chip.rotate(90, expand=True, resample=Image.Resampling.BICUBIC)
        img.alpha_composite(rot, (X(x_mm) - rot.size[0] // 2, Y(y_mm) - rot.size[1] // 2))

    for p in b.pads:
        r = p["dia"] / 2.0
        if p["net"] == "MOUNT":
            col = (50, 50, 50, 255)
        elif p["net"] == "GND":
            col = (232, 184, 40, 255)
        elif p["net"] in POWER_NETS:
            col = (230, 70, 60, 255)
        else:
            col = (255, 255, 255, 255)
        draw.ellipse([X(p["x"] - r), Y(p["y"] + r), X(p["x"] + r), Y(p["y"] - r)], fill=col, outline=(20, 20, 20, 255))
        dr = p["drill"] / 2.0
        hole = (248, 246, 240, 255) if p["net"] == "MOUNT" else (31, 122, 58, 255)
        draw.ellipse([X(p["x"] - dr), Y(p["y"] + dr), X(p["x"] + dr), Y(p["y"] - dr)], fill=hole)

    for h in b.headers:
        p1 = h["pads"][0]
        draw.rectangle(
            [X(p1["x"] - 1.35), Y(p1["y"] + 1.35), X(p1["x"] + 1.35), Y(p1["y"] - 1.35)],
            outline=(180, 20, 20, 255),
            width=2,
        )
        for p in h["pads"]:
            below = p.get("role") == "esp"
            paste_up(p["name"], p["x"], p["y"] - 2.7 if below else p["y"] + 2.7, pin_f, (15, 15, 15, 255))

    for p in b.pads:
        if p["kind"] == "screw":
            paste_up(p["name"], p["x"], p["y"] - 2.5, name_f, (90, 20, 20, 255))

    # Width and height arrows in the margin.
    ax0, ax1 = X(0), X(width)
    ay = Y(0) + int(7.2 * scale)
    draw.line([(ax0, ay), (ax1, ay)], fill=(20, 20, 20, 255), width=2)
    draw.text(((ax0 + ax1) // 2 - 40, ay + 4), "{:.0f} mm".format(width), font=head_f, fill=(20, 20, 20, 255))
    hy0, hy1 = Y(height), Y(0)
    hx = X(0) - int(6 * scale)
    draw.line([(hx, hy0), (hx, hy1)], fill=(20, 20, 20, 255), width=2)
    draw.text((hx - 52, (hy0 + hy1) // 2), "{:.0f} mm".format(height), font=head_f, fill=(20, 20, 20, 255))

    # Pin list.
    px = X(width) + int(5 * scale)
    py = Y(height) + 4
    draw.text((px, py), "PIN LIST  (pin 1 is first)", font=list_b, fill=(20, 20, 20, 255))
    py += 22
    draw.text((px, py), "Red = power   Gold = ground   White = signal", font=list_f, fill=(60, 60, 60, 255))
    py += 22
    for h in b.headers:
        draw.text((px, py), h["title"], font=list_b, fill=(120, 30, 30, 255))
        py += 18
        for i, p in enumerate(h["pads"], start=1):
            draw.text((px, py), "{:2d}  {:7s}  {}".format(i, p["name"], p["net"]), font=list_f, fill=(20, 20, 20, 255))
            py += 15
        py += 8
    draw.text((px, py), "POWER SCREWS", font=list_b, fill=(120, 30, 30, 255))
    py += 18
    screws = sorted((p for p in b.pads if p["kind"] == "screw"), key=lambda p: (-round(p["y"], 1), p["x"]))
    last_y = None
    for p in screws:
        band = round(p["y"], 1)
        if last_y is not None and band < last_y - 2 and py < img_h - 40:
            py += 6
            draw.text((px, py), "MOTOR AND LAMP SCREWS", font=list_b, fill=(120, 30, 30, 255))
            py += 18
        last_y = band
        draw.text((px, py), p["name"] + "   " + p["net"], font=list_f, fill=(20, 20, 20, 255))
        py += 15

    img.convert("RGB").save(path, "PNG")


def main():
    b, width, height = build()
    print(f"Board size: {width:.1f} mm x {height:.1f} mm")
    print(f"Pads: {len(b.pads)}  vias: {len(b.vias)}  traces: {len(b.traces)}")
    drc(b)
    write_layout_png(b, width, height, os.path.join(OUT_DIR, "layout.png"))
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
