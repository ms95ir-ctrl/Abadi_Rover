#!/usr/bin/env python3
"""Build the robot motherboard draft (100 x 100 mm) as a KiCad board, ready for auto-routing.

Positions come from the v1 floor plan (pcb/draft/floorplan_v1.py). Everything marked PROVISIONAL
(module pin orders, ESP32 pin map) has to be checked against the real parts before ordering.

Usage: build_board.py <out.kicad_pcb> [--layers 2|4]
Needs KiCad 7's python module (pcbnew).
"""
import json
import sys

import pcbnew
from pcbnew import FromMM, VECTOR2I

OUT = sys.argv[1]
FINE = "--fine" in sys.argv
LAYERS = 4 if "--layers" in sys.argv and sys.argv[sys.argv.index("--layers") + 1] == "4" else 2
OX, OY = 100.0, 50.0           # where the board's top-left corner sits on the KiCad page
BW = BH = 100.0
PITCH = 2.54

board = pcbnew.BOARD()
nets = {}


def P(x, y):
    """Board mm (origin lower-left, y up) -> KiCad position."""
    return VECTOR2I(FromMM(OX + x), FromMM(OY + BH - y))


def net(name):
    if not name:
        return None
    if name not in nets:
        ni = pcbnew.NETINFO_ITEM(board, name)
        board.Add(ni)
        nets[name] = ni
    return nets[name]


def silk_text(x, y, text, size=1.0, angle=0.0, layer=pcbnew.F_SilkS):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(text)
    t.SetPosition(P(x, y))
    t.SetTextSize(VECTOR2I(FromMM(size), FromMM(size)))
    t.SetTextThickness(FromMM(max(0.15, size * 0.15)))
    t.SetLayer(layer)
    t.SetTextAngle(pcbnew.EDA_ANGLE(angle, pcbnew.DEGREES_T))
    board.Add(t)


def silk_rect(x0, y0, x1, y1, width=0.15):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_RECT)
    s.SetStart(P(x0, y1))
    s.SetEnd(P(x1, y0))
    s.SetWidth(FromMM(width))
    s.SetFilled(False)
    s.SetLayer(pcbnew.F_SilkS)
    board.Add(s)


def silk_line(x0, y0, x1, y1, width=0.15):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(P(x0, y0))
    s.SetEnd(P(x1, y1))
    s.SetWidth(FromMM(width))
    s.SetLayer(pcbnew.F_SilkS)
    board.Add(s)


def footprint(ref, value, pads, drill=1.0, dia=None, first_square=True):
    """pads: list of (x, y, netname). Pad numbers are 1..n in list order."""
    dia = dia if dia is not None else (1.7 if FINE else 1.8)
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetFPID(pcbnew.LIB_ID("abadi", "FP_" + ref))
    fp.SetPosition(P(pads[0][0], pads[0][1]))
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    for i, (x, y, nn) in enumerate(pads, start=1):
        d, g = (drill, dia)
        if len(pads[0]) > 3 and False:
            pass
        pad = pcbnew.PAD(fp)
        pad.SetNumber(str(i))
        pad.SetShape(pcbnew.PAD_SHAPE_RECT if (i == 1 and first_square) else pcbnew.PAD_SHAPE_CIRCLE)
        pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
        pad.SetLayerSet(pad.PTHMask())
        pad.SetSize(VECTOR2I(FromMM(g), FromMM(g)))
        pad.SetDrillSize(VECTOR2I(FromMM(d), FromMM(d)))
        ap = P(x, y)
        pad.SetPos0(VECTOR2I(ap.x - fp.GetPosition().x, ap.y - fp.GetPosition().y))
        pad.SetPosition(ap)
        n = net(nn)
        if n is not None:
            pad.SetNet(n)
        fp.Add(pad)
    board.Add(fp)
    return fp


def row(x, y, names, vertical=False, step=PITCH):
    """names: list of net names; returns pad list."""
    return [((x, y + i * step) if vertical else (x + i * step, y), nn) for i, nn in enumerate(names)]


def pads_from(rowspec):
    return [(p[0], p[1], nn) for p, nn in rowspec]


