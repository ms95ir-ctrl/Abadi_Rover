# Robot 2: mechanical design (first draft)

Written 5 November 2026 for the telepresence robot. This file covers the body only: base, wheels, mast, head, pan/tilt, cable routes, weights, tip-over, print list, hardware, assembly. The small computer is chosen in `sbc-selection.md`. Wiring, software and the shopping list are in other files.

**Words used here.** SBC = single board computer (the Raspberry-Pi-type brain). Motherboard = your 100 x 100 mm ESP32 board. Mast = the tube between base and head. Pan = turn left/right. Tilt = nod up/down. Yoke = the U-shaped fork that holds the head. CoG = centre of gravity (the balance point). PETG = a strong 3D-printer plastic. Heat-set insert = a small brass nut that you melt into plastic with a soldering iron. STL = the file format a 3D printer slicer reads. OpenSCAD = a free program that builds 3D models from numbers.

**How sure am I.** (V) = I saw it in a source or file. (A) = my assumption or my own calculation; check it. All prices are about-prices in EUR (A); check the shop on the day.

---

## 1. The short answer

| | |
|---|---|
| **What I designed** | A round, low base (260 mm wide, 105 mm high) with two driven wheels, one ball caster and four anti-tip feet. A 214 mm mast carries a head with the 7 inch HDMI screen and the webcam on a pan/tilt fork. Total height **504 mm**. |
| **Recommended chassis** | A **new printed two-wheel base** (not the ELEGOO Conqueror tracks). Reasons in section 3. |
| **Head height** | The screen centre is at 412 mm and the camera lens at 485 mm above the floor. That is about sofa-seat height for the screen. A shorter 340 mm version is one number to change (section 8). |
| **Motors** | **Pololu 25D metal gearmotor, 12 V, medium-power, 47:1** (two). The 1:48 TT motors are too weak (calculation in section 5.5). |
| **Weight** | About **2.6 kg** (first estimate). That is above the 1.5 to 2 kg in your request, so the motors are sized for 3 kg. |
| **Stability** | Static tilt about **24 degrees** before it tips. The smallest sideways or forward push that tips it is about **4.7 N** (about 0.5 kg of force) at head height. That is honest but not great: see section 8 for what to do about it. |
| **Printing** | 39 pieces, 33 different parts, about 1.1 kg of PETG, about 44 hours (rough). Biggest part 178 x 138 mm, so a printer bed of **180 x 180 mm works (tight), 200 x 200 mm is comfortable**. |
| **Pan/tilt** | My own default uses two MG996R servos. The part you can swap for your own design is the round **INTERFACE 1 plate** at the top of the mast, plus an optional **INTERFACE 2 pad** on the back of the head. Section 7.4 lists the dimensions I need from you. |

### Questions I need you to answer (they change the design)

1. **Which 3D printer do you have, and what is its bed size?** (Largest part 178 x 138 mm; tallest part 125 mm.) If the bed is smaller than 180 x 180 mm, tell me; I will cut the parts smaller.
2. **Where will you print?** The plan assumes you print **before** you travel and pack the parts (they stack in a small box). Is that right?
3. **Send me the real size of the webcam SC-012-SN259** (length x width x height of the body, and where the lens is). I assumed 60 x 30 x 28 mm.
4. **Which exact 7 inch screen** will you buy? (I designed for 165 x 107 x 10 mm, see section 7.1.)
5. **Your pan/tilt design:** the numbers in section 7.4, or a photo or STL of it.
6. **Is robot 1's battery pack reused or is this a new pack?** I assumed a plain 2 x 18650 holder (77 x 40 x 21 mm).

---

## 2. Pictures

All pictures are in `../3d/renders/`. They are drawn from the real 3D files (the OpenSCAD files in `../3d/`).

| Picture | What it shows |
|---|---|
| `robot2-iso.png` | Whole robot, isometric view |
| `robot2-front.png` | Front view with the main dimensions |
| `robot2-side.png` | Side view with the main dimensions and the balance point |
| `robot2-sketch-side-phone.png` | **Simple dimensioned side sketch for a phone screen** |
| `robot2-base-exploded.png` | **Exploded view of the base electronics layout** |
| `robot2-layout-top.png` | Top views: lower compartment and deck level |
| `robot2-head-pantilt.png` | **Close view of the head and pan/tilt** (front and back) |
| `robot2-section.png` | Cut through the middle: cable path in the mast |
| `robot2-stability.png` | Tip-over picture (top view, support area) |
| `robot2-print-parts.png` | Every printed part in its printing position |

![isometric](../3d/renders/robot2-iso.png)
![phone sketch](../3d/renders/robot2-sketch-side-phone.png)

---

## 3. Chassis: ELEGOO Conqueror tracks or a new printed base?

| | (a) Re-use the ELEGOO Conqueror tracked chassis | (b) New printed two-wheel base (recommended) |
|---|---|---|
| **Is it free?** | It is robot 1's chassis. You would have to take robot 1 apart or buy a second one. | Costs filament (about 40 EUR, A) and print time. |
| **Size and weight** | Listings give about 21.8 x 22.3 x 18.8 cm and about 1.5 kg (V, shop listings; the order of the three numbers is not stated). Heavy to carry on a trip. | Parts are small pieces you can pack in a box. Base is 260 mm wide, printed parts weigh about 0.65 kg for the base. |
| **Turning** | Tracks scrub on carpet when turning. You need more motor torque and the carpet wears. | Two wheels in the middle turn on the spot with little scrub. |
| **Stability** | Narrow track (about 16 cm, A) for a 0.5 m tall robot. Tips easier. | Wheel track 234 mm plus four anti-tip feet. |
| **Room inside** | Open metal plates made for an Arduino. The 100 x 100 mm board, the SBC, a 2S pack and 4 bucks do not fit without a new top plate. | Designed around your parts: 100 x 100 mm board on its 4 holes, SBC, pack, bucks, fuses. |
| **Mast fixing** | Needs a printed top plate anyway. | Mast is part of the design. |
| **Looks** | A tank. | A friendly round base, like a small home robot. |

**Recommendation: (b).** The tracks fit a rough-terrain tank, not a tall robot that rolls over a living-room floor, and robot 1 needs that chassis.

---

## 4. The design in one page

### 4.1 Coordinates (used in all files)

Origin on the floor under the centre of the base. **+x = front** (the way the screen looks), **+y = robot left**, **+z = up**. All sizes in millimetres.

### 4.2 Main dimensions

