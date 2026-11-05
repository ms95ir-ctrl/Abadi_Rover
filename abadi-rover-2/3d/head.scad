// =====================================================================
// HEAD: shell (front bezel, walls, camera brow with LED hole and slide-cover slot, servo cut-out) + back lid (air grille, interface pad) + pivot bush + camera slide cover.
// Frame: head centre = origin, front (screen side) = +x, width along y, height along z. Tilt axis at (x = head_axis_y, z = head_axis_z).
// Default output = the shell.
// =====================================================================
_robot2_lib = true;   // tells robot2_params.scad that it is used as a library (no demo shape)
include <robot2_params.scad>

show = "shell";   // "shell" | "lid" | "bush" | "cam_cover"

// OWN PAN/TILT (see docs/mechanical-design.md, section 7.4).
//   use_default_tilt = true : my default. The head has the window for the tilt servo (MG996R) in its +y wall, 4 ear bosses with nut pockets, and the
//                              M5 pivot hole with its boss in the -y wall. Needs yoke + pivot_bush from pan_tilt_interface.scad / this file.
//   use_default_tilt = false: you bring your own pan/tilt. The shell is CLOSED: no servo window, no ear bosses, no pivot hole, no nut pockets. The head is carried by
//                              the INTERFACE 2 pad on the lid (4 x M3 inserts, if2_bolt_dx x if2_bolt_dy). Then also enter the height of YOUR tilt axis above the floor in head_axis_h
//                              (robot2_params.scad); head_axis_y / head_axis_z only matter for the default tilt. Print neck_plate, mast, head and base only (no turntable, yoke, pivot_bush).
// To change it, edit the word true / false on the next line and export again. (From the command line the same works with  -D use_default_tilt=false  ; tested with print_parts.scad.)
use_default_tilt = true;
function head_has_default_tilt() = use_default_tilt;   // assembly.scad reads the switch through this function

x_f = head_d / 2;                 // front face 22
x_rim = -head_d / 2 + lid_t;      // rear edge of the shell (lid sits behind it) -19.6
inner_w = head_w - 2 * head_wall;
inner_h = head_h - 2 * head_wall;
brow_zb = head_h / 2;             // brow starts at the top of the head
brow_zt = head_h / 2 + brow_h;
lens_z  = brow_zb + 1 + cam_h / 2 + cam_lens_dz;
ax = head_axis_y;  az = head_axis_z;

module body2d() { rrect2(head_w, head_h, head_r); }
module brow2d() { translate([0, (brow_zb - 3 + brow_zt) / 2]) rrect2(brow_w, brow_zt - brow_zb + 3, 6); }
module brow_in2d() { translate([0, (brow_zb + brow_zt - 3) / 2]) rrect2(brow_w - 2 * brow_front_t, brow_zt - brow_zb - 3, 3); }
module inner2d() { rrect2(inner_w, inner_h, 0.8); }

// ear holes of the tilt servo (servo long axis vertical, overhang downward, shaft along +y)
srv_z_top = az + srv_shaft_off;                     // top of the case
srv_z_bot = az - (srv_l - srv_shaft_off);           // bottom of the case
ear_c = az - ((srv_l - srv_shaft_off) - srv_shaft_off) / 2;      // centre of case along z
ear_holes = [for (dz = [srv_ear_hole_dx / 2, -srv_ear_hole_dx / 2], dx = [-srv_ear_hole_dy / 2, srv_ear_hole_dy / 2]) [ax + dx, ear_c + dz]];

