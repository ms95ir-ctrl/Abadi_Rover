// =====================================================================
// BASE: lower tray (floor + rim + wheel wells), upper deck, cover, caster, motor caps, skids, bumper.
// The three big discs (tray, deck, cover) are printed in 4 pieces each (FL, FR, RL, RR) that lock with
// dovetails and are glued. Change  show  below to look at one thing. Default output = the whole tray.
// =====================================================================
_robot2_lib = true;   // tells robot2_params.scad that it is used as a library (no demo shape)
include <robot2_params.scad>

show = "tray";   // "tray" | "deck" | "cover" | "caster" | "bumper" | "tray_FL" ...

// ------------------------------------------------------------------ dovetail pieces
module dovetail2d(c = 0) polygon([[-1, -5 - c], [8 + c, -7 - c], [8 + c, 7 + c], [-1, 5 + c]]);
xs_y0 = [-95, -15, 25];       // dovetail positions along the left/right seam (x)
ys_x  = [25, 62];            // dovetail positions along the front/rear seam (|y|)
module piece2d(q) {
    big = 400;
    isF = (q == "FL" || q == "FR");  isL = (q == "FL" || q == "RL");
    x0 = isF ? cut_x : -big;  x1 = isF ? big : cut_x;
    y0 = isL ? cut_y : -big;  y1 = isL ? big : cut_y;
    difference() {
        union() {
            translate([x0, y0]) square([x1 - x0, y1 - y0]);
            if (isL) for (xi = xs_y0) if (xi > x0 && xi < x1) translate([xi, cut_y]) rotate(-90) dovetail2d(0);
            if (isF) for (yi = ys_x) translate([cut_x, (isL ? 1 : -1) * yi]) rotate(180) dovetail2d(0);
        }
        if (!isL) for (xi = xs_y0) if (xi > x0 && xi < x1) translate([xi, cut_y]) rotate(-90) dovetail2d(tab_clear);
        if (!isF) for (yi = ys_x) translate([cut_x, (isL ? 1 : -1) * yi]) rotate(180) dovetail2d(tab_clear);
    }
}
module piece3d(q) { intersection() { children(); translate([0, 0, -20]) linear_extrude(height = 400) piece2d(q); } }

