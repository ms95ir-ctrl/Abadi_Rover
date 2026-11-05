"""Wheel torque, motor check, servo torque, pan inertia and mast bending for Robot 2 (A = my calculation).
   Usage:  python calc2.py     (uses the mass table of analysis.py; writes results/calc2.json)"""
import math, json
import numpy as np
from r2paths import *
g = 9.81
D = scad_value('wheel_d', 65.0) / 1000.0
r = D / 2

def need(m, crr=0.10, slope_deg=0.0, a=0.0):
    """force [N] and torque per wheel [N m] for mass m [kg]: rolling resistance crr, slope, acceleration a [m/s2]"""
    F = m*g*(crr*math.cos(math.radians(slope_deg)) + math.sin(math.radians(slope_deg))) + m*a
    return F, F*r/2

MOTORS = {   # name: (rated V, rpm no load at rated V, stall torque kg.cm at rated V, stall current A at rated V, no-load current A, source)
 'TT 1:48 (yellow, 3-6 V)': dict(Vr=6.0, rpm=200, Ts=0.8, Is=1.5, I0=0.15, src='shop copies of Adafruit data'),
 'Pololu 25D LP 12 V 47:1': dict(Vr=12.0, rpm=120, Ts=4.8, Is=0.9, I0=0.05, src='Pololu page, item 3253'),
 'Pololu 25D MP 12 V 47:1': dict(Vr=12.0, rpm=170, Ts=0.17*46.85*0.65, Is=1.8, I0=0.10, src='speed and stall current from item 3229; stall torque is my estimate: 0.17 kg.cm x 46.85 x 65 % gearbox'),
 'generic 25GA-370 12 V 130 rpm': dict(Vr=12.0, rpm=130, Ts=2.0, Is=0.9, I0=0.085, src='one seller; others claim much more'),
}

