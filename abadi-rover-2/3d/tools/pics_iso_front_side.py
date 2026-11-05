"""Pictures 1 to 3: isometric view, front view, side view (robot2-iso.png, robot2-front.png, robot2-side.png)."""
from pics_common import *
from r2paths import scad_value
HEAD_W = scad_value('scr_w') + scad_value('scr_clear') + 2*scad_value('head_wall')
HEAD_H = scad_value('scr_h') + scad_value('scr_clear') + 2*scad_value('head_wall')

def iso():
    sc = robot_scene()
    cam = Camera(az=35, el=22, scale=2.15, center=[20, 0, 252], W=1600, H=1300)
    img = render(sc, cam)
    fig, ax = fig_for(img)
    ax.text(40, 60, 'Robot 2 (telepresence robot): isometric view', fontsize=28, fontweight='bold', color=INK, va='center')
    ax.text(40, 100, '7 inch HDMI screen + USB webcam on a pan/tilt head, mast, round base with 2 drive wheels and 1 ball caster', fontsize=16, color=INK, va='center')
    items = [('#d98f2b', 'printed base (tray, deck, cover, plug hood)'), ('#d9dee3', 'printed mast (2 half-shells per segment)'), ('#6b7b8c', 'printed pan/tilt (neck plate, turntable, yoke)'), ('#3f8fc0', 'printed head (shell + lid)'), ('#3b3b3b', 'bought parts (wheels, servos, screen)')]
    y = 170
    for c, t in items:
        ax.add_patch(plt.Rectangle((40, y-10), 26, 20, fc=c, ec=INK, lw=0.8)); ax.text(78, y, t, fontsize=15, va='center', color=INK); y += 30
    lab = [((0, 117, 36), 'drive wheel (65 mm)', (1190, 1010)), ((62+22, 0, 150), 'mast: 56 x 44 mm, 2 segments', (1130, 640)), ((62, 0, 486), 'webcam behind the lens window', (1010, 250)),
           ((62+22, 0, 412), '7 inch screen', (1230, 420)), ((104, 0, 3), 'ball caster (below)', (1130, 1230)), ((62, 60, 114), 'call / STOP button', (1190, 800))]
    for p, t, xt in lab:
        sx, sy = P(cam, p); label(ax, (sx, sy), t, xt, fs=15)
    save(fig, 'robot2-iso.png')

def front_side():
    sc = robot_scene()
    cam = Camera(az=0, el=0, scale=2.0, center=[0, 0, 250], W=1500, H=1380)
    img = render(sc, cam, shadow=False)
    fig, ax = fig_for(img)
    ax.text(40, 50, 'Robot 2: front view, main dimensions (mm)', fontsize=26, fontweight='bold', color=INK, va='center')
    def Pw(y, z): return (0, y, z)
    dim(ax, cam, Pw(130, 0), Pw(130, 504), off=(330, 0), text='overall height 504', fs=17)
    dim(ax, cam, Pw(100, 420), Pw(100, 0), off=(255, 0), text='tilt axis 420', fs=17)
    dim(ax, cam, Pw(70, 485), Pw(70, 0), off=(180, 0), text='camera lens 485', fs=17)
    dim(ax, cam, Pw(-130, 0), Pw(130, 0), off=(0, 60), text='base diameter 260', fs=17)
    dim(ax, cam, Pw(-117, 0), Pw(117, 0), off=(0, 115), text='wheel track 234 (centres)', fs=17)
    dim(ax, cam, Pw(-103, 300), Pw(103, 300), off=(0, 0), text='yoke 206 (outer)', fs=17, ext=False, text_off=(0, -18))
    dim(ax, cam, Pw(-HEAD_W/2, 470), Pw(HEAD_W/2, 470), off=(0, -95), text='head %.1f wide x %.1f high (screen 165 x 107)' % (HEAD_W, HEAD_H), fs=17, text_off=(0, -26))
    dim(ax, cam, Pw(-28, 150), Pw(28, 150), off=(0, 0), text='mast 56', fs=17, ext=False, text_off=(0, -18))
    dim(ax, cam, Pw(-130, 105), Pw(-130, 0), off=(-175, 0), text='base height 105', fs=17)
    dim(ax, cam, Pw(-117, 65), Pw(-117, 0), off=(-85, 0), text='wheel 65', fs=17)
    label(ax, P(cam, (0, 0, 478)), 'webcam lens', (1075, 150), fs=15)
    label(ax, P(cam, (0, -60, 50)), 'ultrasonic sensors (x2)', (40, 880), fs=15)
    save(fig, 'robot2-front.png')

    cam = Camera(az=-90, el=0, scale=2.0, center=[10, 0, 250], W=1500, H=1380)
    img = render(sc, cam, shadow=False)
    fig, ax = fig_for(img)
    ax.text(40, 50, 'Robot 2: side view, main dimensions (mm); front is on the right', fontsize=26, fontweight='bold', color=INK, va='center')
    def Ps(x, z): return (x, 0, z)
    dim(ax, cam, Ps(43, 0), Ps(43, 504), off=(-300, 0), text='overall height 504', fs=17)
    dim(ax, cam, Ps(62, 79), Ps(62, 293), off=(120, 0), text='mast shells 214', fs=17)
    dim(ax, cam, Ps(135, 0), Ps(135, 420), off=(300, 0), text='tilt axis 420 above the floor', fs=17)
    dim(ax, cam, Ps(135, 0), Ps(135, 105), off=(150, 0), text='base 105', fs=17)
    dim(ax, cam, Ps(135, 0), Ps(135, 12), off=(105, 0), text='12', fs=16)
    dim(ax, cam, Ps(-130, 0), Ps(130, 0), off=(0, 70), text='base diameter 260', fs=17)
    dim(ax, cam, Ps(0, 0), Ps(104, 0), off=(0, 125), text='axle to caster 104', fs=17)
    dim(ax, cam, Ps(43, 504), Ps(87, 501), off=(0, -45), text='head depth 44', fs=16, text_off=(0, -24))
    cgx, cgz = CG
    cx, cy = P(cam, (cgx, 0, cgz))
    ax.plot([cx], [cy], 'o', ms=16, mfc='white', mec=ACC, mew=3); ax.plot([cx], [cy], '+', ms=16, color=ACC, mew=2.5)
    label(ax, (cx, cy), 'centre of gravity: x = +%.0f, z = %.0f mm' % (cgx, cgz), (60, 800), fs=15, color=ACC)
    label(ax, P(cam, (0, 0, 32)), 'drive axle', (60, 1120), fs=15)
    label(ax, P(cam, (104, 0, 8)), 'ball caster', (1150, 1290), fs=15)
    label(ax, P(cam, (111, 0, 45)), 'sonar (x2)', (1000, 880), fs=15)
    label(ax, P(cam, (8, -45, 116)), 'plug hood on the cover', (330, 905), fs=15)
    save(fig, 'robot2-side.png')

if __name__ == '__main__':
    import json
    from r2paths import TOOLS
    CG = json.load(open(TOOLS/'results'/'numbers.json'))['mass']['cog_mm']; CG = (CG[0], CG[2])
    iso(); front_side()
