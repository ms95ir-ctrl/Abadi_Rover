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
skid_gap    = 1.5;     // skid height above floor when level (was 4 mm; with 1.5 mm they touch after about 1 degree tilting backwards and about 2.7 degrees tilting forwards/sideways; they scrape door thresholds and thick carpet)

// ---------------------------------------------------------------- MOTHERBOARD (V: 100x100, holes 4/96 mm)
mb_size   = 100;
mb_hole   = 4;         // hole offset from board edge
mb_x0     = 14;        // robot x of the board's BOTTOM edge (servo plugs face front, +x)
mb_y0     = -88;       // robot y of the board's LEFT edge (power terminals face the robot's right)
mb_stand  = 6;         // standoff height above deck
mb_pcb_t  = 1.6;
mb_tall   = 20;        // tallest part above the PCB, bare (A: ESP32 on sockets ~15, PCA9685 module with its bare header strip ~19, DRV8833 on sockets ~17, 470 uF cap ~13). Servo PLUGS ARE NOT INCLUDED here: see PCA9685 SERVO-PLUG RELIEF below.
// board (bx,by) -> robot (x,y):  x = mb_x0 - by ;  y = mb_y0 + bx   (board turned 90 deg)
function mb_xy(bx,by) = [mb_x0 - by, mb_y0 + bx];

// ---------------------------------------------------------------- PCA9685 SERVO-PLUG RELIEF (window in the cover + printed plug_hood)
// A servo plug on the PCA9685 header is taller than the 3 mm of free space under the cover (cover underside 102.6, bare header top 98.7).
// With the assumed plug (14 mm) the plug top is at 106.2 and the wires need another 8 mm to bend away, so the cover gets a window and a hood.
// plug_relief = false: no window and no hood (use right-angle servo plugs, about 6 mm high, or MEASURE your plugs first).
plug_relief   = true;
plug_h        = 14;    // (A) height of a 3-pin servo plug housing on the 2.54 mm header (typical Dupont / JR size). MEASURE YOUR PLUG, then change this number.
plug_bend     = 8;     // (A) extra room above the plug so the wires can turn sideways
hdr_plastic_h = 2.5;   // (A) black plastic base of the header (the plug sits on it)
pca_top_h     = 10.1;  // PCA9685 board top above the motherboard top face (from robot2_ghosts.scad, mb_pca)
mb_top_z      = z_deck_t + mb_stand + mb_pcb_t;                 // 79.6 top face of the motherboard
plug_top_z    = mb_top_z + pca_top_h + hdr_plastic_h + plug_h;  // 106.2 top of the plug housings
cover_in_z    = z_cover_top - cover_top_t;                      // 102.6 underside of the cover top plate
relief_h      = max(0, ceil(plug_top_z + plug_bend - cover_in_z));   // 12 mm of extra headroom above the cover underside (computed)
// window (robot frame): the header strip (board bx 11..74, by 2..8) plus 3 mm either side, and 15 mm toward the mast for the wires
relief_p0 = mb_xy(8, 13);     // corner 1 = [1, -80]
relief_p1 = mb_xy(77, -10);   // corner 2 = [24, -11]
relief_cx = (relief_p0[0] + relief_p1[0]) / 2;   relief_cy = (relief_p0[1] + relief_p1[1]) / 2;     // window centre = [12.5, -45.5]
relief_wx = abs(relief_p1[0] - relief_p0[0]);    relief_wy = abs(relief_p1[1] - relief_p0[1]);      // window size = 23 x 69
hood_wall = 2;  hood_top_t = 2;  hood_fl_w = 4;  hood_fl_t = 1.6;     // plug_hood (base.scad): wall, top thickness, flange width, flange thickness
hood_h_in = relief_h - cover_top_t;                                    // 9.6 inside height above the cover top face
hood_top_z = z_cover_top + hood_h_in + hood_top_t;                     // 116.6 top of the hood (outside), robot frame

