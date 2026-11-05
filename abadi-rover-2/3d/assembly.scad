// =====================================================================
// WHOLE ROBOT 2 (telepresence robot). Printed parts (orange / grey / blue) and bought parts ("ghosts").
// Everything is placed in the robot frame: origin on the floor under the centre of the base, +x = front, +y = left, +z = up.
//   group   = "" draws the whole robot; a group name draws only that group (used by the picture script)
//   tilt    = head nod in degrees (positive = looks down),  pan = head turn in degrees (positive = to the left)
//   cables  = draw the cable routes
// Note: the OpenSCAD *preview* window can show the half-shell mast wrongly (a known preview quirk with coplanar
// faces); press F6 (full render) to see it right. The STL export is always right.
// =====================================================================
_robot2_lib = true;   // tells robot2_params.scad that it is used as a library (no demo shape)
include <robot2_params.scad>
use <robot2_ghosts.scad>
use <base.scad>
use <mast.scad>
use <pan_tilt_interface.scad>
use <head.scad>

group  = "";
tilt   = 0;
pan    = 0;
cables = true;

module G(name) { if (group == "" || group == name) children(); }

seg_h_a = (z_mast_top - z_mast_bot) / 2;
x_f_a   = head_d / 2;

// ----------------------------------------------------------------- base: printed
module base_printed() {
    G("tray")   tray_full();
    G("deck")   deck_full();
    G("cover")  cover_full();
    G("caster") translate([caster_x, 0, 0]) { caster_cup(); caster_ring(); }
    G("motorcaps") for (s = [-1, 1]) for (yc = [58, 90]) translate([axle_x - 20, s * yc - 6, wheel_r]) motor_cap();
    G("skids")  for (p = skid_pos) translate([p[0], p[1], skid_gap]) skid();
    G("bumper") bumper();
}
// ----------------------------------------------------------------- base: bought parts
module base_bought() {
    G("ball")    translate([caster_x, 0, caster_ball / 2]) ghost_ball();
    G("wheels")  for (s = [-1, 1]) translate([axle_x, s * wheel_y, wheel_r]) ghost_wheel();
    G("motors")  for (s = [-1, 1]) translate([axle_x, s * motor_face_y, wheel_r]) mirror([0, s < 0 ? 1 : 0, 0]) ghost_motor();
    G("sonars")  for (s = [-1, 1]) rotate(s * sonar_ang) translate([base_r - 0.5, 0, sonar_z]) ghost_sonar();
    G("cliffs")  for (s = [-1, 1]) rotate(s * cliff_ang) translate([cliff_r, 0, z_floor_t + 3.5]) ghost_cliff();
    G("battery") translate([batt_x - batt_l / 2, batt_y - batt_w / 2, z_floor_t]) cube([batt_l, batt_w, batt_h]);
    G("bms")     translate([batt_x - 28, -10.5, z_floor_t + batt_h]) cube([56, 21, 4]);
    G("xl")      for (q = xl_pos) translate([q[0] - xl_l / 2, q[1] - xl_w / 2, z_floor_t]) cube([xl_l, xl_w, xl_h]);
    G("minibuck") for (q = mini_pos) translate([q[0] - mini_l / 2, q[1] - mini_w / 2, z_floor_t]) cube([mini_l, mini_w, mini_h]);
    G("fuses")   for (q = fuse_pos) translate([q[0] - fuse_l / 2, q[1] - fuse_w / 2, z_floor_t]) cube([fuse_l, fuse_w, fuse_h]);
    G("wagos")   for (q = wago_pos) translate([q[0] - wago_l / 2, q[1] - wago_w / 2, z_floor_t]) cube([wago_l, wago_w, wago_h]);
    G("charger") translate([chg_pos[0] - chg_l / 2, chg_pos[1] - chg_w / 2, z_floor_t + 3]) cube([chg_l, chg_w, chg_h]);
    G("switch")  translate([-sqrt(base_r * base_r - sw_pos_y * sw_pos_y) + 2, sw_pos_y, 40]) rotate([0, -90, 0]) ghost_switch();
    // deck level
    translate([mb_x0, mb_y0, z_deck_t + mb_stand]) rotate(90) {
        G("mb_pcb") mb_pcb();   G("mb_esp") mb_esp();   G("mb_drv") mb_drv();   G("mb_pca") mb_pca();
        G("mb_gyro") mb_gyro(); G("mb_terms") mb_terms(); G("mb_caps") mb_caps(); G("mb_hdrs") mb_hdrs();
    }
    translate([sbc_x0, sbc_y0, z_deck_t + sbc_stand]) rotate(180) {
        G("sbc_pcb") sbc_pcb();  G("sbc_ports") sbc_ports();  G("sbc_cooler") sbc_cooler();
    }
}

