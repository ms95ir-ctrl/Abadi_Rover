// =====================================================================
// ROBOT 2 (telepresence robot) - ALL PARAMETERS IN ONE PLACE
// Units: millimetres. Frame: origin on the floor under the centre of the base,
//   +x = front (the way the screen looks), +y = robot LEFT, +z = up.
// Every other .scad file does   include <robot2_params.scad>
// Values marked (V) were seen in a source, (A) are assumptions. See docs/mechanical-design.md.
// To change the robot: edit numbers HERE, then re-export the parts.
// =====================================================================
$fn = 48;
eps = 0.01;

// ---------------------------------------------------------------- BASE (round puck)
base_r      = 130;     // base radius -> 260 mm diameter
z_floor_b   = 12;      // floor underside above ground (ground clearance)
floor_t     = 3;       // floor thickness
z_floor_t   = z_floor_b + floor_t;   // 15 = top of floor
z_deck_b    = 68;      // deck underside = top of the tray rim (wheel top is 65)
deck_t      = 4;       // deck thickness
z_deck_t    = z_deck_b + deck_t;     // 72
cover_wall  = 2.0;     // cover skirt thickness
cover_top_t = 2.4;     // cover top plate thickness
z_cover_top = 105;     // top of cover
rim_t       = 2.0;     // tray rim wall

// split lines for printing the big discs in 4 pieces (any bed >= 180 mm)
cut_x = -40;           // front/rear split (rear pieces are x < cut_x)
cut_y = 0;             // left/right split
tab_clear = 0.25;      // dovetail clearance (female is bigger by this)

// ---------------------------------------------------------------- WHEELS, MOTORS, CASTER
wheel_d     = 65;      // PARAMETER: drive wheel diameter
wheel_w     = 26;      // wheel width (A)
wheel_r     = wheel_d/2;
axle_x      = 0;       // drive axle position
wheel_y     = 117;     // wheel centre plane (|y|) -> outer face at 130
wheel_gap   = 1.5;
motor_d     = 25;      // gearmotor body diameter (Pololu 25D / 25GA370 class)
motor_len   = 52;      // body incl. gearbox (V Pololu 25Dx52L)
motor_face_y= wheel_y - wheel_w/2 - 2.5 - 0.5; // gearbox face |y| = 101 (wall is behind it)
motor_shaft_d = 4;     // D-shaft (V Pololu 25D)
motor_shaft_len = 12;
well_wall_y = 101.2;   // inner wall of wheel well, |y| start
well_wall_t = 1.6;
caster_x    = 104;     // ball caster centre
caster_ball = 16;      // steel ball diameter (A: common 16 mm bearing ball)
caster_flange_d = 38;
caster_cup_d    = 28;
skid_pos    = [[95, 58], [95, -58], [-85, 85], [-85, -85]];   // 4 anti-tip skids (front-side and rear-side corners)
skid_gap    = 4;       // skid height above floor when level (they touch after about 2 degrees of tilt)

// ---------------------------------------------------------------- MOTHERBOARD (V: 100x100, holes 4/96 mm)
mb_size   = 100;
mb_hole   = 4;         // hole offset from board edge
mb_x0     = 14;        // robot x of the board's BOTTOM edge (servo plugs face front, +x)
mb_y0     = -88;       // robot y of the board's LEFT edge (power terminals face the robot's right)
mb_stand  = 6;         // standoff height above deck
mb_pcb_t  = 1.6;
mb_tall   = 20;        // tallest part above the PCB (A: ESP32 on sockets ~15, PCA9685 ~13, DRV8833 on sockets ~17, 470 uF cap ~13)
// board (bx,by) -> robot (x,y):  x = mb_x0 - by ;  y = mb_y0 + bx   (board turned 90 deg)
function mb_xy(bx,by) = [mb_x0 - by, mb_y0 + bx];

// ---------------------------------------------------------------- SBC (generic Raspberry-Pi sized envelope)
sbc_l = 85;  sbc_w = 56;  sbc_stand = 5;
sbc_hole_dx = 58; sbc_hole_dy = 49; sbc_hole_off = 3.5;   // (V-ish: Pi family 58 x 49, M2.5)
sbc_hole_d  = 2.2;                  // M2.5 self-tapping
sbc_tall    = 17;                   // USB-A stack height above PCB (A)
sbc_x0 = 13;  sbc_y0 = 92;          // robot x,y of the board's lower-left corner (board rotated 180 deg)
// SBC (u,v) -> robot (x,y):  x = sbc_x0 - u ; y = sbc_y0 - v   (USB ports at the rear, HDMI/power edge faces +y)
function sbc_xy(u,v) = [sbc_x0 - u, sbc_y0 - v];

