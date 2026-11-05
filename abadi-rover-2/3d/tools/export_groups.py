"""Export the groups of assembly.scad (the whole robot split into named pieces) to work/groups/NAME.stl.
   The picture scripts read these files. Usage:  python export_groups.py"""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from r2paths import *

def export(name):
    cmd = [OPENSCAD, '-D', 'group="%s"' % name, '-o', str(GROUPS / (name + '.stl')), 'assembly.scad']
    r = subprocess.run(cmd, cwd=D3, capture_output=True, text=True)
    text = (r.stdout or '') + (r.stderr or '')
    (LOGS / ('group_' + name + '.log')).write_text(text)
    bad = [l for l in text.splitlines() if 'WARNING' in l or 'ERROR' in l]
    return name, r.returncode, bad

if __name__ == '__main__':
    GROUPS.mkdir(parents=True, exist_ok=True); LOGS.mkdir(parents=True, exist_ok=True)
    for f in GROUPS.glob('*.stl'):
        f.unlink()
    names = lines('groups.txt')
    fail = 0
    with ThreadPoolExecutor(4) as ex:
        for name, code, bad in ex.map(export, names):
            ok = code == 0 and not bad
            fail += (not ok)
            print('%-14s %s' % (name, 'ok' if ok else 'FAILED exit %d %s' % (code, bad[:2])))
    print('%d groups, %d failed' % (len(names), fail))
    sys.exit(1 if fail else 0)
