import sys, json, pcbnew
b = pcbnew.LoadBoard(sys.argv[1]); OX, OY = 100.0, 50.0
def U(p): return [round(p.x/1e6 - OX, 3), round(100 - (p.y/1e6 - OY), 3)]
d = {"tracks": [], "vias": [], "pads": []}
for t in b.GetTracks():
    if t.GetClass() == "PCB_VIA":
        d["vias"].append({"p": U(t.GetPosition()), "d": t.GetWidth()/1e6, "net": t.GetNetname()})
    else:
        d["tracks"].append({"a": U(t.GetStart()), "b": U(t.GetEnd()), "w": t.GetWidth()/1e6, "top": t.GetLayer() == pcbnew.F_Cu, "net": t.GetNetname()})
for p in b.GetPads():
    d["pads"].append({"p": U(p.GetPosition()), "d": p.GetSizeX()/1e6, "h": p.GetDrillSizeX()/1e6, "npth": p.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH, "net": p.GetNetname(), "ref": p.GetParent().GetReference(), "n": p.GetNumber()})
json.dump(d, open(sys.argv[2], "w"))
