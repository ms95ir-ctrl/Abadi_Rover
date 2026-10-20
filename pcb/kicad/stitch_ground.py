#!/usr/bin/env python3
"""Add ground stitching vias to a routed board: they tie the top and bottom ground pours together in open areas, so the two layers
act as one ground plane (without them the layers meet only at the plated holes of the GND pins).

Usage: stitch_ground.py <in.kicad_pcb> <out.kicad_pcb> [max_vias]
Run it after routing and before finish_board.py (which refills the pours). The .kicad_pro must sit next to the input board.
A via is only added where it has room: at least 0.7 mm of clear space to every pad, track, via and hole, and where both layers
already have ground copper around it. The greedy choice always picks the spot farthest from the existing ground ties.
"""
import math
import sys

import pcbnew
from pcbnew import FromMM, VECTOR2I

src, dst = sys.argv[1], sys.argv[2]
LIMIT = int(sys.argv[3]) if len(sys.argv) > 3 else 30
OX, OY = 100.0, 50.0
VIA_D, VIA_H = 0.6, 0.3
NEED = 0.7                       # clear space (mm) between a via's edge and any other copper edge

b = pcbnew.LoadBoard(src)
gnd = b.FindNet("GND")


def U(p):
    return (p.x / 1e6 - OX, 100.0 - (p.y / 1e6 - OY))


def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


pads = [(U(p.GetPosition()), max(p.GetSizeX(), p.GetSizeY()) / 2e6) for p in b.GetPads()]
tracks, vias, ties = [], [], []
for t in b.GetTracks():
    if t.GetClass() == "PCB_VIA":
        vias.append((U(t.GetPosition()), t.GetWidth() / 2e6))
        if t.GetNetname() == "GND":
            ties.append(U(t.GetPosition()))
    else:
        tracks.append((U(t.GetStart()), U(t.GetEnd()), t.GetWidth() / 2e6))
for p in b.GetPads():
    if p.GetNetname() == "GND" and p.GetAttribute() != pcbnew.PAD_ATTRIB_NPTH:
        ties.append(U(p.GetPosition()))

KEEPOUT = (22.0, 66.0, 36.0, 94.0)           # antenna keep-out, x0 y0 x1 y1 (board mm)
HOLES = [(4, 4), (96, 4), (4, 96), (96, 96)]


def inside_pour(layer, x, y):
    """True if ground copper surrounds (x, y) on this layer (centre and four points 0.6 mm away)."""
    for z in b.Zones():
        if z.GetIsRuleArea() or z.GetNetname() != "GND" or not z.IsOnLayer(layer):
            continue
        fp = z.GetFilledPolysList(layer)
        pts = [(0, 0), (0.6, 0), (-0.6, 0), (0, 0.6), (0, -0.6)]
        return all(fp.Collide(VECTOR2I(FromMM(OX + x + dx), FromMM(OY + 100.0 - (y + dy)))) for dx, dy in pts)
    return False


def free(x, y):
    if not (2.0 <= x <= 98.0 and 2.0 <= y <= 98.0):
        return False
    if KEEPOUT[0] - 0.7 <= x <= KEEPOUT[2] + 0.7 and KEEPOUT[1] - 0.7 <= y <= KEEPOUT[3] + 0.7:
        return False
    if any(math.hypot(x - hx, y - hy) < 1.6 + NEED + 0.3 + 1.0 for hx, hy in HOLES):
        return False
    if any(math.hypot(x - p[0], y - p[1]) < r + 0.3 + NEED for p, r in pads):
        return False
    if any(math.hypot(x - p[0], y - p[1]) < r + 0.3 + NEED for p, r in vias):
        return False
    if any(seg_dist(x, y, a[0], a[1], c[0], c[1]) < w + 0.3 + NEED for a, c, w in tracks):
        return False
    return inside_pour(pcbnew.F_Cu, x, y) and inside_pour(pcbnew.B_Cu, x, y)


cands = [(x / 2.0, y / 2.0) for x in range(8, 192) for y in range(8, 192)]
cands = [c for c in cands if free(*c)]
added = []
while len(added) < LIMIT and cands:
    far = max(cands, key=lambda c: min(math.hypot(c[0] - t[0], c[1] - t[1]) for t in ties))
    d = min(math.hypot(far[0] - t[0], far[1] - t[1]) for t in ties)
    if d < 8.0:
        break
    v = pcbnew.PCB_VIA(b)
    v.SetPosition(VECTOR2I(FromMM(OX + far[0]), FromMM(OY + 100.0 - far[1])))
    v.SetWidth(FromMM(VIA_D))
    v.SetDrill(FromMM(VIA_H))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    v.SetNet(gnd)
    b.Add(v)
    added.append(far)
    ties.append(far)
    vias.append((far, VIA_D / 2))
    cands = [c for c in cands if math.hypot(c[0] - far[0], c[1] - far[1]) >= VIA_D + NEED]
print("stitching vias added:", len(added), "| farthest remaining spot from a ground tie: %.1f mm" %
      max((min(math.hypot(c[0] - t[0], c[1] - t[1]) for t in ties) for c in cands), default=0))
b.Save(dst)
