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
for (a, b) in (((0, 0), (BW, 0)), ((BW, 0), (BW, BH)), ((BW, BH), (0, BH)), ((0, BH), (0, 0))):
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

# ------------------------------------------------------------------ ESP32-S3 DevKit (PROVISIONAL pin order)
ESP_Y0, ROW_GAP = 66.0, 22.86
lower_y, upper_y = ESP_Y0 + (25.4 - ROW_GAP) / 2, ESP_Y0 + (25.4 + ROW_GAP) / 2
# GPIO order on the two DevKit headers, pin 1 first (PROVISIONAL: check against your board)
J1_PINS = ["3V3", "3V3", "RST", 4, 5, 6, 7, 15, 16, 17, 18, 8, 3, 46, 9, 10, 11, 12, 13, 14, "5V", "G"]
J3_PINS = ["G", 43, 44, 1, 2, 42, 41, 40, 39, 38, 37, 36, 35, 0, 45, 48, 47, 21, 20, 19, "G", "G"]
# which signal each usable GPIO carries; pinmap.json (from assign_pins.py) overrides this default
DEFAULT_MAP = {4: "IN1A", 5: "IN2A", 6: "IN3A", 7: "IN4A", 15: "IN1B", 16: "IN2B", 17: "IN3B", 18: "IN4B",
               8: "SDA", 9: "SCL", 10: "LCD_RST", 11: "MOSI", 12: "SCK", 13: "CS_L", 14: "CS_R", 21: "LCD_DC",
               1: "RLY1", 2: "RLY2", 3: "RLY3", 41: "TRIG", 42: "ECHO1_3V", 40: "ECHO2_3V", 39: "TOUCH1",
               46: "TOUCH2"}
FIXED = {"3V3": "ESP3V3", "5V": "ESP5V", "G": "GND", 43: "UART_TX", 44: "UART_RX", 3: "SPARE3", 46: "SPARE46",
         45: "SPARE45", 48: "SPARE48", 38: "SPARE38", 47: "SPARE47"}
import os
pm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pinmap.json")
GPIO_MAP = {int(k): v for k, v in json.load(open(pm_path)).items()} if ("--pinmap" in sys.argv and os.path.exists(pm_path)) else DEFAULT_MAP


def pin_net(g):
    return GPIO_MAP.get(g) or FIXED.get(g) or ""


J1 = [pin_net(g) for g in J1_PINS]
J3 = [pin_net(g) for g in J3_PINS]
footprint("J1", "ESP32-S3 J1 (lower row)", pads_from(row(31.0, lower_y, J1)))
footprint("J3", "ESP32-S3 J3 (upper row)", pads_from(row(31.0, upper_y, J3)))
silk_rect(26.0, 66.0, 95.6, 91.4)
silk_text(62, 78.7, "ESP32-S3 DEVKIT  (USB-C end ->)", 1.2)
for i, g in enumerate(J1_PINS):
    silk_text(31.0 + i * PITCH, lower_y + 3.2, str(g), 0.9, angle=90)
for i, g in enumerate(J3_PINS):
    silk_text(31.0 + i * PITCH, upper_y - 3.2, str(g), 0.9, angle=90)

# ------------------------------------------------------------------ DRV8833 x2 (PROVISIONAL pin order)
for nm, x0, ins in (("A", 34.0, ("IN1A", "IN2A", "IN3A", "IN4A")), ("B", 60.0, ("IN1B", "IN2B", "IN3B", "IN4B"))):
    y0 = 29.5
    outs = ("M1A", "M1B", "M2A", "M2B") if nm == "A" else ("M3A", "M3B", "M4A", "M4B")
    upper = row(x0 + 4.0, y0 + 16.5, list(ins) + ["GND"])
    lower = row(x0 + 4.0, y0 + 1.5, ["VBAT"] + list(outs))
    footprint("DRV" + nm, "DRV8833 " + nm, pads_from(upper) + pads_from(lower))
    silk_rect(x0, y0, x0 + 21.0, y0 + 18.0)
    silk_text(x0 + 10.5, y0 + 9.0, "DRV8833 " + nm, 1.0)

# ------------------------------------------------------------------ PCA9685 (socket only; module sits above)
PX, PY = 11.0, 2.0
footprint("PCA", "PCA9685 control (GND OE SCL SDA VCC V+)",
          pads_from(row(PX + 12.0, PY + 25.4 - 1.5, ["GND", "", "SCL", "SDA", "ESP3V3", ""])))
silk_rect(PX, PY, PX + 62.5, PY + 25.4)
silk_text(PX + 31, PY + 13, "PCA9685 SERVO BOARD", 1.2)
silk_text(PX + 31, PY + 9.5, "servo plugs face this edge  v", 0.9)
silk_text(PX + 18, PY + 22.2, "V+ not used on header", 0.8)

