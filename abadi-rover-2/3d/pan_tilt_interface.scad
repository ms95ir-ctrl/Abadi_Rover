// =====================================================================
// ###  PAN / TILT INTERFACE  -  THE PART THE OWNER CAN REPLACE WITH HIS OWN DESIGN  ###
//
// Two interfaces, both with their numbers in robot2_params.scad (section PAN / TILT):
//   INTERFACE 1  "mast top":  the round MAST-TOP PLATE (neck_plate) below. It carries 4 x M4 holes on a
//                 if1_bolt_dx x if1_bolt_dy pattern, a cable opening (a kidney shape: the swept envelope of the cable bundle for
//                 +-pan_cable_deg, see CABLE PATH in robot2_params.scad), and the stadium socket that the mast shells slide into.
//                 His pan/tilt base bolts to these 4 holes.
//   INTERFACE 2  "head back": a pad on the head lid with 4 x M3 inserts on an if2_bolt_dx x if2_bolt_dy pattern.
//                 His tilt output (platform / bracket) bolts to these 4 inserts.
// My DEFAULT pan/tilt (two MG996R servos): neck_plate + turntable + 2 yoke halves + the head's own servo pocket.
// If you use his design: print neck_plate only, skip turntable and yoke_half, and tell me the numbers listed in
// docs/mechanical-design.md, section "What I need from you for the pan/tilt".
// Default output of this file = the mast-top plate.
// =====================================================================
_robot2_lib = true;   // tells robot2_params.scad that it is used as a library (no demo shape)
include <robot2_params.scad>

show = "plate";    // "plate" | "turntable" | "yoke_servo" | "yoke_plain" | "stack"

// ------------------------------------------------------------------ INTERFACE 1: mast-top plate  (print 1)
// Cable opening (finding 20 / R21). The bundle (bundle_w x bundle_t, centre y = bundle_cy) is held by the turntable slot and turns with the head. The plate is fixed, so its opening must hold the
// bundle at every pan angle from -pan_cable_deg to +pan_cable_deg: it is the union of the bundle rectangle (plus cable_clr all round) turned in steps of cable_sweep_step degrees.
// It is clipped to the inside of the mast socket below (44.4 x 56.4 mm), so it never cuts into the socket wall. At +-30 degrees a straight, stiff bundle still pokes about 1 mm into the socket wall at one corner
// and about 4 mm into the shell wall under the plate (the shells are 3 mm thick, their cavity is 38 x 50 mm): a soft bundle squeezes in there.
module plate_cable_opening2d() {
    intersection() {
        union() for (a = [-pan_cable_deg : cable_sweep_step : pan_cable_deg])
            rotate(a) translate([0, bundle_cy]) square([bundle_w + 2 * cable_clr, bundle_t + 2 * cable_clr], center = true);
        rrect2(mast_d + 0.4, mast_w + 0.4, mast_r + 0.2);
    }
}
// local z = 0 is the underside of the plate; the socket reaches down to z = -neck_sock_h
module neck_plate() {
    difference() {
        union() {
            cylinder(r = 50, h = neck_plate_t);                                          // plate, 100 mm round
            translate([0, 0, -neck_sock_h]) linear_extrude(height = neck_sock_h + eps)       // socket for the mast shells
                difference() { rrect2(mast_d + 5.6, mast_w + 5.6, mast_r + 2.8); rrect2(mast_d + 0.4, mast_w + 0.4, mast_r + 0.2); }
        }
        // cable opening: swept envelope of the bundle for pan -pan_cable_deg ... +pan_cable_deg (inside the mast cavity, beside the pan servo). Was a fixed 38 x 12.5 slot.
        translate([0, 0, -1]) linear_extrude(height = neck_plate_t + 2) plate_cable_opening2d();
        // pan horn (aluminium 25T disc, M3 threads in the horn): 4 x M3 x 14 from BELOW through plain holes, and a centre hole for the horn screw
        for (a = [45, 135, 225, 315]) translate([horn_pcd / 2 * cos(a), horn_pcd / 2 * sin(a), -1]) cylinder(d = horn_hole, h = neck_plate_t + 2, $fn = 16);
        translate([0, 0, -1]) cylinder(d = 8, h = neck_plate_t + 2, $fn = 30);
        // INTERFACE 1 bolt pattern: 4 x M4 through holes (his pan/tilt base bolts here)
        for (sx = [-1, 1], sy = [-1, 1]) translate([sx * if1_bolt_dx / 2, sy * if1_bolt_dy / 2, -1]) cylinder(d = if1_bolt_d, h = neck_plate_t + 2, $fn = 24);
        // socket screws (2): along x through the socket walls, M3 x 12
        for (s = [-1, 1]) translate([s * (mast_d / 2 + 4), 0, -neck_sock_h / 2]) rotate([0, 90, 0]) cylinder(d = 3.4, h = 10, center = true, $fn = 16);
    }
}

