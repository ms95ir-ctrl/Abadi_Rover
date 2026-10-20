#!/usr/bin/env python3
"""Independent check of a KiCad Gerber export. Does NOT trust KiCad's own checker.

Reads the copper Gerbers and the drill files, rebuilds which copper touches which (islands joined by plated
holes), then compares with the net list dumped from the board design (dump_board.py JSON).
Reports shorts, opens, and basic fab-limit numbers (spacing, annular ring, hole spacing, edge distance).

Usage: audit_kicad_gerbers.py <gerber_dir> <board_dump.json> [prefix]
Needs gerbonara + shapely (pip install gerbonara shapely).
"""
import json
import math
import re
import sys
from collections import defaultdict

from gerbonara import GerberFile
from shapely import STRtree
from shapely.geometry import LineString, Point, Polygon, box
from shapely.affinity import rotate
from shapely.ops import unary_union

gdir, dump = sys.argv[1], sys.argv[2]
prefix = sys.argv[3] if len(sys.argv) > 3 else "abadi-motherboard"
design = json.load(open(dump))
COPPER = {"top": "%s-F_Cu.gtl", "bot": "%s-B_Cu.gbl"}


def layer_geometry(path):
    gf = GerberFile.open(path)
    geom = None
    for obj in gf.objects:
        for p in obj.to_primitives("mm"):
            n = type(p).__name__
            if n == "Circle":
                s = Point(p.x, p.y).buffer(p.r, 24)
            elif n == "Rectangle":
                s = box(p.x - p.w / 2, p.y - p.h / 2, p.x + p.w / 2, p.y + p.h / 2)
                if p.rotation:
                    s = rotate(s, math.degrees(p.rotation), origin=(p.x, p.y))
            elif n == "Line":
                s = LineString([(p.x1, p.y1), (p.x2, p.y2)]).buffer(p.width / 2, 12)
            elif n == "ArcPoly":
                assert all(c is None for c in (p.arc_centers or [])), "arc in region not handled"
                s = Polygon(p.outline).buffer(0)
            else:
                raise SystemExit("unhandled primitive " + n)
            if p.polarity_dark:
                geom = s if geom is None else geom.union(s)
            elif geom is not None:
                geom = geom.difference(s)
    return geom


def read_drill(path):
    holes, tools, cur = [], {}, None
    for line in open(path):
        line = line.strip()
        m = re.match(r"T(\d+)C([\d.]+)", line)
        if m:
            tools[int(m.group(1))] = float(m.group(2))
        elif re.match(r"^T\d+$", line):
            cur = tools[int(line[1:])]
        elif line.startswith("X"):
            m = re.match(r"X(-?[\d.]+)Y(-?[\d.]+)", line)
            holes.append((float(m.group(1)), float(m.group(2)), cur))
    return holes


def parts(g):
    return [] if g is None else (list(g.geoms) if g.geom_type == "MultiPolygon" else [g])


lay = {k: layer_geometry(gdir + "/" + (v % prefix)) for k, v in COPPER.items()}
isl = {k: parts(g) for k, g in lay.items()}
tree = {k: STRtree(v) for k, v in isl.items()}
pth = read_drill(gdir + "/%s-PTH.drl" % prefix)
npth = read_drill(gdir + "/%s-NPTH.drl" % prefix)
print("PTH holes %d, NPTH holes %d, copper islands top %d bottom %d" % (len(pth), len(npth), len(isl["top"]), len(isl["bot"])))

parent = {}


def find(a):
    parent.setdefault(a, a)
    while parent[a] != a:
        parent[a] = parent[parent[a]]
        a = parent[a]
    return a


def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[ra] = rb


for k in isl:
    for i in range(len(isl[k])):
        find((k, i))

hole_nodes = []
for (x, y, d) in pth:
    barrel = Point(x, y).buffer(d / 2)
    touched = []
    for k in isl:
        for i in tree[k].query(barrel):
            if isl[k][i].intersection(barrel).area > 0:
                touched.append((k, int(i)))
    for t in touched[1:]:
        union(touched[0], t)
    hole_nodes.append(touched)

# label each island with the intended nets of the pads/vias drilled in it
items = [(p["p"][0], p["p"][1], p["net"], p["ref"] + "." + p["n"]) for p in design["pads"] if not p["npth"]] + \
        [(v["p"][0], v["p"][1], v["net"], "via") for v in design["vias"]]
