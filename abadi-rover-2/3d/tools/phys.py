"""Tip-over, push-force and braking model of Robot 2 (quasi-static rigid body, A = my model, not measured).

WHAT THE MODEL DOES (plain words)
  The robot stands on 3 points: two wheels and the ball caster. Four small skids (feet) hang skid_gap mm above the floor.
  When the robot is pushed (or the floor tilts), it first rocks over the edge of the wheel/caster triangle.
  After a little rocking a skid touches the floor, and the robot rests on a new, larger area.
  It only falls over when the balance point passes the edge of the LAST area it can reach.
  The script follows this step by step for every direction (0 to 360 degrees) and reports:
    slope_deg   = THE TIP ANGLE: angle of a ramp (or of a tilted table under the robot) at which it falls over.
                  This is the "static tilt angle" of the mechanical doc. Braking limit = g x tan(slope_deg).
    F_tip       = smallest horizontal push at head height that carries it past that point (slow push, no impact)
    tilt_body   = for information: how far the robot body itself is tilted from vertical at the point of no return.
                  It is larger than slope_deg because the robot has rocked forward onto its skids by then.
  Assumptions: rigid body, skids touch the floor "softly" (no bounce), friction is large enough that nothing slides
  (the wheel grip is about 12 N, checked below), wheel contact on the centre plane of each wheel (a little conservative).
  A skid is a 14 mm disc; the model uses its centre (the outer edge would give 7 mm more lever, also conservative).
"""
import sys, json, math, copy
import numpy as np
from r2paths import *

g = 9.81
WHEEL_Y = scad_value('wheel_y', 117.0)
CASTER_X = scad_value('caster_x', 104.0)
SKID_GAP = scad_value('skid_gap', 1.5)
SKID_POS = [tuple(p) for p in scad_array('skid_pos')]
MAST_X = scad_value('mast_x', 62.0)
AXIS_H = scad_value('head_axis_h', 420.0)
HEAD_AXIS_Y = scad_value('head_axis_y', -3.0)
HEAD_AXIS_Z = scad_value('head_axis_z', 8.0)
WHEELS = [(0.0, WHEEL_Y), (0.0, -WHEEL_Y)]
CASTER = (CASTER_X, 0.0)
SKIDS = SKID_POS
# the push point: centre of the head (screen centre) = tilt axis minus head_axis_z, 3 mm in front of the mast axis
PUSH_POINT = (MAST_X - HEAD_AXIS_Y, 0.0, AXIS_H - HEAD_AXIS_Z)

def support_points(gap=None):
    gap = SKID_GAP if gap is None else gap
    return np.array([(x, y, 0.0) for (x, y) in WHEELS + [CASTER]] + [(x, y, gap) for (x, y) in SKIDS], float)

# ------------------------------------------------------------------ plan-view helpers (also used by the picture script)
def hull(pts):
    pts = sorted(set(map(tuple, np.round(np.array(pts, float), 9))))
    if len(pts) < 3: return pts
    def cross(o, a, b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 1e-12: lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 1e-12: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]            # counter-clockwise

def margin_dir(c, poly, u):
    """distance from point c along unit direction u to the polygon boundary (exit point)"""
    r = ray_poly(np.array(c, float), np.array(u, float), poly)
    return max(t for t, i, s in r) if r else 0.0

def ray_poly(c, u, poly):
    """all crossings of the ray c + tau*u (tau > 0) with the polygon boundary: list of (tau, edge index, s)"""
    out = []; n = len(poly)
    for i in range(n):
        p = np.array(poly[i], float); q = np.array(poly[(i+1) % n], float); e = q - p
        den = u[0]*e[1] - u[1]*e[0]
        if abs(den) < 1e-12: continue
        w = p - c
        tau = (w[0]*e[1] - w[1]*e[0]) / den
        s = (w[0]*u[1] - w[1]*u[0]) / den
        if tau > 1e-9 and -1e-9 <= s <= 1 + 1e-9: out.append((tau, i, s))
    return out

def rodrigues(a, th):
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(th)*K + (1 - math.cos(th))*(K @ K)