// ---------------------------------------------------------------- COVER TOP: BUTTON, SPEAKER, SPEAKERPHONE  (R23, open item C5; sizes from docs/peripherals.md 5.6)
// Positions are on the cover top, robot frame. Each place is kept clear of the mast cut-out (x 38..86, |y| < 30), the plug hood (x -5..30, y -86..-5), the cover posts, the vents and each other.
// The cover prints top face DOWN, so the speaker pocket (a ring that hangs under the top plate) stands up from the bed and needs no support.
btn_hole_d = 30;                 // call / STOP button: round hole in the cover top (A: MEASURE your button; many 30 mm arcade buttons need a 28 to 30 mm hole and a plate of 2 to 3 mm)
btn_pos    = [62, 60];           // robot LEFT of the mast. Under it: 30 mm free down to the deck (the button needs about 25 mm), the foot plate ends at |y| = 42, the button body starts at |y| = 46
btn_depth  = 25;                 // (A, peripherals 5.6) free depth needed behind the panel
btn_body_d = 28;  btn_cap_d = 33;  btn_cap_h = 9;   // (A) ghost only: body behind the panel, cap above the panel
spk_place    = true;             // route B speaker place (grille + pocket) in the cover top. false = plain cover top
spk_pos      = [56, -60];        // robot RIGHT of the mast. The speaker faces UP; the microphone is in the head, 0.4 m higher
spk_grille_d = 36;               // grille opening about 36 mm across (19 holes of 3.5 mm inside it)
spk_pocket_d = 42;               // pocket about 42 mm across (inside)
spk_pocket_h = 15;               // pocket depth under the plate. (A: MEASURE the real speaker depth.)
spk_wall     = 1.6;              // pocket wall thickness
spk_body_h   = 12;               // (A) ghost only: speaker thickness
spkA_pos = [-14, 59];  spkA_d = 115;  spkA_h = 35;   // route A: flat spot on the cover top for a USB speakerphone. 115 mm is the biggest circle that stays free (mast, hood, posts, vents, button, speaker). (A: its real size, 100 to 125 mm, and weight, 350 g, are not verified.) Only kept free, nothing is cut. Ghost: ghost_speakerphone().

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
tt_top_above_plate = neck_ped_h + srv_ear_to_horn_bottom;                      // 16.4 (neck_ped_h is 0)
tt_t   = 4;                     // turntable plate thickness
skirt_r = 44;                   // turntable skirt radius (rotating, rides on PTFE tape ring)
skirt_t = 2;
pan_range_deg = 180;            // stock MG996R travel +-90 (A). INTERIM SOFTWARE PAN LIMIT = +-pan_limit_interim (see CABLE PATH below), normal limit +-80 only after the cable loop is proven in Stage 6. The 270-degree servo is optional and only needed for the 120-degree case.
neck_plate_t = 9;               // mast-top (interface) plate thickness
// interface 1: where the pan/tilt module bolts to the mast-top plate (owner's design replaces mine here)
if1_bolt_dx = 60; if1_bolt_dy = 40; if1_bolt_d = 4.4;   // 4 x M4 pattern (A, default)
// interface 2: where the head is held by the tilt output (rear pad on the head lid)
if2_bolt_dx = 60; if2_bolt_dy = 40; if2_bolt_d = 3.4;   // 4 x M3 pattern on the head back (A, default)
// TILT SIGN CONVENTION (same in every file and in the serial protocol): 0 = level, POSITIVE = the head looks UP, NEGATIVE = looks DOWN.
tilt_range = [-25, 35];         // degrees: [-25 = 25 degrees down, +35 = 35 degrees up]

