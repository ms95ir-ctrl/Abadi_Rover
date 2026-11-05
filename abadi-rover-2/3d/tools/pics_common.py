"""Drawing helpers shared by the picture scripts (dimension lines, labels with leader lines, label placement that avoids overlaps)."""
import numpy as np
from scenes import *
from r2paths import RENDERS, lines
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
OUTDIR = str(RENDERS) + '/'
INK = '#1b2733'; ACC = '#c0392b'; GRID = '#8a98a6'

def fig_for(img, dpi=100):
    H, W = img.shape[:2]
    fig = plt.figure(figsize=(W/dpi, H/dpi), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1]); ax.imshow(img, extent=[0, W, H, 0], interpolation='lanczos'); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis('off')
    return fig, ax

def P(cam, pt):
    sx, sy, _ = cam.project(pt); return float(sx[0]), float(sy[0])

def dim(ax, cam, p0, p1, off=(0, 0), text='', fs=17, color=INK, lw=1.6, ext=True, text_off=(0, 0), rot=None, bg=True):
    """dimension line between two world points, displaced in the picture by off=(dx,dy) pixels; text on the line."""
    a = np.array(P(cam, p0)); b = np.array(P(cam, p1)); o = np.array(off, float)
    a2 = a + o; b2 = b + o
    if ext:
        ax.plot([a[0], a2[0]], [a[1], a2[1]], color=color, lw=0.9, alpha=0.7)
        ax.plot([b[0], b2[0]], [b[1], b2[1]], color=color, lw=0.9, alpha=0.7)
    ax.add_patch(FancyArrowPatch(tuple(a2), tuple(b2), arrowstyle='<|-|>', mutation_scale=13, lw=lw, color=color, shrinkA=0, shrinkB=0))
    m = (a2 + b2)/2 + np.array(text_off, float)
    ang = np.degrees(np.arctan2(-(b2[1]-a2[1]), (b2[0]-a2[0]))) if rot is None else rot
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    ax.text(m[0], m[1], text, fontsize=fs, color=color, ha='center', va='center', rotation=ang,
            bbox=dict(fc='white', ec='none', pad=1.5, alpha=0.85) if bg else None, fontweight='bold')

def label(ax, xy, text, xytext, fs=16, color=INK, arrow=True, ha='left', weight='bold', box=True):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=fs, color=color, ha=ha, va='center', fontweight=weight,
        arrowprops=dict(arrowstyle='-', color=color, lw=1.2, shrinkA=2, shrinkB=0) if arrow else None,
        bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=color, lw=0.8, alpha=0.92) if box else None)

def save(fig, name, dpi=100):
    fig.savefig(OUTDIR + name, dpi=dpi); plt.close(fig); print('saved', name)

def text_box(ax, text, x, y, fs=14, ha='left', va='center', **kw):
    """draw text and return its pixel box (x0, y0, x1, y1) in the picture (y downwards)"""
    t = ax.text(x, y, text, fontsize=fs, ha=ha, va=va, **kw)
    ax.figure.canvas.draw()
    bb = t.get_window_extent(ax.figure.canvas.get_renderer())
    H = ax.figure.get_figheight()*ax.figure.dpi
    return t, (bb.x0, H - bb.y1, bb.x1, H - bb.y0)

def overlap(a, b, pad=0):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])

def boxes_overlapping(boxes, pad=2):
    """list of index pairs of boxes that overlap"""
    out = []
    for i in range(len(boxes)):
        for j in range(i+1, len(boxes)):
            if overlap(boxes[i], boxes[j], pad): out.append((i, j))
    return out
