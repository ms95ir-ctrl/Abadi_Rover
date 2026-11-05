// =====================================================================
// GHOST MODELS of the bought parts (not printed). Simple shapes with the right size,
// used by assembly.scad for pictures and for fit checks.  Run this file alone to see them in a row.
// =====================================================================
_robot2_lib = true;   // tells robot2_params.scad that it is used as a library (no demo shape)
include <robot2_params.scad>

module gbox(s, c="gray", a=1, o=[0,0,0]) {          // box, corner at o
    color(c, a) translate(o) cube(s);
}
module gcyl(d, h, c="gray", a=1) { color(c, a) cylinder(d=d, h=h, $fn=40); }

// ---- 100 x 100 motherboard with its tall parts, board frame (bx,by), z = 0 at underside of PCB
// split into sub-modules so that pictures can colour them separately; ghost_motherboard() draws all of them
module mb_pcb()  { color("seagreen") cube([100, 100, mb_pcb_t]); }
module mb_esp()  {      // ESP32-S3 devkit on two 22-pin sockets: carrier 57 x 28, USB-C toward +bx
    z0 = mb_pcb_t;
    color("black") translate([35.25, 65.3, z0]) cube([57, 28, 8.5 + 1.6]);
    color("dimgray") translate([42, 67, z0 + 10.1]) cube([30, 24, 4]);
    color("silver") translate([89.5, 68.5, z0 + 10.1]) cube([4.5, 9, 3.3]);
    color("silver") translate([89.5, 80.7, z0 + 10.1]) cube([4.5, 9, 3.3]);
}
module mb_drv()  {      // 2 x DRV8833 HW-627 on sockets (outline 21 x 19), tall 17
    z0 = mb_pcb_t;
    for (x0 = [34, 60]) {
        color("crimson") translate([x0, 29.5, z0 + 8.5]) cube([21, 19, 1.6]);
        color("black") translate([x0 + 4, 29.5, z0]) cube([13, 19, 8.5]);
        color("white") translate([x0 + 3, 29.5, z0 + 10.1]) cube([14, 5, 6]);
    }
}
module mb_pca()  {      // PCA9685 board 63 x 25.4 on 1x6 header, servo plugs facing the bottom edge
    z0 = mb_pcb_t;
    color("royalblue") translate([11, 2, z0 + 8.5]) cube([63, 25.4, 1.6]);
    color("black") translate([12, 8, z0]) cube([2.5, 15.2, 8.5]);
    color("lightgray") translate([12, 2, z0 + 10.1]) cube([61, 5, 9]);
    color("lightgreen") translate([58, 20, z0 + 10.1]) cube([14, 7, 9.5]);
}
module mb_gyro() {
    z0 = mb_pcb_t;
    color("royalblue") translate([11, 48, z0 + 8.5]) cube([21.2, 16.4, 1.6]);
    color("black") translate([12, 61, z0]) cube([20, 2.5, 8.5]);
}
module mb_terms() {     // 4 screw terminals on the left edge + POWER OUT header
    z0 = mb_pcb_t;
    for (k = [0, 1, 5, 6]) color("limegreen") translate([2.5, 10 + k * 10.16, z0]) cube([8.5, 10.16, 10]);
    color("black") translate([5, 33.5, z0]) cube([10.2, 5.1, 8.5]);
}
module mb_caps() {
    z0 = mb_pcb_t;
    color("navy") translate([79.5, 15, z0]) cylinder(d = 8, h = 12.5, $fn = 24);
    color("navy") translate([79.5, 6, z0]) cylinder(d = 6.3, h = 11, $fn = 24);
}
module mb_hdrs() {      // motor JSTs at the right edge, sonar/relay and screen-strip headers
    z0 = mb_pcb_t;
    for (k = [0:3]) color("white") translate([92, 14 + k * 10.16, z0]) cube([5, 5, 6]);
    color("black") translate([35, 55, z0]) cube([60, 3, 8.5]);
    color("black") translate([37, 94, z0]) cube([60, 2.5, 8.5]);
}
module ghost_motherboard() { mb_pcb(); mb_esp(); mb_drv(); mb_pca(); mb_gyro(); mb_terms(); mb_caps(); mb_hdrs(); }

