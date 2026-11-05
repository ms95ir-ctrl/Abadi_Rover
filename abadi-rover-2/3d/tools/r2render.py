"""Small z-buffer renderer for the robot-2 pictures (orthographic, flat shading, outlines) + helpers.
   Needs: numpy, trimesh, numba, scipy, matplotlib (see README.md)."""
import numpy as np, trimesh, math
from numba import njit
from r2paths import GROUPS as _GROUPS

GROUPS = str(_GROUPS)

COL = {
 'tray':'#d98f2b','deck':'#e8a33d','cover':'#f3c76f','caster':'#d98f2b','motorcaps':'#d98f2b','skids':'#d98f2b','bumper':'#e0652f','plug_hood':'#f3c76f',
 'foot':'#cfd5db','mast_lo_f':'#d9dee3','mast_lo_b':'#c3cad1','mast_up_f':'#d9dee3','mast_up_b':'#c3cad1','collar_f':'#8fa0b0','collar_b':'#8fa0b0',
 'neck_plate':'#6b7b8c','turntable':'#6b7b8c','yoke':'#7a8a9b','head_shell':'#3f8fc0','head_lid':'#2f6f93','pivot_bush':'#6b7b8c','cam_cover':'#e0652f',
 'ball':'#c0c0c0','wheels':'#3b3b3b','motors':'#c9a227','sonars':'#3a78b5','cliffs':'#3a78b5','battery':'#1f5fa8','bms':'#2e8b57',
 'xl':'#7a5fc4','minibuck':'#2fa38f','fuses':'#d33232','wagos':'#e8e4c0','charger':'#b34f8a','switch':'#d62828',
 'button':'#d62828','speaker':'#555b61','led':'#2fbf4a','bump_switches':'#555b61',
 'mb_pcb':'#1f7a4d','mb_esp':'#25282c','mb_drv':'#c0392b','mb_pca':'#2e5fb0','mb_gyro':'#2e5fb0','mb_terms':'#35b84b','mb_caps':'#1a2a6c','mb_hdrs':'#2b2b2b',
 'sbc_pcb':'#1c8a3a','sbc_ports':'#c8c8c8','sbc_cooler':'#dcdcdc','pan_servo':'#ff8c00','tilt_servo':'#ff8c00','pan_horn':'#c8c8c8',
 'screen':'#14181d','webcam':'#4a4f55','cable_hdmi':'#ffd400','cable_usb':'#2f9e44','cable_pwr':'#d6336c',
}
HEAD_GROUPS = ['head_shell','head_lid','pivot_bush','screen','webcam','tilt_servo','led','cam_cover']
PAN_GROUPS  = HEAD_GROUPS + ['turntable','yoke']

def hex2rgb(h):
    h=h.lstrip('#'); return np.array([int(h[i:i+2],16)/255.0 for i in (0,2,4)])

_cache = {}
def load(name):
    if name not in _cache:
        m = trimesh.load(f'{GROUPS}/{name}.stl', process=True)
        _cache[name] = m
    return _cache[name].copy()

def rot_y(deg, about):
    a=math.radians(deg); c,s=math.cos(a),math.sin(a)
    R=np.array([[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]],float)
    T=np.eye(4); T[:3,3]=about; Ti=np.eye(4); Ti[:3,3]=-np.array(about)
    return T@R@Ti
def rot_z(deg, about):
    a=math.radians(deg); c,s=math.cos(a),math.sin(a)
    R=np.array([[c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1]],float)
    T=np.eye(4); T[:3,3]=about; Ti=np.eye(4); Ti[:3,3]=-np.array(about)
    return T@R@Ti
def trans(v):
    T=np.eye(4); T[:3,3]=v; return T