# ------------------------------------------------------------------ board outline, holes
OI = 0.05      # outline centre line 0.05 mm inside, so the plotted extents (line width 0.1 mm) are exactly 100.0 x 100.0
for (a, b) in (((OI, OI), (BW - OI, OI)), ((BW - OI, OI), (BW - OI, BH - OI)), ((BW - OI, BH - OI), (OI, BH - OI)), ((OI, BH - OI), (OI, OI))):
    seg = pcbnew.PCB_SHAPE(board)
    seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
    seg.SetStart(P(*a))
    seg.SetEnd(P(*b))
    seg.SetWidth(FromMM(0.1))
    seg.SetLayer(pcbnew.Edge_Cuts)
    board.Add(seg)

for i, (hx, hy) in enumerate(((4, 4), (96, 4), (4, 96), (96, 96)), start=1):
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference("H%d" % i)
    fp.SetFPID(pcbnew.LIB_ID("abadi", "MOUNT_M3"))
    fp.SetPosition(P(hx, hy))
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    pad = pcbnew.PAD(fp)
    pad.SetNumber("")
    pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
    pad.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
    pad.SetLayerSet(pad.UnplatedHoleMask())
    pad.SetSize(VECTOR2I(FromMM(3.2), FromMM(3.2)))
    pad.SetDrillSize(VECTOR2I(FromMM(3.2), FromMM(3.2)))
    pad.SetPosition(P(hx, hy))
    fp.Add(pad)
    board.Add(fp)

# ------------------------------------------------------------------ ESP32-S3 DevKit (measured: 57 x 28 mm, rows 25.4 mm apart)
ESP_X1 = 37.0                    # x of pin 1 (antenna end) in both rows
ROW_GAP = 25.4                   # centre to centre of the two rows (1.000 inch)
lower_y = 66.6                   # the row that starts 3V3 3V3 RST ...
upper_y = lower_y + ROW_GAP      # the row that starts GND TX RX ...
PCB_X0, PCB_X1 = ESP_X1 - 1.75, ESP_X1 + 21 * PITCH + 1.75      # carrier PCB ends (antenna end, USB end)
PCB_Y0, PCB_Y1 = lower_y - 1.3, upper_y + 1.3                     # 28 mm wide
ESP_CY = (lower_y + upper_y) / 2
ANT_LEN, ANT_W = 6.3, 18.0       # black antenna part hanging off the antenna end
# GPIO order on the two DevKit rows, pin 1 first (from the board's own silkscreen)
J1_PINS = ["3V3", "3V3", "RST", 4, 5, 6, 7, 15, 16, 17, 18, 8, 3, 46, 9, 10, 11, 12, 13, 14, "5V", "G"]
J3_PINS = ["G", 43, 44, 1, 2, 42, 41, 40, 39, 38, 37, 36, 35, 0, 45, 48, 47, 21, 20, 19, "G", "G"]
# GPIOs that are safe for general use (no USB 19/20, UART0 43/44, boot 0, PSRAM 35-37, RGB LED 38/48, strapping 3/45/46)
SAFE = {4, 5, 6, 7, 15, 16, 17, 18, 8, 9, 10, 11, 12, 13, 14, 1, 2, 42, 41, 40, 39, 47, 21}
# which signal each usable GPIO carries; pinmap.json (from assign_pins.py) overrides this default
DEFAULT_MAP = {4: "IN1A", 5: "IN2A", 6: "IN3A", 7: "IN4A", 15: "IN1B", 16: "IN2B", 17: "IN3B", 18: "IN4B",
               8: "SDA", 9: "SCL", 10: "LCD_RST", 11: "MOSI", 12: "SCK", 13: "CS_L", 14: "CS_R", 21: "LCD_DC",
               1: "RLY1", 2: "RLY2", 42: "RLY3", 41: "TRIG", 40: "ECHO1_3V", 39: "ECHO2_3V"}
