# Robot motherboard - routed draft v5, 2 layers, 100 x 100 mm

**Status: DRAFT. Do not order yet.** v5 is built from the owner's paper test-fits, photos and readings of the real modules. It is fully
routed and passes every check I could run on the files. Before ordering: print the new template, check the two DRV8833 modules
and a screen cable against it (see "Still to confirm"), and read the independent-review notes below.

## What changed in v5

- **DRV8833 (HW-627) footprints redrawn: two rows of 6 holes**, as read from the real module. Top row, left to right: IN1 IN2 VCC GND IN3 IN4
  (VCC is the motor supply = the battery). Bottom row, the side with the white plug: EEP OUT1 OUT2 OUT3 OUT4 ULT (EEP and ULT are not used).
  The pin names are printed beside the holes. M1 = DRV A OUT1+OUT2, M2 = DRV A OUT3+OUT4, M3/M4 = the same for DRV B.
  Note: the owner's own wording listed the IN row as "IN4 IN3 GND VCC IN2 IN1"; I drew it in the opposite direction (IN1 IN2 VCC GND IN3 IN4),
  assuming each row was read upright from its own edge, which also matches the seller's pin table. A thick silkscreen bar marks the plug side.
- **Screen headers follow the screens' own order:** CS DC RST SDA SCL VCC GND (pin 1 = square pad = CS).
- **Capacitor ratings are printed on the board** (C1 470uF 16V, C2 100uF 10V, C3/C4 100n) and listed in `parts-list.md`.
- **Plotted board size is exactly 100.0 x 100.0 mm** (the outline line used to add 0.1 mm). The fab cuts along the middle of that 0.1 mm line, so the finished board is
  99.9 x 99.9 mm; the mounting holes do not move. This keeps it inside the cheapest price tier.
- **30 ground stitching vias** tie the top and bottom ground pours together (the farthest spot from a tie is now about 12 mm instead of 37 mm).
- The relay/sonar and I2C/UART header strips have 3.0 mm between neighbouring headers (the screen and SPARE strip at the top is tighter: use slim plugs there),
  the labels on the top header row moved away from the pads and the board edge, version text says v5.
- New files: `shopping-list.md` (everything to buy, including the parts that are not on the board) and `stitch_ground.py`.

Carried over from v4: four 5.08 mm left-edge screw terminals (SERVO 5V IN, BATT IN, CLEAN 5V IN, 3.3V IN), the POWER OUT header
(2 x clean 5 V, 2 x 3.3 V from the 3.3 V buck, 4 x GND), 2-pin JST-style motor spots M1-M4, no series resistors on the relay inputs
(3 V relay modules have their own input circuit), sonar echo dividers 1k/2k (ESP32-S3 pins are not 5 V tolerant).

## How to wire the power

The three bucks are separate modules (not on the board). Each one has an input pair (IN+ / IN-) and an output pair (OUT+ / OUT-).

```
battery pack -> BMS -> main switch -> splice (lever connectors, one for + and one for -; 6-way if the Pi buck is used), one FUSE per branch:
     |-> board terminal BATT IN        (motors; 5 A slow-blow, 6 A at most: the board's 2 mm battery copper is a roughly 6 A design)
     |-> servo buck IN+/IN-  (5 A fuse)  its OUT+/OUT- go to the board terminal SERVO 5V IN   (-> PCA9685 V+ pin)
     |-> clean 5V buck IN+/IN-  (2 A fuse)  its OUT+/OUT- go to the board terminal CLEAN 5V IN   (-> ESP32 5V pin via diode D1, both sonars, POWER OUT 5V pins)
     |-> 3.3V buck IN+/IN-  (2 A fuse)   its OUT+/OUT- go to the board terminal 3.3V IN       (-> relays, screens, POWER OUT 3V3 pins)
     '-> (optional) Raspberry Pi 5: own 5.1 V buck, 5 A fuse, straight to the Pi. It does not touch the board.
```