// ---------------------------------------------------------------- MAST
mast_x    = 62;        // mast axis x (robot frame), y = 0
mast_w    = 56;        // outer width  (along y)
mast_d    = 44;        // outer depth  (along x)
mast_r    = 10;        // corner radius
mast_wall = 3;
mast_in_w = mast_w - 2*mast_wall;   // 50
mast_in_d = mast_d - 2*mast_wall;   // 38
foot_w = 84; foot_d = 70; foot_t = 4;  // foot plate on the deck
foot_sock_h = 18;      // socket height (shell slides in)
foot_bolt_dx = 60; foot_bolt_dy = 46;   // 4 x M4 (or M3) holes to the deck
foot_pad_h = 3;                         // 4 pads on the deck lift the foot plate (M4 inserts sit in the pads)
z_mast_bot  = z_deck_t + foot_pad_h + foot_t;   // shell bottom (79)
// head geometry drives the mast height (see head parameters below)

// ---------------------------------------------------------------- PAN / TILT  (== INTERFACE, see pan_tilt_interface.scad)
// MG996R class servo (A: most values from shop listings, see doc)
srv_l = 40.7; srv_w = 19.7;     // (V) case footprint
srv_case_h = 36.5;              // (A) case height without the output spline
srv_total_h = 42.9;             // (V) incl. output spline
srv_ear_len = 54;               // (A) length over the mounting ears
srv_ear_below_top = 10;         // (A) ear plane below the output face
srv_shaft_off = 10.2;           // (A) output shaft centre from the end of the case
srv_ear_hole_dx = 49.5;         // (A) mounting hole spacing along the length
srv_ear_hole_dy = 9.5;          // (V kitronik) across the width
srv_ear_hole_d  = 4.2;
horn_d = 20;  horn_t = 3;  horn_pcd = 14;  horn_hole = 3.2;   // (V) 25T aluminium disc horn: 20 mm, 4 x M3 on 14 mm
// vertical neck stack above the mast-top plate
neck_ped_h  = 0;                // (no raised pedestal: the plate top is the horn attach face; plate is flat so it prints face-down)
srv_spline_above_case = srv_total_h - srv_case_h;  // 6.4
// turntable top = ear plane. distance ear plane -> horn bottom:
srv_ear_to_horn_bottom = srv_ear_below_top + srv_spline_above_case;           // 16.4 (horn is fixed to the pedestal, flush with the spline end)
tt_top_above_plate = neck_ped_h + srv_ear_to_horn_bottom;                      // 20.4
tt_t   = 4;                     // turntable plate thickness
skirt_r = 44;                   // turntable skirt radius (rotating, rides on PTFE tape ring)
skirt_t = 2;
pan_range_deg = 180;            // stock MG996R; cables are designed for +-120 (240) if a 270-degree servo is used
neck_plate_t = 9;               // mast-top (interface) plate thickness
// interface 1: where the pan/tilt module bolts to the mast-top plate (owner's design replaces mine here)
if1_bolt_dx = 60; if1_bolt_dy = 40; if1_bolt_d = 4.4;   // 4 x M4 pattern (A, default)
if1_slot_w = 30; if1_slot_h = 14;                       // cable slot in the plate
// interface 2: where the head is held by the tilt output (rear pad on the head lid)
if2_bolt_dx = 60; if2_bolt_dy = 40; if2_bolt_d = 3.4;   // 4 x M3 pattern on the head back (A, default)
tilt_range = [-25, 35];         // degrees (down, up)

// ---------------------------------------------------------------- HEAD (7 inch default)
scr_w = 165; scr_h = 107; scr_t = 10;     // (A) 165 x 100 assumed in the task; Waveshare wiki says 164.9 x 106.96 x 8 (V) -> pocket takes both
scr_vis_w = 156; scr_vis_h = 88;          // window in the bezel (V: active area 154.2 x 85.9)
scr_vis_dz = 0;                           // window offset up (A)
scr_clear = 0.6;
head_wall = 4.2;
head_r    = 8.5;
head_w = scr_w + scr_clear + 2*head_wall;   // 174
head_h = scr_h + scr_clear + 2*head_wall;   // 116
head_d = 44;
lip_t  = 2;                                  // front plate in front of the screen
head_axis_y = -3;                            // tilt axis depth (head centre = 0, front = +22)
head_axis_z = 8;                             // tilt axis above head centre
lid_t = 2.4;
cam_w = 60; cam_d = 30; cam_h = 28;          // (A) webcam body, SC-012-SN259 unknown: send real size
cam_lens_d = 16; cam_lens_dz = 0;
brow_w = cam_w + 8; brow_h = cam_h + 6;      // brow box outside size
brow_front_t = 3;
speaker_d = 40;                              // (A) optional speaker pocket in the lid
head_boss_t = 3;                             // inner boss that the servo ears press on
yoke_gap = srv_ear_below_top + srv_spline_above_case - head_wall - head_boss_t;   // 9.2: head wall to yoke arm; the horn attach face is the arm's inner face
yoke_arm_t = 7;
yoke_arm_w = 46;                             // depth of yoke arm / bar (along robot x)
yoke_bar_t = 6;

