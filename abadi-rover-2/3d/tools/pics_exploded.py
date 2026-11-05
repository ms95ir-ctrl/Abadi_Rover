"""Picture 4: exploded view of the base layout (robot2-base-exploded.png)."""
from pics_common import *

def spread(ys, gap, lo, hi):
    ys = list(ys); n = len(ys)
    order = sorted(range(n), key=lambda i: ys[i]); out = [0]*n
    prev = lo - gap
    for i in order:
        y = max(ys[i], prev + gap); out[i] = y; prev = y
    over = out[order[-1]] - hi
    if over > 0:
        for i in order: out[i] -= over
    return out

def autolabels(ax, cam, items, W, H, fs=15, left_x=30, right_x=None, top=140, bottom=None, colw=330, gap=36, x_off=0):
    """items: list of (text, world point, 'L'|'R'). Places labels in two columns with leader lines."""
    right_x = right_x or (W-30-colw)
    bottom = bottom or H-40
    pts = [(it[0], P(cam, it[1]), it[2]) for it in items]
    for sd in ('L', 'R'):
        col = [x for x in pts if x[2] == sd]
        if not col: continue
        ys = spread([x[1][1] for x in col], gap, top, bottom)
        for (t, (px, py), _), y in zip(col, ys):
            label(ax, (px+x_off, py), t, ((left_x if sd == 'L' else right_x)+x_off, y), fs=fs, ha='left')

def exploded():
    lower = ['ball', 'wheels', 'motors', 'sonars', 'cliffs', 'battery', 'bms', 'xl', 'minibuck', 'fuses', 'wagos', 'charger', 'switch', 'motorcaps', 'caster', 'skids']
    dz = {}
    for n in lower: dz[n] = 70
    dz['deck'] = 185
    for n in ['mb_pcb', 'mb_esp', 'mb_drv', 'mb_pca', 'mb_gyro', 'mb_terms', 'mb_caps', 'mb_hdrs', 'sbc_pcb', 'sbc_ports', 'sbc_cooler']: dz[n] = 185 + 65
    for n in ('cover', 'plug_hood', 'button', 'speaker'): dz[n] = 185 + 65 + 190
    names = [n for n in DEFAULT if n in BASE_PRINTED + BASE_BOUGHT]
    sc = robot_scene(names=names, dz=dz)
    W, H = 1800, 1850
    cam = Camera(az=40, el=33, scale=2.3, center=[0, 0, 265], W=W, H=H)
    img = render(sc, cam)
    fig, ax = fig_for(img)
    ax.text(40, 50, 'Robot 2: base electronics layout, exploded view', fontsize=28, fontweight='bold', color=INK, va='center')
    ax.text(40, 92, 'layers from the bottom: tray + drive parts, lower electronics, deck with motherboard and SBC, cover (mast and head not shown)', fontsize=16, color=INK, va='center')
    def c(n):
        m = load(n); return m.bounds.mean(axis=0) + np.array([0, 0, dz.get(n, 0)])
    def top_of(n, off=0):
        m = load(n); b = m.bounds; return np.array([(b[0][0]+b[1][0])/2, (b[0][1]+b[1][1])/2, b[1][2]+dz.get(n, 0)+off])
    items = [
     ('cover (print: 4 pieces)', top_of('cover') + np.array([-20, 40, 0]), 'R'),
     ('plug hood (glued on the cover)', top_of('plug_hood'), 'R'),
     ('call / STOP button', top_of('button'), 'R'),
     ('speaker grille (route B)', top_of('speaker') + np.array([0, 0, -8]), 'R'),
     ('SBC (Raspberry-Pi size)', top_of('sbc_cooler'), 'R'),
     ('motherboard 100 x 100', top_of('mb_pcb') + np.array([30, -20, 0]), 'L'),
     ('ESP32-S3 on the board', top_of('mb_esp'), 'L'),
     ('PCA9685 servo board', top_of('mb_pca'), 'L'),
     ('2 x DRV8833 motor drivers', top_of('mb_drv'), 'L'),
     ('screw terminals (battery, bucks)', top_of('mb_terms'), 'L'),
     ('deck (4 pieces)', c('deck') + np.array([60, -110, 0]), 'L'),
     ('main switch (rear wall)', c('switch'), 'R'),
     ('lever connectors (2 bays)', top_of('wagos'), 'R'),
     ('USB-C charger board', top_of('charger'), 'R'),
     ('fuse holders (5 bays)', top_of('fuses'), 'R'),
     ('2 fixed bucks (5 V, 3.3 V)', top_of('minibuck'), 'R'),
     ('BMS on the battery', top_of('bms'), 'R'),
     ('2S battery: 2 x 18650 holder', top_of('battery') + np.array([0, 10, 0]), 'R'),
     ('drive wheel (x2)', c('wheels') + np.array([0, 110, 0]), 'R'),
     ('gearmotor (x2)', c('motors') + np.array([0, -80, 0]), 'L'),
     ('2 x XL4016 buck (servo 5 V, SBC 5.1 V)', top_of('xl') + np.array([0, -30, 0]), 'L'),
     ('sonar HC-SR04 (x2)', c('sonars') + np.array([0, 40, 0]), 'L'),
     ('cliff sensor (x2)', c('cliffs') + np.array([0, 30, 0]), 'L'),
     ('ball caster', c('caster'), 'L'),
     ('anti-tip skids (x4)', c('skids') + np.array([90, 30, -4]), 'L'),
     ('tray (4 pieces)', np.array([-100, 60, 15]), 'R'),
    ]
    autolabels(ax, cam, items, W, H, fs=14, top=140, gap=38)
    save(fig, 'robot2-base-exploded.png')

if __name__ == '__main__':
    exploded()
