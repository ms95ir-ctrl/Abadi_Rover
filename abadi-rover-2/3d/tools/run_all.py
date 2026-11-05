"""Run everything in the right order: STL files, checks, group files, numbers, pictures. Takes about 3 minutes.
   Usage:  python run_all.py"""
import subprocess, sys
from r2paths import TOOLS
for script in ('export_stl.py', 'check_stl.py', 'export_groups.py', 'summary.py', 'make_pictures.py'):
    print('=== ' + script)
    r = subprocess.run([sys.executable, script], cwd=TOOLS)
    if r.returncode != 0:
        sys.exit('stopped: %s failed' % script)
print('all done')