// ---------------------------------------------------------------- CABLE PATH THROUGH THE NECK  (finding 20, decision R21: OPEN DESIGN ITEM)
// The bundle (HDMI + USB + power + servo leads) goes up the mast, through the neck plate (fixed), through the turntable (turns with the head), then into the head.
// The plate and the turntable are only tt_top_above_plate - tt_t = 12.4 mm apart and the bundle sits about 19 mm off the pan axis. So when the head pans by an angle,
// the turntable slot moves sideways by 2 x 19 x sin(angle / 2) (9.8 mm at 30 degrees, 26.9 mm at 90 degrees) and turns by the same angle. The old 38 x 12.5 slot in the plate
// (same place as the turntable slot) could not follow: a straight 25 x 12 bundle turned by 30 degrees had 30 percent of its section outside the plate slot, by 90 degrees all of it.
// WHAT IS DONE (no height is changed):
//   - The plate opening is now the swept envelope of the bundle for +-pan_cable_deg (a kidney shape, 762 mm2 against 475 mm2 before, clipped to the inside of the mast socket), see neck_plate().
//   - The turntable slot is 38 x 14 (was 38 x 12.5) so that the 12 mm bundle has 1 mm of play on each side.
//   - The bundle is NOT tied at the neck plate any more (doc 6.3 said so). It is tied low in the mast (self-adhesive tie mount on a shell or on the deck) and inside the head, so
//     the pan twist is spread over about 240 mm of free cable. The tie points are NOT modelled (use adhesive tie mounts). Do not tie the bundle to the plate or to the turntable.
//   - The HDMI cable is threaded from the HEAD end: its big 21 x 11 mm plug stays in the head and never has to pass the neck.
// WHAT WAS REJECTED: a service loop in the gap between plate and turntable. An S-bend of a 12 mm bundle (bend radius about 30 mm, ASSUMED) needs about 33 mm of height for +-30 degrees
//   and about 50 mm for +-90 degrees, plus about 10 mm for the two clamps: a gap of about 43 mm or 60 mm against 12.4 mm now, i.e. +31 mm or +48 mm. That is more than the 20 mm limit
//   of decision R21, so the heights stay as they are.
// INTERIM RULE: pan soft limit +-30 degrees (pan_limit_interim) until the loop is proven with the REAL bundle in Stage 6. Test result (straight, stiff 25 x 12 bundle turned with the head, intersection volumes): it fits the new plate
//   opening up to about +-28 degrees (13 mm3 of corner at +-30; the 21 x 11 HDMI plug fits at +-30 with 0), but it touches the rounded corners of the mast hole under the plate from about +-5 degrees (11 mm2 of its 300 mm2
//   section at +-15, 31 mm2 = 10 percent, a 4 mm corner, at +-30). So a soft bundle has to squeeze one corner by up to 4 mm at +-30. If the real bundle is stiff, lower the limit to +-20 degrees.
// OPEN ITEM: +-90 degrees needs the cable on the pan axis (hollow pan shaft, slip ring) or a taller neck. Both change the heights by more than 20 mm. Not designed yet.
bundle_w = 25;  bundle_t = 12;         // (A) cable bundle section: 25 x 12 mm (docs/mechanical-design.md 6.2)
hdmi_plug_w = 21;  hdmi_plug_t = 11;  hdmi_plug_l = 40;   // (A) full-size HDMI plug 21 x 11 mm, about 40 mm long (only a test ghost)
bundle_cy = -19;                       // bundle centre, y (x = 0), pan-axis frame: beside the pan servo (case edge at |y| 10.15) and inside the yoke bar edge (|y| 26)
cable_clr = 1.0;                       // play around the bundle in the openings
pan_limit_interim = 30;                // INTERIM software pan limit, +- degrees (R21)
pan_cable_deg = pan_limit_interim;     // the plate opening is cut for the bundle swept over +-pan_cable_deg
cable_sweep_step = 5;                  // degrees between the rectangles of the sweep (0.03 mm error at the corners)
tt_slot_x0 = -19;  tt_slot_x1 = 19;  tt_slot_y0 = -26;  tt_slot_y1 = -12;   // turntable slot (turns with the head): 38 x 14
if1_slot_w = bundle_w + 2 * cable_clr; if1_slot_h = bundle_t + 2 * cable_clr;   // INTERFACE 1 cable opening in the plate AT PAN 0 (27 x 14). The real opening is wider: the swept envelope for +-pan_cable_deg (neck_plate). Was 30 x 14, never used.

