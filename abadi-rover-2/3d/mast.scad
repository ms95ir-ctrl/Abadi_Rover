// =====================================================================
// MAST: two segments, each made of a FRONT and a BACK half-shell (clamshell, cables are laid in before closing),
// a collar over the joint, a foot plate with socket (bolted to the deck) and (in pan_tilt_interface.scad) the mast-top plate.
// Local frame of every shell / collar: mast axis = z axis, front = +x. z = 0 is the bottom of the part.
// Default output = the lower segment, both halves, side by side.
// =====================================================================
_robot2_lib = true;   // tells robot2_params.scad that it is used as a library (no demo shape)
include <robot2_params.scad>

show = "lower";   // "lower" | "upper" | "collar" | "foot" | "front_lo" ...
seg_h = (z_mast_top - z_mast_bot) / 2;

module shell_profile() { difference() { rrect2(mast_d, mast_w, mast_r); rrect2(mast_in_d, mast_in_w, mast_r - mast_wall); } }

// side = +1 front half, -1 back half; nut_z = heights of the socket-screw nuts (captive M3 nut on the inside)
module shell_half(side, h, nut_z = []) {
    bx = mast_d / 2 - mast_wall;           // inner face of the front/back wall (19)
    difference() {
        union() {
            intersection() {
                linear_extrude(height = h) shell_profile();
                translate([side > 0 ? 0 : -50, -50, -1]) cube([50, 100, h + 2]);
            }
            if (side > 0) for (sy = [-1, 1]) translate([-1.5, sy * (mast_w / 2 - 1.5) - 0.6, 0]) cube([1.6, 1.2, h]);   // tongue
            for (z = nut_z) translate([side > 0 ? bx - 4 : -bx, -6, z - 7]) cube([4, 12, 14]);                           // nut boss
        }
        if (side < 0) for (sy = [-1, 1]) translate([-1.6, sy * (mast_w / 2 - 1.5) - 0.9, -1]) cube([1.6 + eps, 1.8, h + 2]);   // groove
        for (z = nut_z) {
            translate([side * (bx - 5), 0, z]) rotate([0, 90, 0]) cylinder(d = 3.4, h = 12, $fn = 16);
            if (side > 0) translate([bx - 4, 0, z]) rotate([0, 90, 0]) hexnut_pocket(5.7, 2.6);
            else translate([-(bx - 4), 0, z]) rotate([0, -90, 0]) hexnut_pocket(5.7, 2.6);
        }
    }
}
module lower_pair() {   // lower segment: nut at the bottom (foot socket)
    shell_half(+1, seg_h, [foot_sock_h / 2]);
    translate([0, mast_w + 12, 0]) shell_half(-1, seg_h, [foot_sock_h / 2]);
}
module upper_pair() {   // upper segment: nut at the top (neck socket)
    shell_half(+1, seg_h, [seg_h - neck_sock_h / 2]);
    translate([0, mast_w + 12, 0]) shell_half(-1, seg_h, [seg_h - neck_sock_h / 2]);
}

// collar: two halves, bolted together with 4 x M3 x 20 (+ nuts) through the lugs on both sides
module collar_half(side) {
    t = 3.2;  lug_y = mast_w / 2 + t;
    difference() {
        union() {
            intersection() {
                linear_extrude(height = collar_h) difference() { rrect2(mast_d + 2 * t, mast_w + 2 * t, mast_r + t); rrect2(mast_d + 0.4, mast_w + 0.4, mast_r + 0.2); }
                translate([side > 0 ? 0 : -60, -60, -1]) cube([60, 120, collar_h + 2]);
            }
            for (sy = [-1, 1]) translate([side > 0 ? 0 : -9, sy > 0 ? lug_y - 1 : -lug_y - 8.5 + 1, 0]) cube([9, 8.5, collar_h]);
        }
        for (sy = [-1, 1], z = [10, collar_h - 10]) {
            translate([-12, sy * (lug_y + 3.6), z]) rotate([0, 90, 0]) cylinder(d = 3.4, h = 24, $fn = 16);
            if (side > 0) translate([5, sy * (lug_y + 3.6), z]) rotate([0, 90, 0]) cylinder(d = 6.4, h = 5, $fn = 24);          // screw head
            else translate([-9 - eps, sy * (lug_y + 3.6), z]) rotate([0, 90, 0]) hexnut_pocket(5.7, 2.8);                            // nut
        }
    }
}
module collar_pair() { collar_half(+1); translate([0, mast_w + 40, 0]) collar_half(-1); }

// foot plate with socket (print 1): bolts to the deck with 4 x M4
module foot_plate() {
    difference() {
        union() {
            linear_extrude(height = foot_t) rrect2(foot_d, foot_w, 8);
            linear_extrude(height = foot_t + foot_sock_h) difference() { rrect2(mast_d + 5.6, mast_w + 5.6, mast_r + 2.8); rrect2(mast_d + 0.4, mast_w + 0.4, mast_r + 0.2); }
        }
        translate([0, 0, -1]) linear_extrude(height = foot_t + 2) rrect2(mast_in_d - 2, mast_in_w - 2, 5);       // cable opening
        for (sx = [-1, 1], sy = [-1, 1]) translate([sx * foot_bolt_dx / 2, sy * foot_bolt_dy / 2, -1]) cylinder(d = 4.5, h = foot_t + 2, $fn = 24);
        for (s = [-1, 1]) translate([s * (mast_d / 2 + 4), 0, foot_t + foot_sock_h / 2]) rotate([0, 90, 0]) cylinder(d = 3.4, h = 10, center = true, $fn = 16);
    }
}

if (show == "lower") lower_pair();
else if (show == "upper") upper_pair();
else if (show == "collar") collar_pair();
else if (show == "foot") foot_plate();