| Item | Value |
|---|---|
| Base | round, **260 mm** diameter, **105 mm** high, floor underside 12 mm above the ground. 265 mm front to back with the bumper. |
| Drive wheels | **65 mm** diameter (parameter `wheel_d`), 26 mm wide, axle at x = 0, wheel centres at y = +-117 (track 234 mm) |
| Ball caster | x = +104 (axle to caster 104 mm), steel ball 16 mm |
| Anti-tip feet | 4 feet, 4 mm above the floor: (95, +-58) and (-85, +-85) |
| Mast | stadium-rounded rectangle **56 x 44 mm**, wall 3 mm, at x = +62; shells from z = 79 to z = 292.6 (214 mm) |
| Mast-top plate (INTERFACE 1) | round 100 mm, 9 mm thick, top at z = 301.6 |
| Turntable top | z = 318 |
| Tilt axis | z = **420** (parameter `head_axis_h`) |
| Head | **174 wide x 116 high x 44 deep**, centre at z = 412, camera "brow" on top; top of brow z = **504** |
| Yoke (fork) | 206 mm wide over the arms |
| Camera lens | z = 485 |
| Pan range | +-90 degrees with the stock MG996R (180 degree servo). The cable slack is designed for +-120 degrees if you fit a 270 degree servo. |
| Tilt range | 25 degrees down, 35 degrees up |

![front](../3d/renders/robot2-front.png)
![side](../3d/renders/robot2-side.png)

### 4.3 Layers of the base (bottom to top)

| Layer | Height z (mm) | What is on it |
|---|---|---|
| **Tray** (printed) | floor 12 to 15, rim up to 68 | wheel wells with motor saddles, caster, battery cradle, buck modules, fuses, lever connectors, charger board, main switch, sonars, cliff sensors |
| **Deck** (printed) | 68 to 72 | the 100 x 100 mm motherboard on 4 standoffs, the SBC on 4 standoffs, the mast foot |
| **Cover** (printed) | 72 to 105 | closes the base, vent slots at the rear, opening for the mast |
| Bumper (printed) | z 18 to 34, 5 mm outside the rim | front arc with two micro switches (optional) |

The tray, deck and cover are each **printed in 4 pieces** (front-left, front-right, rear-left, rear-right) that lock with dovetails and are glued. This is what makes the base fit a small printer bed.

![exploded](../3d/renders/robot2-base-exploded.png)
![layout](../3d/renders/robot2-layout-top.png)

---

## 5. Base in detail

### 5.1 Motherboard (V board data from `pcb/kicad/`)

- The board sits on the **deck** on **4 printed standoffs, 6 mm high**, on its four M3 holes (92 mm spacing). Hole positions on the deck: (10, -84), (10, 8), (-82, -84), (-82, 8). Standoffs have M3 heat-set inserts; use 4 screws M3 x 8.
- The board is turned 90 degrees: its **bottom edge (PCA9685 servo plugs) faces the front and the mast**, its **left edge (the four screw terminals and POWER OUT) faces the robot's right side**, its **right edge (motor plugs M1 to M4 and the ESP32 USB-C end) faces the SBC**.
- **ESP32 USB-C:** the two USB-C sockets sit 8 mm inside the right edge. A straight plug sticks out about 12 mm more. The SBC starts 24 mm from the board edge, so a data-only USB-C cable about 20 cm long makes the bend easily (V: the board says USB-C toward the right edge).
- **Tall parts on the board** (from `build_board.py`; heights above the board top are my estimate, A): ESP32 on its two sockets about 15 mm, PCA9685 module on its header with plugs about 19 mm, DRV8833 modules on sockets about 17 mm (white plug on the plug side), screw terminals 10 mm, capacitor C1 12.5 mm. **Budget 20 mm.** The cover is 3 mm above that (underside at z = 102.6; board top at z = 79.6; 99.6 is the tallest point).
- **DRV8833 plug side:** the modules are inserted so the white plug side is toward the bottom edge of the board (the board prints "white plug v"). On the deck this is the side toward the mast. There are 15 mm of free space in front of the plugs.
- **Wire holes in the deck** (so wires go between the compartments): a 36 x 10 mm slot next to the motor plugs M1/M2; a 45 x 9 mm slot at the board's left edge for battery and buck wires; a 8 x 32 mm slot under the board's header strip for the sensor wires (sonar, cliff, bumper); a 14 x 8 mm spare slot.

### 5.2 SBC (generic Raspberry-Pi-sized envelope 85 x 56 mm, parameter)

- SBC mount holes: 58 x 49 mm pattern, M2.5 (A: the usual Raspberry Pi pattern, from memory; check your board). Four printed standoffs 5 mm high, hole 2.2 mm for self-tapping M2.5 x 6 screws (an upgrade is 4 M2.5 inserts).
- Position: x from -72 to 13, y from 36 to 92. The **USB and network end faces the rear**, the **edge with the power and micro-HDMI sockets faces the robot's left rim**.
- Cables: **HDMI** leaves the left edge (about x = -14), bends toward the mast foot. **USB webcam** plugs into a USB port at the rear end and runs forward. **Data-only USB cable** to the ESP32 (see `sbc-selection.md`). **5.1 V power** comes from the XL4016 module in the lower compartment through the deck slot.
- The cover is at 102.6, a Pi 5 with Active Cooler is about 95 mm high at its tallest point (V cooler 63.5 x 42.5 x 13.7 mm; USB stack height A). A different board of Raspberry-Pi size also fits; for a different shape change `sbc_l`, `sbc_w` and the hole parameters.

### 5.3 Power parts (lower compartment)

All of these are shown in `robot2-layout-top.png`. Sizes of bought modules are my assumptions (A); measure yours and change the numbers in `robot2_params.scad`.

| Part | Count | Where | Size used (A) |
|---|---|---|---|
| 2 x 18650 holder (the 2S pack) | 1 | in a low cradle at the centre, x -2 | 77 x 40 x 21 |
| BMS board (HX-2S-JH20 type) | 1 | on top of the pack | 56 x 21 x 4 |
| XL4016 buck modules (servo 5 V and SBC 5.1 V) | 2 | front, beside the caster, long side across | 46 x 60 x 22 with heat sink |
| Fixed bucks (clean 5 V, 3.3 V) | 2 | rear left and right | 23 x 17 x 8 |
| Fuse holders (BATT IN, servo, clean 5 V, 3.3 V, SBC) | 5 | rear, in a row | 30 x 16 x 12 |
| Lever connectors (Wago-type) | 2 | rear | 40 x 17 x 17 |
| USB-C charger board | 1 | rear centre, **USB-C socket faces the rear window** (16 x 12 mm hole in the rim, 19 to 31 mm above the floor) | 45 x 26 x 10 |
| Main switch | 1 | rear wall, left, hole 19 mm (parameter `sw_d`) | round rocker, 15 mm body |

Everything is held with double-sided foam tape and zip ties. The floor has 36 slots (3 x 1.6 mm pairs) next to every module for zip ties. The XL4016 modules get warm: the cover has vent slots and the rim has 4 vent slots at the rear.

### 5.4 Wheels, caster, anti-tip feet

