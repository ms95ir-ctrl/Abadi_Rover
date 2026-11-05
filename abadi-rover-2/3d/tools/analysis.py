"""Mass, centre of gravity (CoG) and printed mass of Robot 2.
   Reads the group STL files in work/groups (python export_groups.py makes them) and adds the bought parts as numbers.
   Printed mass = STL volume x PETG density x a fill factor (how much of the volume is plastic after slicing; ASSUMED).
   Usage:  python analysis.py   (prints the table and writes results/mass_rows.json)"""
import json, math
import numpy as np
from r2render import load
from r2paths import *
RHO = 1.27   # g/cm3 PETG
# ---- printed groups: (group, fill factor)  [assumed]
PRINTED = {
 'tray':0.75,'deck':0.50,'cover':0.75,'plug_hood':0.9,'caster':0.9,'motorcaps':0.9,'skids':0.9,
 'foot':0.6,'mast_lo_f':0.85,'mast_lo_b':0.85,'mast_up_f':0.85,'mast_up_b':0.85,'collar_f':0.8,'collar_b':0.8,
 'neck_plate':0.45,'turntable':0.55,'yoke':0.5,'head_shell':0.8,'head_lid':0.6,'pivot_bush':1.0,'cam_cover':1.0}
# optional bumper (NOT in the first build): used only for the "with bumper" variant
OPTIONAL_PRINTED = {'bumper':0.9}
# ---- bought parts: (group, mass g, note)   (A) = assumed
BOUGHT = {
 'ball':(17,'16 mm steel ball (calc)'),
 'wheels':(60,'2 x 30 g (A)'),
 'motors':(180,'2 x 90 g (Pololu 25D, about 90 g each)'),
 'sonars':(18,'2 x 9 g (A)'),
 'cliffs':(8,'2 x 4 g (A)'),
 'battery':(115,'2 x 18650 about 46 g + holder (A)'),
 'bms':(6,'(A)'),
 'xl':(110,'2 x XL4016 with heat sink (A)'),
 'minibuck':(8,'2 x 4 g (A)'),
 'fuses':(54,'6 holders with fuses, cheap build with route B (A)'),
 'wagos':(40,'4 five-way lever connectors, about 10 g each (A)'),
 'charger':(12,'USB-C charger board (A)'),
 'switch':(15,'(A)'),
 'button':(20,'call / STOP button with cap and nut (A)'),
 'led':(1,'5 mm LED (A)'),
 'speaker':(20,'40 mm speaker, route B (A)'),
 'sbc_pcb':(46,'Pi 5 about 46 g (A)'),'sbc_ports':(0,''),'sbc_cooler':(10,'Active Cooler (A)'),
 'mb_pcb':(30,'PCB 100x100x1.6 (calc)'),'mb_esp':(14,'(A)'),'mb_drv':(8,'(A)'),'mb_pca':(16,'(A)'),'mb_gyro':(3,'(A)'),'mb_terms':(20,'(A)'),'mb_caps':(6,'(A)'),'mb_hdrs':(12,'(A)'),
 'pan_servo':(55,'MG996R 55 g (shop listings)'),'pan_horn':(5,'(A)'),
 'tilt_servo':(60,'MG996R 55 g + horn (A)'),
 'screen':(230,'7 in HDMI screen with driver board, 200-250 g (task)'),
 'webcam':(60,'(A)'),
}
EXTRA = [  # (name, mass g, (x,y,z), class)
 ('wiring, connectors, zip ties (base)',60,(0,0,40),'base'),
 ('screws, nuts, inserts (base)',45,(0,0,50),'base'),
 ('cables in mast (HDMI, USB, 5 V, servo leads)',45,(62,-18,190),'mast'),
 ('screws, inserts (mast)',10,(62,0,190),'mast'),
 ('cables in neck and head',40,(62,0,380),'head'),
 ('screws, inserts, foam (head)',25,(62,0,400),'head'),
]
HEAD_G={'head_shell','head_lid','pivot_bush','screen','webcam','tilt_servo','turntable','yoke','neck_plate','pan_horn','pan_servo','led','cam_cover'}
MAST_G={'foot','mast_lo_f','mast_lo_b','mast_up_f','mast_up_b','collar_f','collar_b'}
# the part of the head that nods with the tilt servo (used for the tilt torque)
TILTING_G={'head_shell','head_lid','pivot_bush','screen','webcam','led','cam_cover'}

def build_rows():
    rows=[]
    for g,f in PRINTED.items():
        m=load(g); vol=m.volume/1000.0
        rows.append(dict(name=g,mass=vol*RHO*f,pos=m.center_mass.tolist(),kind='printed',vol=vol,f=f))
    for g,(mass,note) in BOUGHT.items():
        if mass==0: continue
        m=load(g)
        rows.append(dict(name=g,mass=mass,pos=m.center_mass.tolist(),kind='bought',note=note))
    for n,mass,pos,grp in EXTRA:
        rows.append(dict(name=n,mass=mass,pos=list(pos),kind='extra',cls=grp))
    def cls(r):
        if 'cls' in r: return r['cls']
        n=r['name']
        if n in HEAD_G: return 'head'
        if n in MAST_G: return 'mast'
        return 'base'
    for r in rows: r['cls']=cls(r)
    return rows

def total(rs):
    M=sum(r['mass'] for r in rs); c=sum(np.array(r['pos'])*r['mass'] for r in rs)/M
    return M,c

rows=build_rows()

if __name__=='__main__':
    for k in ('base','mast','head'):
        rs=[r for r in rows if r['cls']==k]; M,c=total(rs); print(k, round(M), c.round(1))
    M,c=total(rows); print('TOTAL',round(M),c.round(1))
    print('printed', round(sum(r['mass'] for r in rows if r['kind']=='printed')), 'bought', round(sum(r['mass'] for r in rows if r['kind']=='bought')), 'extra', round(sum(r['mass'] for r in rows if r['kind']=='extra')))
    for r in sorted(rows,key=lambda r:-r['mass'])[:70]: print(f"{r['name']:45s} {r['mass']:7.0f} g  x={r['pos'][0]:7.1f} y={r['pos'][1]:7.1f} z={r['pos'][2]:7.1f}  {r['cls']} {r['kind']}")
    RES=TOOLS/'results'; RES.mkdir(exist_ok=True)
    json.dump(rows,open(RES/'mass_rows.json','w'),indent=1)
