// =====================================================================
// WHOLE ROBOT 2 (telepresence robot). Printed parts (orange / grey / blue) and bought parts ("ghosts").
// Everything is placed in the robot frame: origin on the floor under the centre of the base, +x = front, +y = left, +z = up.
//   group   = "" draws the whole robot; a group name draws only that group (used by the picture script)
//   tilt    = head nod in degrees. SAME SIGN AS tilt_range AND THE SERIAL PROTOCOL: 0 = level, positive = looks UP, negative = looks DOWN.
//   pan     = head turn in degrees, positive = to the LEFT seen from above (the serial protocol uses + = right: flip the sign when you copy numbers).
//   show_bumper / show_plugs = draw the optional bumper (with its switches) / the servo-plug ghosts on the PCA9685 (also drawn when group names them)
//   show_speakerphone / show_bundle = draw the route A speakerphone puck on the cover top / the cable bundle + HDMI plug test ghosts in the neck (they turn with `pan`)
//   cam_cover_pull = how far the camera slide cover is pulled out of the brow, in mm (0 = closed, cov_pull = 24 = open)
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
show_bumper = false;   // the bumper is optional and not in the first build, so it is not drawn unless you ask
show_plugs  = false;   // servo plugs + wire room on the PCA9685 (ghost, for fit checks)
show_speakerphone = false;   // route A: USB speakerphone puck on the cover top (ghost)
cam_cover_pull = 0;    // camera slide cover: 0 = closed (shuts the lens), cov_pull (24 mm) = open, lens window free
show_bundle = false;   // cable bundle 25 x 12 and HDMI plug 21 x 11 through the neck (ghosts for the pan test; they sit in the turntable slot and turn with the head)