module sbc_pcb()    { color("forestgreen") cube([sbc_l, sbc_w, 1.6]); }
module sbc_ports()  {
    color("silver") translate([sbc_l - 21, 3, 1.6]) cube([21, 13.5, sbc_tall]);
    color("silver") translate([sbc_l - 21, 21, 1.6]) cube([21, 13.5, sbc_tall]);
    color("silver") translate([sbc_l - 21, 38, 1.6]) cube([21, 16, 13.5]);
    color("gold") translate([10, -1.5, 1.6]) cube([8, 6, 3.2]);
    color("gold") translate([22, -1.5, 1.6]) cube([7, 6, 3.5]);
    color("gold") translate([35.5, -1.5, 1.6]) cube([7, 6, 3.5]);
}
module sbc_cooler() { color("lightgray") translate([22, 12, 1.6]) cube([40, 40, 13.7]); }
module ghost_sbc() { sbc_pcb(); sbc_ports(); sbc_cooler(); }   // Raspberry-Pi sized: local frame u (long), v (short); z = 0 PCB underside

module ghost_servo() {          // origin = shaft axis on the output face; shaft points +z; length along x
    color("orange") translate([-srv_shaft_off, -srv_w/2, -srv_case_h]) cube([srv_l, srv_w, srv_case_h]);
    color("orange") translate([-srv_shaft_off - (srv_ear_len - srv_l)/2, -srv_w/2, -srv_ear_below_top - 2.5])
        cube([srv_ear_len, srv_w, 2.5]);
    color("silver") cylinder(d = 12, h = srv_spline_above_case);                       // spline boss
}
module ghost_horn() { color("silver") translate([0, 0, srv_spline_above_case - horn_t]) cylinder(d = horn_d, h = horn_t); }

module ghost_screen() {         // local: width x, height z, depth y (front face at y = 0, body behind it)
    color("black") translate([-scr_w/2, -scr_t, -scr_h/2]) cube([scr_w, scr_t, scr_h]);
    color("darkslategray") translate([-scr_w/2 + 6, -scr_t - 6, -scr_h/2 + 6]) cube([scr_w - 12, 6, 22]);   // driver board bump
    color("silver") translate([-12, -scr_t - 12, -scr_h/2 - 0.5]) cube([22, 12, 13]);                       // HDMI plug
}
module ghost_webcam() {         // local: width x, depth y (lens toward +y), height z, centred
    color("dimgray") translate([-cam_w/2, -cam_d/2, 0]) cube([cam_w, cam_d, cam_h]);
    color("black") translate([0, cam_d/2, cam_h/2]) rotate([-90, 0, 0]) cylinder(d = cam_lens_d, h = 2);
}
module ghost_motor() {          // shaft axis = +y direction (outwards for the right-hand side), origin = gearbox face centre
    color("goldenrod") rotate([90, 0, 0]) cylinder(d = motor_d, h = motor_len, $fn = 40);   // body toward -y from the face
    color("silver") rotate([-90, 0, 0]) cylinder(d = motor_shaft_d, h = motor_shaft_len, $fn = 20);
}
module ghost_wheel() {          // axis along y, origin = wheel centre plane
    color("dimgray") rotate([90, 0, 0]) translate([0, 0, -wheel_w/2]) cylinder(d = wheel_d, h = wheel_w, $fn = 60);
    color("silver") rotate([90, 0, 0]) translate([0, 0, -wheel_w/2 - 0.2]) cylinder(d = 22, h = wheel_w + 0.4, $fn = 30);
}
module ghost_ball() { color("silver") sphere(d = caster_ball, $fn = 32); }
module ghost_sonar() {          // local: lens side toward +x (front face of the transducers at x = 0), centred on y; z = centre height
    color("steelblue") translate([-13.6, -sonar_l/2, -sonar_w/2]) cube([1.6, sonar_l, sonar_w]);
    for (s = [-1, 1]) color("silver") translate([-12, s * sonar_pitch/2, 0]) rotate([0, 90, 0]) cylinder(d = 16, h = 12, $fn = 30);
}
module ghost_cliff() { color("steelblue") translate([-15, -7, 0]) cube([30, 14, 7]); color("black") translate([-2, -3, -3]) cube([4, 6, 3]); }
module ghost_switch() { color("red") rotate([0, 90, 0]) cylinder(d = 15, h = 18, $fn = 30); }

module ghost_row() {
    ghost_motherboard();
    translate([120, 0, 0]) ghost_sbc();
    translate([240, 0, 40]) ghost_servo();
    translate([300, 0, 0]) rotate([90, 0, 0]) ghost_screen();
    translate([300, 100, 0]) ghost_webcam();
    translate([400, 0, 40]) ghost_wheel();
    translate([480, 0, 0]) ghost_motor();
    translate([540, 0, 0]) ghost_sonar();
}
ghost_row();