// ---------------------------------------------------------------- HEAD (7 inch default)
scr_w = 165; scr_h = 107; scr_t = 10;     // (A) 165 x 100 assumed in the task; Waveshare wiki says 164.9 x 106.96 x 8 (V, search summary only: re-check the page) -> pocket takes both
scr_vis_w = 156; scr_vis_h = 88;          // window in the bezel (V, search summary only: active area 154.2 x 85.9)
scr_vis_dz = 0;                           // window offset up: ASSUMED (A). The real active area is probably NOT centred on the board. Cut a paper template of the real screen (outline and picture area) before you print head_shell, then change this number.
scr_clear = 1.2;                          // (A) play around the screen in the pocket: 0.6 mm per side (was 0.6 mm in total: too tight for printed PETG). Pocket = 166.2 x 108.2 mm.
head_wall = 4.2;
head_r    = 8.5;
head_w = scr_w + scr_clear + 2*head_wall;   // 174.6
head_h = scr_h + scr_clear + 2*head_wall;   // 116.6
head_d = 44;
lip_t  = 2;                                  // front plate in front of the screen
head_axis_y = -3;                            // tilt axis depth (head centre = 0, front = +22)
head_axis_z = 8;                             // tilt axis above head centre
lid_t = 2.4;
cam_w = 60; cam_d = 30; cam_h = 28;          // (A) webcam body, SC-012-SN259 unknown: send real size
cam_lens_d = 16; cam_lens_dz = 0;
brow_extra = 8;                              // each side of the camera: extra brow width for the camera-live LED (R23); was 0 (brow was 68 wide)
brow_w = cam_w + 8 + 2 * brow_extra; brow_h = cam_h + 6;      // brow box outside size (84 x 34)
brow_front_t = 3;
cam_gap = 1.5;                               // (A) air / foam between the brow front wall and the webcam body. Must be at least 1.2 mm so that the 2 mm lens bump stays behind the slide cover.
// R23 (open item C5): camera-live LED hole and camera slide cover, in the brow front wall. Sizes from docs/peripherals.md 5.6.
led_d = 5.2;                                 // (A) hole for a 5 mm LED (the LED flange, 5.8 mm, sits behind the wall). MEASURE YOUR LED.
led_y = -(cam_w / 2 + 4);                    // LED hole centre y, head frame: 4 mm beyond the webcam body edge, robot RIGHT side (-y). Same height as the lens.
cov_t = 1.0;                                 // (A) slide cover thickness: printed 1 mm (print part cam_cover) or a thin plastic card
cov_play = 0.4;                              // total play in the cover slot (thickness)
cov_skin = (brow_front_t - cov_t - cov_play) / 2;   // 0.8 mm of wall in front of and behind the slot (two perimeters)
cov_slot_h = cam_lens_d + 6;                 // slot height = lens window + 6 = 22 mm
cov_y0 = -(cam_lens_d / 2 + 6);              // closed end of the slot, y: 6 mm beyond the lens window edge (the slot is open at the +y side of the brow)
cov_h = cov_slot_h - 2;                      // cover height 20 mm
cov_len = 62;                                // cover length: shuts the lens window when pushed in; its end sticks out cov_len + cov_y0 - brow_w / 2 = 6 mm of the brow for the finger
cov_pull = cam_lens_d / 2 - cov_y0 + 2;      // 24 mm: how far to pull the cover out. The cover end must pass the far edge of the lens window (22 mm), plus 2 mm margin. Pulling it further (or out of the slot) is fine.
speaker_d = 40;                              // (A) 40 mm round speaker (route B). It goes into the COVER (see COVER TOP), NOT into the head lid. The 9-hole grille in the lid is only air.
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
z_neck_plate_top = z_tt_top - tt_top_above_plate;     // 301.6 top of mast-top plate
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
cliff_ang   = 52;      // cliff sensors: degrees left/right of the front. KEPT after a search for a place nearer the caster (x 105..125):
cliff_r     = 112;     //   centre radius -> x = 68.96, y = +-88.3. That is 35 mm behind the caster (x 104) and 42.5 mm ahead of the balance point (x 26.5).
                       //   A 30 x 14 mm module has no room ahead of about x = 77: caster flange (to x 123), XL4016 bays (to x 85), columns, sonar cheeks.
                       //   A much smaller module (about 16 x 10 mm) might fit near x = 115, y = +-22 (flat 2D search only, not checked in 3D). So the cliff margin is SHORT: see docs/mechanical-design.md.