def compute(M_kg, m_tilt_kg, m_pan_extra_kg):
    """M_kg = whole robot; m_tilt_kg = mass that nods with the tilt servo; m_pan_extra_kg = yoke + turntable + pan servo (turn with the pan servo)"""
    res = {}
    rows = []
    for m in sorted(set([2.0, round(M_kg, 2), 3.0])):
        for lab, crr, sl, a in (('flat carpet, steady', 0.10, 0, 0), ('flat carpet, accelerating 0.3 m/s2', 0.10, 0, 0.3), ('5 deg ramp on carpet', 0.10, 5, 0)):
            F, T = need(m, crr, sl, a); rows.append(dict(mass_kg=m, case=lab, force_N=round(F, 2), torque_per_wheel_Nm=round(T, 3), torque_per_wheel_kgcm=round(T*10.197, 2)))
    res['need'] = rows
    # headline numbers
    res['ramp_torque_design_Nm'] = round(need(M_kg, 0.10, 5)[1], 3)
    res['ramp_torque_design_kgcm'] = round(need(M_kg, 0.10, 5)[1]*10.197, 2)
    res['ramp_torque_3kg_Nm'] = round(need(3.0, 0.10, 5)[1], 3)
    res['ramp_torque_3kg_kgcm'] = round(need(3.0, 0.10, 5)[1]*10.197, 2)
    res['flat_torque_design_Nm'] = round(need(M_kg)[1], 3)
    out = []
    for name, p in MOTORS.items():
        for V in (6.0, 7.4, 8.0, 8.4):
            k = V/p['Vr']
            rpm0 = p['rpm']*k; Ts = p['Ts']*k; Is = p['Is']*k
            row = dict(motor=name, V=V, rpm0=round(rpm0), v0=round(rpm0*math.pi*D/60, 2), Ts_kgcm=round(Ts, 2), Ts_Nm=round(Ts/10.197, 3), Is=round(Is, 2))
            for lab, T in (('flat design mass', need(M_kg)[1]), ('ramp 3.0 kg', need(3.0, 0.10, 5)[1])):
                Tk = T*10.197; frac = Tk/Ts
                if frac >= 1: row[lab] = dict(frac=round(frac, 2), stalled=True)
                else:
                    rpm = rpm0*(1-frac); I = p['I0']*k + frac*(Is - p['I0']*k)
                    row[lab] = dict(frac=round(frac, 2), rpm=round(rpm), v=round(rpm*math.pi*D/60, 2), I=round(I, 2))
            out.append(row)
    res['motors'] = out
    # ---------------- servo torque (tilt)
    mg = g
    head_w = scad_value('head_w', 174.6) if scad_value('head_w') else (scad_value('scr_w', 165) + scad_value('scr_clear', 1.2) + 2*scad_value('head_wall', 4.2))
    head_h = scad_value('scr_h', 107) + scad_value('scr_clear', 1.2) + 2*scad_value('head_wall', 4.2)
    head_d = scad_value('head_d', 44)
    res['tilt_mass_kg'] = round(m_tilt_kg, 3)
    for off in (0.010, 0.025):
        res['tilt_static_off%dmm' % int(off*1000)] = round(m_tilt_kg*mg*off, 3)
    I_tilt = m_tilt_kg*((head_h/1000)**2 + (head_d/1000)**2)/12 + m_tilt_kg*0.01**2
    alpha = 4*math.radians(30)/0.3**2                 # 30 degrees in 0.3 s, bang-bang
    res['tilt_inertia'] = round(I_tilt, 5)
    res['tilt_dyn'] = round(I_tilt*alpha, 4)
    res['tilt_total_nominal'] = round(m_tilt_kg*mg*0.010 + I_tilt*alpha + 0.02, 3)
    res['tilt_total_worst'] = round(m_tilt_kg*mg*0.025 + I_tilt*alpha + 0.02, 3)
    res['servo_torque_Nm'] = {'4.8V': round(9.4*0.0980665, 2), '6V': round(11*0.0980665, 2)}
    # ---------------- pan
    m_rot = m_tilt_kg + m_pan_extra_kg
    yoke_m = m_pan_extra_kg - 0.075          # about 55 g pan servo + 20 g turntable: the rest is the yoke
    I_pan = m_tilt_kg*((head_w/1000)**2 + (head_d/1000)**2)/12 + 2*(yoke_m/2)*0.1**2 + 0.02*0.045**2/2
    res['pan_mass_kg'] = round(m_rot, 3)
    res['pan_inertia'] = round(I_pan, 5)
    res['pan_dyn'] = round(I_pan*4*math.radians(90)/1.0**2, 3)
    res['pan_friction'] = round(m_rot*mg*0.25*0.044, 3)
    res['pan_total'] = round(res['pan_dyn'] + res['pan_friction'], 3)
    # ---------------- mast bending: rounded rectangle, wall, numeric
    mw, md, mr, mwall = scad_value('mast_w', 56), scad_value('mast_d', 44), scad_value('mast_r', 10), scad_value('mast_wall', 3)
    a_out, b_out = md/2, mw/2                          # half sizes: x (depth) and y (width)
    n = 2000
    xs = np.linspace(-a_out, a_out, n); ys = np.linspace(-b_out, b_out, n)
    X, Y = np.meshgrid(xs, ys)
    def inside(X, Y, a, b, rc):
        qx = np.abs(X)-(a-rc); qy = np.abs(Y)-(b-rc)
        d = np.where((qx > 0) & (qy > 0), np.hypot(qx, qy)-rc, np.maximum(qx, qy)); return d <= 0
    mask = inside(X, Y, a_out, b_out, mr) & ~inside(X, Y, a_out-mwall, b_out-mwall, mr-mwall)
    dA = (xs[1]-xs[0])*(ys[1]-ys[0])
    A = mask.sum()*dA; Ix = (Y[mask]**2).sum()*dA; Iy = (X[mask]**2).sum()*dA
    res['mast_section'] = dict(A=round(A, 1), I_about_x=round(Ix), I_about_y=round(Iy))
    E = 1500.0   # MPa, printed PETG (A)
    z_mast_bot = scad_value('z_deck_b', 68) + scad_value('deck_t', 4) + scad_value('foot_pad_h', 3) + scad_value('foot_t', 4)
    L = scad_value('head_axis_h', 420) - z_mast_bot      # push at the head centre height: lever from the foot plate top
    for F in (5, 10):
        d_weak = F*L**3/(3*E*Iy); d_str = F*L**3/(3*E*Ix)
        sig = F*L*(a_out)/Iy
        res['mast_push_%dN' % F] = dict(defl_front_back_mm=round(d_weak, 2), defl_side_mm=round(d_str, 2), stress_MPa=round(sig, 2))
    return res

if __name__ == '__main__':
    from analysis import rows, total
    M, c = total(rows)
    mt = sum(r['mass'] for r in rows if r['name'] in ('head_shell', 'head_lid', 'pivot_bush', 'screen', 'webcam', 'tilt_servo', 'led', 'cam_cover', 'screws, inserts, foam (head)', 'cables in neck and head'))/1000
    mp = sum(r['mass'] for r in rows if r['name'] in ('yoke', 'turntable', 'pan_servo'))/1000
    res = compute(M/1000, mt, mp)
    RES = TOOLS/'results'; RES.mkdir(exist_ok=True)
    json.dump(res, open(RES/'calc2.json', 'w'), indent=1)
    print(json.dumps(res, indent=1))
