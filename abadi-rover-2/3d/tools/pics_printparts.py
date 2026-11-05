"""Picture 10: all printed parts laid out in their printing position (robot2-print-parts.png).
   Every label is placed by a small search: inside its own part when it fits, otherwise in free paper next to it (with a short line).
   A label never covers another part or another label; the script checks this and stops with an error if it cannot find a place."""
import json, math
import trimesh
from pics_common import *
from r2paths import STL, TOOLS

COL = {'tray': '#d98f2b', 'deck': '#e8a33d', 'cover': '#f3c76f', 'plug': '#f3c76f', 'caster': '#d98f2b', 'motor': '#d98f2b', 'skid': '#d98f2b', 'bumper': '#e0652f', 'mast': '#d9dee3', 'collar': '#8fa0b0',
       'foot': '#cfd5db', 'neck': '#d6453d', 'turn': '#6b7b8c', 'yoke': '#7a8a9b', 'head': '#3f8fc0', 'pivot': '#6b7b8c', 'cam': '#e0652f'}
def color(n):
    for k, v in COL.items():
        if n.startswith(k): return v
    return '#aaaaaa'

def main():
    pt = json.load(open(TOOLS/'results'/'printtable.json'))
    rows = {r['name']: r for r in pt['rows']}; summ = pt['summary']['all']
    names = [r['name'] for r in pt['rows']]
    meshes = {}
    for n in names:
        m = trimesh.load(str(STL / (n + '.stl'))); m.apply_translation(-m.bounds[0]); meshes[n] = m
    # shelf packing on a plan (mm): wide gaps so that labels have room next to the parts
    order = sorted(names, key=lambda n: -max(meshes[n].extents[:2]))
    x = y = 0; rowh = 0; maxw = 820; pos = {}
    for n in order:
        e = meshes[n].extents
        if x + e[0] > maxw: x = 0; y += rowh + 34; rowh = 0
        pos[n] = (x, y); x += e[0] + 22; rowh = max(rowh, e[1])
    sc = Scene()
    for n in order:
        m = meshes[n].copy(); m.apply_translation([pos[n][0], pos[n][1], 0])
        sc.items.append(dict(name=n, mesh=m, color=hex2rgb(color(n))))
    lo, hi = sc.bounds()
    W, H = 2000, 1720
    cam = Camera(az=-90, el=60, scale=2.0, center=[(lo[0]+hi[0])/2, (lo[1]+hi[1])/2, 20], W=W, H=H, shift=(0, 20))
    img, ids = render(sc, cam, shadow=False, return_ids=True)
    fig, ax = fig_for(img)
    ax.text(40, 50, 'Robot 2: all printed parts, laid out in their printing orientation', fontsize=26, fontweight='bold', color=INK, va='center')
    ax.text(40, 88, '%d different parts, %d pieces in total. Names match the STL files and the print list. A part printed several times is drawn once and marked x4. (opt.) = optional, not in the first build.' % (summ['parts'], summ['pieces']), fontsize=14, color=INK, va='center')
    # ---- labels
    def text_of(n):
        r = rows[n]; t = n
        if r['qty'] > 1: t += ' x%d' % r['qty']
        if r['optional']: t += ' (opt.)'
        return t
    fs = 11
    tmp = {}
    for n in order:
        t = ax.text(0, 0, text_of(n), fontsize=fs, ha='center', va='center', color=INK, fontweight='bold', bbox=dict(fc='white', ec='none', alpha=0.85, pad=1.5))
        fig.canvas.draw(); bb = t.get_window_extent(fig.canvas.get_renderer())
        tmp[n] = (t, bb.width + 6, bb.height + 6)
    mask_of = {n: (ids == k) for k, n in enumerate(order)}
    other_any = ids >= 0
    from scipy.ndimage import binary_dilation
    placed = []
    result = {}
    def box(cx, cy, w, h): return (cx - w/2, cy - h/2, cx + w/2, cy + h/2)
    def ok(n, b, inside):
        x0, y0, x1, y1 = [int(round(v)) for v in b]
        if x0 < 8 or x1 > W - 8 or y0 < 120 or y1 > H - 8: return False
        reg_ids = ids[y0:y1, x0:x1]
        own = (reg_ids == order.index(n)).sum(); tot = reg_ids.size
        other = ((reg_ids >= 0) & (reg_ids != order.index(n))).sum()
        if other > 0: return False
        if inside and own < 0.97 * tot: return False
        for pb in placed:
            if overlap(b, pb, 4): return False
        return True
    # small parts first (fewest options), big ones last (they can take the inside)
    proc = sorted(order, key=lambda n: meshes[n].extents[0] * meshes[n].extents[1])
    for n in proc:
        t, w, h = tmp[n]
        m = mask_of[n]; yy, xx = np.nonzero(m)
        bx0, bx1, by0, by1 = xx.min(), xx.max(), yy.min(), yy.max()
        cxm, cym = xx.mean(), yy.mean()
        cands = []
        g = 5
        for fx in (0.5, 0.2, 0.8):
            cands += [((bx0 + fx*(bx1-bx0)), by0 - h/2 - g, False), ((bx0 + fx*(bx1-bx0)), by1 + h/2 + g, False)]
        for fy in (0.5, 0.2, 0.8):
            cands += [(bx1 + w/2 + g, by0 + fy*(by1-by0), False), (bx0 - w/2 - g, by0 + fy*(by1-by0), False)]
        cands.append((cxm, cym, True))          # inside the part only when no free paper is next to it
        for r in range(14, 260, 12):
            for a in range(0, 360, 20):
                cands.append((cxm + (r + (bx1-bx0)/2) * math.cos(math.radians(a)), cym + (r + (by1-by0)/2) * math.sin(math.radians(a)), False))
        done = False
        for (cx, cy, inside) in cands:
            b = box(cx, cy, w, h)
            if ok(n, b, inside):
                placed.append(b); result[n] = (cx, cy, inside); done = True; break
        if not done: raise SystemExit('no place for the label of ' + n)
    for n in order:
        cx, cy, inside = result[n]; t, w, h = tmp[n]
        t.set_position((cx, cy))
        if not inside:
            b = box(cx, cy, w, h); m = mask_of[n]; yy, xx = np.nonzero(m)
            # distance from the label box to the part: draw a short line only when they do not touch
            dx = np.maximum(np.maximum(b[0] - xx, xx - b[2]), 0); dy = np.maximum(np.maximum(b[1] - yy, yy - b[3]), 0)
            d = np.hypot(dx, dy); k = int(np.argmin(d))
            if d[k] > 9:
                px, py = xx[k], yy[k]
                ax.plot([cx, px], [cy, py], color=INK, lw=0.9, zorder=1)
    for n, (t, w, h) in tmp.items(): t.set_zorder(5)
    save(fig, 'robot2-print-parts.png')
    # ---- check: no two label boxes overlap, none covers another part
    bad = boxes_overlapping(placed, 1)
    print('label boxes:', len(placed), 'overlaps:', len(bad))
    if bad: raise SystemExit('label overlap')

if __name__ == '__main__':
    main()
