# Tools for Abadi Rover 2: STL files, numbers and pictures
Every script finds its files by itself, so you can start it from any folder. Change a number in `../robot2_params.scad`, then run `python run_all.py`.

**You need** OpenSCAD (the command `openscad`; if it is somewhere else, set the variable `OPENSCAD` to its full path) and Python 3 with these packages:
`pip install numpy scipy trimesh networkx matplotlib pillow numba`

| Command | What it does | Result |
|---|---|---|
| `python run_all.py` | runs the five steps below in order (about 3 minutes) | everything |
| `python export_stl.py` | makes one STL file for each printed part in `parts.txt` (35 parts), 4 at a time | `../stl/` |
| `python check_stl.py` | checks every STL: closed, one body, lowest point at z = 0, and writes the sizes | `results/stl_check.txt` |
| `python export_groups.py` | cuts the whole robot into named groups for the pictures | `work/groups/` (scratch, safe to delete) |
| `python summary.py` | mass, balance point, heights, tip-over, braking, push force, wheel torque, servo torque, print time | `results/numbers.json` and `results/numbers.txt` |
| `python make_pictures.py` | draws the 10 pictures with the new numbers | `../renders/` |

The scripts behind them: `analysis.py` (mass table, STL volumes), `phys.py` (tip-over model, the assumptions are in its first lines), `calc2.py` (torques, motors, mast), `printtable.py` (print list), `r2render.py` and `pics_*.py` (pictures).
Plastic mass and print times are rough (assumed): PETG 1.27 g/cm3, 1.9 minutes per gram plus 12 minutes.
