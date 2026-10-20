#!/usr/bin/env python3
"""Write pin-table.md and parts-list.md from the routed board, so the documents always match the design.

Usage: make_docs.py <board.kicad_pcb> <out_dir>
"""
import collections
import sys

import pcbnew

b = pcbnew.LoadBoard(sys.argv[1])
out = sys.argv[2]
J1 = ["3V3", "3V3", "RST", 4, 5, 6, 7, 15, 16, 17, 18, 8, 3, 46, 9, 10, 11, 12, 13, 14, "5V", "G"]
J3 = ["G", "TX(43)", "RX(44)", 1, 2, 42, 41, 40, 39, 38, 37, 36, 35, 0, 45, 48, 47, 21, 20, 19, "G", "G"]


def pads(ref):
    fp = b.FindFootprintByReference(ref)
    return sorted(((int(p.GetNumber()), p.GetNetname()) for p in fp.Pads()))


L = ["# Pin table (generated from the board file - PROVISIONAL)\n",
     "The DRV8833 and screen pin orders are the owner's readings of the real modules; the relay, sonar, gyro and PCA9685 orders match the owner's photos and the usual orders; the I2C and UART headers have no module behind them. Compare each printed name with your real module before ordering.\n",
     "## ESP32-S3 DevKit: which signal each pin carries (pin 1 is the antenna end of each row; row 1 = 3V3 3V3 RST ..., row 2 = GND TX RX ...)\n", "| Header | Pin | GPIO / pin | Signal |", "|---|---|---|---|"]
for ref, names in (("J1", J1), ("J3", J3)):
    for (n, net), g in zip(pads(ref), names):
        L.append("| %s | %d | %s | %s |" % (ref, n, g, net or "-"))
L.append("\n## Other connectors (pin 1 = square pad)\n")
labels = {"DRVA": "DRV8833 A, HW-627 module (pins 1-6 = top row left to right IN1 IN2 VCC GND IN3 IN4, VCC = battery; pins 7-12 = bottom row, the side with the white plug, EEP OUT1 OUT2 OUT3 OUT4 ULT; EEP and ULT are not used)", "DRVB": "DRV8833 B (same layout as DRV A)", "PCA": "PCA9685 header at its LEFT short end (top to bottom)",
          "GYRO": "GY-521 (left to right as printed on the module)", "SCR_L": "Screen L (CS DC RST SDA SCL VCC GND)", "SCR_R": "Screen R (CS DC RST SDA SCL VCC GND)", "SPARE": "Spare IO (GPIO numbers are printed on the board)",
          "RLY1H": "Relay 1", "RLY2H": "Relay 2", "RLY3H": "Relay 3", "SON1": "Sonar 1", "SON2": "Sonar 2", "I2C": "I2C sensor", "UART": "UART",
          "TL0": "SERVO 5V IN (output of the servo buck)", "TL1": "BATT IN (battery pack, for the motors)",
          "TL2": "CLEAN 5V IN (output of the clean 5V buck)", "TL3": "3.3V IN (output of the 3.3V buck)", "PWR": "POWER OUT: upper row = clean 5V, clean 5V, 3.3V, 3.3V (from the bucks); lower row = GND x4", "TM1": "MOTOR 1 (2-pin, for a JST plug)", "TM2": "MOTOR 2 (2-pin)", "TM3": "MOTOR 3 (2-pin)", "TM4": "MOTOR 4 (2-pin)"}
for ref, name in labels.items():
    L.append("- **%s** (%s): %s" % (name, ref, ", ".join("%d=%s" % (n, net or "-") for n, net in pads(ref))))
L.append("\nLeft-edge screw terminals (5.08 mm pitch): the lower/first pin is **+**, marked on the board. Motor connectors are 2-pin spots on a 2.54 mm grid for JST plugs (motors have no polarity; swap the two wires to reverse): M1 = DRV A OUT1+OUT2 (driven by IN1A/IN2A), M2 = DRV A OUT3+OUT4 (IN3A/IN4A), M3 = DRV B OUT1+OUT2, M4 = DRV B OUT3+OUT4.")
open(out + "/pin-table.md", "w").write("\n".join(L) + "\n")

