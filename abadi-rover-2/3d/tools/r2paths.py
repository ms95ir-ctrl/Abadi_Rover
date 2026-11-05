"""Shared paths for the Abadi Rover 2 tools. Every script imports this, so nothing depends on where you start it from."""
import os
from pathlib import Path

TOOLS = Path(__file__).resolve().parent      # .../abadi-rover-2/3d/tools
D3 = TOOLS.parent                            # .../abadi-rover-2/3d  (the .scad files)
STL = D3 / 'stl'                             # print-ready STL files (one per printed part)
RENDERS = D3 / 'renders'                     # the 10 pictures
WORK = TOOLS / 'work'                        # scratch folder (group STL files for the pictures, logs). Safe to delete.
GROUPS = WORK / 'groups'
LOGS = WORK / 'logs'
OPENSCAD = os.environ.get('OPENSCAD', 'openscad')   # set the OPENSCAD variable if openscad is not on your PATH

def lines(name):
    return [l.strip() for l in open(TOOLS / name) if l.strip() and not l.startswith('#')]

def _code_lines():
    """the lines of robot2_params.scad without the // comments"""
    return [l.split('//')[0] for l in open(D3 / 'robot2_params.scad')]

def scad_value(name, default=None):
    """Read a plain 'name = number;' value from robot2_params.scad (first match; several per line are fine)."""
    import re
    for l in _code_lines():
        m = re.search(r'(?<![\w.])%s\s*=\s*(-?[0-9.]+)\s*;' % re.escape(name), l)
        if m:
            return float(m.group(1))
    return default

def scad_array(name):
    """Read a list like  name = [[95, 58], [95, -58]];  from robot2_params.scad (numbers only)."""
    import ast, re
    for l in _code_lines():
        m = re.search(r'(?<![\w.])%s\s*=\s*(\[.*?\])\s*;' % re.escape(name), l)
        if m:
            return ast.literal_eval(m.group(1))
    return None