module head_shell() {
    difference() {
        union() {
            ex(x_rim, x_f) { body2d(); brow2d(); }
        }
        // main cavity (open at the back), screen pocket and the window in the front lip
        ex(x_rim - 1, x_f - lip_t) inner2d();
        ex(x_f - lip_t - 1, x_f + 1) translate([0, scr_vis_dz]) rrect2(scr_vis_w, scr_vis_h, 2);
        // brow cavity (the camera), lens hole, cable hole through the top wall
        ex(x_rim - 1, x_f - brow_front_t) brow_in2d();
        translate([x_f - brow_front_t - 1, 0, lens_z]) rotate([0, 90, 0]) cylinder(d = cam_lens_d, h = brow_front_t + 3, $fn = 40);
        translate([-14, -12, brow_zb - head_wall - 1]) cube([14, 24, head_wall + 3]);
        // camera-live LED hole (R23): 5 mm LED beside the webcam body, robot right side (-y), same height as the lens
        translate([x_f - brow_front_t - 1, led_y, lens_z]) rotate([0, 90, 0]) cylinder(d = led_d, h = brow_front_t + 3, $fn = 30);
        // camera slide-cover slot (R23): a flat channel INSIDE the 3 mm brow front wall (0.8 mm of wall stays in front of it and behind it), closed at y = cov_y0, open at the +y side of the brow.
        // The cover (print part cam_cover) is pushed in from the open side and shuts the lens window. Printed front face down: the roof of the slot is a 22 mm bridge.
        translate([x_f - cov_skin - cov_t - cov_play, cov_y0, lens_z - cov_slot_h / 2]) cube([cov_t + cov_play, brow_w / 2 + 1 - cov_y0, cov_slot_h]);
        // bottom: cable slot (30 x 14) towards the mast. The bundle has to turn 90 degrees between the turntable slot (long side along x) and this slot (long side along y): static, in the 36 mm gap. Thread the HDMI cable from this (head) end.
        translate([ax - 12, -26, -head_h / 2 - 1]) cube([14, 30, head_wall + 2]);
        if (use_default_tilt) {
            // +y wall: servo cut-out (body goes through, ears are on the inside)
            translate([ax - srv_w / 2 - 0.3, head_w / 2 - head_wall - 1, srv_z_bot - 0.3]) cube([srv_w + 0.6, head_wall + 2, srv_z_top - srv_z_bot + 0.6]);
            // -y wall: pivot hole M5
            translate([ax, -head_w / 2 - 1, az]) rotate([-90, 0, 0]) cylinder(d = 5.4, h = head_wall + 2, $fn = 30);
        }
    }
    // inner bosses for the servo ears (M4 screws from inside into nuts in pockets on the outside) and the pivot nut (default tilt only)
    if (use_default_tilt) difference() {
        union() {
            for (p = ear_holes) translate([p[0], head_w / 2 - head_wall + eps, p[1]]) rotate([90, 0, 0]) cylinder(d = 10, h = head_boss_t + eps, $fn = 30);
            translate([ax, -head_w / 2 + head_wall - eps, az]) rotate([-90, 0, 0]) cylinder(d = 16, h = head_boss_t + eps, $fn = 40);
        }
        for (p = ear_holes) translate([p[0], head_w / 2 + 1, p[1]]) rotate([90, 0, 0]) cylinder(d = 4.4, h = head_wall + 6, $fn = 20);
        translate([ax, -head_w / 2 + head_wall + head_boss_t + 1, az]) rotate([90, 0, 0]) cylinder(d = 5.4, h = 12, $fn = 20);
    }
    // nut pockets are cut from the wall's outer face: M4 (7 AF, 3.2 deep)
    // (cut in a second pass so the bosses stay solid)
    // corner bosses: lid screws (M3 insert at the rear end) and screen stops at the front end
    for (sy = [-1, 1], sz = [-1, 1]) translate([x_rim - eps, sy * (inner_w / 2 - 4.0), sz * (inner_h / 2 - 4.0)]) difference() {
        rotate([0, 90, 0]) cylinder(d = 9, h = 9.4 - x_rim + eps, $fn = 30);
        translate([-1, 0, 0]) rotate([0, 90, 0]) insert_hole(4.0, 8.5);
    }
}
// shell with the nut pockets cut in (kept as a separate wrapper so pockets do not cut the bosses)
module head_shell_full() {
    difference() {
        head_shell();
        if (use_default_tilt) {
            for (p = ear_holes) translate([p[0], head_w / 2 - 3.2 + 0.01, p[1]]) rotate([-90, 0, 0]) cylinder(d = 7.6 / cos(30), h = 4, $fn = 6);
            translate([ax, -head_w / 2 + head_wall + head_boss_t + 0.01 + 1, az]) rotate([90, 0, 0]) cylinder(d = 8.4 / cos(30), h = 6.2, $fn = 6);
        }
    }
}

// back lid (print 1): flat, outer side on the bed
module head_lid() {
    difference() {
        union() {
            ex(-head_d / 2, x_rim) { body2d(); brow2d(); }
            ex(-head_d / 2 - 4, -head_d / 2 + eps) translate([0, -22]) rrect2(2 * (if2_bolt_dx / 2 + 8), if2_bolt_dy + 16, 5);   // INTERFACE 2 pad
        }
        for (sy = [-1, 1], sz = [-1, 1]) translate([-head_d / 2 - 5, sy * (inner_w / 2 - 4.0), sz * (inner_h / 2 - 4.0)]) rotate([0, 90, 0]) {
            cylinder(d = 3.4, h = lid_t + 7, $fn = 16);
            translate([0, 0, 4.2]) cylinder(d1 = 6.6, d2 = 3.4, h = 1.8, $fn = 20);
        }
        // INTERFACE 2: 4 x M3 inserts from the back
        for (sx = [-1, 1], sz = [-1, 1]) translate([-head_d / 2 - 4 - 1, sx * if2_bolt_dx / 2, -22 + sz * if2_bolt_dy / 2]) rotate([0, 90, 0]) insert_hole(4.0, 7);
        // air grille: 9 holes on a 24 mm circle, centre at y = -52, z = -12. NOT the speaker: this side faces backward, 10 cm from the microphone. The speaker is in the cover (robot2_params.scad, COVER TOP).
        for (a = [0 : 45 : 315]) translate([-head_d / 2 - 1, -52 + 10 * cos(a), -12 + 10 * sin(a)]) rotate([0, 90, 0]) cylinder(d = 3.5, h = lid_t + 2, $fn = 16);
        translate([-head_d / 2 - 1, -52, -12]) rotate([0, 90, 0]) cylinder(d = 3.5, h = lid_t + 2, $fn = 16);
    }
}
// camera slide cover (R23, optional small part, print flat): length along the slot, height 20, thickness cov_t. Or cut it from a thin plastic card.
// Pushed in from the +y side of the brow it shuts the lens window; pulled out by cov_pull = 24 mm (22 mm reaches the edge of the window exactly, so pull 24 or more) it opens it. Local x = along the slot (head y), local y = height (head z), local z = thickness (head x).
module cam_cover() { cube([cov_len, cov_h, cov_t]); }
module pivot_bush() { difference() { cylinder(d = 14, h = yoke_gap - 0.6, $fn = 40); translate([0, 0, -1]) cylinder(d = 5.6, h = yoke_gap + 2, $fn = 24); } }

if (show == "shell") head_shell_full();
else if (show == "lid") head_lid();
else if (show == "bush") pivot_bush();
else if (show == "cam_cover") cam_cover();