import os
pm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pinmap.json")
GPIO_MAP = {int(k): v for k, v in json.load(open(pm_path)).items()} if ("--pinmap" in sys.argv and os.path.exists(pm_path)) else DEFAULT_MAP
FREE = sorted(SAFE - set(GPIO_MAP))                        # safe pins no signal uses: brought out on the spare header
SPARE_GPIOS = [3, 46, 45, 48, 38] + FREE
FIXED = {"3V3": "ESP3V3", "5V": "ESP5V", "G": "GND", 43: "UART_TX", 44: "UART_RX"}
for _g in SPARE_GPIOS:
    FIXED[_g] = "SPARE%d" % _g


def pin_net(g):
    return GPIO_MAP.get(g) or FIXED.get(g) or ""


J1 = [pin_net(g) for g in J1_PINS]
J3 = [pin_net(g) for g in J3_PINS]
footprint("J1", "ESP32-S3 row 1 (3V3 RST 4 5 ...)", pads_from(row(ESP_X1, lower_y, J1)))
footprint("J3", "ESP32-S3 row 2 (GND TX RX 1 2 ...)", pads_from(row(ESP_X1, upper_y, J3)))
silk_rect(PCB_X0, PCB_Y0, PCB_X1, PCB_Y1)                                   # the carrier PCB
silk_rect(PCB_X0 - ANT_LEN, ESP_CY - ANT_W / 2, PCB_X0, ESP_CY + ANT_W / 2)   # antenna part
for off in (6.2, 18.4):                                                       # the two USB-C sockets (end marks)
    silk_rect(PCB_X1 - 0.5, PCB_Y1 - off - 4.45, PCB_X1, PCB_Y1 - off + 4.45)
silk_text(PCB_X1 - 11.0, PCB_Y1 - 12.3, "USB-C", 1.0)
silk_text(PCB_X0 - ANT_LEN / 2, ESP_CY, "ANTENNA", 1.0, angle=90)
silk_text((PCB_X0 + PCB_X1) / 2, ESP_CY, "ESP32-S3 DEVKIT  USB-C END ->", 1.2)
for i, g in enumerate(J1_PINS):
    silk_text(ESP_X1 + i * PITCH, lower_y + 2.7, str(g), 1.0, angle=90)
for i, g in enumerate(J3_PINS):
    silk_text(ESP_X1 + i * PITCH, upper_y - 2.7, str(g), 1.0, angle=90)

# ------------------------------------------------------------------ DRV8833 x2 (HW-627: two rows of 6 holes)
# Pin names as read from the user's module. IN row (top here), left to right: IN1 IN2 VCC GND IN3 IN4  (VCC = motor supply, the board's VBAT)
# other row (bottom, with the white plug), left to right: EEP OUT1 OUT2 OUT3 OUT4 ULT  (EEP and ULT are not used).
# DRV_GAP = distance between the two rows; the alignment (EEP across from IN1) and the gap still have to be confirmed on the real module.
DRV_GAP = float(os.environ.get("DRV_GAP", "16.0"))
for nm, x0, ins in (("A", 34.0, ("IN1A", "IN2A", "IN3A", "IN4A")), ("B", 60.0, ("IN1B", "IN2B", "IN3B", "IN4B"))):
    y0 = 29.5
    outs = ("M1A", "M1B", "M2A", "M2B") if nm == "A" else ("M3A", "M3B", "M4A", "M4B")
    hx = x0 + 4.15                          # first hole of both rows (rows are 12.7 mm long, centred in the 21 mm outline)
    top_y, bot_y = y0 + 1.5 + DRV_GAP, y0 + 1.5
    upper = row(hx, top_y, [ins[0], ins[1], "VBAT", "GND", ins[2], ins[3]])
    lower = row(hx, bot_y, ["", outs[0], outs[1], outs[2], outs[3], ""])
    footprint("DRV" + nm, "DRV8833 " + nm, pads_from(upper) + pads_from(lower))
    silk_rect(x0, y0, x0 + 21.0, y0 + DRV_GAP + 3.0)
    silk_line(x0 + 0.1, y0 + 0.25, x0 + 20.9, y0 + 0.25, 0.5)      # thick bar on the plug side: a module turned round is obvious
    silk_text(x0 + 10.5, y0 + DRV_GAP / 2 + 2.2, "DRV8833 " + nm, 1.0)
    silk_text(x0 + 10.5, y0 + DRV_GAP / 2 + 0.4, "white plug v", 1.0)
    for i, lab in enumerate(["IN1", "IN2", "VCC", "GND", "IN3", "IN4"]):
        silk_text(hx + i * PITCH, top_y - 2.85, lab, 1.0, angle=90)
    for i, lab in enumerate(["EEP", "OUT1", "OUT2", "OUT3", "OUT4", "ULT"]):
        silk_text(hx + i * PITCH, bot_y + 3.2, lab, 1.0, angle=90)

