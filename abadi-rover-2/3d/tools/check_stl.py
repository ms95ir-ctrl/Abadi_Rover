"""Check every STL in ../stl: closed (watertight), one single body, lowest point at z = 0, and write the bounding boxes.
   Usage:  python check_stl.py        -> prints a table and writes results/stl_check.json and results/stl_check.txt"""
import json, sys
import trimesh
from r2paths import *

# parts whose lowest point is NOT z = 0 on purpose (none at the moment)
ZMIN_EXCEPTIONS = {}

def check():
    rows = []
    for name in lines('parts.txt'):
        f = STL / (name + '.stl')
        if not f.exists():
            rows.append(dict(name=name, error='STL file missing')); continue
        m = trimesh.load(str(f), process=True)
        parts = [c for c in m.split(only_watertight=False) if abs(c.volume) > 1.0]
        b = m.bounds
        size = (b[1] - b[0])
        ok_zmin = abs(b[0][2]) < 0.01 or name in ZMIN_EXCEPTIONS
        rows.append(dict(name=name, size_x=round(float(size[0]), 1), size_y=round(float(size[1]), 1), size_z=round(float(size[2]), 1),
                         zmin=round(float(b[0][2]), 3), volume_cm3=round(float(m.volume) / 1000, 2),
                         watertight=bool(m.is_watertight), bodies=len(parts), triangles=int(len(m.faces)),
                         ok=bool(m.is_watertight and len(parts) == 1 and ok_zmin and m.volume > 0)))
    return rows

if __name__ == '__main__':
    rows = check()
    RES = TOOLS / 'results'; RES.mkdir(exist_ok=True)
    out = []
    out.append('%-17s %7s %7s %7s %7s %9s %5s %6s %s' % ('part', 'x mm', 'y mm', 'z mm', 'zmin', 'cm3', 'wt', 'bodies', 'result'))
    for r in rows:
        if 'error' in r:
            out.append('%-17s %s' % (r['name'], r['error'])); continue
        out.append('%-17s %7.1f %7.1f %7.1f %7.2f %9.2f %5s %6d %s' % (r['name'], r['size_x'], r['size_y'], r['size_z'], r['zmin'], r['volume_cm3'],
                   'yes' if r['watertight'] else 'NO', r['bodies'], 'ok' if r['ok'] else '<<< CHECK'))
    bad = [r['name'] for r in rows if not r.get('ok')]
    out.append('%d parts, %d with a problem%s' % (len(rows), len(bad), (': ' + ', '.join(bad)) if bad else ''))
    txt = '\n'.join(out)
    print(txt)
    (RES / 'stl_check.txt').write_text(txt + '\n')
    (RES / 'stl_check.json').write_text(json.dumps(rows, indent=1))
    sys.exit(1 if bad else 0)