// ------------------------------------------------------------------ TRAY
module motor_saddles() {
    for (s = [-1, 1]) for (yc = [58, 90]) {
        translate([axle_x - 20, s * yc - 6, z_floor_t - eps]) difference() {
            cube([40, 12, wheel_r - z_floor_t + eps]);
            translate([20, -1, wheel_r - z_floor_t + eps]) rotate([-90, 0, 0]) cylinder(d = motor_d + 0.3, h = 14);
            for (sx = [-16.5, 16.5]) translate([20 + sx, 6, wheel_r - z_floor_t - 7 + eps]) insert_hole(4.0, 7.5);
        }
    }
}
module wheel_wells() {
    for (s = [-1, 1]) difference() {
        translate([axle_x - 35.5, s > 0 ? well_wall_y : -(well_wall_y + well_wall_t), z_floor_t - eps])
            cube([71, well_wall_t, z_deck_b - z_floor_t + eps]);
        translate([axle_x, s * (well_wall_y + 0.8), wheel_r]) rotate([90, 0, 0]) cylinder(d = 12, h = 6, center = true);
    }
}
module sonar_cheeks() {
    for (s = [-1, 1]) rotate(s * sonar_ang) for (t = [-1, 1])
        translate([114, t * (sonar_l / 2 + 1.5) - 1.5, z_floor_t - eps]) cube([13, 3, 50]);
}
module cliff_bosses() {
    for (s = [-1, 1]) rotate(s * cliff_ang) translate([cliff_r, 0, z_floor_t - eps])
        for (t = [-11, 11]) translate([0, t, 0]) difference() { cylinder(d = 7, h = 3.5, $fn = 24); translate([0, 0, 0.6]) cylinder(d = 2.7, h = 4, $fn = 16); }
}
module battery_cradle() {
    translate([batt_x, batt_y, z_floor_t - eps]) difference() {
        translate([-(batt_l + 4) / 2, -(batt_w + 4) / 2, 0]) cube([batt_l + 4, batt_w + 4, 7]);
        translate([-(batt_l + 0.6) / 2, -(batt_w + 0.6) / 2, -1]) cube([batt_l + 0.6, batt_w + 0.6, 10]);
        for (sx = [-1, 1]) translate([sx * (batt_l / 2 - 8) - 4, -batt_w, -1]) cube([8, 2 * batt_w, 4]);   // wire notches
    }
}
module skid_bosses() {
    for (p = skid_pos) translate([p[0], p[1], z_floor_t - eps]) difference() {
        cylinder(d = 10, h = 3.4, $fn = 30);
        translate([0, 0, 0.8]) hexnut_pocket(5.7, 3);
    }
}
module tray_full() {
    difference() {
        union() {
            translate([0, 0, z_floor_b]) cylinder(r = base_r, h = floor_t);
            translate([0, 0, z_floor_b]) ring(base_r, base_r - rim_t, z_deck_b - z_floor_b);
            for (p = col_pos) translate([p[0], p[1], z_floor_t - eps]) difference() {
                cylinder(d = col_d, h = z_deck_b - z_floor_t + eps, $fn = 30);
                translate([0, 0, z_deck_b - z_floor_t - 6.5]) insert_hole(4.0, 7);
            }
            motor_saddles();  wheel_wells();  sonar_cheeks();  cliff_bosses();  battery_cradle();  skid_bosses();
        }
        // wheel windows (floor + rim): the wheel (65 x 26) sits here, outer face flush with the rim
        for (s = [-1, 1]) translate([axle_x - wheel_r - 2, s > 0 ? well_wall_y + well_wall_t + 0.6 : -(base_r + 2), z_floor_b - 1])
            cube([wheel_d + 4, base_r + 2 - well_wall_y - well_wall_t - 0.6, z_deck_b - z_floor_b + 1.5]);
        // caster hole + flange bolts + skid holes
        translate([caster_x, 0, z_floor_b - 1]) cylinder(d = caster_cup_d + 0.5, h = 6);
        for (a = [90, 210, 330]) translate([caster_x + (caster_flange_d / 2 - 3.5) * cos(a), (caster_flange_d / 2 - 3.5) * sin(a), z_floor_b - 1]) cylinder(d = 3.4, h = 6, $fn = 16);
        for (p = skid_pos) translate([p[0], p[1], z_floor_b - 1]) cylinder(d = 3.4, h = 8, $fn = 16);
        // sonar windows: two 16.6 mm holes per sensor, through the rim, radial
        for (s = [-1, 1]) rotate(s * sonar_ang) for (t = [-1, 1])
            translate([110, t * sonar_pitch / 2, sonar_z]) rotate([0, 90, 0]) cylinder(d = sonar_hole, h = 30, $fn = 40);
        // cliff windows: 12 x 7 through the floor
        for (s = [-1, 1]) rotate(s * cliff_ang) translate([cliff_r - 6, -3.5, z_floor_b - 1]) cube([12, 7, 6]);
        // rear: USB-C window for the charger, main switch hole, vents
        translate([-base_r - 1, -8, 19]) cube([8, 16, 12]);
        translate([-sqrt(base_r * base_r - sw_pos_y * sw_pos_y) - 3, sw_pos_y, 40]) rotate([0, 90, 0]) cylinder(d = sw_d, h = 10, $fn = 40);
        for (a = [150, 158, 202, 210]) rotate(a) translate([base_r - 4, -1.5, 38]) cube([8, 3, 22]);
        // bumper arm slots (front rim): two 14 x 8 slots
        for (s = [-1, 1]) rotate(s * 38) translate([base_r - 4, -7, 22]) cube([8, 14, 10]);
        // zip-tie slots around the components (3 x 1.6 mm pairs)
        for (p = [[batt_x - 28, 28], [batt_x + 28, 28], [batt_x - 28, -28], [batt_x + 28, -28],
                  [62, -72], [62, 72], [62, -3], [62, 3], [-61, -58], [-61, 34], [-96, -44], [-96, 44],
                  [-96, -18], [-96, 18], [-102, 22], [-102, -22], [-96, -70], [-96, 70]])
            for (d = [-5, 5]) translate([p[0] - 1.5, p[1] + d - 0.8, z_floor_b - 1]) cube([3, 1.6, 6]);
    }
}