# ------------------------------------------------------------------ the step-by-step tipping model
def tip_path(angle_deg, c, M, q, sup, tol=1e-6, max_stages=8):
    """Push direction angle_deg (0 = forward, 90 = to the robot's left), balance point c, mass M [kg], push point q.
       Returns dict(F_tip [N], slope_deg, tilt_body_deg, stages=[...])."""
    u = np.array([math.cos(math.radians(angle_deg)), math.sin(math.radians(angle_deg))])
    R = np.eye(3); t = np.zeros(3)
    c = np.array(c, float); q = np.array(q, float)
    stages = []; F_max = 0.0; tan_max = 0.0
    tilt_final = None
    for k in range(max_stages):
        P = (R @ sup.T).T + t; C = R @ c + t; Q = R @ q + t
        z0 = P[:, 2].min(); P[:, 2] -= z0; C[2] -= z0; Q[2] -= z0; t = t - np.array([0, 0, z0])
        contact = [i for i in range(len(P)) if P[i, 2] < tol]
        poly = hull(P[contact, :2])
        hits = ray_poly(C[:2], u, poly) if len(poly) >= 3 else []
        if not hits:                               # the new resting area cannot hold the robot at any force: it falls on
            tilt_final = math.degrees(math.acos(max(-1, min(1, R[2, 2]))))
            stages.append(dict(stage=k+1, note='no support: falls on'))
            break
        tau, ei, s = max(hits)
        F = M * g * (tau/1000.0) / (Q[2]/1000.0)
        tan_c = tau / C[2]
        F_max = max(F_max, F); tan_max = max(tan_max, tan_c)
        a_pt = np.array([poly[ei][0], poly[ei][1], 0.0]); b_pt = np.array([poly[(ei+1) % len(poly)][0], poly[(ei+1) % len(poly)][1], 0.0])
        ax_ = (b_pt - a_pt) / np.linalg.norm(b_pt - a_pt)          # counter-clockwise edge: +rotation lifts the inside
        def sz(Pj): r = Pj - a_pt; return ax_[0]*r[1] - ax_[1]*r[0]
        d = sz(C); zc = C[2]
        th_tip = math.atan2(d, zc)
        th_land = 1e9
        for j in range(len(P)):
            if j in contact: continue
            sj = sz(P[j])
            if sj < -1e-9 and P[j, 2] > tol:
                th_land = min(th_land, math.atan2(P[j, 2], -sj))
        edge_len_dist = d                                           # horizontal distance of the balance point from the pivot edge
        stages.append(dict(stage=k+1, ray_mm=round(float(tau), 1), edge_dist_mm=round(float(d), 1), cog_height_mm=round(float(zc), 1),
                           push_height_mm=round(float(Q[2]), 1), F_N=round(float(F), 2), slope_deg=round(math.degrees(math.atan(tan_c)), 2),
                           pivot=[[round(float(a_pt[0]), 1), round(float(a_pt[1]), 1)], [round(float(b_pt[0]), 1), round(float(b_pt[1]), 1)]],
                           skid_lands_after_deg=None if th_land > 1e8 else round(math.degrees(th_land), 2),
                           tip_after_deg=round(math.degrees(th_tip), 2), contact=len(contact)))
        if th_land < th_tip - 1e-9:                                 # a skid lands first: new resting area
            Rot = rodrigues(ax_, th_land)
            R = Rot @ R; t = Rot @ (t - a_pt) + a_pt
            continue
        Rot = rodrigues(ax_, th_tip)                                # balance point passes the edge: point of no return
        Rf = Rot @ R
        tilt_final = math.degrees(math.acos(max(-1, min(1, Rf[2, 2]))))
        break
    return dict(angle=angle_deg, F_tip=float(F_max), slope_deg=float(math.degrees(math.atan(tan_max))), brake_ms2=float(g*tan_max), tilt_body_deg=float(tilt_final), stages=stages)

def scan(c, M, q, sup, step=0.5):
    out = []
    for a in np.arange(0, 360, step):
        out.append(tip_path(float(a), c, M, q, sup))
    return out