**+** is the square pad of each terminal. All **-** terminals and all GND pins are one common ground. Before connecting a buck to the board,
power it from the battery alone and set its output with a multimeter (servo buck 5.0 V, clean buck 5.0 V, 3.3 V buck 3.3 V).
The board has no fuse and no reverse-polarity protection. Each POWER OUT rail (two pins) shares one 0.5 mm track: the copper is good for about 2 A,
but the buck also feeds the ESP32, sonars, relays and screens, so plan on about **1 A** for your own sensors. Do not connect one sensor to both the
POWER OUT 3V3 pins (3.3 V buck) and the I2C / SPARE 3V3 pins (the ESP32's own pin): they are different sources. The ESP32
reaches 5 V through D1 and its own diode, so check on first power-up that its 3.3 V pin stays at 3.2 V or higher with Wi-Fi transmitting.

## What is here

| File | What it is |
|---|---|
| `board-top.png` | what the finished board will look like from above |
| `board-copper.png` | both copper layers |
| `fit-template-1to1.pdf` | **print at 100 % / actual size** and lay your modules on it (the 50 mm ruler must measure 50 mm) |
| `abadi-motherboard.kicad_pcb` + `.kicad_pro` | the board in KiCad 7 (keep both files together: the .kicad_pro holds the design rules) |
| `gerber/` and `abadi-motherboard-2layer-gerber.zip` | the fab files (this zip is what you upload to the PCB maker) |
| `pin-table.md` | which ESP32 pin carries which signal, and every connector's pin order |
| `parts-list.md` | what to buy for every footprint, with ratings |
| `shopping-list.md` | everything to buy, on and off the board, plus the first power-up steps |
| `reports/` | KiCad's design-rule report and my independent check of the Gerber files |

## Still to confirm (paper test-fit with the new template)

1. **DRV8833 row gap.** The two rows of holes are drawn 16.0 mm apart (estimated from a photo). Measure the real distance between the
   centres of the two rows and tell me; it moves by a fraction of a millimetre at most, but the pins must fall in the holes.
2. **DRV8833 alignment.** I assumed EEP sits directly across from IN1 (and ULT across from IN4), which matches the seller's pin table.
   Check on the real module. If EEP is across from IN4, the two rows are mirrored and I must redraw them.
3. **Screen cable.** Pin 1 of each screen header is CS. Check against the pin labels printed on your screen.
4. **Compare every printed name with the module's own labels, pin by pin, not just whether the pins fall in the holes.** With the white plug
   toward the bottom edge, the IN row (top) must read IN1 IN2 VCC GND IN3 IN4 from the left, and the module's VCC must be the pin over the
   printed "VCC". VCC and GND are next to each other: a mirrored module would put the battery on its ground pin.
5. On the real module, with a meter: is EEP already tied high? If the motors do not run, EEP (sleep) needs a wire to 3.3 V. The owner says EEP and ULT are not needed.
   The PCA9685's OE pin is left open (the module normally pulls it low).
6. Also lay down the ESP32 (USB-C to the right), PCA9685 (header at the left end), gyro, a sonar cable and a screw terminal.

## What was checked

- KiCad design-rule check: **0 errors, 0 unconnected pads.** (38 notes say the footprints are not from a KiCad library; they are
  drawn in code, so that is expected and harmless.)
- A separate checker I wrote reads only the exported Gerber and drill files, rebuilds which copper touches which, and compares with the
  intended nets: **0 shorts, 0 opens**, all 211 plated holes (pads and vias) match the design (the 4 mounting holes are in a separate unplated file).
  Smallest copper gap 0.152 mm, narrowest track 0.25 mm, smallest drill 0.30 mm, copper at least 0.5 mm from the edge.
- Independent reviewers (separate agents, v4 design): netlist and pin tables (0 mismatches), grounding (all 32 ground pads are one
  connected piece; motor-return resistance about 1 mOhm), fab files, silkscreen, documents, electrical safety. They found the DRV8833 and
  screen mismatches, the missing capacitor ratings and the 100.1 mm size; those are fixed here. The v5 changes (DRV, screens,
  stitching vias) have been checked by KiCad and the Gerber audit; see `reports/` for the latest numbers.

## What is NOT checked

1. **Module pin orders** other than those listed above as read from the owner's modules: the relay (VCC IN GND), sonar (VCC TRIG ECHO GND),
   GY-521 and PCA9685 match the owner's photos and the usual orders; the I2C and UART headers have no module behind them.
2. The ESP32 pin map is my optimized proposal. `plan.md` and `wiring.md` are **not** updated, and their locked pin table still
   describes the old build. SPARE IO pins 3, 45, 46 are boot-strapping pins (46 is input-only) and 38/48 drive the devkit's RGB LED.
3. No schematic and no electrical simulation. The netlist lives in `build_board.py`.
4. Current limits (1 oz copper): VBAT copper is 2.0 mm (a roughly 6 A design), SERVO5 1.5 mm, motor traces 1.0 mm, CLEAN5 / RAILC 0.5 mm. A PCA9685 header
   pin is good for roughly 2-3 A: for big servos also use the module's own screw terminal. Nothing is tested under load.
5. **The ESP32 board only fits one way round:** the USB-C end toward the **right** edge, the antenna toward the left (marked on the board,
   with the two USB-C sockets drawn). Turned around, its 3V3 pins land on the GND pins. The first hole of each row (square pad) is the antenna end.
6. The PCA9685 has no mounting hole: it sits on its header pins. **A DRV8833 module pushed in 180 degrees rotated fits the holes** (the pattern is
   point-symmetric) and would put battery voltage on ESP32 pins GPIO1 / GPIO16 and its outputs on GND and VBAT. Check the thick plug-side bar and
   "white plug v" before every insertion, and insert the DRV modules only after the first power-up test.
   The UART header is the ESP32's console UART (GPIO43/44): it receives boot text, so unplug it while flashing.
7. The power-track widths (VBAT 2.0, SERVO5 1.5, motors 1.0, 5 V / 3.3 V 0.5 mm) exist only in the routed copper, not as rules in the .kicad_pro;
   keep them if you edit the board.
8. The I2C bus has no pull-up resistors on the board; it relies on the PCA9685 and GY-521 modules' own.

## Paper test-fit (10 minutes, free)

Print `fit-template-1to1.pdf` at 100 %. Check the 50 mm ruler. Lay each module on the sheet: its pins should fall in the holes, its body
inside the printed outline. Check polarity marks on the terminals (+ is the square pad) against your wiring. Tell me anything that does not line up.

## Ordering (when the test-fit passes)

JLCPCB, 2 layers, 100 x 100 mm, 5 pieces, 1.6 mm, any solder-mask colour, bare board only (no assembly); HASL with lead is the cheapest
finish, lead-free costs a little more. Upload `abadi-motherboard-2layer-gerber.zip` as it is. JLCPCB's help page lists $2 for five 2-layer
boards up to 10 x 10 cm; shipping and German VAT are added at checkout. The preview must show 100 x 100 mm; the final price appears on their
quote page before you pay. The soldered parts are all through-hole, so assembly by the fab is not an option; buy the parts (see `shopping-list.md`).

## How it was made (to redo it after a change)

```
python3 build_board.py board.kicad_pcb --layers 2 --fine --pinmap     # parts, nets, outline, pours
python3 route_board.py board.kicad_pcb routed.kicad_pcb freerouting-2.0.1.jar 80
python3 stitch_ground.py routed.kicad_pcb stitched.kicad_pcb 30        # ground stitching vias (copy the .kicad_pro next to each file)
python3 finish_board.py stitched.kicad_pcb final.kicad_pcb              # silk size, pour refill, DRC report
kicad-cli pcb export gerbers ... ; kicad-cli pcb export drill ...        # fab files
python3 dump_board.py final.kicad_pcb design.json
python3 audit_kicad_gerbers.py gerber design.json                       # independent check
python3 render_board.py gerber pics ; python3 make_docs.py final.kicad_pcb docs   # pictures, template PDF, pin table, parts list
```

The delivered board has two small hand edits after routing (the 30 stitching vias, and a 0.14 mm dogleg in the RAILC trunk below RLY1H pad 1 to remove
a 0.03 mm slit), plus the silkscreen tweaks that are also in `build_board.py`. The auto-router gives a different result each time the board is rebuilt (even with the file name changed). Rebuild and re-route, or change
`HDR_GAP` slightly, until the report shows 0 unconnected and the audit shows no copper gap or slit below 0.14 mm. `assign_pins.py` re-optimizes which
ESP32 pin drives which signal. Needs KiCad 7 (python3 `pcbnew`), Java 21 and
[Freerouting 2.0.1](https://github.com/freerouting/freerouting/releases/tag/v2.0.1). The earlier `pcb/` files from Cursor (the 4-layer
105 x 84 mm draft) are superseded by this folder.
