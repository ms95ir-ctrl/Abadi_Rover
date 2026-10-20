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
     "Everything here follows the module pin orders I assumed. Check each one against your real module before ordering.\n",
     "## ESP32-S3 DevKit: which signal each pin carries (pin 1 is the antenna end of each row; row 1 = 3V3 3V3 RST ..., row 2 = GND TX RX ...)\n", "| Header | Pin | GPIO / pin | Signal |", "|---|---|---|---|"]
for ref, names in (("J1", J1), ("J3", J3)):
    for (n, net), g in zip(pads(ref), names):
        L.append("| %s | %d | %s | %s |" % (ref, n, g, net or "-"))
L.append("\n## Other connectors (pin 1 = square pad)\n")
labels = {"DRVA": "DRV8833 A (2 rows: inputs row first, then power/outputs row)", "DRVB": "DRV8833 B", "PCA": "PCA9685 header at its LEFT short end (top to bottom)",
          "GYRO": "GY-521 (left to right as printed on the module)", "SCR_L": "Screen L", "SCR_R": "Screen R", "SPARE": "Spare IO (GPIO numbers are printed on the board)",
          "RLY1H": "Relay 1", "RLY2H": "Relay 2", "RLY3H": "Relay 3", "SON1": "Sonar 1", "SON2": "Sonar 2", "I2C": "I2C sensor", "UART": "UART",
          "TL0": "SERVO 5V IN (output of the servo buck)", "TL1": "BATT IN (battery pack, for the motors)",
          "TL2": "CLEAN 5V IN (output of the clean 5V buck)", "TL3": "3.3V IN (output of the 3.3V buck)", "PWR": "POWER OUT: upper row = clean 5V, clean 5V, 3.3V, 3.3V (from the bucks); lower row = GND x4", "TM1": "MOTOR 1 (2-pin, for a JST plug)", "TM2": "MOTOR 2 (2-pin)", "TM3": "MOTOR 3 (2-pin)", "TM4": "MOTOR 4 (2-pin)"}
for ref, name in labels.items():
    L.append("- **%s** (%s): %s" % (name, ref, ", ".join("%d=%s" % (n, net or "-") for n, net in pads(ref))))
L.append("\nLeft-edge screw terminals (5.08 mm pitch): the lower/first pin is **+**, marked on the board. Motor connectors are 2-pin spots on a 2.54 mm grid for JST plugs (motors have no polarity; swap the two wires to reverse): M1 = DRV A out 1, M2 = DRV A out 2, M3 = DRV B out 1, M4 = DRV B out 2.")
open(out + "/pin-table.md", "w").write("\n".join(L) + "\n")

groups = collections.OrderedDict()
for fp in sorted(b.GetFootprints(), key=lambda f: f.GetReference()):
    ref, val, n = fp.GetReference(), fp.GetValue(), len(list(fp.Pads()))
    if ref.startswith("H"):
        key = ("M3 mounting hole (screw + nut), 3.2 mm", 1)
    else:
        key = (val, n)
    groups.setdefault(key, []).append(ref)
P = ["# Parts list (generated from the board file)\n", "| Qty | Item | Pads | Refs |", "|---|---|---|---|"]
for (val, n), refs in groups.items():
    P.append("| %d | %s | %d | %s |" % (len(refs), val, n, ", ".join(refs)))
P.append("\nHeaders are standard 2.54 mm pitch; hole 1.0 mm. Resistors and the diode stand upright or lie flat on 2.54 / 7.62 mm spacing as drawn.")
open(out + "/parts-list.md", "w").write("\n".join(P) + "\n")
print("wrote pin-table.md and parts-list.md")