// ------------------------------------------------------------------ DECK
module standoff(d, h, hole_d, hole_h) { difference() { cylinder(d = d, h = h + eps, $fn = 30); translate([0, 0, h - hole_h + 0.5]) cylinder(d = hole_d, h = hole_h, $fn = 20); } }
module deck_full() {
    mast_pts = [for (sx = [-1, 1], sy = [-1, 1]) [mast_x + sx * foot_bolt_dx / 2, sy * foot_bolt_dy / 2]];
    difference() {
        union() {
            translate([0, 0, z_deck_b]) cylinder(r = base_r, h = deck_t);
            for (hx = [mb_hole, mb_size - mb_hole], hy = [mb_hole, mb_size - mb_hole]) {
                p = mb_xy(hx, hy);  translate([p[0], p[1], z_deck_t - eps]) standoff(8, mb_stand, 4.0, 6.5);
            }
            for (u = [sbc_hole_off, sbc_hole_off + sbc_hole_dx], v = [sbc_hole_off, sbc_hole_off + sbc_hole_dy]) {
                p = sbc_xy(u, v);  translate([p[0], p[1], z_deck_t - eps]) standoff(6.2, sbc_stand, sbc_hole_d, 6);
            }
            for (p = cpost_pos) translate([p[0], p[1], z_deck_t - eps]) standoff(post_d, z_cover_top - cover_top_t - z_deck_t, 4.0, 7);
            // 4 pads on the top for the mast foot (M4 heat-set inserts), foot plate rests on them
            for (p = mast_pts) translate([p[0], p[1], z_deck_t - eps]) cylinder(d = 14, h = foot_pad_h + eps, $fn = 30);
        }
        for (p = col_pos) translate([p[0], p[1], z_deck_b - 1]) { cylinder(d = 3.4, h = deck_t + 2, $fn = 16); translate([0, 0, deck_t - 1.6 + 1]) cylinder(d1 = 3.4, d2 = 6.6, h = 1.7, $fn = 20); }
        for (p = mast_pts) translate([p[0], p[1], z_deck_t + foot_pad_h - 7]) cylinder(d = 5.6, h = 8, $fn = 24);   // M4 insert holes (depth 7)
        translate([mast_x, 0, z_deck_b - 8]) linear_extrude(height = deck_t + 10) rrect2(42, 26, 6);        // mast cable hole
        translate([-36, 18, z_deck_b - 1]) cube([36, 10, deck_t + 2]);                                      // motor wires up (M1, M2 JST)
        translate([-65, -101, z_deck_b - 1]) cube([45, 9, deck_t + 2]);                                     // battery / buck wires up (screw terminals)
        translate([-58, -40, z_deck_b - 1]) cube([8, 32, deck_t + 2]);                                      // sensor wires up (under the board's header strip)
        translate([-20, -20, z_deck_b - 1]) cube([14, 8, deck_t + 2]);                                      // spare servo/USB pass
    }
}