// ---------------------------------------------------------------- OPTIONAL BUMPER (NOT in the first build)
// A low arc around the front (3 printed pieces, glued) with two arms that go through slots in the rim and push two lever micro switches.
// bumper_slots = true: the tray has the two arm slots and the two switch pads (costs nothing, saves a reprint if you add the bumper later).
// bumper_slots = false: closed rim, no pads. The bumper pieces themselves are printed only if you want them (print_parts.scad: bumper_R, bumper_C, bumper_L).
bumper_slots = true;
bump_ang   = 66;       // arm direction, degrees left/right of the front. At 38 deg the arm crossed the sonar cheek (sonars are at +-28 deg); between about 44 and 64 deg the arm or the switch pad hits the cliff modules (52 deg).
bump_z0    = 18;       // bottom of the arc AND of the arms: both lie flat on the print bed, so no supports are needed
bump_arc_h = 16;       // arc height (z 18 to 34, below the sonar holes which start at z 36.7)
bump_arc_t = 4;        // arc wall thickness
bump_arm_w = 12;  bump_arm_h = 6;
bump_arm_r0 = 124;     // radius of the inner end of the arm (the arm sticks out 9 mm beyond this, through the rim). Moved outward so the 20 mm switch clears the wheel-well wall and the cliff module (about 2.5 mm each).
bump_travel = 3.5;     // (A) how far the arc is pushed in a front hit. The arm slots are widened so the arms can slide sideways by travel x sin(ang).
bump_slot_w = bump_arm_w + 2 * (bump_travel * sin(bump_ang) + 0.5);     // 19.4 at 66 deg
bump_sw_l = 20;  bump_sw_w = 10.2;  bump_sw_t = 6.4;   // (A) lever micro switch (KW12-3 type) lying flat: 20 x 10.2 x 6.4 mm, mounting holes 9.5 mm apart along the 20 mm side; the arm pushes the lever
bump_sw_pitch = 9.5;
bump_pad_h = bump_z0 + bump_arm_h / 2 - bump_sw_t / 2 - z_floor_t;     // 2.8: pad height so that the switch lever is level with the middle of the arm
bump_pad_w = 14;  bump_pad_l = 12;                                      // pad: 14 mm along the arc x 12 mm radial (the 20 mm switch overhangs it a little)

// ---------------------------------------------------------------- BAYS (positions of bought parts in the base, robot frame)
batt_x = -2;  batt_y = 0;   batt_l = 77; batt_w = 40; batt_h = 21;      // 2 x 18650 holder (A)
xl_pos  = [[62,-36],[62,36]];  xl_l = 46; xl_w = 60; xl_h = 22;         // 2 x XL4016 (A) long side along y
mini_pos = [[-96,-56],[-96,56]];  mini_l = 23; mini_w = 17; mini_h = 8;   // fixed bucks (A)
fuse_pos = [[-61,-48],[-61,-30],[-61,-12],[-61,6],[-61,24]]; fuse_l = 30; fuse_w = 16; fuse_h = 12;   // 5 inline blade-fuse holders (A)
wago_pos = [[-96,-30],[-96,30]]; wago_l = 40; wago_w = 17; wago_h = 17;  // 2 lever connectors (A)
chg_pos  = [-102, 0]; chg_l = 45; chg_w = 26; chg_h = 10;               // USB-C charger board, socket faces rear (A)
sw_pos_y = 50;  sw_d = 19;                                              // main switch through the rear wall

// ---------------------------------------------------------------- columns and posts
col_pos  = [[28,48],[28,-48],[-70,64],[-70,-64],[98,48],[98,-48]];   // tray -> deck columns (M3 insert on top). Rear pair moved from (-70,+-35) to (-70,+-64): the old ones stood inside the fuse holders.
cpost_pos = [[85,70],[85,-70],[-100,40],[-100,-40]];                 // deck -> cover posts
col_d = 10; post_d = 9;

skirt_h = tt_top_above_plate - tt_t - 0.4;   // turntable skirt height (12)

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