# ------------------------------------------------------------------ PCA9685 (63 x 25.4 mm; 6-pin header on a SHORT end)
PX, PY, PL, PWD = 11.0, 2.0, 63.0, 25.4
# servo plugs face the bottom edge, the power terminal faces up. The header at this (left) end reads, top to bottom:
# GND OE SCL SDA VCC V+  (OE is left open; V+ is servo power from SERVO 5V IN)
pca_x = PX + 1.3
pca_y0 = PY + PWD / 2 + 2.5 * PITCH
pca_names = ["GND", "", "SCL", "SDA", "ESP3V3", "SERVO5"]
footprint("PCA", "PCA9685 header (GND OE SCL SDA VCC V+)",
          [(pca_x, pca_y0 - i * PITCH, n) for i, n in enumerate(pca_names)])
silk_rect(PX, PY, PX + PL, PY + PWD)
silk_text(PX + 36, PY + 14, "PCA9685 SERVO BOARD", 1.2)
silk_text(PX + 36, PY + 9, "servo plugs face this edge  v", 1.0)
silk_text(PX + 36, PY + 20, "power terminal faces up", 1.0)
for i, n in enumerate(("GND", "OE", "SCL", "SDA", "VCC", "V+")):
    silk_text(pca_x + 3.6, pca_y0 - i * PITCH, n, 1.0)

# ------------------------------------------------------------------ gyro GY-521: INT AD0 XCL XDA SDA SCL GND VCC (left to right)
GX, GY = 11.0, 48.0
gyro_y = GY + 16.4 - 1.5
footprint("GYRO", "GY-521 (INT AD0 XCL XDA SDA SCL GND VCC)", pads_from(row(GX + 1.4, gyro_y,
                                         ["", "", "", "", "SDA", "SCL", "GND", "ESP3V3"])))
silk_rect(GX, GY, GX + 21.2, GY + 16.4)
silk_text(GX + 10.6, GY + 6, "GY-521 GYRO", 1.0)
for i, n in enumerate(("INT", "AD0", "XCL", "XDA", "SDA", "SCL", "GND", "VCC")):
    silk_text(GX + 1.4 + i * PITCH, gyro_y - 3.4, n, 1.0, angle=90)

# screens and the spare header sit in the free strip above the ESP32, next to the pins they use
TOP_Y = 95.8
SCR_PINS = ["CS", "DC", "RST", "SDA", "SCL", "VCC", "GND"]
SCR_L_X, SCR_R_X = 37.0, 55.0
footprint("SCR_L", "SCREEN L", pads_from(row(SCR_L_X, TOP_Y, ["CS_L", "LCD_DC", "LCD_RST", "MOSI", "SCK", "RAILC", "GND"])))
footprint("SCR_R", "SCREEN R", pads_from(row(SCR_R_X, TOP_Y, ["CS_R", "LCD_DC", "LCD_RST", "MOSI", "SCK", "RAILC", "GND"])))
silk_text(SCR_L_X + 3 * PITCH, TOP_Y - 1.68, "SCREEN L", 1.0)
silk_text(SCR_R_X + 3 * PITCH, TOP_Y - 1.68, "SCREEN R", 1.0)
for x0 in (SCR_L_X, SCR_R_X):
    for i, lab in enumerate(SCR_PINS):
        silk_text(x0 + i * PITCH, TOP_Y + 2.48, lab, 1.0, angle=90)
