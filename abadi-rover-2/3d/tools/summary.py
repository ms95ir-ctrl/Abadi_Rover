"""Run all the calculations and write ONE set of numbers:  results/numbers.json  and  results/numbers.txt
   Needs: the STL files (python export_stl.py) and the group files (python export_groups.py).
   Usage:  python summary.py"""
import json, math, copy
import numpy as np
from r2paths import *
import analysis, phys, calc2, printtable
from r2render import load

TILT_G = ('head_shell', 'head_lid', 'pivot_bush', 'screen', 'webcam', 'tilt_servo', 'led', 'cam_cover', 'screws, inserts, foam (head)', 'cables in neck and head')
PAN_G = ('yoke', 'turntable', 'pan_servo')

def heights(rows):
    top = 0; names = lines('groups.txt')
    for n in names:
        if n in ('bumper', 'bump_switches'): continue
        z = load(n).bounds[1][2]
        top = max(top, z)
    axis = scad_value('head_axis_h'); hh = scad_value('scr_h') + scad_value('scr_clear') + 2*scad_value('head_wall')
    lens = axis - scad_value('head_axis_z') + hh/2 + 1 + scad_value('cam_h')/2 + scad_value('cam_lens_dz', 0)
    return dict(total_height_mm=round(float(top), 1), tilt_axis_mm=axis, screen_centre_mm=axis - scad_value('head_axis_z'), camera_lens_mm=round(lens, 1),
                cover_top_mm=scad_value('z_cover_top'), plug_hood_top_mm=load('plug_hood').bounds[1][2] if True else None,
                base_diameter_mm=2*scad_value('base_r'), head_w_mm=round(scad_value('scr_w') + scad_value('scr_clear') + 2*scad_value('head_wall'), 1), head_h_mm=round(hh, 1), head_d_mm=scad_value('head_d'))

def tip_row(rs, label, hp_dz=0.0):
    M, c = analysis.total(rs)
    q = (phys.PUSH_POINT[0], phys.PUSH_POINT[1], phys.PUSH_POINT[2] + hp_dz)
    r = phys.analyse(c, M/1000, label, q=q)
    r['mass_kg'] = round(M/1000, 3)
    return r