// ---------------------------------------------------------------- HEIGHTS (decided)
head_axis_h = 420;                           // tilt axis above floor
neck_axis_above_tt = ceil((srv_case_h - srv_ear_below_top)                                   // tilt axis above the turntable top: pan servo body height above the ears
    + sqrt(pow(head_d / 2 + abs(head_axis_y), 2) + pow(head_h / 2 + head_axis_z, 2)) + 4);   // + swept radius of the head corner + 4 mm = 102 for the 7 inch head

z_tt_top    = head_axis_h - neck_axis_above_tt;       // 318 turntable top
z_neck_plate_top = z_tt_top - tt_top_above_plate;     // 297.6 top of mast-top plate
z_neck_plate_bot = z_neck_plate_top - neck_plate_t;
z_mast_top  = z_neck_plate_bot;                       // shell top
neck_sock_h = 16;
mast_split_z = (z_mast_bot + z_mast_top)/2;           // junction of the two shell segments
collar_h    = 40;

// ---------------------------------------------------------------- SENSORS
sonar_ang   = 28;      // deg left/right of the front
sonar_r     = 126;
sonar_z     = 45;
sonar_l=45; sonar_w=20; sonar_t=15; sonar_hole=16.6; sonar_pitch=26;   // (V mostly: 45x20x15, 16 mm transducers; pitch A)
cliff_ang   = 52;
cliff_r     = 112;

// ---------------------------------------------------------------- BAYS (positions of bought parts in the base, robot frame)
batt_x = -2;  batt_y = 0;   batt_l = 77; batt_w = 40; batt_h = 21;      // 2 x 18650 holder (A)
xl_pos  = [[62,-36],[62,36]];  xl_l = 46; xl_w = 60; xl_h = 22;         // 2 x XL4016 (A) long side along y
mini_pos = [[-96,-56],[-96,56]];  mini_l = 23; mini_w = 17; mini_h = 8;   // fixed bucks (A)
fuse_pos = [[-61,-48],[-61,-30],[-61,-12],[-61,6],[-61,24]]; fuse_l = 30; fuse_w = 16; fuse_h = 12;   // 5 inline blade-fuse holders (A)
wago_pos = [[-96,-30],[-96,30]]; wago_l = 40; wago_w = 17; wago_h = 17;  // 2 lever connectors (A)
chg_pos  = [-102, 0]; chg_l = 45; chg_w = 26; chg_h = 10;               // USB-C charger board, socket faces rear (A)
sw_pos_y = 50;  sw_d = 19;                                              // main switch through the rear wall

// ---------------------------------------------------------------- columns and posts
col_pos  = [[28,48],[28,-48],[-70,35],[-70,-35],[98,48],[98,-48]];   // tray -> deck columns (M3 insert on top)
cpost_pos = [[85,70],[85,-70],[-100,40],[-100,-40]];                 // deck -> cover posts
col_d = 10; post_d = 9;

skirt_h = tt_top_above_plate - tt_t - 0.4;   // turntable skirt height (16)

// ---------------------------------------------------------------- small helpers shared by all files
module ring(r1, r2, h) { difference() { cylinder(r = r1, h = h); translate([0, 0, -1]) cylinder(r = r2, h = h + 2); } }
module hexnut_pocket(af = 5.7, h = 2.6) { cylinder(d = af / cos(30), h = h, $fn = 6); }   // M3 nut is 5.5 AF, +0.2
module insert_hole(d = 4.0, h = 6.5) { cylinder(d = d, h = h, $fn = 20); }              // M3 heat-set insert hole
module rrect2(w, d, r) { offset(r) square([w - 2 * r, d - 2 * r], center = true); }     // 2D rounded rectangle, w along x
// profile drawn in (y,z) and extruded along x from x0 to x1:
module ex(x0, x1) { translate([x0, 0, 0]) rotate([90, 0, 90]) linear_extrude(height = x1 - x0) children(); }

// ---------------------------------------------------------------- demo shape (only when THIS file is opened or exported on its own)
// A 100 x 100 mm plate with the 4 motherboard holes (M3 at 4 mm from the edges): print it to check the hole pattern on your printer.
module params_demo() {
    difference() {
        cube([mb_size, mb_size, mb_pcb_t]);
        for (hx = [mb_hole, mb_size - mb_hole], hy = [mb_hole, mb_size - mb_hole]) translate([hx, hy, -1]) cylinder(d = 3.2, h = 5, $fn = 24);
    }
}
if (is_undef(_robot2_lib)) params_demo();