groups = collections.OrderedDict()
for fp in sorted(b.GetFootprints(), key=lambda f: f.GetReference()):
    ref, val, n = fp.GetReference(), fp.GetValue(), len(list(fp.Pads()))
    if ref.startswith("H"):
        key = ("M3 mounting hole (screw + nut), 3.2 mm", 1)
    else:
        key = (val, n)
    groups.setdefault(key, []).append(ref)
BUY = {
    "C1": "470 uF electrolytic capacitor, 16 V or higher (25 V is fine), radial, 3.5 mm lead spacing; long leg / no stripe = + (square pad)",
    "C2": "100 uF electrolytic capacitor, 10 V or higher, radial, 2.5 mm lead spacing; long leg / no stripe = + (square pad)",
    "C3": "100 nF ceramic capacitor (marked 104), 16 V or higher, 2.54 mm lead spacing, no polarity",
    "C4": "100 nF ceramic capacitor (marked 104), 16 V or higher, 2.54 mm lead spacing, no polarity",
    "D1": "1N5819 Schottky diode; the stripe end = K, goes to the hole marked K",
    "RD1a": "1 kOhm resistor, 1/4 W, stands upright", "RD2a": "1 kOhm resistor, 1/4 W, stands upright",
    "RD1b": "2 kOhm resistor, 1/4 W, stands upright", "RD2b": "2 kOhm resistor, 1/4 W, stands upright",
    "TL0": "screw terminal, 2-pole, 5.08 mm pitch (hole 1.3 mm)", "TL1": "screw terminal, 2-pole, 5.08 mm pitch (hole 1.3 mm)",
    "TL2": "screw terminal, 2-pole, 5.08 mm pitch (hole 1.3 mm)", "TL3": "screw terminal, 2-pole, 5.08 mm pitch (hole 1.3 mm)",
    "TM1": "2-pin 2.54 mm header or JST socket for the motor plug", "TM2": "2-pin 2.54 mm header or JST socket for the motor plug",
    "TM3": "2-pin 2.54 mm header or JST socket for the motor plug", "TM4": "2-pin 2.54 mm header or JST socket for the motor plug",
    "J1": "22-pin female socket, 2.54 mm (the ESP32-S3 devkit's pins plug in)", "J3": "22-pin female socket, 2.54 mm (the ESP32-S3 devkit's pins plug in)",
    "DRVA": "two 1x6 female sockets, 2.54 mm (or solder the module's pins straight in)", "DRVB": "two 1x6 female sockets, 2.54 mm (or solder the module's pins straight in)",
    "PCA": "1x6 pin header (pins down, plastic on the module's underside) plus a 1x6 socket on the board, or solder straight in",
    "GYRO": "1x8 female socket, 2.54 mm",
    "PWR": "2x4 pin header, 2.54 mm",
}
P = ["# Parts list (generated from the board file)\n", "| Qty | Item | Pads | Refs |", "|---|---|---|---|"]
for (val, n), refs in groups.items():
    item = BUY.get(refs[0]) or (val if val.startswith("M3 mounting") else "%d-pin 2.54 mm male header or JST-XH socket (%s)" % (n, val))
    P.append("| %d | %s | %d | %s |" % (len(refs), item, n, ", ".join(refs)))
P.append("\nCable ports (relay, sonar, screen, I2C, UART, SPARE IO): standard 2.54 mm male pin headers, or JST-XH sockets (2.5 mm pitch; "
         "the owner's plugs fit this spacing). Power outputs and ground on the POWER OUT header: about 2 A per rail at most. "
         "The two resistors per sonar stand upright (holes 2.54 mm apart); D1 lies flat (holes 7.62 mm apart). "
         "See shopping-list.md for the parts that are not on the board (bucks, BMS, charger, fuses, connectors).")
open(out + "/parts-list.md", "w").write("\n".join(P) + "\n")
print("wrote pin-table.md and parts-list.md")