def run():
    rows = analysis.rows
    M, c = analysis.total(rows)
    out = {}
    cls_mass = {k: round(analysis.total([r for r in rows if r['cls'] == k])[0]) for k in ('base', 'mast', 'head')}
    cls_cog = {k: [round(float(v), 1) for v in analysis.total([r for r in rows if r['cls'] == k])[1]] for k in ('base', 'mast', 'head')}
    out['mass'] = dict(total_g=round(M), total_kg=round(M/1000, 3), cog_mm=[round(float(v), 1) for v in c], by_class_g=cls_mass, by_class_cog_mm=cls_cog,
                       printed_g_in_mass_table=round(sum(r['mass'] for r in rows if r['kind'] == 'printed')),
                       bought_g=round(sum(r['mass'] for r in rows if r['kind'] == 'bought')), extra_g=round(sum(r['mass'] for r in rows if r['kind'] == 'extra')),
                       biggest_items=[dict(name=r['name'], g=round(r['mass']), z_mm=round(r['pos'][2]), kind=r['kind']) for r in sorted(rows, key=lambda r: -r['mass'])[:16]])
    out['heights'] = heights(rows)
    out['heights']['plug_hood_top_mm'] = round(float(out['heights']['plug_hood_top_mm']), 1)
    # ---- tip-over: design + variants
    design = tip_row(rows, 'design: axis %d mm' % phys.AXIS_H)
    out['tip'] = design
    var = {}
    var['axis 340 mm (short mast)'] = tip_row(analysis.rows if False else phys.variant(rows, dh=-80), 'axis 340 mm (short mast)', -80)
    var['axis 420 mm (DEFAULT)'] = design
    var['axis 500 mm (tall mast)'] = tip_row(phys.variant(rows, dh=80), 'axis 500 mm (tall mast)', 80)
    var['axis 420 mm + 400 g steel ballast'] = tip_row(phys.variant(rows, ballast=400), 'axis 420 mm + 400 g steel ballast')
    var['10.1 inch head (+0.55 kg), axis 420 mm'] = tip_row(phys.variant(rows, head_mass_add=550), '10.1 inch head (+0.55 kg), axis 420 mm')
    ox, oy = scad_array('spkA_pos') if scad_array('spkA_pos') else (-14, 59)
    comfy = phys.variant(rows, drop=('speaker',), add=[dict(name='USB speakerphone (route A, A)', mass=350, pos=[-14, 59, scad_value('z_cover_top') + 17.5], cls='base', kind='x'),
                                                      dict(name='2 more cells (4-cell pack, A)', mass=92, pos=[-2, 0, 26], cls='base', kind='x')])
    var['comfortable build: 4 cells + speakerphone on the cover top (A)'] = tip_row(comfy, 'comfortable build: 4 cells + speakerphone on the cover top')
    bump = phys.variant(rows, add=[dict(name='bumper', mass=34, pos=[98, 0, 26], cls='base', kind='x')])
    var['with the optional bumper'] = tip_row(bump, 'with the optional bumper')
    out['tip_variants'] = var
    # ---- sensitivity to the skid gap (same mass and balance point)
    sens = {}
    for gap in (0.0, 1.5, 4.0):
        r = phys.analyse(c, M/1000, 'skid_gap %.1f' % gap, gap=gap)
        sens['%.1f' % gap] = dict(gap_mm=gap, worst_slope_deg=r['worst_slope']['slope_deg'], worst_push_N=r['worst_push']['F_tip'], forward_slope_deg=r['dirs']['forward']['slope_deg'],
                                  sideways_slope_deg=r['sideways']['slope_deg'], backward_slope_deg=r['dirs']['backward']['slope_deg'], brake_worst_ms2=r['brake_worst_ms2'])
    out['skid_gap_sensitivity'] = sens
    # ---- torque, motors, servos, mast
    mt = sum(r['mass'] for r in rows if r['name'] in TILT_G)/1000
    mp = sum(r['mass'] for r in rows if r['name'] in PAN_G)/1000
    out['calc2'] = calc2.compute(M/1000, mt, mp)
    # ---- print list
    prow, psum = printtable.compute()
    out['print'] = dict(summary=psum, rows=prow)
    # ---- hardware counts that can be read from the parameters
    n = lambda name: len(scad_array(name) or [])
    out['hardware'] = dict(
        from_the_cad_parameters=dict(drive_wheels=2, gearmotors=2, motor_caps=4, ball_caster=1, skids=n('skid_pos'), tray_to_deck_columns=n('col_pos'), deck_to_cover_posts=n('cpost_pos'),
                                     xl4016_bucks=n('xl_pos'), mini_bucks=n('mini_pos'), fuse_holder_bays_in_the_cad=n('fuse_pos'), lever_connector_bays_in_the_cad=n('wago_pos'),
                                     sonar_modules=2, cliff_modules=2, mg996r_servos=2),
        note='Fuse holders: the CAD shows 5 bays; decision R13 asks for 6 holders in the cheap build (route B). Lever connectors: decision R14 asks for FOUR 5-way connectors; the CAD has two 40 x 17 x 17 bays, each can hold two side by side (check on the real parts).',
        screw_and_insert_counts='unchanged from docs/mechanical-design.md section 10 except: motherboard screws are M3 x 6 (insert hole 6 mm deep); optional bumper adds 2 micro switches and 4 small screws (2 per switch, pilot holes 1.8 mm); no new heat-set inserts were added by the CAD stages',
        insert_hole_helper_counts=dict(M3_insert_holes_made_with_insert_hole=30, nut_pockets_made_with_hexnut_pocket=12, note='counted by running the model with a counter in the two helper modules (copy of the files). Other holes (cover posts, board standoffs, caster, ...) are plain cylinders and are NOT in this count, so these two numbers do NOT add up to the 37 inserts of the doc.'),
        printed_parts=psum['all']['parts'], printed_pieces=psum['all']['pieces'])
    out['inputs'] = dict(skid_gap_mm=phys.SKID_GAP, push_point_mm=list(phys.PUSH_POINT), wheel_y_mm=phys.WHEEL_Y, caster_x_mm=phys.CASTER_X,
                         skids=[list(p) for p in phys.SKIDS], model='quasi-static rigid body; see phys.py (A = my calculation)')
    return out

