#!/usr/bin/env python3
"""Final touches on a routed board: silkscreen text no smaller than a fab can print, refill pours, DRC report.

Usage: finish_board.py <in.kicad_pcb> <out.kicad_pcb>
"""
import sys

import pcbnew

b = pcbnew.LoadBoard(sys.argv[1])
n = 0
for d in b.GetDrawings():
    if d.GetClass() == "PCB_TEXT" and d.GetLayer() == pcbnew.F_SilkS:
        h = d.GetTextHeight()
        if h < 1.0e6:
            d.SetTextSize(pcbnew.VECTOR2I(int(1.0e6), int(1.0e6)))
            n += 1
        d.SetTextThickness(max(d.GetTextThickness(), int(0.15e6)))
print("silk labels enlarged to 1.0 mm:", n)
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
b.Save(sys.argv[2])
rep = sys.argv[2].rsplit(".", 1)[0] + "_drc.rpt"
pcbnew.WriteDRCReport(b, rep, pcbnew.EDA_UNITS_MILLIMETRES, True)
print("DRC report:", rep)
