"""Pictures 8 and 9: section through the middle (robot2-section.png) and the tip-over picture (robot2-stability.png)."""
import json, math
from pics_common import *
from matplotlib.patches import Rectangle, Circle, Polygon, FancyArrowPatch
from r2paths import TOOLS
import phys

def section():
    clip = ([0, 0, 0], [0, -1, 0])     # keep y <= 0 (the robot's right half)
    sc = robot_scene(names=[n for n in DEFAULT], clip=clip)
    W, H = 1700, 1500
    cam = Camera(az=90, el=0, scale=2.5, center=[40, 0, 262], W=W, H=H)
    img = render(sc, cam, shadow=False)
    fig, ax = fig_for(img)
    ax.text(40, 50, 'Robot 2: section through the middle (right half shown), front is on the LEFT', fontsize=26, fontweight='bold', color=INK, va='center')
    ax.text(40, 92, 'yellow = HDMI flat cable, green = USB (webcam), pink = 5 V power. They run in the mast channel, through the opening in the neck plate, and loop into the head.', fontsize=15, color=INK, va='center')
    def lab(txt, p, xt, yt, color=INK):
        x, y = P(cam, p); label(ax, (x, y), txt, (xt, yt), fs=15, color=color)
    lab('head: screen, webcam in the brow, tilt servo', (65, -40, 440), 1150, 170)
    lab('pan servo (upside down, body turns)', (52, 0, 330), 1150, 300)
    lab('turntable + yoke (turn with the pan servo)', (62, -60, 322), 1150, 420)
    lab('INTERFACE 1: mast-top plate + cable opening', (62, -20, 297), 1150, 540, ACC)
    lab('collar over the joint of the two segments', (62, -28, 186), 1150, 700)
    lab('mast: two half-shell segments, cables inside', (62, -26, 130), 1150, 860)
    lab('foot plate + 4 x M4 into deck pads', (62, -30, 81), 1150, 1000)
    lab('cover (top), deck, tray: 3 layers', (-100, -60, 90), 1150, 1120)
    lab('motherboard on 6 mm standoffs', (-36, -60, 80), 1150, 1230)
    lab('battery + BMS', (-2, -10, 30), 1150, 1330)
    lab('drive wheel + gearmotor', (0, -100, 32), 1150, 1410)
    lab('ball caster', (104, 0, 8), 40, 1330)
    lab('front sonar', (120, -20, 45), 40, 1160)
    lab('plug hood over the servo plugs', (8, -45, 112), 40, 900)
    save(fig, 'robot2-section.png')