def fmt_dir(d):
    return '%5.1f deg  %4.1f N  braking %4.2f m/s2  (lever %s mm)' % (d['slope_deg'], d['F_tip'], d['brake_ms2'], d['lever_mm'])

def text(o):
    t = []; a = t.append
    m = o['mass']; h = o['heights']; tp = o['tip']; c2 = o['calc2']; p = o['print']['summary']
    a('ABADI ROVER 2: NUMBERS FROM THE CAD (made by tools/summary.py). (A) = my calculation, not measured.')
    a('')
    a('SIZE')
    a('  total height %.1f mm | tilt axis %.0f | screen centre %.0f | camera lens %.1f | cover top %.0f | plug hood top %.1f | base diameter %.0f' % (h['total_height_mm'], h['tilt_axis_mm'], h['screen_centre_mm'], h['camera_lens_mm'], h['cover_top_mm'], h['plug_hood_top_mm'], h['base_diameter_mm']))
    a('  head %.1f x %.1f x %.0f mm' % (h['head_w_mm'], h['head_h_mm'], h['head_d_mm']))
    a('MASS AND BALANCE POINT (first build: cheap build, route B speaker, 2 cells, no bumper)')
    a('  total %d g (%.2f kg) | balance point x %.1f, y %.1f, z %.1f mm | base %d g, mast %d g, head %d g' % (m['total_g'], m['total_kg'], m['cog_mm'][0], m['cog_mm'][1], m['cog_mm'][2], m['by_class_g']['base'], m['by_class_g']['mast'], m['by_class_g']['head']))
    a('  printed %d g | bought %d g | small parts and cables %d g' % (m['printed_g_in_mass_table'], m['bought_g'], m['extra_g']))
    a('TIP-OVER (skids %.1f mm above the floor; push at head centre %.0f mm; slow push; A)' % (o['inputs']['skid_gap_mm'], tp['push_point'][2]))
    a('  direction            tip angle (ramp)   smallest push   braking limit')
    for k, lab in (('forward', 'forward'), ('backward', 'backward')):
        a('  %-20s %s' % (lab, fmt_dir(tp['dirs'][k])))
    a('  %-20s %s' % ('sideways', fmt_dir(dict(tp['sideways'], lever_mm=tp['sideways']['lever_mm']))))
    a('  worst direction      %.1f deg (at %.0f deg off forward) | smallest push %.2f N (at %.0f deg) | braking while turning %.2f m/s2, straight %.2f m/s2' % (tp['worst_slope']['slope_deg'], tp['worst_slope']['angle'], tp['worst_push']['F_tip'], tp['worst_push']['angle'], tp['brake_worst_ms2'], tp['brake_straight_ms2']))
    a('  without skids: %.1f deg (edge %.1f mm from the balance point). Skids touch after %.1f deg backwards, %.1f deg forwards/sideways (front skid %.1f mm outside the wheel-caster edge).' % (tp['no_skids_tilt_deg'], tp['no_skids_edge_mm'], tp['skids_touch_backwards_deg'], tp['skids_touch_forward_deg'], tp['front_skid_outside_edge_mm']))
    a('  wheel grip against sliding sideways %.1f N (caster carries %.1f percent of the weight)' % (tp['F_slip_side'], tp['caster_share_pct']))
    a('  effect of the skid gap on the worst direction:')
    for k, v in o['skid_gap_sensitivity'].items():
        a('    gap %s mm: tip angle %.1f deg, smallest push %.2f N, forward %.1f, sideways %.1f, backward %.1f deg, braking while turning %.2f m/s2' % (k, v['worst_slope_deg'], v['worst_push_N'], v['forward_slope_deg'], v['sideways_slope_deg'], v['backward_slope_deg'], v['brake_worst_ms2']))
    a('  variants:        mass kg | balance height mm | tip angle deg (worst) | smallest push N | sideways push N | braking turning m/s2')
    for k, v in o['tip_variants'].items():
        a('    %-62s %.2f | %5.0f | %5.1f | %4.2f | %4.2f | %4.2f' % (k, v['mass_kg'], v['cg'][2], v['worst_slope']['slope_deg'], v['worst_push']['F_tip'], v['sideways']['F_tip'], v['brake_worst_ms2']))
    a('DRIVE')
    a('  wheel torque per wheel, design mass: flat %.3f N m, ramp 5 deg on carpet %.3f N m (%.2f kg cm); at 3.0 kg: ramp %.3f N m (%.2f kg cm)' % (c2['flat_torque_design_Nm'], c2['ramp_torque_design_Nm'], c2['ramp_torque_design_kgcm'], c2['ramp_torque_3kg_Nm'], c2['ramp_torque_3kg_kgcm']))
    for r in c2['motors']:
        if 'MP' in r['motor']:
            f = r['flat design mass']; rp = r['ramp 3.0 kg']
            a('  %s at %.1f V: no load %.2f m/s, stall %.2f kg cm | flat %s | ramp %s' % (r['motor'], r['V'], r['v0'], r['Ts_kgcm'], ('%d%% of stall, %.2f m/s, %.2f A' % (f['frac']*100, f['v'], f['I'])) if 'v' in f else 'STALLED', ('%d%% of stall, %.2f m/s, %.2f A' % (rp['frac']*100, rp['v'], rp['I'])) if 'v' in rp else 'STALLED'))
    a('SERVOS AND MAST')
    a('  tilting mass %.3f kg: tilt torque %.3f N m nominal, %.3f N m worst (servo 0.92 N m at 4.8 V) | pan: %.3f kg, %.3f N m (inertia %.5f kg m2)' % (c2['tilt_mass_kg'], c2['tilt_total_nominal'], c2['tilt_total_worst'], c2['pan_mass_kg'], c2['pan_total'], c2['pan_inertia']))
    a('  mast push 5 N at head height: %s | 10 N: %s' % (c2['mast_push_5N'], c2['mast_push_10N']))
    a('PRINTING (PETG, rough, A)')
    for k, v in p.items():
        a('  %-32s %2d different parts, %2d pieces, %4d g, %.1f h' % (k, v['parts'], v['pieces'], v['mass_g'], v['hours']))
    a('HARDWARE (see numbers.json for the notes)')
    a('  ' + ', '.join('%s %s' % (k.replace('_', ' '), v) for k, v in o['hardware']['from_the_cad_parameters'].items()))
    return '\n'.join(t) + '\n'

if __name__ == '__main__':
    RES = TOOLS/'results'; RES.mkdir(exist_ok=True)
    o = run()
    def clean(x):
        if isinstance(x, dict): return {k: clean(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)): return [clean(v) for v in x]
        if isinstance(x, (np.floating,)): return float(x)
        if isinstance(x, (np.integer,)): return int(x)
        return x
    o = clean(o)
    json.dump(o, open(RES/'numbers.json', 'w'), indent=1)
    tx = text(o)
    (RES/'numbers.txt').write_text(tx)
    print(tx)
