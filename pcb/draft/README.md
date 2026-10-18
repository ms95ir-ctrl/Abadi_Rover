# Draft v0 - reusable robot carrier board (100 x 100 mm)

A placement picture only, so the layout can be imagined and discussed. Nothing is routed and
nothing here can be sent to a PCB maker.

- `floorplan_v0_top.png` - to-scale top view
- `floorplan_v0_3d.png` - 3D-style view with real component heights
- `floorplan_v0.py` - generates both pictures and checks that no part overlaps, leaves the board,
  or sits on a mounting hole

## What is on the board

| Item | How it connects |
|---|---|
| ESP32-S3 DevKit (dual USB-C) | two 1x22 sockets, USB end at the right edge, antenna end kept free of copper |
| DRV8833 x 2 | sockets (pin layout still to be confirmed from photos) |
| GY-521 gyro | 1x8 socket |
| Screens L and R | 1x7 pin headers, cables to the screens |
| Relay boards A and B | 1x4 headers, cables to the relay boards |
| Ultrasonic sensor | 1x4 header (echo divider on the board) |
| Servo board (PCA9685) | I2C 1 header, plus SERVO V+ OUT terminal for its power |
| Extra sensors | I2C 2 and I2C 3 headers |
| Extras | UART header, SPARE IO header (spare ESP32 pins) |
| Power | screw terminals: QUIET 5V in, NOISY 5V in, to/from 3.3V buck, to/from 7V boost, fan, Pi GND |
| Motors | 4 two-pole screw terminals, M1/M2 from DRV A, M3/M4 from DRV B |
| Rail capacitors | 100uF + 100nF on the 3.3V rail and on the 7V rail |

## Assumed sizes (to be checked against the real parts)

| Part | Assumed |
|---|---|
| ESP32-S3 board | 69.6 x 25.4 mm, pin rows 22.86 mm apart, 22 pins per row |
| DRV8833 board | 21 x 18 mm, 2 x 5 pins |
| GY-521 | 21.2 x 16.4 mm, 8-pin header |
| Screw terminals | 5.08 mm pitch, 8 mm deep |
| Mounting holes | 4 x M3 at 4 mm from each corner |

## Not decided yet

- 2 layers (cheapest) or 4 layers - depends on how the routing turns out.
- Which "more stuff" to keep (spare IO, extra I2C ports, UART, battery sense, fuse).
- Pin map for two DRV8833 drivers. The locked table in `plan.md` is for the TB6612 and is not changed.