def stability():
    o = json.load(open(TOOLS/'results'/'numbers.json'))
    t = o['tip']; M = t['M']; cg = t['cg']; gap = t['skid_gap']
    ws = t['worst_slope']; wp = t['worst_push']
    fwd = t['dirs']['forward']; bwd = t['dirs']['backward']; sid = t['sideways']
    fig = plt.figure(figsize=(12, 9.2), dpi=100)
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.60]); ax.set_aspect('equal'); ax.axis('off')
    # robot frame: x forward -> up in the picture, y left -> left in the picture (so picture x = -y)
    def T(x, y): return (-y, x)
    ax.add_patch(Circle((0, 0), 130, fc='#f7e2b8', ec=INK, lw=2))
    for sgn in (-1, 1): ax.add_patch(Rectangle((-(117*sgn)-13, -32.5), 26, 65, fc='#3b3b3b', ec=INK, zorder=2))
    W = phys.WHEELS; C = phys.CASTER; SK = phys.SKIDS
    tri = phys.hull(W + [C]); pent = phys.hull(W + [C] + SK)
    ax.add_patch(Polygon([T(*p) for p in pent], fc='#c8e6c9', ec='#2e7d32', lw=2.5, alpha=0.55, zorder=3))
    ax.add_patch(Polygon([T(*p) for p in tri], fc='none', ec='#1565c0', lw=2.5, ls='--', zorder=4))
    for p in SK: ax.add_patch(Circle(T(*p), 7, fc='#9e9e9e', ec=INK, zorder=5))
    ax.add_patch(Circle(T(*C), 8, fc='#c0c0c0', ec=INK, zorder=5))
    for p in W: ax.add_patch(Circle(T(*p), 4, fc=INK, zorder=5))
    cx, cy = T(cg[0], cg[1])
    ax.add_patch(Circle((cx, cy), 6, fc='white', ec=ACC, lw=3, zorder=8)); ax.plot([cx], [cy], '+', color=ACC, ms=14, zorder=9)
    # black arrows: balance point to the FIRST tipping edge (blue triangle) in 4 directions; the lengths are in the legend, not on the arrows
    first = {}
    for name, ang in (('forward', 0), ('backward', 180), ('left', 90), ('right', -90)):
        u = np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang))])
        m = phys.margin_dir((cg[0], cg[1]), tri, u); first[name] = m
        q = np.array([cg[0], cg[1]]) + u*m
        ax.annotate('', xy=T(*q), xytext=(cx, cy), arrowprops=dict(arrowstyle='->', color=INK, lw=2.0), zorder=7)
    a = ws['angle']; u = np.array([math.cos(math.radians(a)), math.sin(math.radians(a))])
    m = phys.margin_dir((cg[0], cg[1]), pent, u); q = np.array([cg[0], cg[1]]) + u*m
    ax.annotate('', xy=T(*q), xytext=(cx, cy), arrowprops=dict(arrowstyle='->', color=ACC, lw=2.6), zorder=7)
    # direction names outside the wheels and the circle
    ax.text(*T(146, 0), 'FRONT', fontsize=14, fontweight='bold', ha='center', va='center')
    ax.text(*T(-146, 0), 'REAR', fontsize=14, fontweight='bold', ha='center', va='center')
    ax.text(*T(0, 172), 'LEFT', fontsize=12, fontweight='bold', ha='center', va='center', color='#4a5a68')
    ax.text(*T(0, -172), 'RIGHT', fontsize=12, fontweight='bold', ha='center', va='center', color='#4a5a68')
    # legend text blocks on the right, one per item, each with its own colour
    ax.text(212, 100, 'centre of gravity: x = +%.0f mm, height %.0f mm' % (cg[0], cg[2]), fontsize=13, color=ACC, fontweight='bold', va='center')
    ax.text(212, 60, 'blue dashed: wheels + caster only. The robot first\nrocks over these edges. Black arrows: balance point to\nthe first edge: forward %.0f mm, backward %.0f mm,\nleft %.0f mm, right %.0f mm.' % (first['forward'], first['backward'], first['left'], first['right']), fontsize=13, color='#1565c0', fontweight='bold', va='center')
    ax.text(212, -20, 'green: wheels, caster and 4 skids. The skids hang\n%.1f mm above the floor and take the weight after\n%.1f deg (backwards) or %.1f deg (forwards, sideways).' % (gap, t['skids_touch_backwards_deg'], t['skids_touch_forward_deg']), fontsize=13, color='#2e7d32', fontweight='bold', va='center')
    ax.text(212, -85, 'red arrow: worst direction, %.0f deg off forward' % ws['angle'], fontsize=13, color=ACC, fontweight='bold', va='center')
    ax.set_xlim(-190, 580); ax.set_ylim(-185, 160)
    fig.text(0.04, 0.955, 'Robot 2: tip-over check (top view, head axis 420 mm, mass %.1f kg)' % t['mass_kg'], fontsize=22, fontweight='bold', color=INK)
    fig.text(0.04, 0.915, 'Worst direction: it tips on a ramp of about %.0f deg. The smallest slow push at head height (%.0f mm) that tips it is %.1f N.' % (ws['slope_deg'], t['push_point'][2], wp['F_tip']), fontsize=13.5, color=INK)
    fig.text(0.04, 0.887, 'Without the skids the ramp limit would be only %.0f deg backwards. The skids are only %.1f mm above the floor, so they scrape thresholds and thick carpet.' % (t['no_skids_tilt_deg'], gap), fontsize=11.5, color='#4a5a68')
    rows = [('direction', 'ramp angle', 'smallest push', 'braking limit')]
    rows.append(('forward', '%.1f deg' % fwd['slope_deg'], '%.1f N' % fwd['F_tip'], '%.1f m/s2' % fwd['brake_ms2']))
    rows.append(('backward', '%.1f deg' % bwd['slope_deg'], '%.1f N' % bwd['F_tip'], '%.1f m/s2' % bwd['brake_ms2']))
    rows.append(('sideways', '%.1f deg' % sid['slope_deg'], '%.1f N' % sid['F_tip'], '%.1f m/s2' % sid['brake_ms2']))
    rows.append(('worst direction', '%.1f deg' % ws['slope_deg'], '%.1f N' % wp['F_tip'], '%.1f m/s2 (turning)' % t['brake_worst_ms2']))
    y = 0.835
    for i, r in enumerate(rows):
        fw = 'bold' if i in (0, 4) else 'normal'; col = ACC if i == 4 else INK
        for xx, txt in zip((0.04, 0.24, 0.42, 0.62), r):
            fig.text(xx, y, txt, fontsize=13, fontweight=fw, color=col)
        y -= 0.033
    save(fig, 'robot2-stability.png')

if __name__ == '__main__':
    import sys
    w = sys.argv[1:] or ['section', 'stability']
    if 'section' in w: section()
    if 'stability' in w: stability()