// ------------------------------------------------------------------ turntable  (print 1)
// local z = 0 is the underside of the plate that rests on the glide ring; skirt hangs below.
// Servo (inverted, long axis along x, overhang to the back) sits in the cut-out with its ears on top of the plate.
module turntable() {
    ear_cx = -(srv_l - srv_shaft_off - srv_shaft_off) / 2;                           // centre of the servo case along x (negative = back)
    difference() {
        union() {
            cylinder(r = skirt_r + skirt_t, h = tt_t);
            translate([0, 0, -skirt_h]) ring(skirt_r + skirt_t, skirt_r, skirt_h + eps);
            for (x = [srv_ear_hole_dx / 2 + ear_cx, -srv_ear_hole_dx / 2 + ear_cx], y = [-srv_ear_hole_dy / 2, srv_ear_hole_dy / 2])
                translate([x, y, -3]) cylinder(d = 11, h = 3 + eps, $fn = 30);          // pads under the ear screws (insert depth); the case cut-out below trims their inner side flat
        }
        // servo case cut-out. It starts BELOW the pads (z -4), so it also trims the inner edge of the 4 ear pads: before, the pads (d 11) reached 1.1 mm into the servo case.
        translate([-(srv_l - srv_shaft_off) - 0.2, -srv_w / 2 - 0.3, -4]) cube([srv_l + 0.4, srv_w + 0.6, tt_t + 5]);
        for (x = [srv_ear_hole_dx / 2 + ear_cx, -srv_ear_hole_dx / 2 + ear_cx], y = [-srv_ear_hole_dy / 2, srv_ear_hole_dy / 2])
            translate([x, y, tt_t - 6]) cylinder(d = 5.6, h = 10, $fn = 24);          // M4 insert holes from the top
        translate([tt_slot_x0, tt_slot_y0, -1]) cube([tt_slot_x1 - tt_slot_x0, tt_slot_y1 - tt_slot_y0, tt_t + 2]);   // cable slot 38 x 14 (turns with the head; the bundle sits at y = bundle_cy in it; the plate opening below follows the bundle, see neck_plate)
        for (sy = [-1, 1], sx = [-12, 12], y = [30, 37]) translate([sx, sy * y, -1]) cylinder(d = 3.4, h = tt_t + 2, $fn = 16);   // yoke screws from below
    }
}

// ------------------------------------------------------------------ yoke half  (print 2: one with servo=true on the +y side, one plain on -y)
// local z = 0 is the top of the turntable. +y half. head_w/2 + yoke_gap = inner face of the arm.
module yoke_half(servo = true) {
    y_in = head_w / 2 + yoke_gap;
    y_out = y_in + yoke_arm_t;
    ax = neck_axis_above_tt;
    difference() {
        union() {
            translate([-yoke_arm_w / 2, 26, 0]) cube([yoke_arm_w, y_out - 26, yoke_bar_t]);              // bar on the turntable
            translate([0, y_out, 0]) rotate([90, 0, 0]) linear_extrude(height = yoke_arm_t)             // arm
                hull() { translate([0, ax]) circle(r = yoke_arm_w / 2, $fn = 60); translate([-yoke_arm_w / 2, 0]) square([yoke_arm_w, 1]); }
            // gusset
            hull() { translate([-yoke_arm_w / 2, y_in - 22, 0]) cube([yoke_arm_w, 22, yoke_bar_t]);
                     translate([-yoke_arm_w / 2, y_in - 0.1, 0]) cube([yoke_arm_w, 0.1, 40]); }
        }
        // 4 inserts from below for the turntable screws (M3)
        for (sx = [-12, 12], y = [30, 37]) translate([sx, y, -1]) insert_hole(4.0, 7);
        // pivot / horn centre hole
        translate([0, y_in - 1, ax]) rotate([-90, 0, 0]) cylinder(d = servo ? 8 : 5.4, h = yoke_arm_t + 2, $fn = 30);
        if (servo) for (a = [45, 135, 225, 315])                                                       // horn: 4 x M3 on the 14 mm circle, from the outside
            translate([horn_pcd / 2 * cos(a), y_in - 1, ax + horn_pcd / 2 * sin(a)]) rotate([-90, 0, 0]) cylinder(d = horn_hole, h = yoke_arm_t + 2, $fn = 16);
    }
}
module yoke_half_minus() { mirror([0, 1, 0]) yoke_half(false); }

// ------------------------------------------------------------------ default output
module stack_view() {
    neck_plate();
    translate([0, 0, neck_plate_t + tt_top_above_plate - tt_t]) turntable();
    translate([0, 0, neck_plate_t + tt_top_above_plate]) { yoke_half(true); yoke_half_minus(); }
}
if (show == "plate") neck_plate();
else if (show == "turntable") turntable();
else if (show == "yoke_servo") yoke_half(true);
else if (show == "yoke_plain") yoke_half(false);
else stack_view();