- **Wheels:** 65 mm rubber-tyre robot wheels with a hub for a 4 mm D-shaft (A: the Pololu 25D shaft is a 4 mm D-shaft; check on the motor you buy). Parameter `wheel_d`. Wheel width 26 mm (A). The wheel sits in a **window in the tray rim**, outer face flush with the rim.
- **Motor mount:** the motor body (25 mm round, 52 mm long) lies on a **printed saddle** and is held by two **printed caps** per motor (2 x M3 x 20 each). The gearbox face sits 0.2 mm from a thin printed wall; the 4 mm shaft and the small round boss on the gearbox go through a 12 mm hole in that wall.
- **Ball caster:** a printed cup (flange on the floor) holds a **16 mm steel ball** (a 5/8 inch bearing ball also fits) behind a printed ring with a 14 mm hole. 3 x M3 screws hold the ring, 3 x M3 + nuts hold the flange. If you prefer, buy a ready ball caster and change `caster_x`; the floor has a 28.5 mm hole.
- **Anti-tip feet:** four printed feet (Ø 14) on M3 screws, **4 mm above the floor**. They only touch when the robot tilts about 2 degrees. They stop the nose-up tip behind the wheels and widen the sideways support.

### 5.5 Motor choice and the torque calculation

**What the robot needs.** Rolling resistance of a small hard wheel on carpet: coefficient 0.10 (A, typical range 0.05 to 0.15). Wheel radius 32.5 mm. Torque per wheel = force x 0.0325 / 2.

| Robot mass | Flat carpet, steady | Flat carpet, speeding up 0.3 m/s2 | 5 degree ramp on carpet |
|---|---|---|---|
| 2.0 kg | 0.032 N·m (0.33 kg·cm) | 0.042 N·m | 0.060 N·m (0.61 kg·cm) |
| **2.6 kg (this design)** | 0.041 N·m (0.42 kg·cm) | 0.054 N·m | **0.077 N·m (0.79 kg·cm)** |
| 3.0 kg (design limit) | 0.048 N·m | 0.062 N·m | 0.089 N·m (0.91 kg·cm) |

**TT 1:48 motors (the yellow ones).** Shop copies of Adafruit's figures (V): 200 rpm no load at 6 V, stall torque 0.8 kg·cm at 6 V, stall current 1.5 A at 6 V (about 1.85 A at 7.4 V, calculated). Result for this robot:
- The motor is **rated for 6 V maximum**; on the 7.4 V pack it would draw up to 1.85 A when stalled. The DRV8833 module gives 1.5 A continuous (2 A peak) per channel (V from your brief). Over the limit.
- At 6 V the stall torque (0.8 kg·cm) is **less than the ramp need (0.91 kg·cm at 3 kg)**. At 7.4 V the ramp takes 92 % of stall torque: 1.7 A and 0.06 m/s.
- On flat carpet it needs 43 to 53 % of stall torque all the time. Plastic gears, hot motor. **Too weak. I do not recommend them.**

**Chosen motor: Pololu 25D metal gearmotor, 12 V, medium power (MP), 47:1** (Pololu item 3229). 25 mm round, 52 mm long, 4 mm D-shaft. These are 12 V motors run from the 6.0 to 8.4 V pack, so they are slower and gentler than on 12 V. Values for the 7.4 V case (speeds follow from 12 V data by simple scaling, A):

