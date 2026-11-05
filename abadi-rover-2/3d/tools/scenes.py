"""Scenes of the whole robot built from the group STL files (work/groups). Pictures use these."""
import numpy as np
from r2render import *
from r2paths import lines, scad_value
MAST_X = scad_value('mast_x', 62.0); AXIS_H = scad_value('head_axis_h', 420.0)
OPTIONAL = {'bumper', 'bump_switches'}                      # not in the first build: drawn only when asked for
ALL = [l for l in lines('groups.txt')]
DEFAULT = [n for n in ALL if n not in OPTIONAL]
BASE_PRINTED = ['tray', 'deck', 'cover', 'plug_hood', 'caster', 'motorcaps', 'skids']
BASE_BOUGHT = ['ball', 'wheels', 'motors', 'sonars', 'cliffs', 'battery', 'bms', 'xl', 'minibuck', 'fuses', 'wagos', 'charger', 'switch', 'button', 'speaker',
               'mb_pcb', 'mb_esp', 'mb_drv', 'mb_pca', 'mb_gyro', 'mb_terms', 'mb_caps', 'mb_hdrs', 'sbc_pcb', 'sbc_ports', 'sbc_cooler']
MAST = ['foot', 'mast_lo_f', 'mast_lo_b', 'mast_up_f', 'mast_up_b', 'collar_f', 'collar_b', 'neck_plate', 'pan_horn', 'pan_servo']
CABLES = ['cable_hdmi', 'cable_usb', 'cable_pwr']
TURNING = ['turntable', 'yoke', 'pan_servo']        # turn with the pan servo (the pan servo BODY turns, only its horn is fixed)

def robot_scene(tilt=0, pan=0, names=None, clip=None, explode=0, hide=(), dz=None, colors=None):
    """tilt: 0 = level, POSITIVE = the head looks UP, negative = looks down (same as tilt_range and the serial protocol).
       pan: positive = turned to the robot's LEFT seen from above (same as assembly.scad)."""
    sc = Scene()
    names = names or DEFAULT
    Tt = rot_y(-tilt, [MAST_X, 0, AXIS_H])         # rotating about +y by a positive angle would put the front DOWN, so the sign is flipped
    Tp = rot_z(pan, [MAST_X, 0, 0])
    for n in names:
        if n in hide: continue
        T = None
        if n in HEAD_GROUPS: T = Tp @ Tt
        elif n in TURNING: T = Tp
        if dz and n in dz: T = (trans([0, 0, dz[n]]) if T is None else trans([0, 0, dz[n]]) @ T)
        sc.add(n, T=T, clip=clip, color=(colors or {}).get(n))
    return sc

def Tpoint(p, tilt=0, pan=0, kind='head'):
    Tt = rot_y(-tilt, [MAST_X, 0, AXIS_H]); Tp = rot_z(pan, [MAST_X, 0, 0])
    T = Tp @ Tt if kind == 'head' else (Tp if kind == 'pan' else np.eye(4))
    q = T @ np.array([p[0], p[1], p[2], 1.0]); return q[:3]