spare_names = ["GND", "ESP3V3"] + ["SPARE%d" % g for g in SPARE_GPIOS]
spare_x = 73.2
footprint("SPARE", "SPARE IO", pads_from(row(spare_x, TOP_Y, spare_names)))
silk_text(spare_x + 8.9, TOP_Y - 1.68, "SPARE IO", 1.0)
for i, lab in enumerate(["GND", "3V3"] + [str(g) for g in SPARE_GPIOS]):
    silk_text(spare_x + i * PITCH, TOP_Y + 2.48, lab, 1.0, angle=90)

# ------------------------------------------------------------------ cable headers on two strips
S1, S2, X0 = 61.0, 56.6, 35.0
HDR_GAP = float(os.environ.get("HDR_GAP", "3.0"))      # extra space between neighbouring cable headers
strip_x = {}


def strip(y, items):
    """Cable headers in a row. Pin functions are printed rotated above (strip S1) or below (strip S2) each pin;
    the module name sits on the other side, close to the pins."""
    x = X0
    for ref, label, names, funcs in items:
        footprint(ref, label, pads_from(row(x, y, names)))
        for i, f in enumerate(funcs):
            if y == S1:
                silk_text(x + i * PITCH, y + 2.55, f, 1.0, angle=90)
            else:
                silk_text(x + i * PITCH, y - 2.75, f, 1.0, angle=90)
        silk_text(x + (len(names) - 1) * PITCH / 2, y - 1.75 if y == S1 else y - 5.3, label, 1.0)
        strip_x[ref] = x
        x += len(names) * PITCH + HDR_GAP


strip(S1, [("RLY1H", "RELAY 1", ["RAILC", "RLY1", "GND"], ["VCC", "IN", "GND"]),
           ("RLY2H", "RELAY 2", ["RAILC", "RLY2", "GND"], ["VCC", "IN", "GND"]),
           ("RLY3H", "RELAY 3", ["RAILC", "RLY3", "GND"], ["VCC", "IN", "GND"]),
           ("SON1", "SONAR 1", ["ESP5V_S", "TRIG", "ECHO1_5V", "GND"], ["VCC", "TRG", "ECH", "GND"]),
           ("SON2", "SONAR 2", ["ESP5V_S", "TRIG", "ECHO2_5V", "GND"], ["VCC", "TRG", "ECH", "GND"])])
strip(S2, [("I2C", "I2C SENSOR", ["ESP3V3", "GND", "SDA", "SCL"], ["3V3", "GND", "SDA", "SCL"]),
           ("UART", "UART", ["GND", "UART_TX", "UART_RX"], ["GND", "TX", "RX"])])

# ------------------------------------------------------------------ small parts (vertical resistors, 2.54 mm)
RY = 57.5


def resistor(ref, value, x, y, a, b):
    footprint(ref, value, [(x, y, a), (x, y + 2.54, b)], drill=0.9, dia=1.7, first_square=False)


# sonar echo dividers: 5V echo -1k- 3V echo -2k- GND (value printed under each; swapping them would give the ESP only 1.7 V)
for k, (ech5, ech3) in enumerate((("ECHO1_5V", "ECHO1_3V"), ("ECHO2_5V", "ECHO2_3V"))):
    bx = strip_x["SON%d" % (k + 1)] + 1.5
    footprint("RD%da" % (k + 1), "1k", [(bx, RY, ech5), (bx + 2.54, RY, ech3)], drill=0.9, dia=1.7, first_square=False)
    footprint("RD%db" % (k + 1), "2k", [(bx + 5.0, RY, ech3), (bx + 7.54, RY, "GND")], drill=0.9, dia=1.7,
              first_square=False)
    silk_text(bx + 1.27, RY - 2.05, "1k", 1.0)
    silk_text(bx + 6.27, RY - 2.05, "2k", 1.0)

# Schottky diode: 5V clean -> ESP 5V pin (so USB power can never back-feed the buck)
footprint("D1", "Schottky 1N5819", [(91.0, 56.0, "CLEAN5"), (91.0, 63.62, "ESP5V")], drill=1.0, dia=1.8)
silk_text(95.4, 59.8, "D1 1N5819", 1.0, angle=90)
silk_text(93.2, 56.0, "A", 1.0)       # square pad = anode, from CLEAN 5V
silk_text(93.2, 63.62, "K", 1.0)      # cathode (band side) = ESP32 5V pin