def analyse(c, M, label='', q=None, gap=None, step=0.5):
    q = PUSH_POINT if q is None else q
    sup = support_points(gap)
    res = dict(label=label, M=float(M), cg=[round(float(c[0]), 1), round(float(c[1]), 1), round(float(c[2]), 1)], push_point=list(map(float, q)),
               skid_gap=SKID_GAP if gap is None else gap)
    allr = scan(c, M, q, sup, step)
    def best(key, fn=min):
        r = fn(allr, key=lambda r: r[key]); return r
    def sel(a): return tip_path(a, c, M, q, sup)
    dirs = {}
    for name, a in (('forward', 0.0), ('backward', 180.0), ('sideways left', 90.0), ('sideways right', 270.0)):
        r = sel(a)
        dirs[name] = dict(angle=a, slope_deg=round(r['slope_deg'], 1), F_tip=round(r['F_tip'], 2), tilt_body_deg=round(r['tilt_body_deg'], 1),
                          brake_ms2=round(r['brake_ms2'], 2), lever_mm=r['stages'][-1].get('ray_mm'), stages=r['stages'])
    side = min(dirs['sideways left'], dirs['sideways right'], key=lambda d: d['slope_deg'])
    res['dirs'] = dirs
    res['sideways'] = dict(angle=side['angle'], slope_deg=side['slope_deg'], F_tip=side['F_tip'], tilt_body_deg=side['tilt_body_deg'], brake_ms2=side['brake_ms2'], lever_mm=side['lever_mm'])
    wf = best('F_tip'); wb = best('brake_ms2'); ws = best('slope_deg')
    res['worst_slope'] = dict(angle=float(ws['angle']), slope_deg=round(ws['slope_deg'], 1), F_tip=round(ws['F_tip'], 2), tilt_body_deg=round(ws['tilt_body_deg'], 1), stages=ws['stages'])
    res['worst_push'] = dict(angle=float(wf['angle']), F_tip=round(wf['F_tip'], 2), slope_deg=round(wf['slope_deg'], 1))
    res['brake_straight_ms2'] = dirs['forward']['brake_ms2']
    res['brake_worst_ms2'] = round(wb['brake_ms2'], 2); res['brake_worst_angle'] = float(wb['angle'])
    res['no_support_directions'] = sum(1 for r in allr if any('no support' in s.get('note', '') for s in r['stages']))
    # first pivot only: wheels + caster, no skids (what the robot does with no feet at all)
    tri = hull(WHEELS + [CASTER])
    dmin_t = min(abs(((np.array(tri[(i+1) % 3]) - np.array(tri[i]))[0] * (c[1]-tri[i][1]) - (np.array(tri[(i+1) % 3]) - np.array(tri[i]))[1] * (c[0]-tri[i][0])) / np.linalg.norm(np.array(tri[(i+1) % 3]) - np.array(tri[i]))) for i in range(3))
    res['no_skids_tilt_deg'] = round(math.degrees(math.atan(dmin_t / c[2])), 1)
    res['no_skids_edge_mm'] = round(float(dmin_t), 1)
    # skids touch after (degrees of tilt): backwards over the axle, and forwards over the wheel-caster edge
    xs_rear = [abs(p[0]) for p in SKIDS if p[0] < 0]; xs_front = [p for p in SKIDS if p[0] > 0]
    if xs_rear: res['skids_touch_backwards_deg'] = round(math.degrees(math.atan(SKID_GAP / min(xs_rear))) if gap is None else math.degrees(math.atan(gap / min(xs_rear))), 2)
    # front skid distance outside the wheel-caster edge
    w = np.array(WHEELS[0]); cc = np.array(CASTER); e = (cc - w) / np.linalg.norm(cc - w)
    dist_front = min(abs(e[0]*(p[1]-w[1]) - e[1]*(p[0]-w[0])) for p in xs_front)
    res['front_skid_outside_edge_mm'] = round(float(dist_front), 1)
    res['skids_touch_forward_deg'] = round(math.degrees(math.atan((SKID_GAP if gap is None else gap) / dist_front)), 2)
    # sliding check: wheel grip against sliding sideways (friction 0.6 under the wheels, 0.1 under the ball)
    Nc = M*g*(c[0]/CASTER_X); Nw = M*g - Nc
    res['N_caster'] = round(float(Nc), 1); res['N_wheels'] = round(float(Nw), 1); res['caster_share_pct'] = round(100*float(Nc)/(M*g), 1)
    res['F_slip_side'] = round(0.6*float(Nw) + 0.1*float(Nc), 1)
    return res

# ------------------------------------------------------------------ variants of the robot (mast height, ballast, bigger head, builds)
def variant(base_rows, dh=0, head_mass_add=0, ballast=0, drop=(), add=()):
    rs = copy.deepcopy([r for r in base_rows if r['name'] not in drop])
    L0 = 292.6 - 79
    for r in rs:
        if r['cls'] == 'head': r['pos'][2] += dh
        if r['cls'] == 'mast': r['pos'][2] = 79 + (r['pos'][2] - 79) * (1 + dh / L0)
    for r in rs:
        if r['cls'] == 'mast': r['mass'] *= (L0 + dh) / L0
    if head_mass_add: rs.append(dict(name='bigger screen', mass=head_mass_add, pos=[75, 0, 412 + dh], cls='head', kind='x'))
    if ballast: rs.append(dict(name='ballast', mass=ballast, pos=[10, 0, 20], cls='base', kind='x'))
    for a in add: rs.append(a)
    return rs

if __name__ == '__main__':
    from analysis import rows, total
    M, c = total(rows)
    out = {}
    out['design'] = analyse(c, M/1000, 'design (axis %d mm)' % AXIS_H)
    print(json.dumps({k: v for k, v in out['design'].items() if k not in ('dirs', 'worst_tilt')}, indent=1))
    RES = TOOLS / 'results'; RES.mkdir(exist_ok=True)
    json.dump(out, open(RES / 'phys_quick.json', 'w'), indent=1)
