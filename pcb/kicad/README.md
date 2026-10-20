# Robot motherboard - routed draft v4, 2 layers, 100 x 100 mm

**Status: DRAFT. Do not order yet.** v4 is built from a real paper test-fit (your photos and notes) and measured module
data. It is fully routed and passes every check I could run on the files. One more paper test-fit with the new
template is the last step before ordering.

## What changed in v4 (power wiring)

- **The three TO BUCK terminals are gone.** The three buck modules now get their battery power straight from the pack, outside the board
  (see "How to wire the power" below). The left edge has four terminals: SERVO 5V IN, BATT IN, CLEAN 5V IN, 3.3V IN.
- **The relay series resistors (330R) are gone.** The relay modules are 3 V types with their own input circuit, so each relay header's IN pin
  now goes straight to its ESP32 pin. (Set each module's high/low trigger jumper to match your code.)
- **More room:** the cable headers are spaced 3 mm apart instead of 1.9 mm, the I2C / UART headers moved up 2 mm to give space above the DRV8833 modules,
  and diode D1 moved to the right edge of the strip.
- **New POWER OUT header** (left edge, where the old terminals were): 2 x clean 5 V, 2 x 3.3 V (from the 3.3 V buck, not the ESP32's own pin)
  and 4 x GND, 2.54 mm pins, each power pin with a ground pin directly below it.

## How to wire the power

The three bucks are separate modules (not on the board). Each one has an input pair (IN+ / IN-) and an output pair (OUT+ / OUT-).

```
battery pack -> BMS -> FUSE -> splice (insulated lever connectors, one for + and one for -) ->
     |-> board terminal BATT IN        (the motors; DRV8833 modules take the battery voltage from here)
     |-> servo buck IN+/IN-            its OUT+/OUT- go to the board terminal SERVO 5V IN   (-> PCA9685 V+ pin)
     |-> clean 5V buck IN+/IN-         its OUT+/OUT- go to the board terminal CLEAN 5V IN   (-> ESP32 5V pin via diode D1, both sonars, POWER OUT 5V pins)
     '-> 3.3V buck IN+/IN-             its OUT+/OUT- go to the board terminal 3.3V IN       (-> relays, screens, POWER OUT 3V3 pins)
```

Terminal pairs: **+** is the square pad. All **-** terminals and all GND pins are one common ground. Before connecting a buck to the board,
power it from the battery alone and set its output with a multimeter (servo buck 5.0 V, clean buck 5.0 V, 3.3 V buck 3.3 V). The board has
no fuse and no reverse-polarity protection: use one fuse (10-15 A) in the battery + lead before the splice.

## What changed since v2 (from your test-fit notes)

| Your note | What I did |
|---|---|
| "3 mm displacement" (ESP32) | The ESP32's two pin rows are **25.4 mm** apart (measured from your photo and the listing drawing), not the 22.86 mm I assumed. Footprint rebuilt: 57 x 28 mm board, 22 + 22 pins at 2.54 mm, 6.3 x 18 mm antenna part with a no-copper zone under it, two USB-C marks. |
| "missing pin" (ESP32) | Same cause: your board sat 1.7 mm off along its length because my pin positions were wrong. Fixed by the rebuilt footprint. |
| "numbered GPIOs should be there" | The ESP32 pin numbers are printed beside both rows, and the SPARE IO header now has GPIO numbers above every pin. |
| Touch headers crossed out | Removed. |
| DRV8833 "perfectly fine" | Left exactly as it was. |
| PCA9685 circled holes | The PCA9685's control header is on a **short end** of the module (it has one at each end), not on the long edge. Footprint moved to the left short end. V+ is now wired to a new **SERVO 5V IN** terminal. |
| "should be 2 mm larger" near M1-M4 | My reading: terminal spacing should be 5.08 mm, not 3.5 mm. All screw terminals are now 5.08 mm. **Please confirm.** |

Added after an independent review of v3 (kept in v4):

- **Polarity and values are printed on the board:** `+` and a square pad on the two big capacitors (C1, C2), `A` / `K` and `1N5819` at the
  diode D1 (K = the band side = the ESP32 5V pin), and `1k` / `2k` under each sonar divider
  (swapped, the ESP32 would see only 1.7 V from the sonar and read nothing). The sonar divider is needed because the ESP32-S3's pins
  are not 5 V tolerant (maximum about 3.6 V) and the sonar's ECHO pin gives 5 V.
- **Every header now prints its pin functions** next to the pins (relay VCC IN GND, sonar VCC TRG ECH GND, screens VCC GND CS RST DC SDA SCL,
  I2C, UART; the spare IO header already showed its GPIO numbers). The DRV8833 holes have no labels yet: follow the pin-table.
- **The two screen headers are 2.54 mm apart** (v3 had them closer together than one pin).
- **The antenna keep-out is bigger:** no copper on either layer from 7 mm in front of the antenna tip and 4 mm beside it, so Wi-Fi/Bluetooth is not detuned.
- Floating scraps of ground copper are removed automatically.

Also fixed, found while reading your photos: the GY-521's pin order. The module reads INT AD0 XCL XDA SDA SCL GND VCC left to
right, so the board's holes now follow that order (v2 had VCC on the wrong end).

## What is here

| File | What it is |
|---|---|
| `board-top.png` | what the finished board will look like from above |
| `board-copper.png` | both copper layers |
| `fit-template-1to1.pdf` | **print at 100 % / actual size** and lay your modules on it (the 50 mm ruler must measure 50 mm) |
| `abadi-motherboard.kicad_pcb` + `.kicad_pro` | the board in KiCad 7 (keep both files together: the .kicad_pro holds the design rules) |
| `gerber/` and `abadi-motherboard-2layer-gerber.zip` | the fab files (this zip is what you upload to the PCB maker) |
| `pin-table.md` | which ESP32 pin carries which signal, and every connector's pin order |
| `parts-list.md` | headers, terminals, resistors, capacitors to buy |
| `reports/` | KiCad's design-rule report and my independent check of the Gerber files |

## What was checked

- KiCad design-rule check: **0 errors, 0 unconnected pads.** (43 notes say the footprints are not from a KiCad library; they
  are drawn in code, so that is expected and harmless.)
- A separate checker I wrote reads only the exported Gerber and drill files, rebuilds which copper touches which, and compares
  with the intended nets: **0 shorts, 0 opens**, all 177 plated holes match the design (the 4 mounting holes are in a separate unplated file).
  I tested the checker by cutting a track in a copy: it reported the break.
- Fab limits (typical cheap 2-layer): smallest copper gap 0.152 mm, narrowest track 0.25 mm, smallest drill 0.30 mm,
  copper at least 0.5 mm from the edge.
- Independent reviewers (separate agents) checked the footprints against your photos, the netlist, the fab files and your notes.

## What is NOT checked

1. **Module pin orders and sizes** other than the ESP32 (measured) and the GY-521 (read from your photo). PCA9685 header position
   (centred on the short end, 1.3 mm in) is an estimate from the photo. The relay, sonar and screen pin orders are assumptions.
2. The ESP32 pin map is my optimized proposal. `plan.md` is **not** updated, and its locked pin table still describes the old build.
3. No schematic and no electrical simulation. The netlist lives in `build_board.py`.
4. Current limits: the battery copper is 2-3 mm wide, servo power 1.5 mm, motor traces 1 mm. Nothing is tested under load. A header
   pin carries the PCA9685's V+ (a header pin is good for roughly 2-3 A): for big servos also use the module's own screw terminal.
5. **The ESP32 board only fits one way round:** the USB-C end toward the **right** edge, the antenna toward the left (marked on the board,
   with the two USB-C sockets drawn). Turned around, its 3V3 pins land on the GND pins. The first hole of each row (square pad) is the antenna end.
6. PCA9685 orientation (header at the left end, servo plugs toward the bottom edge) and the DRV8833 pin layout still need your OK
   (see the questions in the chat). Whether the PCA9685 sits flat or needs spacers/screws is not designed yet: there is no mounting hole for it.

## Paper test-fit (10 minutes, free)

Print `fit-template-1to1.pdf` at 100 %. Check the 50 mm ruler. Lay each module on the sheet: its pins should fall in the
holes, its body inside the printed outline. Check polarity marks on the terminals (+ is the square pad) against your wiring.
Tell me anything that does not line up.

## Ordering (when the test-fit passes)

JLCPCB, 2 layers, 100 x 100 mm, 5 pieces, 1.6 mm, lead-free HASL, any solder-mask colour, bare board only (no assembly).
JLCPCB's help page lists $2 for five 2-layer boards up to 10 x 10 cm; shipping and German VAT are added at checkout. The
final price appears on their quote page before you pay.

## How it was made (to redo it after a change)

```
python3 build_board.py board.kicad_pcb --layers 2 --fine --pinmap     # parts, nets, outline, pours
python3 route_board.py board.kicad_pcb routed.kicad_pcb freerouting-2.0.1.jar 80
python3 finish_board.py routed.kicad_pcb final.kicad_pcb              # silk size, pour refill, DRC report
kicad-cli pcb export gerbers ... ; kicad-cli pcb export drill ...        # fab files
python3 audit_kicad_gerbers.py gerber design.json                       # independent check
```

The auto-router gives a different result each time the board is rebuilt. Rebuild and re-route until the report shows 0 unconnected
(it took 2 builds here). `assign_pins.py` re-optimizes which ESP32 pin drives which signal (run `build_board.py` once without
`--pinmap`, dump it with `dump_board.py`, then run `assign_pins.py`). Needs KiCad 7 (python3 `pcbnew`), Java 21 and
[Freerouting 2.0.1](https://github.com/freerouting/freerouting/releases/tag/v2.0.1).
The earlier `pcb/` files from Cursor (the 4-layer 105 x 84 mm draft) are superseded by this folder.