# ------------------------------------------------------------------ gyro, I2C sensor, UART, spare
GX, GY = 11.0, 48.0
footprint("GYRO", "GY-521", pads_from(row(GX + 1.4, GY + 16.4 - 1.5,
                                         ["ESP3V3", "GND", "SCL", "SDA", "", "", "", ""])))
silk_rect(GX, GY, GX + 21.2, GY + 16.4)
silk_text(GX + 10.6, GY + 7, "GY-521 GYRO", 1.0)

# screens and the spare header sit in the free strip above the ESP32, next to the pins they use
TOP_Y = 95.0
footprint("SCR_L", "SCREEN L", pads_from(row(33.0, TOP_Y, ["RAILC", "GND", "CS_L", "LCD_RST", "LCD_DC", "MOSI", "SCK"])))
footprint("SCR_R", "SCREEN R", pads_from(row(53.0, TOP_Y, ["RAILC", "GND", "CS_R", "LCD_RST", "LCD_DC", "MOSI", "SCK"])))
silk_text(41, 97.9, "SCREEN L", 0.8)
silk_text(61, 97.9, "SCREEN R", 0.8)
footprint("SPARE", "SPARE IO", pads_from(row(73.0, TOP_Y, ["GND", "ESP3V3", "SPARE3", "SPARE46", "SPARE45", "SPARE48"])))
silk_text(79, 97.9, "SPARE IO", 0.8)

# ------------------------------------------------------------------ cable headers on two strips
S1, S2, X0 = 61.0, 54.5, 35.0
strip_x = {}


def strip(y, items):
    x = X0
    for ref, label, names in items:
        footprint(ref, label, pads_from(row(x, y, names)))
        silk_text(x + (len(names) - 1) * PITCH / 2, y + 2.6 if y == S1 else y - 2.6, label, 0.8)
        strip_x[ref] = x
        x += len(names) * PITCH + 1.9


strip(S1, [("RLY1H", "RELAY 1", ["RAILC", "RLY1_H", "GND"]), ("RLY2H", "RELAY 2", ["RAILC", "RLY2_H", "GND"]),
           ("RLY3H", "RELAY 3", ["RAILC", "RLY3_H", "GND"]),
           ("SON1", "SONAR 1", ["ESP5V_S", "TRIG", "ECHO1_5V", "GND"]),
           ("SON2", "SONAR 2", ["ESP5V_S", "TRIG", "ECHO2_5V", "GND"])])
strip(S2, [("I2C", "I2C SENSOR", ["ESP3V3", "GND", "SDA", "SCL"]), ("UART", "UART", ["GND", "UART_TX", "UART_RX"]),
           ("TCH1", "TOUCH 1", ["RAILC", "TOUCH1", "GND"]), ("TCH2", "TOUCH 2", ["RAILC", "TOUCH2", "GND"])])

# ------------------------------------------------------------------ small parts (vertical resistors, 2.54 mm)
RY = 57.5


def resistor(ref, value, x, y, a, b):
    footprint(ref, value, [(x, y, a), (x, y + 2.54, b)], drill=0.9, dia=1.7, first_square=False)


# relay series resistors: GPIO net -> header IN net
for i, rx in enumerate((35.0 + 2.54, 35.0 + 7.62 + 1.9 + 2.54, 35.0 + 2 * (7.62 + 1.9) + 2.54), start=1):
    footprint("RS%d" % i, "330R", [(rx - 1.27, RY, "RLY%d" % i), (rx + 1.27, RY, "RLY%d_H" % i)],
              drill=0.9, dia=1.7, first_square=False)
# sonar echo dividers: 5V echo -1k- 3V echo -2k- GND
sx = strip_x["SON1"]
for k, (ech5, ech3) in enumerate((("ECHO1_5V", "ECHO1_3V"), ("ECHO2_5V", "ECHO2_3V"))):
    bx = sx + k * 12.06 + 1.5
    footprint("RD%da" % (k + 1), "1k", [(bx, RY, ech5), (bx + 2.54, RY, ech3)], drill=0.9, dia=1.7, first_square=False)
    footprint("RD%db" % (k + 1), "2k", [(bx + 5.0, RY, ech3), (bx + 7.54, RY, "GND")], drill=0.9, dia=1.7,
              first_square=False)

# Schottky diode: 5V clean -> ESP 5V pin (so USB power can never back-feed the buck)
footprint("D1", "Schottky 1N5819", [(87.0, 57.0, "CLEAN5"), (87.0, 64.6, "ESP5V")], drill=1.0, dia=1.8)
silk_text(86.5, 60.8, "D1", 0.8, angle=90)

