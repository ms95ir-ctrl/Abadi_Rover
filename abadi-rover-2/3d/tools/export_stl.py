"""Export every printed part to ../stl/NAME.stl (the part names are in parts.txt). Runs 4 OpenSCAD jobs at once.
   Usage:  python export_stl.py          (old STL files are deleted only after OpenSCAD has been found)
   A part is OK when OpenSCAD ends with exit code 0 and prints no WARNING or ERROR line."""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from r2paths import *

def export(name):
    log = LOGS / (name + '.log')
    cmd = [OPENSCAD, '-D', 'part="%s"' % name, '-o', str(STL / (name + '.stl')), 'print_parts.scad']
    r = subprocess.run(cmd, cwd=D3, capture_output=True, text=True)
    text = (r.stdout or '') + (r.stderr or '')
    log.write_text(text)
    bad = [l for l in text.splitlines() if 'WARNING' in l or 'ERROR' in l]
    return name, r.returncode, bad

if __name__ == '__main__':
    try:                                    # look for OpenSCAD first, so nothing is deleted when it is missing
        subprocess.run([OPENSCAD, '--version'], capture_output=True, check=True)
    except Exception:
        sys.exit('OpenSCAD was not found. Nothing was changed. Install OpenSCAD or set the OPENSCAD variable to its full path, then run this again.')
    STL.mkdir(exist_ok=True); LOGS.mkdir(parents=True, exist_ok=True)
    for f in STL.glob('*.stl'):
        f.unlink()
    names = lines('parts.txt')
    fail = 0
    with ThreadPoolExecutor(4) as ex:
        for name, code, bad in ex.map(export, names):
            ok = code == 0 and not bad
            fail += (not ok)
            print('%-18s %s' % (name, 'ok' if ok else 'FAILED exit %d %s' % (code, bad[:2])))
    print('%d parts, %d failed' % (len(names), fail))
    sys.exit(1 if fail else 0)