class Scene:
    def __init__(self): self.items=[]
    def add(self, name, color=None, T=None, clip=None, alpha=None, label=None):
        m = load(name)
        if T is not None: m.apply_transform(T)
        if clip is not None:
            try: m = m.slice_plane(clip[0], clip[1], cap=True)
            except Exception as e: print('clip fail', name, e)
            if m is None or len(m.faces)==0: return
        self.items.append(dict(name=label or name, mesh=m, color=hex2rgb(color or COL.get(name,'#aaaaaa'))))
    def bounds(self):
        b=np.array([it['mesh'].bounds for it in self.items]); return b[:,0].min(0), b[:,1].max(0)

@njit(cache=True)
def _raster(sx, sy, sz, cols, ids, W, H, zbuf, cbuf, idbuf, nbuf, nrm):
    n = sx.shape[0]
    for i in range(n):
        x0=sx[i,0]; x1=sx[i,1]; x2=sx[i,2]
        y0=sy[i,0]; y1=sy[i,1]; y2=sy[i,2]
        z0=sz[i,0]; z1=sz[i,1]; z2=sz[i,2]
        area=(x1-x0)*(y2-y0)-(x2-x0)*(y1-y0)
        if abs(area)<1e-12: continue
        minx=int(max(0, math.floor(min(x0,min(x1,x2)))))
        maxx=int(min(W-1, math.ceil(max(x0,max(x1,x2)))))
        miny=int(max(0, math.floor(min(y0,min(y1,y2)))))
        maxy=int(min(H-1, math.ceil(max(y0,max(y1,y2)))))
        for y in range(miny,maxy+1):
            py=y+0.5
            for x in range(minx,maxx+1):
                px=x+0.5
                w0=((x1-px)*(y2-py)-(x2-px)*(y1-py))/area
                w1=((x2-px)*(y0-py)-(x0-px)*(y2-py))/area
                w2=1.0-w0-w1
                if w0>=-1e-9 and w1>=-1e-9 and w2>=-1e-9:
                    z=w0*z0+w1*z1+w2*z2
                    if z>zbuf[y,x]:
                        zbuf[y,x]=z
                        cbuf[y,x,0]=cols[i,0]; cbuf[y,x,1]=cols[i,1]; cbuf[y,x,2]=cols[i,2]
                        idbuf[y,x]=ids[i]
                        nbuf[y,x,0]=nrm[i,0]; nbuf[y,x,1]=nrm[i,1]; nbuf[y,x,2]=nrm[i,2]

class Camera:
    def __init__(self, az, el, scale, center, W, H, shift=(0,0)):
        """az/el in degrees (camera direction FROM the target), scale = pixels per mm, center = world point at image centre."""
        a,e=math.radians(az),math.radians(el)
        d=np.array([math.cos(e)*math.cos(a), math.cos(e)*math.sin(a), math.sin(e)])   # towards camera
        up=np.array([0,0,1.0])
        r=np.cross(up,d)
        if np.linalg.norm(r)<1e-6:
            r=np.array([0,-1.0,0]); u=np.array([1.0,0,0]) if d[2]>0 else np.array([-1.0,0,0])   # top / bottom view: front (+x) at the top of the picture
        else:
            r/=np.linalg.norm(r); u=np.cross(d,r); u/=np.linalg.norm(u)
        self.d,self.r,self.u=d,r,u
        self.scale=scale; self.center=np.array(center,float); self.W=W; self.H=H; self.shift=shift
    def project(self, P):
        P=np.atleast_2d(np.array(P,float))-self.center
        x=P@self.r; y=P@self.u; z=P@self.d
        sx=self.W/2+self.shift[0]+self.scale*x
        sy=self.H/2+self.shift[1]-self.scale*y
        return sx,sy,z