// ----------------------------------------------------------------- mast (printed)
module mast_all() {
    G("foot") translate([mast_x, 0, z_deck_t + foot_pad_h]) foot_plate();
    G("mast_lo_f") translate([mast_x, 0, z_mast_bot]) shell_half(+1, seg_h_a, [foot_sock_h / 2]);
    G("mast_lo_b") translate([mast_x, 0, z_mast_bot]) shell_half(-1, seg_h_a, [foot_sock_h / 2]);
    G("mast_up_f") translate([mast_x, 0, z_mast_bot + seg_h_a]) shell_half(+1, seg_h_a, [seg_h_a - neck_sock_h / 2]);
    G("mast_up_b") translate([mast_x, 0, z_mast_bot + seg_h_a]) shell_half(-1, seg_h_a, [seg_h_a - neck_sock_h / 2]);
    G("collar_f") translate([mast_x, 0, z_mast_bot + seg_h_a - collar_h / 2]) collar_half(+1);
    G("collar_b") translate([mast_x, 0, z_mast_bot + seg_h_a - collar_h / 2]) collar_half(-1);
}

// ----------------------------------------------------------------- neck, pan/tilt, head
module neck_and_head() {
    G("neck_plate") translate([mast_x, 0, z_neck_plate_top - neck_plate_t]) neck_plate();
    G("pan_horn")   translate([mast_x, 0, z_neck_plate_top + neck_ped_h]) cylinder(d = horn_d, h = horn_t, $fn = 40);
    G("pan_servo")  translate([mast_x, 0, z_neck_plate_top + neck_ped_h + srv_spline_above_case]) rotate([0, 180, 0]) ghost_servo();
    translate([mast_x, 0, 0]) rotate([0, 0, pan]) {
        G("turntable") translate([0, 0, z_tt_top - tt_t]) turntable();
        G("yoke")      translate([0, 0, z_tt_top]) { yoke_half(true); mirror([0, 1, 0]) yoke_half(false); }
        translate([0, 0, head_axis_h]) rotate([0, tilt, 0]) translate([-head_axis_y, 0, -head_axis_z]) head_all();
    }
}
module head_all() {
    G("head_shell") head_shell_full();
    G("head_lid")   head_lid();
    G("pivot_bush") translate([head_axis_y, -head_w / 2, head_axis_z]) rotate([90, 0, 0]) pivot_bush();
    G("screen")     translate([x_f_a - lip_t, 0, 0]) rotate([0, 0, -90]) ghost_screen();
    G("webcam")     translate([x_f_a - brow_front_t - 0.5 - cam_d / 2, 0, head_h / 2 + 0.8]) rotate([0, 0, -90]) ghost_webcam();
    G("tilt_servo") translate([head_axis_y, head_w / 2 - head_wall - head_boss_t + srv_ear_below_top, head_axis_z])
        multmatrix([[0, -1, 0, 0], [0, 0, 1, 0], [-1, 0, 0, 0], [0, 0, 0, 1]]) { ghost_servo(); ghost_horn(); }
}

// ----------------------------------------------------------------- cables (thin tubes)
module tube(pts, d = 4) {
    for (i = [0 : len(pts) - 2]) hull() { translate(pts[i]) sphere(d = d, $fn = 10); translate(pts[i + 1]) sphere(d = d, $fn = 10); }
}
module cable_routes() {
    hdmi = [[-13.5, 100, 86], [20, 100, 90], [mast_x - 10, 40, 92], [mast_x - 12, -15, 92], [mast_x - 12, -19, 150],
            [mast_x - 12, -19, z_neck_plate_top + 2], [mast_x - 12, -19, z_tt_top + 8], [mast_x - 20, -40, z_tt_top + 30],
            [mast_x - 20, -10, z_tt_top + 55]];
    usb = [[-70, 60, 86], [-50, 40, 90], [mast_x - 14, 20, 92], [mast_x - 14, -8, 92], [mast_x - 14, -17, 150],
           [mast_x - 14, -17, z_neck_plate_top + 2], [mast_x - 16, -17, z_tt_top + 8], [mast_x - 24, -30, z_tt_top + 36], [mast_x - 24, 0, z_tt_top + 66]];
    pwr = [[-30, -60, 82], [mast_x - 8, -20, 92], [mast_x - 8, -21, 150], [mast_x - 8, -21, z_neck_plate_top + 2],
           [mast_x - 8, -23, z_tt_top + 10], [mast_x - 18, -40, z_tt_top + 28], [mast_x - 18, -20, z_tt_top + 58]];
    G("cable_hdmi") tube(hdmi, 5);
    G("cable_usb")  tube(usb, 3.5);
    G("cable_pwr")  tube(pwr, 3.5);
}

// ----------------------------------------------------------------- assemble
base_printed();
base_bought();
mast_all();
neck_and_head();
if (cables) cable_routes();
