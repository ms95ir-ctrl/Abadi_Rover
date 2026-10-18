#!/usr/bin/env python3
"""Auto-route a board made by build_board.py with Freerouting, fill the pours, run KiCad's DRC.

Usage: route_board.py <in.kicad_pcb> <out.kicad_pcb> <freerouting.jar> [passes]
"""
import os
import re
import subprocess
import sys

import pcbnew

src, dst, jar = sys.argv[1], sys.argv[2], sys.argv[3]
SEED = int(os.environ.get("ROUTE_SEED", "0"))
passes = sys.argv[4] if len(sys.argv) > 4 else "60"
work = os.path.splitext(dst)[0]


def import_ses(board, ses_path, nets):
    """KiCad 7's python cannot import a .ses into a loaded board, so read the routes directly.
    SES units: resolution 'um 10' = 0.1 um, y is mirrored (y_kicad = -y_ses), same origin as the exported DSN."""
    s = open(ses_path).read()
    scale = 1000.0 / 10.0 if False else 1.0
    layers = {"F.Cu": pcbnew.F_Cu, "B.Cu": pcbnew.B_Cu, "In1.Cu": pcbnew.In1_Cu, "In2.Cu": pcbnew.In2_Cu}
    count_w = count_v = 0
    for nm in re.finditer(r"\(net (\S+)\s", s):
        pass
    # walk net blocks of network_out
    out = s[s.index("(network_out"):]
    for blk in re.finditer(r"\(net (\"[^\"]*\"|\S+)\s*(.*?)\n\s{4}\)", out, re.S):
        name = blk.group(1).strip('"')
        if name not in nets:
            continue
        body = blk.group(2)
        for w in re.finditer(r"\(wire\s*\(path (\S+) (\d+)\s+([-\d.\s]+)\)", body):
            lay, width = layers[w.group(1)], int(w.group(2))
            nums = [float(v) for v in w.group(3).split()]
            pts = list(zip(nums[0::2], nums[1::2]))
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                if (x1, y1) == (x2, y2):
                    continue
                t = pcbnew.PCB_TRACK(board)
                t.SetStart(pcbnew.VECTOR2I(int(round(x1 * 100)), int(round(-y1 * 100))))
                t.SetEnd(pcbnew.VECTOR2I(int(round(x2 * 100)), int(round(-y2 * 100))))
                t.SetWidth(width * 100)
                t.SetLayer(lay)
                t.SetNet(nets[name])
                board.Add(t)
                count_w += 1
        for v in re.finditer(r"\(via (\S+) ([-\d.]+) ([-\d.]+)", body):
            via = pcbnew.PCB_VIA(board)
            via.SetPosition(pcbnew.VECTOR2I(int(round(float(v.group(2)) * 100)), int(round(-float(v.group(3)) * 100))))
            dnc = board.GetDesignSettings().m_NetSettings.m_DefaultNetClass
            via.SetWidth(dnc.GetViaDiameter())
            via.SetDrill(dnc.GetViaDrill())
            via.SetViaType(pcbnew.VIATYPE_THROUGH)
            via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
            via.SetNet(nets[name])
            board.Add(via)
            count_v += 1
    print("imported", count_w, "track segments and", count_v, "vias from", os.path.basename(ses_path))


board = pcbnew.LoadBoard(src)
dsn, ses = work + ".dsn", work + ".ses"
assert pcbnew.ExportSpecctraDSN(board, dsn)
txt = open(dsn).read()

# ground is poured after routing: hide the pours from the router (a "plane" would block every other net)
txt = re.sub(r"\n\s*\(plane GND \(polygon [^)]*\)\)", "", txt)
txt = re.sub(r"\n\s*\(net GND\n\s*\(pins[^)]*\)\n\s*\)", "", txt)

txt = re.sub(r"(\(layer In1\.Cu\s*\(type) signal", r"\1 power", txt)
via_name = re.search(r'\(via ("?[^")\s]+"?)\)', txt).group(1)
base_w = int(re.search(r"\(rule\s+\(width (\d+)\)", txt).group(1))
clr = re.search(r"\(clearance ([\d.]+)\)", txt).group(1)
m = re.search(r"\(class kicad_default (.*?)\n\s*\(circuit", txt, re.S)
names = [n for n in m.group(1).split() if n not in ('""', "GND")]
wide = {"VBAT": 2000, "M1A": 1000, "M1B": 1000, "M2A": 1000, "M2B": 1000, "M3A": 1000, "M3B": 1000,
        "M4A": 1000, "M4B": 1000, "RAILC": 500, "CLEAN5": 500, "ESP5V": 500}
classes = {}
for n in names:
    classes.setdefault(wide.get(n, base_w), []).append(n)
blocks = []
for w, ns in sorted(classes.items()):
    blocks.append("    (class w%d %s\n      (circuit\n        (use_via %s)\n      )\n"
                  "      (rule\n        (width %d)\n        (clearance %s)\n      )\n    )"
                  % (w, " ".join(ns), via_name, w, clr))
start = txt.index("    (class kicad_default")
end_marker = txt.index("\n    )\n", start) + len("\n    )\n")
txt = txt[:start] + "\n".join(blocks) + "\n" + txt[end_marker:]
if SEED:   # the router is deterministic, so vary the order the nets are presented in
    import random
    nb = re.search(r"  \(network\n(.*?)\n    \(class ", txt, re.S)
    net_blocks = re.findall(r"    \(net .*?\n    \)", nb.group(1), re.S)
    random.Random(SEED).shuffle(net_blocks)
    txt = txt[:nb.start(1)] + "\n".join(net_blocks) + txt[nb.end(1):]
open(dsn, "w").write(txt)

cmd = ["java", "-jar", jar, "-de", dsn, "-do", ses, "-mp", passes]
print("running:", " ".join(cmd))
r = subprocess.run(cmd, capture_output=True, text=True, timeout=3000)
tail = (r.stdout + r.stderr).strip().splitlines()[-25:]
print("\n".join(l for l in tail if "Picked up" not in l))
if not os.path.exists(ses):
    sys.exit("no .ses written - routing failed")

board = pcbnew.LoadBoard(src)
nets_by_name = {}
for pad in board.GetPads():
    if pad.GetNetname():
        nets_by_name[pad.GetNetname()] = pad.GetNet()
old_tracks = [tr for tr in board.GetTracks()]
for old in old_tracks:
    board.Remove(old)
import_ses(board, ses, nets_by_name)
pcbnew.ZONE_FILLER(board).Fill(board.Zones())
board.Save(dst)
n_tracks = sum(1 for t in board.GetTracks() if t.GetClass() == "PCB_TRACK")
n_vias = sum(1 for t in board.GetTracks() if t.GetClass() == "PCB_VIA")
print("saved", dst, "| tracks", n_tracks, "| vias", n_vias)
rep = work + "_drc.rpt"
pcbnew.WriteDRCReport(board, rep, pcbnew.EDA_UNITS_MILLIMETRES, True)
print("DRC report:", rep)