# ------------------------------------------------------------------ screw terminals (PROVISIONAL polarity: lower pin = +)
for i, (label, plus) in enumerate((("BATT IN", "VBAT"), ("TO BUCK 1", "VBAT"), ("TO BUCK 2", "VBAT"),
                                   ("TO BUCK 3", "VBAT"))):
    y0 = 10.0 + i * 2 * 5.08
    footprint("TL%d" % i, label, [(5.5, y0 + 2.54, plus), (5.5, y0 + 7.62, "GND")], drill=1.3, dia=2.8)
    silk_text(7.9, y0 + 2.54, "+", 1.0)
    silk_text(7.9, y0 + 7.62, "-", 1.0)
    silk_text(9.3, y0 + 5.08, label, 0.8, angle=90)
y = 12.0
for ref, label, short, plus in (("TR_5V", "CLEAN 5V IN", "5V IN", "CLEAN5"), ("TR_33", "3.3V IN", "3V3 IN", "RAILC")):
    footprint(ref, label, [(94.5, y + 1.75, plus), (94.5, y + 5.25, "GND")], drill=1.2, dia=2.4)
    silk_text(92.0, y + 1.75, "+", 1.0)
    silk_text(92.0, y + 5.25, "-", 1.0)
    silk_text(97.9, y + 3.5, short, 0.8, angle=90)
    y += 7.0
for k, (a, b) in enumerate((("M1A", "M1B"), ("M2A", "M2B"), ("M3A", "M3B"), ("M4A", "M4B")), start=1):
    footprint("TM%d" % k, "MOTOR %d" % k, [(94.5, y + 1.75, a), (94.5, y + 5.25, b)], drill=1.2, dia=2.4)
    silk_text(97.9, y + 3.5, "M%d" % k, 0.9, angle=90)
    y += 7.0

# ------------------------------------------------------------------ capacitors
footprint("C1", "470uF pack", [(77.75, 15.0, "VBAT"), (81.25, 15.0, "GND")], drill=1.0, dia=2.0, first_square=False)
footprint("C2", "100uF 3V3", [(78.25, 6.0, "RAILC"), (80.75, 6.0, "GND")], drill=0.9, dia=1.8, first_square=False)
footprint("C3", "100nF pack", [(87.0, 8.23, "VBAT"), (87.0, 10.77, "GND")], drill=0.8, dia=1.6, first_square=False)
footprint("C4", "100nF 3V3", [(87.0, 2.73, "RAILC"), (87.0, 5.27, "GND")], drill=0.8, dia=1.6, first_square=False)

# thick VBAT bus beside the battery terminals (3 mm, bottom layer): BATT IN + the three feeds to the bucks
def track(x1, y1, x2, y2, width, netname, layer=pcbnew.B_Cu):
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(P(x1, y1))
    t.SetEnd(P(x2, y2))
    t.SetWidth(FromMM(width))
    t.SetLayer(layer)
    t.SetNet(net(netname))
    board.Add(t)


BUS_X = 2.1
vb_ys = [10.0 + i * 2 * 5.08 + 2.54 for i in range(4)]
track(BUS_X, vb_ys[0], BUS_X, vb_ys[-1], 3.0, "VBAT")
for vy in vb_ys:
    track(BUS_X, vy, 5.5, vy, 3.0, "VBAT")

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
    o = z.Outline()
    o.NewOutline()
    for (x, y) in pts:
        o.Append(P(x, y).x, P(x, y).y)
    board.Add(z)
    return z


copper = [pcbnew.F_Cu, pcbnew.B_Cu]
zone(copper, [(26, 66), (30.2, 66), (30.2, 91.4), (26, 91.4)], keepout=True)   # antenna end, before pin 1
silk_text(28.1, 79, "ANT", 0.9, angle=90)
inset = 0.5
gnd_pts = [(inset, inset), (BW - inset, inset), (BW - inset, BH - inset), (inset, BH - inset)]
if LAYERS == 2:
    zone([pcbnew.B_Cu], gnd_pts, "GND")
    zone([pcbnew.F_Cu], gnd_pts, "GND", full=True)   # top pour solid: pins are soldered on the bottom
else:
    zone([pcbnew.In1_Cu], gnd_pts, "GND")
    zone([pcbnew.B_Cu], gnd_pts, "GND")

silk_text(9, 75, "ABADI ROBOT MOTHERBOARD  DRAFT v2  %d LAYER" % LAYERS, 1.0, angle=90)

# aux origin = lower-left corner so Gerber/drill files come out in plain mm, y up
ds.SetAuxOrigin(P(0, 0))
board.Save(OUT)
json.dump({n: i for i, n in enumerate(sorted(nets))}, open(OUT + ".nets.json", "w"))
print("saved", OUT, "| layers", LAYERS, "| footprints", len(board.GetFootprints()), "| nets", len(nets),
      "| pads", len(board.GetPads()))