def render(scene, cam, bg=(0.97,0.97,0.96), ss=2, light=(-0.45,0.55,0.70), outline=True, ambient=0.42, shadow=True, return_ids=False):
    """returns the image (H x W x 3, 0..1). With return_ids=True also the item number under every pixel (-1 = background); used to keep labels off other parts."""
    W,H=cam.W*ss,cam.H*ss
    c2=Camera.__new__(Camera); c2.__dict__.update(cam.__dict__); c2.scale=cam.scale*ss; c2.W=W; c2.H=H; c2.shift=(cam.shift[0]*ss,cam.shift[1]*ss)
    zbuf=np.full((H,W),-1e18); cbuf=np.zeros((H,W,3)); idbuf=np.full((H,W),-1,np.int32); nbuf=np.zeros((H,W,3))
    L=cam.r*light[0]+cam.u*light[1]+cam.d*light[2]; L/=np.linalg.norm(L)
    for k,it in enumerate(scene.items):
        m=it['mesh']; V=m.vertices; F=m.faces
        sx,sy,sz=c2.project(V)
        tri=F
        N=m.face_normals.copy()
        flip=(N@cam.d)<0; N[flip]*=-1
        inten=ambient+(1-ambient)*np.clip(N@L,0,1)
        cols=it['color'][None,:]*inten[:,None]
        ids=np.full(len(tri),k,np.int32)
        _raster(sx[tri],sy[tri],sz[tri],cols,ids,W,H,zbuf,cbuf,idbuf,nbuf,N)
    img=np.empty((H,W,3)); img[:]=np.array(bg)
    if shadow: img=_ground_shadow(img,scene,c2,bg)
    mask=idbuf>=0
    img[mask]=cbuf[mask]
    if outline:
        edge=np.zeros((H,W),bool)
        idd=idbuf
        edge[:,1:] |= (idd[:,1:]!=idd[:,:-1])
        edge[1:,:] |= (idd[1:,:]!=idd[:-1,:])
        zb=np.where(mask,zbuf,0)
        ddx=np.abs(zb[:,1:]-zb[:,:-1]); ddy=np.abs(zb[1:,:]-zb[:-1,:])
        zt=6.0   # mm depth jump
        edge[:,1:] |= (ddx>zt)&mask[:,1:]&mask[:,:-1]
        edge[1:,:] |= (ddy>zt)&mask[1:,:]&mask[:-1,:]
        # normal discontinuity (creases)
        nd=np.abs((nbuf[:,1:]*nbuf[:,:-1]).sum(-1)); nd2=np.abs((nbuf[1:,:]*nbuf[:-1,:]).sum(-1))
        edge[:,1:] |= (nd<0.55)&mask[:,1:]&mask[:,:-1]
        edge[1:,:] |= (nd2<0.55)&mask[1:,:]&mask[:-1,:]
        edge &= (mask | np.roll(mask,1,0) | np.roll(mask,1,1))
        from scipy.ndimage import binary_dilation
        edge=binary_dilation(edge,iterations=max(1,ss//2))
        img[edge&np.isfinite(zbuf)&(mask)]*=0.45
    img=img.reshape(cam.H,ss,cam.W,ss,3).mean(axis=(1,3))
    if return_ids:
        return np.clip(img,0,1), idbuf[ss//2::ss, ss//2::ss].copy()
    return np.clip(img,0,1)

def _ground_shadow(img,scene,c2,bg):
    lo,hi=scene.bounds()
    cx=(lo[0]+hi[0])/2; cy=(lo[1]+hi[1])/2
    rr=max(hi[0]-lo[0],hi[1]-lo[1])/2*1.02
    H,W=img.shape[:2]
    th=np.linspace(0,2*np.pi,90)
    pts=np.stack([cx+rr*np.cos(th),cy+rr*np.sin(th),np.zeros_like(th)],1)
    sx,sy,_=c2.project(pts)
    from matplotlib.path import Path
    path=Path(np.stack([sx,sy],1))
    yy,xx=np.mgrid[0:H,0:W]
    inside=path.contains_points(np.stack([xx.ravel()+0.5,yy.ravel()+0.5],1)).reshape(H,W)
    from scipy.ndimage import gaussian_filter
    a=gaussian_filter(inside.astype(float),sigma=max(4,W/90))*0.28
    img=img*(1-a[...,None])+np.array([0.35,0.35,0.35])*a[...,None]
    return img
