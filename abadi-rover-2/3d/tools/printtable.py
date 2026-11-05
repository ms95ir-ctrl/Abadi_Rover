"""Print list: size, plastic mass and rough print time of every part (from ../stl). Assumptions (A): PETG 1.27 g/cm3, fill factor per part,
   time = 1.9 minutes per gram + 12 minutes start-up (0.4 mm nozzle, 0.2 mm layers, 4 walls, ordinary 60 mm/s printer).
   Usage:  python printtable.py      (writes results/printtable.json and results/printtable.txt)"""
import json
import trimesh
from r2paths import *

FILL = {'tray':0.75,'deck':0.50,'cover':0.75,'plug_hood':0.9,'caster_cup':0.9,'caster_ring':0.9,'motor_cap':0.9,'skid':0.9,'bumper':0.9,'mast':0.85,'collar':0.8,
        'foot':0.6,'neck':0.45,'turntable':0.55,'yoke':0.5,'head_shell':0.8,'head_lid':0.6,'pivot':1.0,'cam_cover':1.0}
def fill(n):
    for k, v in FILL.items():
        if n.startswith(k): return v
    return 0.7
# name -> (quantity, orientation, supports, optional?)
INFO = {}
for q in ('FL', 'FR', 'RL', 'RR'):
    INFO['tray_' + q] = (1, 'floor down, rim and posts up', 'none; use a brim (the 53 mm posts are tall and thin). The 19.4 mm bumper slots in the rim are short bridges', False)
    INFO['deck_' + q] = (1, 'flat, plate down, standoffs up', 'none', False)
    INFO['cover_' + q] = (1, 'upside down: top plate on the bed, skirt up', 'none (the speaker pocket ring stands up from the bed)', False)
INFO.update({
 'caster_cup': (1, 'flange down', 'none', False), 'caster_ring': (1, 'flat', 'none', False), 'motor_cap': (4, 'flat, top face down (as exported)', 'none', False),
 'skid': (4, 'as exported', 'none', False),
 'plug_hood': (1, 'upside down: hood top on the bed, flange up', 'none: a 45 degree fillet under the flange holds it up (glue the flat flange face to the cover top)', False),
 'bumper_R': (1, 'arc standing on its edge, arm lying flat on the bed (as exported)', 'none', True),
 'bumper_C': (1, 'arc standing on its edge (as exported)', 'none', True),
 'bumper_L': (1, 'arc standing on its edge, arm lying flat on the bed (as exported)', 'none', True),
 'mast_lo_front': (1, 'lying on the outer back face, open side up', 'none', False), 'mast_lo_back': (1, 'lying on the outer back face, open side up', 'none', False),
 'mast_up_front': (1, 'lying on the outer back face, open side up', 'none', False), 'mast_up_back': (1, 'lying on the outer back face, open side up', 'none', False),
 'collar_front': (1, 'as exported (standing)', 'none', False), 'collar_back': (1, 'as exported (standing)', 'none', False),
 'foot_plate': (1, 'plate down, socket up', 'none', False), 'neck_plate': (1, 'top face down, socket up', 'none', False), 'turntable': (1, 'top face down, skirt up', 'none', False),
 'yoke_servo_side': (1, 'bar flat on the bed, arm standing (125 mm high)', 'none; add a brim', False), 'yoke_plain_side': (1, 'bar flat on the bed, arm standing (125 mm high)', 'none; add a brim', False),
 'head_shell': (1, 'front face down', 'none; a support only under the 41 mm servo window if it sags. The 22 mm bridge over the camera-cover slot may sag: then use a 1 mm plastic card as the cover', False),
 'head_lid': (1, 'interface-pad side down', 'none', False), 'pivot_bush': (1, 'as exported', 'none', False),
 'cam_cover': (1, 'flat', 'none (or use a 1 mm plastic card)', True),
})

def compute():
    rows = []
    for n in lines('parts.txt'):
        m = trimesh.load(str(STL / (n + '.stl')))
        sz = (m.bounds[1] - m.bounds[0])
        mass = m.volume/1000*1.27*fill(n); minutes = mass*1.9 + 12
        q, o, s, opt = INFO[n]
        rows.append(dict(name=n, qty=q, size_mm=[round(float(v), 1) for v in sz], volume_cm3=round(float(m.volume)/1000, 1), mass_g=round(float(mass), 1),
                         minutes=round(float(minutes)), orientation=o, supports=s, optional=opt))
    def tot(rs):
        return dict(parts=len(rs), pieces=sum(r['qty'] for r in rs), mass_g=round(sum(r['mass_g']*r['qty'] for r in rs)),
                    hours=round(sum(r['minutes']*r['qty'] for r in rs)/60, 1))
    summary = dict(all=tot(rows), first_build_without_optional=tot([r for r in rows if not r['optional']]),
                   first_build_without_bumper=tot([r for r in rows if not r['name'].startswith('bumper')]),
                   bumper_only=tot([r for r in rows if r['name'].startswith('bumper')]))
    return rows, summary

if __name__ == '__main__':
    rows, summary = compute()
    RES = TOOLS/'results'; RES.mkdir(exist_ok=True)
    json.dump(dict(rows=rows, summary=summary), open(RES/'printtable.json', 'w'), indent=1)
    out = ['%-16s %3s %20s %9s %7s %8s  %s' % ('part', 'qty', 'size x,y,z mm', 'volume', 'g', 'time', 'orientation / supports')]
    for r in rows:
        out.append('%-16s %3d %20s %7.1fcm3 %6.0fg %4dh%02d  %s%s | %s' % (r['name'], r['qty'], 'x'.join(('%.1f' % v) if v < 20 else ('%.0f' % v) for v in r['size_mm']), r['volume_cm3'], r['mass_g'], r['minutes']//60, r['minutes'] % 60, r['orientation'], ' (OPTIONAL)' if r['optional'] else '', r['supports']))
    for k, v in summary.items(): out.append('%s: %d different parts, %d pieces, %d g, %.1f h' % (k, v['parts'], v['pieces'], v['mass_g'], v['hours']))
    (RES/'printtable.txt').write_text('\n'.join(out) + '\n')
    print('\n'.join(out))