module G(name) { if (group == "" || group == name) children(); }
module GO(name, flag) { if (group == name || (group == "" && flag)) children(); }   // optional things: drawn when asked for by name or by flag

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
    G("plug_hood") if (plug_relief) plug_hood();
    GO("bumper", show_bumper) bumper();
}
// ----------------------------------------------------------------- base: bought parts
module base_bought() {
    G("ball")    translate([caster_x, 0, caster_ball / 2]) ghost_ball();
    G("wheels")  for (s = [-1, 1]) translate([axle_x, s * wheel_y, wheel_r]) ghost_wheel();
    G("motors")  for (s = [-1, 1]) translate([axle_x, s * motor_face_y, wheel_r]) mirror([0, s < 0 ? 1 : 0, 0]) ghost_motor();
    G("sonars")  for (s = [-1, 1]) rotate(s * sonar_ang) translate([base_r - 0.5, 0, sonar_z]) ghost_sonar();
    G("cliffs")  for (s = [-1, 1]) rotate(s * cliff_ang) translate([cliff_r, 0, z_floor_t + 3.5]) rotate(90) ghost_cliff();   // long side along the arc, like the two bosses
    G("battery") translate([batt_x - batt_l / 2, batt_y - batt_w / 2, z_floor_t]) cube([batt_l, batt_w, batt_h]);
    G("bms")     translate([batt_x - 28, -10.5, z_floor_t + batt_h]) cube([56, 21, 4]);
    G("xl")      for (q = xl_pos) translate([q[0] - xl_l / 2, q[1] - xl_w / 2, z_floor_t]) cube([xl_l, xl_w, xl_h]);
    G("minibuck") for (q = mini_pos) translate([q[0] - mini_l / 2, q[1] - mini_w / 2, z_floor_t]) cube([mini_l, mini_w, mini_h]);
    G("fuses")   for (q = fuse_pos) translate([q[0] - fuse_l / 2, q[1] - fuse_w / 2, z_floor_t]) cube([fuse_l, fuse_w, fuse_h]);
    G("wagos")   for (q = wago_pos) translate([q[0] - wago_l / 2, q[1] - wago_w / 2, z_floor_t]) cube([wago_l, wago_w, wago_h]);
    G("charger") translate([chg_pos[0] - chg_l / 2, chg_pos[1] - chg_w / 2, z_floor_t + 3]) cube([chg_l, chg_w, chg_h]);
    G("switch")  translate([-sqrt(base_r * base_r - sw_pos_y * sw_pos_y) - 2, sw_pos_y, 40]) ghost_switch();   // ghost_switch already lies along +x: it goes through the d19 rim hole, 2 mm out, 16 mm in
    G("button")  translate([btn_pos[0], btn_pos[1], z_cover_top]) ghost_button();                                  // call / STOP button in the cover top (R23)
    G("speaker") if (spk_place) translate([spk_pos[0], spk_pos[1], cover_in_z - 2 * eps]) ghost_speaker40();                // route B speaker under the grille (R23)
    GO("speakerphone", show_speakerphone) translate([spkA_pos[0], spkA_pos[1], z_cover_top]) ghost_speakerphone();   // route A flat spot (R23)
    GO("bump_switches", show_bumper) if (bumper_slots)
        for (s = [-1, 1]) rotate(s * bump_ang) translate([bump_arm_r0 - 1 - bump_pad_l / 2, 0, z_floor_t + bump_pad_h]) ghost_bump_switch();
    // deck level
    translate([mb_x0, mb_y0, z_deck_t + mb_stand]) rotate(90) {
        G("mb_pcb") mb_pcb();   G("mb_esp") mb_esp();   G("mb_drv") mb_drv();   G("mb_pca") mb_pca();
        G("mb_gyro") mb_gyro(); G("mb_terms") mb_terms(); G("mb_caps") mb_caps(); G("mb_hdrs") mb_hdrs();
        GO("mb_plugs", show_plugs) mb_plugs();
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
    translate([mast_x, 0, 0]) rotate([0, 0, pan]) {
        // the pan servo BODY turns with the turntable (only its horn is fixed to the plate), so it is drawn inside the turning block
        G("pan_servo") translate([0, 0, z_neck_plate_top + neck_ped_h + srv_spline_above_case]) rotate([0, 180, 0]) ghost_servo();
        G("turntable") translate([0, 0, z_tt_top - tt_t]) turntable();
        if (head_has_default_tilt()) G("yoke") translate([0, 0, z_tt_top]) { yoke_half(true); mirror([0, 1, 0]) yoke_half(false); }
        // rotate about +y by -tilt: with positive tilt the front of the head (+x) goes UP (rotating about +y by a positive angle would put it down)
        translate([0, 0, head_axis_h]) rotate([0, -tilt, 0]) translate([-head_axis_y, 0, -head_axis_z]) head_all();
        // test ghosts (finding 20): the bundle and the HDMI plug stand in the turntable slot (centre y = bundle_cy) from below the plate to above the turntable and turn with it
        GO("bundle", show_bundle) translate([0, bundle_cy, z_neck_plate_bot - 30]) ghost_bundle(z_tt_top + 20 - (z_neck_plate_bot - 30));
        GO("hdmi_plug", show_bundle) translate([0, bundle_cy, z_neck_plate_bot - 5]) ghost_hdmi_plug(hdmi_plug_l);
    }
}
module head_all() {
    G("head_shell") head_shell_full();
    G("head_lid")   head_lid();
    if (head_has_default_tilt()) G("pivot_bush") translate([head_axis_y, -head_w / 2, head_axis_z]) rotate([90, 0, 0]) pivot_bush();
    G("screen")     translate([x_f_a - lip_t, 0, 0]) rotate([0, 0, -90]) ghost_screen();
    G("webcam")     translate([x_f_a - brow_front_t - cam_gap - cam_d / 2, 0, head_h / 2 + 0.8]) rotate([0, 0, -90]) ghost_webcam();
    G("led")        translate([x_f_a - brow_front_t, led_y, head_h / 2 + 1 + cam_h / 2 + cam_lens_dz]) ghost_led5();        // camera-live LED in the brow front wall (R23)
    // camera slide cover (R23), shown CLOSED unless cam_cover_pull is set (cov_pull = fully open): local x -> head y, local y -> head z, local z -> head x
    G("cam_cover")  multmatrix([[0, 0, 1, x_f_a - cov_skin - cov_play / 2 - cov_t], [1, 0, 0, cov_y0 + cam_cover_pull], [0, 1, 0, head_h / 2 + 1 + cam_h / 2 + cam_lens_dz - cov_h / 2], [0, 0, 0, 1]]) color("goldenrod") cam_cover();
    if (head_has_default_tilt()) G("tilt_servo") translate([head_axis_y, head_w / 2 - head_wall - head_boss_t + srv_ear_below_top, head_axis_z])
        multmatrix([[0, -1, 0, 0], [0, 0, 1, 0], [-1, 0, 0, 0], [0, 0, 0, 1]]) { ghost_servo(); ghost_horn(); }
}

// ----------------------------------------------------------------- cables (thin tubes)
// ILLUSTRATION ONLY (nothing printed or exported depends on them). The three cables are drawn along the real openings, so that they do not cut through printed parts:
//   SBC port -> over the deck -> down through the deck slot beside the SBC (the 36 x 10 mm slot at y 18 to 28; the build may use any free slot) -> under the deck ->
//   up through the 42 x 26 mm mast cable hole in the deck -> foot plate opening -> mast channel -> neck-plate opening -> turntable slot -> 14 x 30 mm cable slot in the head bottom -> inside the head.
// The 5 V power cable starts in the lower compartment (on top of the XL4016 module). Positions inside the head are only a sketch (the cables end at the screen and the camera).
// The two plug ends are left out of the picture (the tubes stop at the front of the SBC ports); the cables at the neck do not turn with `pan` in this picture.
module tube(pts, d = 4) {
    for (i = [0 : len(pts) - 2]) hull() { translate(pts[i]) sphere(d = d, $fn = 10); translate(pts[i + 1]) sphere(d = d, $fn = 10); }
}
module cable_routes() {
    cy = bundle_cy;                                   // -19: the bundle line through the neck plate opening, the turntable slot and the head slot
    zt = z_tt_top;
    x_h = 54;  x_u = 59;  x_p = 59;                   // x of the HDMI, USB and power tubes in the mast (the head slot is x 50 to 64, the screen starts at x 63)
    y_u = cy - 3;  y_p = cy + 3;                      // USB and power sit either side of the HDMI line in y
    hdmi = [[-27, 97, 86], [-27, 106, 85], [14, 108, 83], [22, 100, 82], [22, 30, 80], [-10, 23, 76], [-10, 23, 60], [30, 12, 62], [x_h, 0, 64],
            [x_h, 0, 112], [x_h, cy, 150], [x_h, cy, zt + 70], [x_h, cy + 14, zt + 84]];
    usb = [[-76, 62, 88], [-76, 62, 98], [-30, 62, 98.5], [18, 60, 98], [22, 34, 88], [10, 28, 84], [-22, 26, 80], [-22, 26, 54], [20, 16, 54], [x_u, -4, 56],
           [x_u, -4, 112], [x_u, y_u, 150], [x_u, y_u, zt + 70], [x_u, y_u + 12, zt + 84]];
    pwr = [[58, 22, 39.5], [x_p, 8, 60], [x_p, 4, 66], [x_p, 4, 112], [x_p, y_p, 150], [x_p, y_p, zt + 70], [x_p, y_p + 12, zt + 84]];
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