# ------------------------------------------------------------------ screw terminals, all 5.08 mm pitch (PROVISIONAL polarity: lower pin = +)
# left edge: the battery in, and the three outputs of the OFF-BOARD buck modules coming back in (the bucks get their battery
# power from the pack directly, outside the board). The slot number is the position along the edge (10.16 mm per terminal).
LEFT = [("SERVO 5V IN", "SERVO5", 0), ("BATT IN", "VBAT", 1), ("CLEAN 5V IN", "CLEAN5", 5), ("3.3V IN", "RAILC", 6)]
for i, (label, plus, slot) in enumerate(LEFT):
    y0 = 10.0 + slot * 2 * 5.08
    footprint("TL%d" % i, label, [(5.5, y0 + 2.54, plus), (5.5, y0 + 7.62, "GND")], drill=1.3, dia=2.8)
    silk_text(7.9, y0 + 2.54, "+", 1.0)
    silk_text(7.9, y0 + 7.62, "-", 1.0)
    silk_text(9.3, y0 + 5.08, label, 1.0, angle=90)
# extra power outlets in the gap the three removed terminals left: 2 x clean 5 V and 2 x 3.3 V (both from the bucks, not the ESP32
# pin) in the upper row, 4 x GND in the lower row, so every power pin has a ground right below it for a 2-wire plug
PW_X, PW_Y = 6.0, 36.0
pw_up = ["CLEAN5", "CLEAN5", "RAILC", "RAILC"]
footprint("PWR", "POWER OUT (5V 5V 3V3 3V3 / GND x4)",
          [(PW_X + i * PITCH, PW_Y + PITCH, n) for i, n in enumerate(pw_up)] + [(PW_X + i * PITCH, PW_Y, "GND") for i in range(4)])
for i, lab in enumerate(("5V", "5V", "3V3", "3V3")):
    silk_text(PW_X + i * PITCH, PW_Y + PITCH + 2.55, lab, 1.0, angle=90)
for i in range(4):
    silk_text(PW_X + i * PITCH, PW_Y - 2.85, "GND", 1.0, angle=90)
silk_text(PW_X + 1.5 * PITCH, PW_Y + PITCH + 6.3, "POWER OUT", 1.0)
# right edge: the four motors, 2-pin positions on a 2.54 mm grid for the 2-pin JST plugs (pad 1 / pad 2 = the two motor wires)
for k, (a, b) in enumerate((("M1A", "M1B"), ("M2A", "M2B"), ("M3A", "M3B"), ("M4A", "M4B")), start=1):
    yc = 10.0 + (k - 1) * 2 * 5.08 + 5.08
    footprint("TM%d" % k, "MOTOR %d (2-pin JST)" % k, [(94.5, yc - 1.27, a), (94.5, yc + 1.27, b)])
    silk_text(90.0, yc, "M%d" % k, 1.0, angle=90)

# ------------------------------------------------------------------ capacitors
footprint("C1", "470uF pack", [(77.75, 15.0, "VBAT"), (81.25, 15.0, "GND")], drill=1.0, dia=2.0)
footprint("C2", "100uF 3V3", [(78.25, 6.0, "RAILC"), (80.75, 6.0, "GND")], drill=0.9, dia=1.8)
footprint("C3", "100nF pack", [(87.0, 8.23, "VBAT"), (87.0, 10.77, "GND")], drill=0.8, dia=1.6, first_square=False)
footprint("C4", "100nF 3V3", [(87.0, 2.73, "RAILC"), (87.0, 5.27, "GND")], drill=0.8, dia=1.6, first_square=False)
silk_text(75.6, 15.0, "+", 1.0)                      # electrolytic: the square pad and the long leg are plus
silk_text(81.0, 17.3, "C1 470uF 16V", 1.0)
silk_text(76.1, 6.0, "+", 1.0)
silk_text(80.0, 3.7, "C2 100uF 10V", 1.0)
silk_text(81.5, 9.5, "C3 100n", 1.0)
silk_text(81.5, 1.7, "C4 100n", 1.0)