node_nets = defaultdict(set)
node_names = defaultdict(list)
unmatched = 0
for (x, y, d), touched in zip(pth, hole_nodes):
    m = [it for it in items if abs(it[0] - x) < 0.02 and abs(it[1] - y) < 0.02]
    if not m:
        unmatched += 1
        continue
    it = m[0]
    if not touched:
        print("  hole with no copper at all:", it)
    for t in touched:
        node_nets[find(t)].add(it[2] or "(no net)")
        node_names[find(t)].append(it[3])
print("drill hits without a matching designed pad/via: %d   designed pads/vias without a drill hit: %d" %
      (unmatched, len(items) - (len(pth) - unmatched)))

shorts = {r: n for r, n in node_nets.items() if len(n - {"(no net)"}) > 1}
print("\nSHORTS (copper joining different nets): %d" % len(shorts))
for r, n in list(shorts.items())[:10]:
    print("  ", sorted(n), node_names[r][:6])
by_net = defaultdict(set)
for r, nets in node_nets.items():
    for n in nets:
        if n != "(no net)":
            by_net[n].add(r)
opens = {n: r for n, r in by_net.items() if len(r) > 1}
print("OPENS (a net split into separate copper islands): %d" % len(opens))
for n, r in sorted(opens.items()):
    print("  ", n, "in", len(r), "islands")
    for isl_root in sorted(r, key=lambda q: len(node_names[q])):
        print("      island with", len(node_names[isl_root]), "holes, e.g.", node_names[isl_root][:8])

print("\n--- fab-limit numbers (typical cheap 2-layer limits in brackets) ---")
for k in isl:
    best = (9e9, None)
    for i, a in enumerate(isl[k]):
        for j in tree[k].query(a.buffer(0.4)):
            if j > i:
                dd = a.distance(isl[k][j])
                if dd < best[0]:
                    best = (dd, a.representative_point().coords[0])
    print("smallest copper gap on %s: %.3f mm   [fab minimum ~0.127]" % (k, best[0]))
# narrow slits INSIDE one copper piece (e.g. a track running 0.03 mm beside a pad of the same net): closing each island by 0.07 mm
# fills any slit narrower than 0.14 mm; what it fills is reported (corner rounding is below the 0.03 mm2 threshold)
for k in isl:
    slits = []
    for g in isl[k]:
        if g.area < 0.5:
            continue
        diff = g.buffer(0.07, join_style=2).buffer(-0.07, join_style=2).difference(g)
        for piece in (list(diff.geoms) if diff.geom_type == "MultiPolygon" else [diff]):
            if piece.area > 0.03:
                slits.append((round(piece.area, 3), tuple(round(v, 2) for v in piece.representative_point().coords[0])))
    print("narrow slits (<0.14 mm) inside one copper piece on %s: %d %s" % (k, len(slits), sorted(slits, reverse=True)[:6]))
tw = min((t["w"] for t in design["tracks"]), default=0)
print("narrowest track: %.3f mm   [fab minimum ~0.127]" % tw)
ring = min(((p["d"] - p["h"]) / 2 for p in design["pads"] if not p["npth"]), default=0)
vring = min(((v["d"] - 0.3) / 2 for v in design["vias"]), default=0)
print("smallest pad ring: %.3f mm, smallest via ring: %.3f mm   [fab minimum ~0.13]" % (ring, vring))
allh = [(x, y, d) for (x, y, d) in pth + npth]
w = 9e9
for i in range(len(allh)):
    for j in range(i + 1, len(allh)):
        w = min(w, math.hypot(allh[i][0] - allh[j][0], allh[i][1] - allh[j][1]) - allh[i][2] / 2 - allh[j][2] / 2)
print("smallest wall between two holes: %.3f mm   [fab minimum ~0.25]" % w)
for k in lay:
    b = lay[k].bounds
    print("copper to board edge on %s: %.3f mm   [fab minimum ~0.3]" % (k, min(b[0], b[1], 100 - b[2], 100 - b[3])))
bad = [h for h in npth if any(lay[k].distance(Point(h[0], h[1])) < h[2] / 2 + 0.1 for k in lay)]
print("unplated mounting holes with copper closer than 0.1 mm: %d" % len(bad))
print("min drill: %.2f mm   [fab minimum 0.2-0.3]" % min(d for _, _, d in pth))