// ------------------------------------------------------------------ COVER
module cover_solid(r, h, ch) { union() { cylinder(r = r, h = h - ch); translate([0, 0, h - ch]) cylinder(r1 = r, r2 = r - ch, h = ch); } }
module cover_full() {
    H = z_cover_top - z_deck_t;
    difference() {
        translate([0, 0, z_deck_t]) cover_solid(base_r, H, 8);
        translate([0, 0, z_deck_t - eps]) cover_solid(base_r - cover_wall, H - cover_top_t, 8);
        translate([mast_x, 0, z_deck_t]) linear_extrude(height = H + 1) rrect2(mast_d + 4, mast_w + 4, mast_r + 2);
        for (p = cpost_pos) translate([p[0], p[1], z_cover_top - cover_top_t - 1]) {
            cylinder(d = 3.4, h = cover_top_t + 2, $fn = 16);
            translate([0, 0, cover_top_t - 1.2 + 1]) cylinder(d1 = 3.4, d2 = 6.6, h = 1.3, $fn = 20);
        }
        // vent slots in the top (rear half) and a few in the skirt at the rear
        for (a = [-36, -18, 0, 18, 36]) rotate(180 + a) translate([92, -1.5, z_cover_top - cover_top_t - 1]) cube([30, 3, cover_top_t + 2]);
    }
}

// ------------------------------------------------------------------ small printed parts
module caster_cup() {            // ball socket; flange sits on the floor (print flange-down, see print_parts.scad)
    difference() {
        union() {
            translate([0, 0, 4.8]) cylinder(d = caster_cup_d, h = 15 - 4.8, $fn = 48);       // body, passes through the floor hole
            translate([0, 0, z_floor_t]) cylinder(d = caster_flange_d, h = 3.4, $fn = 48);    // flange on the floor top
        }
        translate([0, 0, caster_ball / 2]) sphere(d = caster_ball + 0.8, $fn = 48);
        translate([0, 0, 14]) cylinder(d = 3, h = 12, $fn = 16);                              // vent
        for (a = [90, 210, 330]) translate([(caster_flange_d / 2 - 3.5) * cos(a), (caster_flange_d / 2 - 3.5) * sin(a), z_floor_t - 1]) cylinder(d = 3.4, h = 6, $fn = 16);
        for (a = [30, 150, 270]) translate([11.2 * cos(a), 11.2 * sin(a), 3]) cylinder(d = 4.0, h = 8, $fn = 16);   // inserts for the ring
    }
}
module caster_ring() {
    difference() {
        translate([0, 0, 3]) cylinder(d = caster_cup_d, h = 1.8, $fn = 48);
        translate([0, 0, 2]) cylinder(d = 14, h = 4, $fn = 40);
        for (a = [30, 150, 270]) translate([11.2 * cos(a), 11.2 * sin(a), 2]) cylinder(d = 3.4, h = 4, $fn = 16);
    }
}
module motor_cap() {             // strap over the motor (print 4)
    difference() {
        cube([40, 12, 16]);
        translate([20, -1, 0]) rotate([-90, 0, 0]) cylinder(d = motor_d + 0.3, h = 14);
        for (sx = [-16.5, 16.5]) translate([20 + sx, 6, -1]) { cylinder(d = 3.4, h = 18, $fn = 16); translate([0, 0, 13]) cylinder(d = 6.4, h = 4, $fn = 20); }
    }
}
module skid() {                  // anti-tip foot (print 2): M3 x 16 screw through it
    difference() { cylinder(d = 14, h = z_floor_b - skid_gap, $fn = 36);
                   translate([0, 0, -1]) cylinder(d = 3.4, h = 12, $fn = 16);
                   translate([0, 0, -1]) cylinder(d = 6.2, h = 2.2, $fn = 20); }
}
module bumper_seg(k) {           // front arc bumper in 3 segments of 50 degrees (k = 0 right, 1 centre, 2 left); low, below the sonars
    a0 = -75 + 50 * k;
    rotate(a0) rotate_extrude(angle = 50, $fn = 100) translate([base_r + 1, 18]) square([4, 16]);
    if (k != 1) rotate(k == 0 ? -38 : 38) translate([base_r - 14, -6, 24]) cube([16, 12, 6]);   // arm through the rim slot
}
module bumper() { for (k = [0 : 2]) bumper_seg(k); }

// ------------------------------------------------------------------ selection
if (show == "tray") tray_full();
else if (show == "deck") deck_full();
else if (show == "cover") cover_full();
else if (show == "caster") { caster_cup(); caster_ring(); }
else if (show == "bumper") bumper();
else if (show == "tray_FL") piece3d("FL") tray_full();