# CLEAN 5V also feeds the sonar VCC pins (separate from the diode-protected ESP5V pin)
for p in board.GetPads():
    if p.GetNetname() == "ESP5V_S":
        p.SetNet(net("CLEAN5"))

# ------------------------------------------------------------------ rules
ds = board.GetDesignSettings()
board.SetCopperLayerCount(LAYERS)
CLR = 0.15 if FINE else 0.2
TRK = 0.25 if FINE else 0.3
VIA_D, VIA_H = (0.6, 0.3) if FINE else (0.8, 0.4)
ds.m_TrackMinWidth = FromMM(0.2)
ds.m_MinClearance = FromMM(CLR)
ds.m_ViasMinSize = FromMM(0.6)
ds.m_MinThroughDrill = FromMM(0.3)
ds.m_CopperEdgeClearance = FromMM(0.3)
ds.m_HoleToHoleMin = FromMM(0.5)
ds.m_MinResolvedSpokes = 1   # a ground pad with one thermal spoke is still tied on the other layer (top pour is solid)
dnc = ds.m_NetSettings.m_DefaultNetClass
dnc.SetClearance(FromMM(CLR))
dnc.SetTrackWidth(FromMM(TRK))
dnc.SetViaDiameter(FromMM(VIA_D))
dnc.SetViaDrill(FromMM(VIA_H))

# ------------------------------------------------------------------ keep-out under the antenna + ground pours
def zone(layers, pts, netname=None, keepout=False, full=False):
    z = pcbnew.ZONE(board)
    ls = pcbnew.LSET()
    for l in layers:
        ls.AddLayer(l)
    z.SetLayerSet(ls)
    if keepout:
        z.SetIsRuleArea(True)
        z.SetDoNotAllowCopperPour(True)
        z.SetDoNotAllowTracks(True)
        z.SetDoNotAllowVias(True)
        z.SetDoNotAllowPads(False)
        z.SetDoNotAllowFootprints(False)
    else:
        z.SetNet(net(netname))
        z.SetMinThickness(FromMM(0.25))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL if full else pcbnew.ZONE_CONNECTION_THERMAL)
        z.SetThermalReliefGap(FromMM(0.3))
        z.SetThermalReliefSpokeWidth(FromMM(0.4))
        z.SetLocalClearance(FromMM(0.25 if FINE else 0.3))
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)   # no floating copper scraps (e.g. beside a mounting hole)
    o = z.Outline()
    o.NewOutline()
    for (x, y) in pts:
        o.Append(P(x, y).x, P(x, y).y)
    board.Add(z)
    return z


copper = [pcbnew.F_Cu, pcbnew.B_Cu]
KO_X0 = 22.0                                   # 7 mm beyond the antenna tip, 4 mm beyond its sides
zone(copper, [(KO_X0, 66.0), (PCB_X0 + 0.6, 66.0), (PCB_X0 + 0.6, 94.0), (KO_X0, 94.0)], keepout=True)   # under/around the antenna
inset = 0.5
gnd_pts = [(inset, inset), (BW - inset, inset), (BW - inset, BH - inset), (inset, BH - inset)]
if LAYERS == 2:
    zone([pcbnew.B_Cu], gnd_pts, "GND")
    zone([pcbnew.F_Cu], gnd_pts, "GND", full=True)   # top pour solid: pins are soldered on the bottom
else:
    zone([pcbnew.In1_Cu], gnd_pts, "GND")
    zone([pcbnew.B_Cu], gnd_pts, "GND")

silk_text(14, 82, "ABADI MOTHERBOARD v5 (%dL)" % LAYERS, 1.0, angle=90)

# aux origin = lower-left corner so Gerber/drill files come out in plain mm, y up
ds.SetAuxOrigin(P(0, 0))
board.Save(OUT)
json.dump({n: i for i, n in enumerate(sorted(nets))}, open(OUT + ".nets.json", "w"))
print("saved", OUT, "| layers", LAYERS, "| footprints", len(board.GetFootprints()), "| nets", len(nets),
      "| pads", len(board.GetPads()))
