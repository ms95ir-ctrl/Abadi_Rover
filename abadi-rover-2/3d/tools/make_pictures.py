"""Make all 10 pictures into ../renders (the file names stay the same). Needs the STL files, the group files and results/numbers.json:
   python export_stl.py ; python export_groups.py ; python summary.py ; python make_pictures.py"""
import pics_iso_front_side, pics_exploded, pics_head, pics_sketch_layout, pics_section_stability, pics_printparts
import json
from r2paths import TOOLS

if __name__ == '__main__':
    cg = json.load(open(TOOLS / 'results' / 'numbers.json'))['mass']['cog_mm']
    pics_iso_front_side.CG = (cg[0], cg[2])
    pics_iso_front_side.iso(); pics_iso_front_side.front_side()      # robot2-iso, robot2-front, robot2-side
    pics_exploded.exploded()                                          # robot2-base-exploded
    pics_head.head_view()                                             # robot2-head-pantilt
    pics_sketch_layout.sketch(); pics_sketch_layout.layout()          # robot2-sketch-side-phone, robot2-layout-top
    pics_section_stability.section(); pics_section_stability.stability()   # robot2-section, robot2-stability
    pics_printparts.main()                                            # robot2-print-parts
