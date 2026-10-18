# Robot motherboard - routed draft, 2 layers, 100 x 100 mm

**Status: DRAFT. Do not order yet.** The board is fully routed and passes every check I could run on the
files, but the module pin orders and sizes are standard-layout assumptions that nobody has compared with the real
parts yet. A wrong pin order means a wasted 5-board order. Do the paper test-fit below first.

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

- KiCad design-rule check on the final board: **0 errors, 0 unconnected pads.** (44 notes say the footprints are not
  from a KiCad library. They are drawn in code, so that is expected and harmless.)
- A separate checker I wrote reads the exported Gerber and drill files only, rebuilds which copper touches which, and
  compares with the intended nets: **0 shorts, 0 opens**, all 180 plated holes match the design (the 4 mounting holes are in a separate unplated file). I tested the checker
  by cutting a track in a copy: it reported the break.
- Fab limits (typical cheap 2-layer): smallest copper gap 0.152 mm, narrowest track 0.25 mm, smallest drill 0.30 mm,
  copper at least 0.5 mm from the edge, mounting holes in their own unplated drill file.

## What is NOT checked (this is the reason for "draft")

1. **Module pin orders and sizes.** ESP32-S3 DevKit (two 22-pin rows, 22.86 mm apart, pin 1 about 5 mm from the
   antenna end), DRV8833 (two rows of 5), PCA9685 (1x6: GND OE SCL SDA VCC V+), GY-521 (1x8), the relay, sonar, screen
   and touch modules. The DRV8833 order is a pure guess: I have not seen your board.
2. The ESP32 pin map is my optimized proposal. `plan.md` is **not** updated, and its locked pin table still describes the old build.
3. No schematic and no electrical simulation. The netlist lives in `build_board.py`.
4. Current limits: the battery copper is 2-3 mm wide and fine for two DRV8833 drivers, but nothing here is tested under load. Servo power
   never passes through this board (the servo buck feeds the PCA9685's own terminal). The 3.3 V and 5 V traces are 0.5 mm: fine for about 1 A.
5. The antenna keep-out is only the 4 mm at the end of the module. Check it against your board.

## Paper test-fit (10 minutes, free)

Print `fit-template-1to1.pdf` at 100 %. Check the 50 mm ruler. Lay each module on the sheet: its pins should fall in the
holes, its body inside the printed outline. Also check polarity marks on the terminals (+ is the square pad) against your wiring.
Tell me anything that does not line up and I will redo that part.

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
(it took 2 builds here). `assign_pins.py` re-optimizes which ESP32 pin drives which signal.
Needs KiCad 7 (python3 `pcbnew`), Java 21 and [Freerouting 2.0.1](https://github.com/freerouting/freerouting/releases/tag/v2.0.1).
The earlier `pcb/` files from Cursor (the 4-layer 105 x 84 mm draft) are superseded by this folder.
