"""Picture 5: close view of the head, pan/tilt and the top of the mast (robot2-head-pantilt.png)."""
from pics_common import *
from pics_exploded import autolabels
HEADN = [n for n in DEFAULT if n in HEAD_GROUPS + ['turntable', 'yoke', 'neck_plate', 'pan_horn', 'pan_servo', 'mast_up_f', 'mast_up_b', 'collar_f', 'collar_b'] + CABLES]
COLORS = {'neck_plate': '#d6453d'}
HC = np.array([MAST_X + 3, 0, 412.0])   # head centre

def head_view():
    W, H = 1050, 1150
    out = []
    for k, (az, el, tilt, pan) in enumerate([(38, 20, -12, 28), (-142, 22, 0, 0)]):     # tilt -12 = nodded 12 degrees DOWN (positive tilt = up)
        sc = robot_scene(names=HEADN, tilt=tilt, pan=pan, colors=COLORS)
        cam = Camera(az=az, el=el, scale=4.1, center=[MAST_X, 0, 385], W=W, H=H)
        out.append((cam, render(sc, cam), tilt, pan))
    big = np.concatenate([out[0][1], out[1][1]], axis=1)
    fig, ax = fig_for(big)
    ax.text(40, 48, 'Robot 2: head, pan/tilt and mast top (close view)', fontsize=28, fontweight='bold', color=INK, va='center')
    ax.text(40, 88, 'left: front, head turned 28 deg and nodded 12 deg down.   right: rear view with the lid.   red = INTERFACE 1 plate (replaceable)', fontsize=16, color=INK, va='center')
    camA, _, tA, pA = out[0]
    def hp(p): return Tpoint(p, tA, pA, 'head')
    def pp(p): return Tpoint(p, tA, pA, 'pan')
    itemsA = [
     ('7 inch screen 165 x 107', hp(HC + np.array([22, 0, -5])), 'L'),
     ('camera brow + webcam', hp(HC + np.array([22, 0, 76])), 'R'),
     ('camera-live LED (green)', hp(HC + np.array([22, -34, 73])), 'L'),
     ('head shell and lid', hp(HC + np.array([0, -87, 40])), 'L'),
     ('yoke arm + servo horn', pp(np.array([MAST_X, 103, 350])), 'R'),
     ('tilt axis (head nods)', hp(np.array([MAST_X, -96, 420])), 'L'),
     ('turntable + yoke bars', pp(np.array([MAST_X, -50, 322])), 'L'),
     ('pan servo MG996R (upside down)', pp(np.array([MAST_X - 15, 0, 330])), 'R'),
     ('INTERFACE 1: mast-top plate', np.array([MAST_X, -48, 292]), 'L'),
     ('mast: half-shells + collar', np.array([MAST_X + 22, 0, 225]), 'R'),
    ]
    autolabels(ax, camA, itemsA, 1050, H, fs=14, top=150, bottom=H - 60, colw=250, left_x=20, right_x=1050 - 250, gap=44)
    camB, _, _, _ = out[1]
    def sh(p):
        x, y = P(camB, p); return (x + 1050, y)
    def labB(txt, p, xt, yt):
        label(ax, sh(p), txt, (xt + 1050, yt), fs=14)
    labB('lid: 4 corner screws M3 x 8', HC + np.array([-22, 76, 45]), 20, 170)
    labB('INTERFACE 2: pad, 4 x M3 (60 x 40)', HC + np.array([-26, 0, -22]), 20, 300)
    labB('speaker grille (optional, air only)', HC + np.array([-22, -52, -12]), 640, 300)
    labB('cable entry slot (shell bottom)', HC + np.array([-8, -10, -58]), 20, 980)
    labB('yoke arm + pivot bush + M5', np.array([MAST_X, -100, 420]), 720, 440)
    labB('cables: HDMI, USB, 5 V, servos', np.array([MAST_X - 12, -19, 320]), 700, 960)
    labB('neck socket for the mast shells', np.array([MAST_X, -25, 295]), 700, 1050)
    save(fig, 'robot2-head-pantilt.png')

if __name__ == '__main__':
    head_view()
