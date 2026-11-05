// =====================================================================
// PRINT PARTS: every printed part, already turned into its printing orientation (lowest point on z = 0).
// Export one part:   openscad -D 'part="head_shell"' -o stl/head_shell.stl print_parts.scad
// Part names are listed in docs/mechanical-design.md (print list). Default output = the small parts together, spaced at least 5 mm apart (checked: the parts do not touch).
// =====================================================================
_robot2_lib = true;   // tells robot2_params.scad that it is used as a library (no demo shape)
include <robot2_params.scad>
use <base.scad>
use <mast.scad>
use <pan_tilt_interface.scad>
use <head.scad>

part = "small_parts";
seg_h_p = (z_mast_top - z_mast_bot) / 2;

module flat(zmin) { translate([0, 0, -zmin]) children(); }          // put lowest z on 0

module print_part(name) {
    // ---- base discs, 4 pieces each (FL = front left, FR, RL = rear left, RR); orientation = as built (floor / deck down), cover is flipped
    if (name == "tray_FL") flat(z_floor_b) piece3d("FL") tray_full();
    else if (name == "tray_FR") flat(z_floor_b) piece3d("FR") tray_full();
    else if (name == "tray_RL") flat(z_floor_b) piece3d("RL") tray_full();
    else if (name == "tray_RR") flat(z_floor_b) piece3d("RR") tray_full();
    else if (name == "deck_FL") flat(z_deck_b) piece3d("FL") deck_full();
    else if (name == "deck_FR") flat(z_deck_b) piece3d("FR") deck_full();
    else if (name == "deck_RL") flat(z_deck_b) piece3d("RL") deck_full();
    else if (name == "deck_RR") flat(z_deck_b) piece3d("RR") deck_full();
    else if (name == "cover_FL") translate([0, 0, z_cover_top]) rotate([180, 0, 0]) piece3d("FL") cover_full();
    else if (name == "cover_FR") translate([0, 0, z_cover_top]) rotate([180, 0, 0]) piece3d("FR") cover_full();
    else if (name == "cover_RL") translate([0, 0, z_cover_top]) rotate([180, 0, 0]) piece3d("RL") cover_full();
    else if (name == "cover_RR") translate([0, 0, z_cover_top]) rotate([180, 0, 0]) piece3d("RR") cover_full();
    // ---- small base parts
    else if (name == "caster_cup") translate([0, 0, z_floor_t + 3.4]) rotate([180, 0, 0]) caster_cup();   // flange down
    else if (name == "caster_ring") flat(3) caster_ring();
    else if (name == "motor_cap") translate([0, 0, 16]) rotate([180, 0, 0]) motor_cap();                  // flat top down
    else if (name == "skid") skid();
    else if (name == "plug_hood") translate([-relief_cx, relief_cy, hood_top_z]) rotate([180, 0, 0]) plug_hood();   // upside down (hood top on the bed), flange up; the 45 degree fillet under the flange makes supports unnecessary
    // optional bumper (not in the first build): arc standing up, arm lying on the bed (arc and arm both start at z = bump_z0): no supports
    else if (name == "bumper_R") flat(bump_z0) bumper_seg(0);
    else if (name == "bumper_C") flat(bump_z0) bumper_seg(1);
    else if (name == "bumper_L") flat(bump_z0) bumper_seg(2);
    // ---- mast: half shells lie on their outer back face, open side up
    else if (name == "mast_lo_front") translate([0, 0, 22]) rotate([0, 90, 0]) shell_half(+1, seg_h_p, [foot_sock_h / 2]);
    else if (name == "mast_lo_back")  translate([0, 0, 22]) rotate([0, -90, 0]) shell_half(-1, seg_h_p, [foot_sock_h / 2]);
    else if (name == "mast_up_front") translate([0, 0, 22]) rotate([0, 90, 0]) shell_half(+1, seg_h_p, [seg_h_p - neck_sock_h / 2]);
    else if (name == "mast_up_back")  translate([0, 0, 22]) rotate([0, -90, 0]) shell_half(-1, seg_h_p, [seg_h_p - neck_sock_h / 2]);
    else if (name == "collar_front") collar_half(+1);
    else if (name == "collar_back") collar_half(-1);
    else if (name == "foot_plate") foot_plate();
    // ---- INTERFACE plate + default pan/tilt
    else if (name == "neck_plate") translate([0, 0, neck_plate_t]) rotate([180, 0, 0]) neck_plate();       // top face down, socket up
    else if (name == "turntable") translate([0, 0, tt_t]) rotate([180, 0, 0]) turntable();                  // plate top down, skirt up
    else if (name == "yoke_servo_side") yoke_half(true);
    else if (name == "yoke_plain_side") yoke_half(false);
    // ---- head
    else if (name == "head_shell") translate([0, 0, head_d / 2]) rotate([0, 90, 0]) head_shell_full();      // front face down
    else if (name == "head_lid") translate([0, 0, head_d / 2 + 4]) rotate([0, -90, 0]) head_lid();            // interface pad down
    else if (name == "pivot_bush") pivot_bush();
    else if (name == "cam_cover") cam_cover();                                                                 // optional camera slide cover, 62 x 20 x 1 mm, lies flat
}

module small_parts() {
    print_part("caster_cup");
    translate([45, 0, 0]) print_part("caster_ring");
    for (i = [0 : 3]) translate([90 + i * 45, 0, 0]) print_part("motor_cap");
    for (i = [0 : 3]) translate([i * 20, 40, 0]) print_part("skid");
    translate([90, 40, 0]) print_part("pivot_bush");
    translate([150, 90, 0]) print_part("plug_hood");
    translate([45, 100, 0]) print_part("cam_cover");
    // the two collar halves stand side by side (each is 25 x 77 mm in plan), clear of the skid row
    translate([6, 95, 0]) print_part("collar_front");
    translate([-6, 95, 0]) print_part("collar_back");
}

if (part == "small_parts") small_parts();
else print_part(part);
