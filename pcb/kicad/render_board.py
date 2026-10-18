#!/usr/bin/env python3
"""Draw pictures of the board from its exported Gerber files, plus a 1:1 paper template for test-fitting parts.

Usage: render_board.py <gerber_dir> <out_dir> [prefix]
Writes board-top.png (what the finished board looks like), board-copper.png (both copper layers) and
fit-template-1to1.pdf (print at 100 % / "actual size" on A4, lay your modules on it).
Needs gerbonara, shapely, matplotlib.
"""
import math
import re
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from gerbonara import GerberFile
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, PathPatch, Rectangle
from matplotlib.path import Path
from shapely.affinity import rotate
from shapely.geometry import LineString, Point, Polygon, box

gdir, out = sys.argv[1], sys.argv[2]
prefix = sys.argv[3] if len(sys.argv) > 3 else "abadi-motherboard"


def load(path):
    """-> (shapely geometry of all dark copper-like shapes, list of silk line segments, list of clear shapes)"""
    gf = GerberFile.open(path)
    geom, lines = None, []
    for obj in gf.objects:
        for p in obj.to_primitives("mm"):
            n = type(p).__name__
            if n == "Line":
                if p.polarity_dark:
                    lines.append(((p.x1, p.y1), (p.x2, p.y2), p.width))
                    s = LineString([(p.x1, p.y1), (p.x2, p.y2)]).buffer(p.width / 2, 6)
                else:
                    continue
            elif n == "Circle":
                s = Point(p.x, p.y).buffer(p.r, 20)
            elif n == "Rectangle":
                s = box(p.x - p.w / 2, p.y - p.h / 2, p.x + p.w / 2, p.y + p.h / 2)
                if p.rotation:
                    s = rotate(s, math.degrees(p.rotation), origin=(p.x, p.y))
            elif n == "ArcPoly":
                s = Polygon(p.outline).buffer(0)
            else:
                continue
            if p.polarity_dark:
                geom = s if geom is None else geom.union(s)
            elif geom is not None:
                geom = geom.difference(s)
    return geom, lines


def drill(path):
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


def patches(geom, **kw):
    out_p = []
    if geom is None:
        return out_p
    for g in (geom.geoms if geom.geom_type == "MultiPolygon" else [geom]):
        verts, codes = [], []
        for ring in [g.exterior] + list(g.interiors):
            xy = list(ring.coords)
            verts += xy
            codes += [Path.MOVETO] + [Path.LINETO] * (len(xy) - 2) + [Path.CLOSEPOLY]
        out_p.append(PathPatch(Path(verts, codes), **kw))
    return out_p


top, _ = load("%s/%s-F_Cu.gtl" % (gdir, prefix))
bot, _ = load("%s/%s-B_Cu.gbl" % (gdir, prefix))
mask_top, _ = load("%s/%s-F_Mask.gts" % (gdir, prefix))
_, silk = load("%s/%s-F_Silkscreen.gto" % (gdir, prefix))
pth = drill("%s/%s-PTH.drl" % (gdir, prefix))
npth = drill("%s/%s-NPTH.drl" % (gdir, prefix))


def base(ax, title):
    ax.set_xlim(-2, 102)
    ax.set_ylim(-2, 102)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 100, 100, fc="#1e6b3a", ec="#0a2a14", lw=2))
    ax.set_title(title, fontsize=13, fontweight="bold")


def holes(ax):
    for x, y, d in pth:
        ax.add_patch(Circle((x, y), d / 2, fc="#101010", zorder=8))
    for x, y, d in npth:
        ax.add_patch(Circle((x, y), d / 2, fc="#f4f1e8", ec="#101010", lw=1, zorder=8))


# 1. what the finished board looks like from above
fig, ax = plt.subplots(figsize=(13, 13), dpi=100)
base(ax, "Draft motherboard, 2 layers, 100 x 100 mm - top view (as it will look when printed)")
for p in patches(top, fc="#2a8a4d", ec="none", zorder=2):       # covered copper: slightly lighter green
    ax.add_patch(p)
exposed = top.intersection(mask_top) if mask_top is not None else top
for p in patches(exposed, fc="#e8c14a", ec="#8a6d12", lw=0.3, zorder=5):   # bare pads (gold)
    ax.add_patch(p)
ax.add_collection(LineCollection([[a, b] for a, b, w in silk], colors="white", linewidths=0.9, zorder=6))
holes(ax)
fig.savefig(out + "/board-top.png", bbox_inches="tight", facecolor="#f8f6f0")
plt.close(fig)

# 2. both copper layers
fig, axes = plt.subplots(1, 2, figsize=(22, 11), dpi=90)
for ax, g, col, name in ((axes[0], top, "#ff8a50", "TOP copper"), (axes[1], bot, "#50a5f0", "BOTTOM copper")):
    base(ax, name + " (ground pour included)")
    for p in patches(g, fc=col, ec="none", zorder=2):
        ax.add_patch(p)
    holes(ax)
fig.savefig(out + "/board-copper.png", bbox_inches="tight", facecolor="#f8f6f0")
plt.close(fig)

# 3. 1:1 paper template (A4 portrait). Print at 100 % - the ruler below must measure exactly 50 mm.
MM = 1 / 25.4
fig = plt.figure(figsize=(210 * MM, 297 * MM))
ox, oy = 55.0, 120.0      # board lower-left on the sheet, mm
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 210)
ax.set_ylim(0, 297)
ax.axis("off")
ax.add_patch(Rectangle((ox, oy), 100, 100, fc="none", ec="black", lw=1.0))
for p in patches(top, fc="#dddddd", ec="none", zorder=1):
    p.set_transform(p.get_transform() + matplotlib.transforms.Affine2D().translate(ox, oy) + ax.transData)
    ax.add_patch(p)
ax.add_collection(LineCollection([[(a[0] + ox, a[1] + oy), (b[0] + ox, b[1] + oy)] for a, b, w in silk],
                                 colors="black", linewidths=0.6, zorder=4))
for x, y, d in pth:
    ax.add_patch(Circle((ox + x, oy + y), d / 2, fc="white", ec="black", lw=0.5, zorder=6))
for x, y, d in npth:
    ax.add_patch(Circle((ox + x, oy + y), d / 2, fc="white", ec="black", lw=0.8, zorder=6))
ax.plot([ox, ox + 50], [oy - 12, oy - 12], color="black", lw=1.5)
for k in range(0, 51, 10):
    ax.plot([ox + k, ox + k], [oy - 14, oy - 10], color="black", lw=1)
ax.text(10, oy - 19, "Print at 100% / actual size. The line above must measure exactly 50 mm.", fontsize=9)
ax.text(10, oy + 112, "DRAFT motherboard 100 x 100 mm - hole template.", fontsize=11, fontweight="bold")
ax.text(10, oy + 107, "Lay each module on it: do its pins fall in the holes, and does its body fit the outline?", fontsize=9)
fig.savefig(out + "/fit-template-1to1.pdf")
plt.close(fig)
print("wrote board-top.png, board-copper.png, fit-template-1to1.pdf in", out)