| Motor | Seen on the Pololu page (V) | At 7.4 V: no-load speed | At 7.4 V: stall torque | At 7.4 V: stall current | Flat carpet, 2.6 kg | 5 degree ramp, 3 kg |
|---|---|---|---|---|---|---|
| TT 1:48 | 200 rpm, 0.8 kg·cm, 1.5 A (at 6 V) | 0.84 m/s | 0.99 kg·cm | **1.85 A** (too high) | 0.48 m/s, 0.9 A | **92 % of stall**, 0.06 m/s, 1.7 A |
| **Pololu 25D MP 47:1** | 170 rpm, 1.8 A stall at 12 V (V). Stall torque about 5.2 kg·cm at 12 V is my estimate (A: 0.17 kg·cm motor torque x 46.85 x 65 % gearbox) | **0.36 m/s** | 3.2 kg·cm (A) | **1.11 A** (1.26 A at 8.4 V) | 0.31 m/s, 0.2 A | 0.25 m/s, 0.36 A |
| Pololu 25D LP 47:1 (cooler, slower) | 120 rpm, 0.9 A, 4.8 kg·cm at 12 V (V, item 3253) | 0.25 m/s | 2.96 kg·cm | 0.56 A | 0.22 m/s, 0.11 A | 0.17 m/s, 0.19 A |
| Generic 25GA-370, 12 V, "130 rpm" | **sellers disagree by 4x**: one lists 0.5 rated and 2 kg·cm stall, others claim 20 kg·cm (V, conflicting) | 0.27 m/s | 1.23 kg·cm (one seller's number) | 0.56 A | 0.18 m/s | **74 % of stall**, 0.07 m/s |

**Result:** the MP 47:1 stays under 1.5 A even when stalled (1.26 A at a full 8.4 V pack) and uses only 13 % (flat) to 29 % (ramp) of its stall torque. It drives at about 0.3 m/s, a slow walking pace. The LP version is a good second choice if a shop has it (slower, 0.2 A). A cheap generic 25GA-370 is only acceptable if the listing **states a stall torque of at least 4 kg·cm at 12 V**; test one before buying two. Price: about 25 to 30 EUR each (A). Check pololu.com (ships to Germany, VAT added at checkout) or a European reseller. The two spare motor spots M3/M4 on the board are not used.

**The robot should not be driven at 100 % into a wall**: stall is survivable for seconds only. Software can limit the PWM to about 85 %.

### 5.6 Sensors and bumper

- **Two front sonars (HC-SR04):** 45 x 20 x 15 mm with two 16 mm transducers (V). They sit at **+-28 degrees**, facing outward through **4 round holes of 16.6 mm** in the rim, centre height 45 mm. Two printed cheeks hold each board; foam tape does the rest. The board's 1k/2k echo dividers are on the motherboard (V).
- **Two downward cliff sensors:** IR reflective modules about 31 x 14 x 7 mm (A) at **+-52 degrees**, radius 112 mm. Each has a 12 x 7 mm window in the floor and two 3.5 mm bosses with 2.7 mm holes (self-tapping M3 x 6). They look at the floor 12 mm below. On carpet the floor can be darker or lighter: tune the sensor's potentiometer. Which spare pins to use is for the wiring file (the SPARE IO header).
- **Bumper:** a low front arc (5 mm outside the rim, z 18 to 34) in **three 50 degree pieces** glued edge to edge. Two arms go through slots in the rim (14 x 10 mm) and rest on two small **lever micro switches** (A: KW12-3 type, 2 pieces, optional). The switch lever is its own return spring. If the arc is pushed 3 to 4 mm, a switch closes. It sits below the sonar holes, so it does not block them.

---

## 6. Mast and cable routing

### 6.1 Mast

- **Two segments, each of two half shells** (front and back), 107 mm long, 56 x 44 mm outside, wall 3 mm. A tongue and groove runs along the seam. This lets you **lay the cables into the channel** before closing, so the connectors never have to pass through a tube.
- Channel inside: **50 x 38 mm**.
- **Foot plate** (70 x 84 mm) bolts to 4 pads on the deck with 4 x M4 x 10 into M4 heat-set inserts. A socket (18 mm high) takes the lower shell; two M3 x 12 screws hold the shell (each shell has a captive M3 nut on the inside).
- A **collar** (two halves, 40 mm high, 4 x M3 x 20 with nuts) clamps the joint between the two segments.
- The top end goes into the **16 mm deep socket under the INTERFACE 1 plate**, again with 2 x M3 x 12 screws.
- **Stiffness (A, my calculation, printed PETG modulus 1500 MPa):** the weak direction (front to back) has I = 50,000 mm4. A 5 N push at head height bends the mast **0.9 mm** and loads the plastic with **0.75 MPa**. The mast is not the weak link. The joints and the base are. After building, do a wiggle test: hold the head and shake the mast; if the collar slips, add 2 M3 screws through the collar into the shells.

### 6.2 Cable list (what goes up the mast)

| Cable | Type | From | To | Notes |
|---|---|---|---|---|
| Screen picture | **HDMI flat cable**, micro-HDMI plug to HDMI-A plug (slim, about 60 to 80 cm) | SBC (HDMI0) | screen | Needs the longest length: about 120 mm along the deck, 215 mm up the mast, 120 mm loop, 60 mm inside the head. Plug size about 21 x 11 mm fits the 38 x 12.5 mm neck slot lengthwise. If it will not pass, thread it from the head end before plugging in. |
| Webcam | USB cable of the webcam (about 1.5 m: coil the extra in the head) | SBC USB port (blue USB 3 port) | webcam in the brow | 4 mm round |
| Screen power | 2 wires (red/black), about 0.5 mm2, 5 V | POWER OUT 5 V pin on the motherboard (wiring file decides) | screen's micro-USB power input (use a power-only cable) | About 0.5 A |
| Servo leads | 2 x servo **extension cable** 50 cm (3 wires each) | PCA9685 channels | pan servo, tilt servo | The pan servo is in the neck, the tilt servo in the head |
| (optional) touch USB | thin USB cable | SBC | screen's touch port | Skip unless you use touch |

Total bundle is about 25 x 12 mm. It passes through the mast channel (50 x 38), the neck-plate slot (38 x 12.5), the turntable slot (same size) and the **30 x 14 mm cable slot in the bottom of the head** (the slot is at y = -26 to +4).

### 6.3 Slack for the pan range of +-120 degrees

The bundle passes about 22 mm beside the pan axis. A turn of 120 degrees moves it by 22 mm x 2.09 = **46 mm**. So: fix the bundle with a zip tie to the neck plate (a slot is left beside the cable slot), fix it again inside the head, and leave **at least 100 mm of free loop in between**. Use the loop in the neck space (between turntable and head bottom); the picture `robot2-head-pantilt.png` shows it. Test the full turn slowly before you close the cover.

![head](../3d/renders/robot2-head-pantilt.png)
![section](../3d/renders/robot2-section.png)

---

## 7. Head and pan/tilt

### 7.1 Screen and camera

- **7 inch screen (default):** I assumed **165 x 100 x 10 mm** as asked. The Waveshare wiki lists the 7 inch HDMI LCD (C) at **164.90 x 106.96 x 8 mm** with a visible area of **154.21 x 85.92 mm** (V, found by web search; I could not open the page). My pocket is **166 x 108 mm** (screen 165 x 107 + 1 mm of play), so both fit. Weight 200 to 250 g with the driver board as in your request; shop listings range from 211 to 380 g (V, conflicting; the larger numbers include packaging). The window in the front plate is 156 x 88 mm. The screen is held by the front lip and by four corner posts (with foam tape). Pocket depth is 10 mm; behind it is a 29.6 mm deep space for the driver board and the HDMI plug.
- **Camera:** the webcam sits in a **brow** above the screen so it looks the same way as the screen (the remote person looks "into" the camera). The brow's inner size fits a webcam up to **60 x 30 x 28 mm (A)**. The lens window is 16 mm. **Please send me the real size** or take the camera out of its case and tell me the circuit board size.
- **Speaker (optional):** the lid has a round grille (9 holes) for a 40 mm speaker (A). Sound must be decided in the software/wiring files.
- **Lid:** 4 x M3 x 8 into inserts in the corner posts. The lid carries the **INTERFACE 2 pad** (section 7.4).

### 7.2 Alternative 10.1 inch screen (parameters)

Change these numbers in `robot2_params.scad` (A: I could not find a reliable outline for the 1024 x 600 10.1 inch HDMI LCD; one shop lists 235 x 144, which may be the outline or the visible area):

```
scr_w = 235;  scr_h = 146;  scr_t = 12;       // outline of the screen (check yours)
scr_vis_w = 224;  scr_vis_h = 126;            // visible area
```

The head becomes about 244 x 155 mm (does not fit a 220 mm bed, needs about 250 mm), the neck height and the yoke follow automatically. The head weighs about 0.55 kg more. The tip-over table (section 8) has a row for this: worst static tilt falls to 18 degrees, so use the shorter mast or the ballast. **My recommendation is to stay at 7 inch for a first build.**

### 7.3 Default pan/tilt (two MG996R servos)

- **Servo (V):** MG996R body **40.7 x 19.7 x 42.9 mm, 55 g** (HobbyKing), 25-tooth spline, metal gears. Ear screw holes about 9.5 mm apart (Kitronik listing, V); I assumed **49.5 mm** along the length, ear plane **10 mm** below the output face, shaft **10.2 mm** from the end of the case (A: these three numbers are not in the sources I found). Put the real servo next to the model before printing the turntable and the head; change `srv_ear_hole_dx`, `srv_ear_below_top`, `srv_shaft_off`, `srv_spline_above_case` if needed.
- **Aluminium horn:** 25T disc horn, **20 mm disc, 4 x M3 threaded holes on a 14 mm circle** (V, shop listings). You need **2 horns** (about 3 to 4 EUR each, A). The servo kit's plastic horn is **not** used.
- **Pan (turn):** the servo is mounted **upside down**. Its horn is screwed to the top of the mast-top plate (4 x M3 x 14 from below, through plain holes). The servo body, the **turntable** and the **yoke** turn. The head weight rides on a **12 mm skirt** of the turntable that slides on a ring of PTFE tape (plastic tape, 0.2 mm) on the plate. The servo only turns; it does not carry the weight sideways. This design keeps the cable channel in the mast free.
- **Tilt (nod):** the second MG996R sits **inside the head** at the right-hand end. Its horn is screwed to the yoke arm (4 x M3 x 10 from the outside). A **printed bush and one M5 x 30 bolt** are the other pivot on the opposite side. The tilt axis passes near the head's balance point (3 mm behind the middle, 8 mm above).
- **Clearance:** the head's lower corner swings on a 70.8 mm radius, 4.7 mm above the pan servo's top at every tilt angle. This is why the axis is 102 mm above the turntable (parameter `neck_axis_above_tt`, calculated).
- **Torque check (A, my calculation):** servo stall torque about 0.92 N·m at 4.8 V and 1.08 N·m at 6 V (9.4 and 11 kg·cm are the usual datasheet numbers; the 6 V servo buck is set to 5.0 V in your power file).

| | Static (balance error) | Moving | Friction | **Need** | Servo has | Load |
|---|---|---|---|---|---|---|
| Tilt, balance point 10 mm off | 0.063 N·m | 0.021 N·m (30 degrees in 0.3 s) | 0.02 N·m | **0.10 N·m** | 0.92 N·m | **11 %** |
| Tilt, balance point 25 mm off (heavy webcam) | 0.157 N·m | 0.021 | 0.02 | **0.20 N·m** | 0.92 N·m | 22 % |
| Pan (turn 90 degrees in 1 s) | none | 0.017 N·m | 0.083 N·m (glide ring) | **0.10 N·m** | 0.92 N·m | 11 % |

Both servos are fine. One warning: **do not force the head by hand while powered**; 10 N at the screen is 1 N·m, which can strip servo gears.

### 7.4 INTERFACE: how to swap in your own pan/tilt design

Two clearly marked interfaces. Their numbers are at the top of `robot2_params.scad` (section "PAN / TILT") and the file `pan_tilt_interface.scad` starts with a comment block that says the same.

| | Where | Default (A) | Variables |
|---|---|---|---|
| **INTERFACE 1** | the round **mast-top plate** (red in the pictures), 100 mm round, 9 mm thick | **4 x M4 holes, 60 x 40 mm pattern**, cable slot 38 x 12.5 mm beside the middle, socket for the mast shells below | `if1_bolt_dx`, `if1_bolt_dy`, `if1_bolt_d`, `if1_slot_w`, `if1_slot_h` |
| **INTERFACE 2** | a **pad on the back of the head lid** | **4 x M3 inserts, 60 x 40 mm pattern**, pad 76 x 56 x 4 mm | `if2_bolt_dx`, `if2_bolt_dy`, `if2_bolt_d` |
| Servo horn | pan: top of the plate. Tilt: inner face of the yoke arm | 25T aluminium disc horn, 20 mm disc, 4 x M3 on a 14 mm circle (V) | `horn_d`, `horn_pcd`, `horn_hole`, `horn_t` |

**To use your design:** print only `neck_plate` (and the mast, head, base). Do not print `turntable`, `yoke_servo_side`, `yoke_plain_side`, `pivot_bush`. Bolt your pan/tilt base to INTERFACE 1 and your tilt output (platform or bracket) to INTERFACE 2 on the head lid.

**Please send me these dimensions (a photo with a ruler is enough):**

1. **Base mounting:** screw size, **hole spacing (x and y)** or bolt-circle diameter, and the outline of the base plate (width x depth). Where is the **pan axis** relative to the holes?
2. **Height** from the base plate's bottom face to the **tilt axis** (mm), and how far forward or back the tilt axis is from the pan axis.
3. **Tilt output:** either (a) the **gap between two arms** and the **diameter of the pivot hole**, or (b) a **platform plate**: its size and the **screw pattern** (screw size, spacing).
4. **Servo models** and the **angles** they give for pan and tilt. Which servo carries the weight?
5. **Cable path:** is there a hollow shaft or a slot? Size of the slot in mm.
6. **Mass** of the whole unit in grams.
7. A **photo, STEP or STL** of the design if you have it. With an STL I can drop it into `assembly.scad` and check collisions.

If his head hangs between two arms like mine, tell me the arm spacing and I move the head pivots. If it screws on a platform from behind, INTERFACE 2 is already the fix.

---

## 8. Weight, balance point and tip-over

### 8.1 Mass and balance point (the numbers come from the real CAD volumes)

Printed parts: volume of every printed part from the STL x 1.27 g/cm3 (PETG) x a fill factor (0.45 to 0.9 depending on wall thickness; plates 0.5, thin walls 0.8). Expect **plus or minus 20 %**; weigh the real parts and tell me. Bought parts: my assumptions (A) unless marked (V).

| Group | Mass | Balance point of the group (x, y, z mm) |
|---|---|---|
| **Base** (printed 625 g, bought 800 g, wiring and screws 105 g) | **1529 g** | (-0.3, -0.4, 45.8) |
| **Mast** (shells, collars, foot, cables, screws) | **229 g** | (62, -3.5, 178) |
| **Head and neck** (screen, head shell, lid, yoke, servos, webcam, cables) | **833 g** | (66, 3.5, 394.7) |
| **Whole robot** | **2591 g** | **(26.5, 0.6, 169.7)** |

Biggest items:

| Item | g | z of its balance point (mm) | Source |
|---|---|---|---|
| Tray (4 pieces) | 267 | 25 | printed |
| 7 inch screen with driver | 230 | 408 | your request (200 to 250 g) |
| Gearmotors x2 | 180 | 33 | V Pololu page: about 90 g each |
| Cover (4 pieces) | 161 | 99 | printed |
| Deck (4 pieces) | 135 | 71 | printed |
| Head shell | 127 | 426 | printed |
| Battery 2 x 18650 + holder | 115 | 26 | A |
| XL4016 x2 | 110 | 26 | A |
| Yoke (2 pieces) | 95 | 353 | printed |
| Wheels x2, wiring, tilt servo, webcam | 60 each | | A |
| Pan servo | 55 | 326 | V (55 g) |
| SBC with cooler | 56 | 78 | A |

**The robot is 2.6 kg, above the 1.5 to 2 kg you asked for.** The printed discs are heavy. Ways to save 150 to 250 g (changes in `base.scad`): cover top 1.6 mm instead of 2.4 mm, cut big windows in the deck, print at 10 % infill with 3 walls, skip the speaker, use a single XL4016 if you skip the SBC buck. None of these is needed for the motors to work.

### 8.2 Tip-over (my calculation from the table above, A)

Support points: wheels at (0, +-117), caster at (104, 0), four feet at (95, +-58) and (-85, +-85). The balance point is at x = +26.5 mm, 169.7 mm high. The feet are 4 mm above the floor, so they take weight after about **2 degrees** of tilt.

| Direction | Distance from balance point to the tipping edge | Static tilt angle before it tips | Push at head centre (412 mm) that tips it |
|---|---|---|---|
| Forward (nose down a slope) | 77 mm | **24.5 degrees** | 4.8 N |
| Backward (nose up a slope) | 112 mm with feet (only **26 mm** without feet) | **33 degrees** (9 degrees without feet) | 6.9 N |
| Sideways | 100 mm | **30.5 degrees** | 6.2 N |
| **Worst direction** (about 8 degrees off forward, over the front corner) | 76.5 mm | **24.3 degrees** | **4.7 N** |

**Push test explained.** A push F at height h tips the robot when F x h is bigger than weight x distance. At the head centre 412 mm this is **4.7 N in the worst direction** (about 0.5 kg of force, about a gentle push with one hand). The wheel grip against sliding sideways is about 12 N, so the robot **tips before it slides**. Braking: the robot tips if it brakes harder than **4.5 m/s2** (a normal stop is below 0.5).

![stability](../3d/renders/robot2-stability.png)

**Mast height comparison (head axis above the floor):**

| Variant | Mass | Balance height | Worst static tilt (without feet) | Smallest tipping push at head centre | Sideways push |
|---|---|---|---|---|---|
| Short, axis **340 mm** | 2.51 kg | 141 mm | 28.9 degrees (10) | 5.7 N | 7.4 N |
| **Default, axis 420 mm** | 2.59 kg | 170 mm | 24.3 degrees (9) | **4.7 N** | 6.2 N |
| Tall, axis 500 mm | 2.68 kg | 199 mm | 20.7 degrees (8) | 4.0 N | 5.3 N |
| Default + 400 g steel ballast in the tray | 2.99 kg | 150 mm | 27.7 degrees (9) | 5.6 N | 7.2 N |
| 10.1 inch head (+0.55 kg), axis 420 mm | 3.14 kg | 212 mm | 17.8 degrees (9) | 5.1 N | 7.1 N |

**Why 420 mm.** A sofa seat is about 40 to 45 cm high, a table about 75 cm. With the screen centre at 412 mm and the camera at 485 mm, the camera sees a person sitting on a sofa from slightly below (tilt up to +35 degrees covers a face at 1.1 m from 2 m away: about 17 degrees up). On a table top, the camera ends up at about eye height of a seated person (75 + 48.5 = 123 cm).

**Is the default stable enough? My honest answer:** it is a **tall and light-headed robot** on a 26 cm base. It is fine for adults and a calm room. In a home with young children or a dog, **use the 340 mm mast and the ballast** (each adds about 1 N to the tipping push). To build the 340 mm version, change one line, `head_axis_h = 340;` in `robot2_params.scad`, and re-export; the mast, neck and heights follow automatically (I tested this: the mast shells become 67 mm each).

**What else helps.**
1. The motherboard has a gyro (GY-521). The software can **stop the motors and hold when the tilt is bigger than 8 degrees**. This is a task for the software file.
2. Drive slowly near stairs; the cliff sensors are there for this.
3. Do the tip test yourself: put the robot on a table over a cushion and slowly tilt the base by hand. It should tip at about 24 degrees. If it tips much earlier, a part (the cells, the SBC) is heavier than I assumed, or the head is.

---

## 9. Print list

All parts are **PETG** (strong, does not creep in a warm room or car; PLA softens at about 55 degrees C and may bend in a summer suitcase). Parts are already **turned into their printing position** in the STL files (lowest point on z = 0). Times are rough (A): 0.4 mm nozzle, 0.2 mm layers, 4 walls, 15 to 20 % gyroid infill, an ordinary 60 mm/s printer. A fast printer can be twice as quick. **Total about 1.1 kg of plastic (plan on 1.5 kg of filament with brim and waste) and about 44 hours.**

**Largest part:** `deck_FL` and `cover_FL` **178 x 138 mm**, `tray_FL` 178 x 133 x 56 mm, `head_shell` 150 x 174 x 42 mm, `head_lid` 150 x 174 x 6 mm, `yoke_*` 46 x 77 x **125 mm tall**. So you need a bed of at least **180 x 180 mm** (very tight; use a skirt, not a wide brim) and a print height of 130 mm. **200 x 200 mm is comfortable; 220 x 220 mm is easy.** Please tell me the printer.

For parts with the same name ending: FL = front left, FR = front right, RL = rear left, RR = rear right (robot's left is +y).

| STL file (`3d/stl/`) | Qty | Size mm (x, y, z) | About g | About time | Orientation | Supports |
|---|---|---|---|---|---|---|
| `tray_FL` | 1 | 178 x 133 x 56 | 92 | 3 h 10 | floor down, rim and posts up | none (use a small brim: posts are tall) |
| `tray_FR` | 1 | 178 x 125 x 56 | 90 | 3 h 05 | same | none |
| `tray_RL` | 1 | 90 x 131 x 56 | 42 | 1 h 35 | same | none |
| `tray_RR` | 1 | 90 x 123 x 56 | 42 | 1 h 30 | same | none |
| `deck_FL` | 1 | 178 x 138 x 35 | 47 | 1 h 45 | flat, standoffs up | none |
| `deck_FR` | 1 | 178 x 130 x 35 | 46 | 1 h 40 | same | none |
| `deck_RL` | 1 | 90 x 131 x 35 | 22 | 55 min | same | none |
| `deck_RR` | 1 | 90 x 123 x 35 | 20 | 50 min | same | none |
| `cover_FL` | 1 | 178 x 138 x 33 | 54 | 1 h 55 | **upside down**: top plate on the bed | none |
| `cover_FR` | 1 | 178 x 130 x 33 | 53 | 1 h 55 | same | none |
| `cover_RL` | 1 | 90 x 131 x 33 | 27 | 1 h 05 | same | none |
| `cover_RR` | 1 | 90 x 123 x 33 | 27 | 1 h 05 | same | none |
| `caster_cup` | 1 | 38 x 38 x 14 | 9 | 30 min | flange down | none |
| `caster_ring` | 1 | 28 x 28 x 2 | 1 | 15 min | flat | none |
| `motor_cap` | 4 | 40 x 12 x 16 | 5 | 20 min each | flat top down | none |
| `skid` | 4 | 14 x 14 x 8 | 1 | 15 min each | as is | none |
| `bumper_R` / `bumper_L` | 1 each | 88 x 75 x 16 | 10 | 30 min each | standing | none |
| `bumper_C` | 1 | 16 x 114 x 16 | 8 | 30 min | standing | none |
| `foot_plate` | 1 | 70 x 84 x 22 | 19 | 50 min | plate down, socket up | none |
| `mast_lo_front`, `mast_lo_back` | 1 each | 107 x 56 x 24 | 31 / 30 | 1 h 10 each | lying on the outer back face, open side up | none |
| `mast_up_front`, `mast_up_back` | 1 each | 107 x 56 x 24 | 31 / 30 | 1 h 10 each | same | none |
| `collar_front`, `collar_back` | 1 each | 25 x 77 x 40 | 17 | 45 min each | standing | none |
| `neck_plate` (INTERFACE 1) | 1 | 100 x 100 x 25 | 42 | 1 h 30 | top face down, socket up | none |
| `turntable` | 1 | 92 x 92 x 16 | 20 | 50 min | top face down, skirt up | none |
| `yoke_servo_side` | 1 | 46 x 77 x 125 | 47 | 1 h 40 | bar flat, arm standing | none (brim) |
| `yoke_plain_side` | 1 | 46 x 77 x 125 | 48 | 1 h 40 | same | none |
| `head_shell` | 1 | 150 x 174 x 42 | 127 | 4 h 15 | **front face down** | none; if the 41 mm bridge over the servo window sags, add a support only there |
| `head_lid` | 1 | 150 x 174 x 6 | 53 | 1 h 55 | pad side down | none |
| `pivot_bush` | 1 | 14 x 14 x 9 | 1 | 15 min | as is | none |

**Tips.** Print the base quarters first and dry-fit them (dovetails need 0.25 mm of play; if they are too tight on your printer sand them). Use 5 walls for `yoke_*`, `neck_plate`, `turntable`, `foot_plate`, `caster_cup`, `motor_cap`. A fixed brim on `tray_*` stops the tall posts from tearing off. Print `mast_*` halves with a good cooling fan: the nut pockets are small.

![print parts](../3d/renders/robot2-print-parts.png)

---

## 10. Hardware list (screws, nuts, inserts, small parts)

Counts for the default design. Buy 20 % spare screws and inserts.

| Item | Count | Where used |
|---|---|---|
| **M3 heat-set inserts** (5.7 mm long brass, hole 4.0 mm) | **37** | 6 tray posts, 4 cover posts, 4 board standoffs, 8 motor saddles, 3 caster cup, 8 yoke bars, 4 head corners |
| M3 heat-set inserts, extra for INTERFACE 2 only if you use your own pan/tilt | (4) | head lid pad |
| **M4 heat-set inserts** (hole 5.6 mm) | **8** | 4 deck pads (mast foot), 4 turntable (pan servo ears) |
| Screw M3 x 6 (self-tapping into plastic) | 4 | cliff sensors |
| Screw M3 x 8 | 12 | head lid 4, motherboard 4, cover top 4 (countersunk) |
| Screw M3 x 10 | 24 | deck to tray posts 6, caster flange 3, caster ring 3, yoke to turntable 8, tilt horn 4 |
| Screw M3 x 12 | 4 | mast sockets (2 at the foot, 2 at the neck) |
| Screw M3 x 14 | 4 | pan horn (from below) |
| Screw M3 x 16 | 4 | anti-tip feet |
| Screw M3 x 20 | 12 | motor caps 8, collars 4 |
| **Nut M3** | **15** | caster flange 3, feet 4, mast sockets 4 (captive in the shells), collar 4 |
| Screw M4 x 10 | 8 | mast foot 4, pan servo ears 4 |
| Screw M4 x 14 | 4 | tilt servo ears (from inside the head) |
| Nut M4 | 4 | tilt servo ears (in the outer wall pockets) |
| Bolt M5 x 30, lock nut M5, 2 washers M5 | 1 set | head pivot (opposite the tilt servo) |
| Screw M2.5 x 6 | 4 | SBC |
| Aluminium servo horn, 25T, 20 mm disc, 4 x M3 threaded | 2 | pan and tilt (the horns' own centre screws are used) |
| Steel ball 16 mm (or 5/8 in) | 1 | caster |
| PTFE tape or Teflon tape, 0.2 mm adhesive | 1 small roll | glide ring on the plate |
| Micro switch with lever (KW12-3 type), optional | 2 | bumper |
| Zip ties 2.5 x 100 mm | about 25 | modules, cables |
| Double-sided foam tape | 1 roll | modules, screen, camera |
| Cyanoacrylate glue (superglue) or 2-part epoxy | 1 | tray, deck, cover and bumper seams |
| Foam pads (about 3 mm) | few | screen retention |

**Bought mechanical parts, with about prices (A: please check on the day).**

| Part | About price | Where to look |
|---|---|---|
| 2 x Pololu 25D MP 12 V 47:1 gearmotor | about 50 to 60 EUR | pololu.com (ships to Germany), or an EU reseller. **Buy in Germany before the trip.** |
| 2 x 65 mm rubber wheels with 4 mm D hub | about 8 to 12 EUR | robot shops, Amazon.de, eBay |
| 7 inch HDMI screen (Waveshare-type) | about 50 to 75 EUR | Eckstein-Komponenten, Berrybase, Reichelt |
| 2 x servo extension cable 50 cm | about 4 EUR | any |
| Flat slim HDMI cable micro-HDMI to HDMI-A, 60 to 80 cm | about 10 to 15 EUR | Amazon.de, Reichelt (see `sbc-selection.md` for the plug type) |
| 2 x 25T aluminium horn | about 6 to 8 EUR | Amazon.de, AliExpress |
| Heat-set inserts M3/M4 assortment | about 8 to 12 EUR | Amazon.de |
| Screws, nuts assortment M2.5/M3/M4/M5 | about 12 to 18 EUR | Amazon.de, Reichelt |
| Steel ball, PTFE tape, zip ties, foam tape, glue | about 10 EUR | hardware store |
| PETG filament 1.5 kg | about 35 to 45 EUR | any |
| **Total mechanical parts (without SBC and electronics)** | **about 190 to 250 EUR** | |

Easy to buy anywhere: screws, nuts, zip ties, tape, glue. Hard to find or slow: the Pololu motors, 25T aluminium horns, heat-set inserts. **Luggage:** the pack and cells go in carry-on only (see the brief); printed parts, motors, screws, the steel ball are fine in checked luggage. The printed base pieces stack into about 30 x 25 x 20 cm.

---

## 11. Assembly steps

Tools: soldering iron (for inserts), small screwdrivers and hex keys, hobby knife, multimeter, side cutters. Do the electrical steps with the wiring file open.

1. **Check the parts.** Dry-fit the base quarters. Sand burrs from the dovetails. Weigh two printed parts and compare with section 8.
2. **Heat-set inserts.** Melt them in with the soldering iron tip set to about 220 degrees C, straight and flush (section 10 list). Do the tray posts, saddles, cup, deck standoffs and posts, yoke bars, head corners, deck pads, turntable.
3. **Glue the quarters:** tray, deck and cover each. Put CA glue or epoxy on the dovetails, press together on a flat table, clamp with tape for a day.
4. **Tray, drive side.** Fit each motor in its saddle, fit the caps (M3 x 20). Fit the wheels on the 4 mm shafts and check they clear the rim window. Mount the caster cup (3 x M3 x 10 + nuts from below), drop in the ball, fix the ring (3 x M3 x 10). Mount the four feet (M3 x 16, nut in the pocket on the floor). Check that the base sits level on the wheel, the ball and later the feet at 4 mm.
5. **Tray, sensors and bumper.** Press the two sonar boards into the cheeks behind the holes; fix the cliff sensors on their bosses; glue the three bumper pieces, slide the arms through the rim slots, add the micro switches.
6. **Lower electronics.** Pack in the cradle, BMS, charger board (USB-C socket in line with the rear window), main switch in the 19 mm hole, fuse holders, lever connectors, bucks, all with foam tape and zip ties. **Do the first power-up steps from `pcb/kicad/shopping-list.md` now**, with the deck still off: set each buck with a multimeter, check nothing is hot.
7. **Deck.** Lay the wires up through the deck slots; screw the deck to the 6 tray posts (M3 x 10). Mount the motherboard (4 x M3 x 8) with the **ESP32 USB-C toward the SBC**, insert the DRV8833 modules **after** the first power test and check the white-plug bar. Mount the SBC (4 x M2.5 x 6).
8. **Mast foot.** Screw the foot plate to the deck pads with 4 x M4 x 10.
9. **Neck on the bench.** Screw the aluminium horn to the neck plate from below (4 x M3 x 14), tape the PTFE ring on the plate, fit the horn on the pan servo (centre servo to 90 degrees first), put the turntable over it, screw the servo ears to the turntable (4 x M4 x 10), screw the two yoke halves to the turntable (8 x M3 x 10). Power the pan servo from a servo tester and check that the turntable turns freely.
10. **Head.** Press in the screen with foam tape, put the webcam in the brow (lens against the window), mount the tilt servo (4 x M4 x 14 from inside, nuts in the outer pockets), fit its horn and screw the horn to the yoke arm (4 x M3 x 10) and fit the M5 pivot with the bush on the other side. Close the lid (4 x M3 x 8).
11. **Mast and cables.** Lay the cables into the lower half shells, close them over the foot socket with the two M3 x 12 screws, add the collar, lay the upper shells, push them into the neck socket. Thread the cables through the plate slot, turntable slot, and head slot, leave 100 mm loop, secure with zip ties.
12. **Cover.** Fit the cover with 4 screws M3 x 8. Check the vent slots are free.
13. **Test.** Wheels off the table: drive each motor, check direction. Sweep pan and tilt slowly to the limits. Tip test on a cushion (section 8). Wiggle the mast. Leave the SBC call test (`sbc-selection.md` section 10) for the end.

---

## 12. Files

| File | What it is |
|---|---|
| `3d/robot2_params.scad` | **all numbers in one place** (sizes, heights, hole patterns, the two INTERFACES) |
| `3d/robot2_ghosts.scad` | simple models of the bought parts (for pictures and fit checks) |
| `3d/base.scad` | tray, deck, cover, caster, motor caps, feet, bumper |
| `3d/mast.scad` | mast half shells, collar, foot plate |
| `3d/pan_tilt_interface.scad` | **INTERFACE 1 plate**, turntable, yoke (the replaceable part) |
| `3d/head.scad` | head shell, lid (with INTERFACE 2 pad), pivot bush |
| `3d/assembly.scad` | the whole robot together |
| `3d/print_parts.scad` | every printed part in its printing position (used for the STL files) |
| `3d/stl/` | 33 STL files, ready to slice |
| `3d/renders/` | the pictures in section 2 |

**To change a number and make new STL files.** Install OpenSCAD (free). Open `3d/robot2_params.scad` in a text editor, change the number (for example `head_axis_h = 340;`), save. To make one STL file, open a terminal in the `3d` folder and type (this tells OpenSCAD to set the part name and write the file):

```
openscad -D 'part="head_shell"' -o stl/head_shell.stl print_parts.scad
```

Every file also compiles on its own and shows its part, so you can look at any file in OpenSCAD with the preview button. **Note:** the preview window can draw the half-shell mast wrongly (a known OpenSCAD preview quirk). Press the render button (F6) to see it right; the STL export is always correct. I tested every file with OpenSCAD 2021.01: all compile and export without warnings, and all 33 print parts are single closed bodies.

---

## 13. What is verified and what is assumed

**Verified (V):** board size, hole pattern and connector sides (files in `pcb/kicad/`); MG996R body size 40.7 x 19.7 x 42.9 mm and 55 g, 25-tooth spline (shop listings); 25T aluminium horn 20 mm disc, 4 x M3 on a 14 mm circle (shop listings); HC-SR04 45 x 20 x 15 mm with 16 mm transducers (shop listings); Waveshare 7 inch HDMI LCD (C) 164.90 x 106.96 x 8 mm, visible 154.21 x 85.92 mm (shop wiki text, I could not open the page); Pololu 25D LP 47:1 (120 rpm, 0.9 A, 4.8 kg·cm) and MP 47:1 (170 rpm, 1.8 A stall) at 12 V; TT motor figures (shop copies of Adafruit's data); ELEGOO Conqueror size and weight (shop listings); Pi 5 Active Cooler 63.5 x 42.5 x 13.7 mm.

**Assumed (A, check these):**
1. All **bought module sizes** in section 5.3 (battery holder, BMS, charger, bucks, fuses, Wago, switch) and the sonar hole pitch 26 mm and the cliff module.
2. The **MG996R ear and shaft numbers** (ear spacing 49.5 mm, ear plane 10 mm below the output face, shaft 10.2 mm from the case end) and the horn position. Dry-fit before you print the turntable and head.
3. **Webcam size** 60 x 30 x 28 mm; **speaker** 40 mm.
4. **Printed masses** (fill factors) and **printing times**; weigh and tell me.
5. **Rolling resistance 0.10** on carpet, wheel width 26 mm, 4 mm D-shaft on the Pololu motor; MP 47:1 stall torque estimate.
6. **Mast joint strength** (collar friction); **dovetail fit** (0.25 mm clearance); the **41 mm bridge** over the servo window.
7. **Prices** in EUR.

---

## 14. Risks and open points

1. **Tippy.** 4.7 N tips it (section 8). Short mast and ballast help; software tilt guard recommended.
2. **Mass 2.6 kg** is above the target. Motors are sized for 3 kg; trims in section 8.1.
3. **Pololu motors are not a German shop item.** Order early (two to three weeks from the US, A). Back-up: a generic 25GA-370 that lists 4 kg·cm stall torque at 12 V, test first.
4. **Real servo and webcam sizes** may differ from my assumed numbers; every one is a parameter and needs a re-print of one or two parts.
5. **The HDMI plug may not fit the neck slot.** Fix: thread it from the head end.
6. **Heat inside the base:** two XL4016 modules and a Pi 5 under a closed cover. The cover has vent slots, but run the 30 minute call test (`sbc-selection.md`) with the cover on and check the temperatures.
7. **Dovetail glue joints** are only as strong as the glue; the screws through the deck posts hold the layers together.
8. **I did not test anything in the real world.** All pictures and numbers come from CAD and calculation. A paper-and-cardboard test of the footprints before printing is cheap: print `robot2_params.scad` (it makes a 100 x 100 mm plate with the 4 board holes) to check your printer's accuracy, then lay your real modules on the printed tray quarter.
