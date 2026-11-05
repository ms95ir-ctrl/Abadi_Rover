"""Pictures 6 and 7: dimensioned side sketch for a phone (robot2-sketch-side-phone.png) and the top views of the base (robot2-layout-top.png)."""
import json
from pics_common import *
from pics_exploded import autolabels
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch
from r2paths import TOOLS, scad_value

def numbers():
    return json.load(open(TOOLS/'results'/'numbers.json'))

def sketch():
    o = numbers(); tip = o['tip']; mass = o['mass']
    cgx, cgz = mass['cog_mm'][0], mass['cog_mm'][2]
    hw = o['heights']['head_w_mm']; hh = o['heights']['head_h_mm']
    W, H = 1080, 1920
    fig = plt.figure(figsize=(W/100, H/100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis('off')
    BG = '#fbfaf6'
    ax.add_patch(Rectangle((0, 0), W, H, fc=BG, ec='none'))
    s = 2.2; x0 = 390; yf = 1440            # x_px = x0 + s*x ; y_px = yf - s*z   (x = 0 is the drive axle, front = right)
    X = lambda x: x0 + s*x; Z = lambda z: yf - s*z
    def rect(x1, x2, z1, z2, fc, ec=INK, lw=2.4, z=2): ax.add_patch(Rectangle((X(x1), Z(z2)), s*(x2-x1), s*(z2-z1), fc=fc, ec=ec, lw=lw, zorder=z))
    ax.text(40, 70, 'Robot 2: side view', fontsize=46, fontweight='bold', color=INK, va='center')
    ax.text(40, 128, 'all sizes in mm. front is on the right.', fontsize=26, color='#4a5a68', va='center')
    ax.plot([40, 1040], [Z(0), Z(0)], color=INK, lw=3.5, zorder=1)
    for i in range(0, 1000, 34): ax.plot([40+i+26, 40+i], [Z(0), Z(0)+26], color=GRID, lw=1.6, zorder=1)
    # base: tray rim, deck, cover, plug hood, skids (1.5 mm above the floor)
    rect(-130, 130, 12, 68, '#d98f2b'); rect(-130, 130, 68, 72, '#e8a33d')
    ax.add_patch(Polygon([(X(-130), Z(72)), (X(130), Z(72)), (X(130), Z(97)), (X(122), Z(105)), (X(-122), Z(105)), (X(-130), Z(97))], fc='#f0c26a', ec=INK, lw=2.4, zorder=2))
    rect(-5, 30, 105, 116.6, '#f3c76f', lw=2.0, z=2)
    gap = o['inputs']['skid_gap_mm']
    for xs in (-92, 88): rect(xs, xs+14, gap, 12, '#d98f2b', lw=1.8, z=3)
    # inside hints
    rect(-80, 16, 78, 98, '#1f7a4d', lw=1.6, z=3)
    rect(-40, 38, 15, 38, '#1f5fa8', lw=1.6, z=3)
    # wheel, caster, sonar
    ax.add_patch(Circle((X(0), Z(32.5)), s*32.5, fc='#3b3b3b', ec=INK, lw=2.6, zorder=4)); ax.add_patch(Circle((X(0), Z(32.5)), s*8, fc='#c8c8c8', ec=INK, lw=2, zorder=5))
    ax.add_patch(Circle((X(104), Z(8)), s*8, fc='#c0c0c0', ec=INK, lw=2.4, zorder=4)); rect(94, 114, 8, 15, '#d98f2b', lw=1.8, z=3)
    ax.add_patch(Circle((X(128), Z(45)), s*8, fc='#3a78b5', ec=INK, lw=2.2, zorder=4))
    # mast, collar, neck plate (red = interface 1)
    rect(40, 84, 72, 293, '#d9dee3'); rect(35, 89, 166, 206, '#8fa0b0', lw=2.2)
    rect(12, 112, 292.6, 301.6, '#d6453d', lw=2.4)
    # pan servo, turntable, yoke arm
    rect(40, 84, 320, 347, '#7a8a9b', lw=1.8, z=3); rect(20, 106, 318, 322, '#6b7b8c', lw=2.2, z=3)
    ax.add_patch(FancyBboxPatch((X(39), Z(443)), s*46, s*(443-318), boxstyle='round,pad=0,rounding_size=20', fc='#7a8a9b', ec=INK, lw=2.4, zorder=3))
    # head, brow, screen, lens, tilt axis
    ax.add_patch(FancyBboxPatch((X(43), Z(412+hh/2)), s*44, s*hh, boxstyle='round,pad=0,rounding_size=7', fc='#3f8fc0', ec=INK, lw=2.6, zorder=4))
    rect(43, 87, 412+hh/2, o['heights']['total_height_mm'], '#3f8fc0', lw=2.6, z=4)
    rect(84.5, 87, 364, 468, '#14181d', lw=1.5, z=5)
    ax.add_patch(Circle((X(87), Z(o['heights']['camera_lens_mm'])), s*6, fc='#14181d', ec=INK, lw=2.2, zorder=6))
    ax.add_patch(Circle((X(62), Z(420)), s*4.5, fc='white', ec=INK, lw=2.4, zorder=7))
    # centre of gravity
    cx, cy = X(cgx), Z(cgz)
    ax.add_patch(Circle((cx, cy), 24, fc='white', ec=ACC, lw=4.5, zorder=9)); ax.plot([cx-24, cx+24], [cy, cy], color=ACC, lw=3.5, zorder=10); ax.plot([cx, cx], [cy-24, cy+24], color=ACC, lw=3.5, zorder=10)
    # numbered markers on the parts that are listed at the bottom (no leader lines, nothing to cross)
    def marker(xpix, ypix, n):
        ax.add_patch(Circle((xpix, ypix), 16, fc='white', ec=INK, lw=2.4, zorder=15)); ax.text(xpix, ypix+1, str(n), fontsize=24, fontweight='bold', color=INK, ha='center', va='center', zorder=16)
    marker(X(0), Z(32.5), 1); marker(X(128), Z(45), 2); marker(X(104), Z(8), 3); marker(X(-83), Z(5.5), 4); marker(X(8), Z(111), 5)
    # ---- dimensions
    def vdim(xpix, z1, z2, txt, color=INK, fs=30, right=False):
        ax.annotate('', xy=(xpix, Z(z1)), xytext=(xpix, Z(z2)), arrowprops=dict(arrowstyle='<|-|>', color=color, lw=2.8, mutation_scale=24, shrinkA=0, shrinkB=0), zorder=12)
        ax.text(xpix + (16 if right else -16), (Z(z1)+Z(z2))/2, txt, fontsize=fs, color=color, fontweight='bold', rotation=90, ha='left' if right else 'right', va='center', bbox=dict(fc=BG, ec='none', pad=2), zorder=13)
    def hdim(y, x1, x2, txt, color=INK, fs=30, tx=None):
        ax.annotate('', xy=(X(x1), y), xytext=(X(x2), y), arrowprops=dict(arrowstyle='<|-|>', color=color, lw=2.8, mutation_scale=24, shrinkA=0, shrinkB=0), zorder=12)
        ax.text((X(x1)+X(x2))/2 if tx is None else tx, y-40, txt, fontsize=fs, color=color, fontweight='bold', ha='center', va='center', bbox=dict(fc=BG, ec='none', pad=2), zorder=13)
    top = o['heights']['total_height_mm']
    for z, xc in ((420, 800), (485, 900), (top, 1000)):
        ax.plot([X(87)+4, xc+10], [Z(z), Z(z)], color=GRID, lw=1.4, zorder=0)
    vdim(800, 0, 420, 'tilt axis 420'); vdim(900, 0, 485, 'camera lens 485'); vdim(1000, 0, round(top), 'overall %d' % round(top))
    ax.plot([X(135)+4, 800], [Z(0), Z(0)], color=GRID, lw=1.2, zorder=0)
    for x in (-130, 130): ax.plot([X(x), X(x)], [Z(0), Z(0)+120], color=GRID, lw=1.4, zorder=0)
    hdim(Z(0)+70, -130, 130, 'base diameter 260')
    ax.plot([X(0), X(0)], [Z(0), Z(0)+190], color=GRID, lw=1.4, zorder=0); ax.plot([X(104), X(104)], [Z(0), Z(0)+190], color=GRID, lw=1.4, zorder=0)
    hdim(Z(0)+140, 0, 104, 'axle to caster 104')
    vdim(730, 0, 105, 'base 105', right=True); ax.plot([X(135)+4, 730], [Z(105), Z(105)], color=GRID, lw=1.2, zorder=0)
    # ---- call-outs (left column; every leader line runs over empty paper)
    def call(txt, pt, tpos, color=INK, fs=30, ha='left'):
        ax.annotate(txt, xy=pt, xytext=tpos, fontsize=fs, color=color, fontweight='bold', ha=ha, va='center',
            arrowprops=dict(arrowstyle='-', color=color, lw=2.2, shrinkA=2), bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=color, lw=1.6), zorder=20)
    call('webcam in the brow', (X(43), Z(487)), (40, 330))
    call('head %.1f x %.1f x 44' % (hw, hh), (X(43), Z(440)), (40, 425), fs=26)
    call('pan/tilt', (X(40), Z(380)), (40, 520), color=ACC)
    call('INTERFACE plate', (X(12), Z(297)), (40, 650), color=ACC)
    call('mast 56 x 44', (X(40), Z(230)), (40, 790))
    call('centre of gravity', (cx, cy), (40, 990), color=ACC)
    call('base cover, deck, tray', (X(-100), Z(88)), (40, 1118), fs=26)
    # ---- key for the numbered markers
    y = 1665
    for xk, n, txt in ((40, 1, 'wheels 65'), (300, 2, 'sonar x2'), (520, 3, 'ball caster'), (770, 4, 'skids x4')):
        ax.add_patch(Circle((xk+16, y), 16, fc='white', ec=INK, lw=2.4)); ax.text(xk+16, y+1, str(n), fontsize=24, fontweight='bold', color=INK, ha='center', va='center')
        ax.text(xk+44, y, txt, fontsize=27, fontweight='bold', color=INK, va='center')
    ax.add_patch(Circle((56, y+50), 16, fc='white', ec=INK, lw=2.4)); ax.text(56, y+51, '5', fontsize=24, fontweight='bold', color=INK, ha='center', va='center')
    ax.text(84, y+50, 'plug hood on the cover', fontsize=27, fontweight='bold', color=INK, va='center')
    ax.text(600, y+50, 'skids: %.1f mm above floor' % gap, fontsize=24, color='#4a5a68', va='center')
    # ---- facts block
    y = 1790
    wd = tip['worst_slope']['slope_deg']; pf = tip['worst_push']['F_tip']
    for line in ('weight about %.1f kg (first estimate)' % mass['total_kg'],
                 'tips over on a ramp of about %.0f deg; push test %.1f N' % (wd, pf),
                 'head turns +-30 deg for now, nods -25 to +35 deg'):
        ax.text(40, y, line, fontsize=27, color=INK, va='center', fontweight='bold'); y += 52
    save(fig, 'robot2-sketch-side-phone.png')

def layout():
    W, H = 1500, 1000                       # one panel; the two panels are stacked, the circle (780 px) is in the middle, labels stand in the side margins
    low = [n for n in DEFAULT if n in ['tray', 'caster', 'motorcaps', 'skids', 'ball', 'wheels', 'motors', 'sonars', 'cliffs', 'battery', 'bms', 'xl', 'minibuck', 'fuses', 'wagos', 'charger', 'switch']]
    cam = Camera(az=0, el=90, scale=3.0, center=[0, 0, 30], W=W, H=H)
    imgA = render(robot_scene(names=low), cam)
    deck = [n for n in DEFAULT if n in ['tray', 'deck', 'caster', 'motorcaps', 'skids', 'wheels', 'sonars', 'mb_pcb', 'mb_esp', 'mb_drv', 'mb_pca', 'mb_gyro', 'mb_terms', 'mb_caps', 'mb_hdrs', 'sbc_pcb', 'sbc_ports', 'sbc_cooler', 'foot']]
    imgB = render(robot_scene(names=deck), cam)
    big = np.concatenate([imgA, imgB], axis=0)
    fig, ax = fig_for(big)
    ax.text(30, 36, 'Lower compartment (deck and cover removed)', fontsize=22, fontweight='bold', color=INK, va='center')
    ax.text(30, 70, 'top view, front (sonars, caster) at the top, robot left = picture left', fontsize=15, color=INK, va='center')
    ax.text(30, H+36, 'Deck level (cover removed)', fontsize=22, fontweight='bold', color=INK, va='center')
    A = [('2S battery + BMS on top', (-2, 0, 38), 'R'), ('2 x XL4016 bucks', (62, 36, 36), 'L'), ('gearmotor (x2)', (0, 80, 32), 'L'), ('drive wheel (x2)', (0, -120, 32), 'R'),
         ('ball caster', (104, 0, 16), 'R'), ('sonar HC-SR04', (108, 58, 45), 'L'), ('cliff sensor', (69, -88, 20), 'R'), ('fuse holders (5 bays;\n6 in the cheap build)', (-61, -30, 26), 'R'),
         ('lever connectors (2 bays drawn, 4 bought)', (-96, 30, 30), 'L'), ('USB-C charger (rear wall)', (-102, 0, 26), 'R'), ('fixed 5 V buck (2nd bay spare)', (-96, 56, 22), 'L'), ('main switch', (-118, 50, 45), 'L')]
    autolabels(ax, cam, A, W, H, fs=14, left_x=12, right_x=1160, top=130, bottom=H-40, gap=40)
    B = [('motherboard 100 x 100', (-36, -38, 80), 'R'), ('ESP32-S3', (-65, -25, 88), 'R'), ('PCA9685 servo board', (-5, -44, 95), 'R'),
         ('battery / buck terminals', (-30, -81, 85), 'R'), ('SBC 85 x 56', (-62, 64, 90), 'L'), ('mast foot, 4 x M4', (62, 0, 86), 'L'), ('wire slot to the motors', (-18, 23, 72), 'L'),
         ('HDMI port (flat cable to the mast)', (-27, 92, 86), 'L')]
    # panel B is the lower half: shift the y of the labels by H
    camB = Camera(az=0, el=90, scale=3.0, center=[0, 0, 30], W=W, H=H, shift=(0, H))
    autolabels(ax, camB, B, W, 2*H, fs=14, left_x=12, right_x=1160, top=H+130, bottom=2*H-40, gap=44)
    save(fig, 'robot2-layout-top.png')

if __name__ == '__main__':
    import sys
    which = sys.argv[1:] or ['sketch', 'layout']
    if 'sketch' in which: sketch()
    if 'layout' in which: layout()
