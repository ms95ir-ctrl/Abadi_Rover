# Brief: robot 2, the telepresence robot (written from the owner's request)

The owner (a hobbyist in Germany, not comfortable with terminal or git shorthand) ordered 5 copies of the same 100 x 100 mm robot
motherboard (`pcb/kicad/`, version v5). Each board is meant for a different robot. Robot 1 is the "Abadi Rover" (see `plan.md`, `wiring.md`; do not
edit them). **Robot 2 is a telepresence robot**, built on the same motherboard.

## What the owner asked for (nearly verbatim)

- A small robot, similar to a famous round home robot that rolls around the house and does video calls (think Samsung Ballie / a telepresence robot).
  Family abroad can put it in their home and call whoever is at home, and the robot can drive around the house.
- The owner is going on vacation to his family abroad. His sister has the robot's equivalent in mind: he wants to take **one PCB** with him and
  **build the robot there**, so he can talk to her and drive the robot around her home afterwards from Germany.
- Same setup as robot 1: the ESP32-S3 on the motherboard drives **2 motors** and the **pan/tilt servos**. The difference: **one screen, an HDMI screen**, attached
  to a **single board computer (SBC)**. "The cheaper the better". Candidates he named: Raspberry Pi, Orange Pi Zero 2W, Radxa Cubie A7S (he wrote
  "Radexa QB A7S"), "or any cheap single board computer".
- Power is still the **2S Li-ion pack** (maybe even re-use the pack from robot 1). The motherboard has no SBC power output; the SBC gets its own buck.
- He has a **pan/tilt design from another Claude Code session** ("a perfect design"). It is NOT in this repository. The head (screen + camera) must carry it.
- Wanted deliverables: a full plan, a wiring diagram, a list of the robot's functions, a parts list, sketches of a 3D design (adjusting the pan/tilt
  for this head), the camera model, the wiring, and what has to be done in code. He is asleep while this runs: decide sensibly, flag assumptions.

## Fixed facts (do not contradict; read the files for details)

- Motherboard v5: `pcb/kicad/README.md`, `pcb/kicad/pin-table.md` (which ESP32 GPIO carries which signal), `pcb/kicad/parts-list.md`, `pcb/kicad/shopping-list.md`,
  `pcb/kicad/power-wiring.png` and `battery-wiring.png`, `pcb/kicad/build_board.py` (geometry).
  Board: 2 layers, 100 x 100 mm, 4 mounting holes M3 at (4,4) (96,4) (4,96) (96,96) mm from the lower-left corner (92 mm spacing).
  ESP32-S3 devkit (dual USB-C, N16R8) plugs in with USB-C toward the right edge. Two DRV8833 modules (HW-627) = 4 motor channels, 2-pin motor spots M1..M4
  (M1/M2 on DRV A, M3/M4 on DRV B); PCA9685 16-channel servo board on the board (servo plugs face the bottom edge); GY-521 gyro; 2 sonar headers (HC-SR04, 5 V
  with a 1k/2k echo divider on the board); 3 relay headers; 2 SPI screen headers (NOT used by robot 2: it has an HDMI screen instead); I2C sensor header
  (3V3 GND SDA SCL); UART header (GND TX RX = ESP32 GPIO43/44, the console UART); SPARE IO header (GND, 3V3, GPIO 3 46 45 48 38 21; 3/45/46 strapping, 46 input only, 38/48 RGB LED).
  Four left-edge 5.08 mm screw terminals: BATT IN (raw pack, motors), SERVO 5V IN (buck output, PCA9685 V+), CLEAN 5V IN (buck output: ESP32 5V via diode D1, sonars,
  POWER OUT 5 V pins), 3.3V IN (buck output: relays, screens, POWER OUT 3V3 pins). POWER OUT header: 2 x 5 V, 2 x 3.3 V, 4 x GND (about 1 A usable per rail).
- Power system: 2S Li-ion pack (6.0-8.4 V) -> 2S balancing BMS (HX-2S-JH20 type) -> USB-C charger board (IP2326, 5 V in, 8.4 V out) -> main switch -> splice -> one fuse per
  branch -> bucks: XL4016 module (servo 5 V), fixed 5 V 1.8 A (clean 5 V), fixed 3.3 V 2 A, and for a Raspberry Pi 5 a second XL4016 set to 5.1 V. BATT IN branch 5 A slow-blow
  (the board's 2 mm battery copper is a roughly 6 A design). The owner owns an XL4016, a 2 A 3.3 V fixed buck and a 1.8 A 5 V fixed buck, a BMS and the charger board.
- The owner already owns (for robot 1, may or may not be re-usable): USB webcam SC-012-SN259, MG996R / MZ996 servos, 1:48 TT-style geared motors, ELEGOO Conqueror tracked chassis,
  Raspberry Pi 5 8 GB, 5 V cooling fan, key switch, lots of old 18650 cells (must be matched pairs).
- Motors: the DRV8833 (HW-627) does 1.5 A continuous / 2 A peak per channel, 2.7-10.8 V. The ESP32 pins are 3.3 V only.
- Out of scope unless the owner asks: AI agent on the robot, turret, anything about robot 1's stages. Do NOT edit `plan.md`, `wiring.md` or anything under `pcb/`.

## Working rules

- Write for a hobbyist: short sentences, plain words, every abbreviation explained once. Tables are good. Prices in EUR for Germany; give a source link or the shop name; say when a price
  is an estimate. The owner will build the robot abroad (country not known yet): say what to buy in Germany before travelling and what is easy to buy anywhere.
  Li-ion cells and power banks go in carry-on luggage only (flag this).
- Be honest about uncertainty. Mark each key fact as VERIFIED (you saw it in a source or file) or ASSUMED. Never invent a part number or a price you did not see: say "about" and where to check.
- Write only into your own files under `telepresence/` (names given in your task). Do not run git. Scratch files go in the scratchpad folder you are told about, not in the repo.
- No application code is to be written now (the owner's rule: one stage at a time, no code for later stages). Plans, specs, tables, diagrams and CAD sketches only.
