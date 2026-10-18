# Draft v1 - robot motherboard, 100 x 100 mm

Placement only, nothing routed, not for fabrication. Pictures: `floorplan_v1_top.png`,
`floorplan_v1_3d.png`. Generated and overlap-checked by `floorplan_v1.py`.

## Power plan (2S Li-ion pack, 6-8.4V, charger and BMS are off the board)

| Rail | Source | Feeds |
|---|---|---|
| Pack 6-8.4V | BATT IN terminal (after fuse and key switch) | both DRV8833 drivers directly, and the three buck inputs |
| Servo 5V (5A+) | Buck 1, e.g. XL4016 8A | PCA9685 servo power, wired to its own terminal |
| Clean 5V (1-2A) | Buck 2, e.g. MP1584EN | ESP32 5V pin (through a Schottky diode), both sonars |
| 3.3V (1-1.5A) | Buck 3, e.g. MP1584EN | relay boards, both screens, touch buttons |

Charging and protection stay off the board: 2S BMS plus a 2S 8.4V Type-C charger module on the pack.

## Connectors

3 relay headers (1x3), 2 sonar headers (1x4), 2 touch-button headers (1x3), 2 screen headers (1x7),
I2C sensor header, UART header, spare IO header, PCA9685 on a 1x6 socket, GY-521 on a 1x8 socket,
4 motor terminals (M1/M2 from DRV A, M3/M4 from DRV B).

## Still to confirm

Module sizes and pin orders (needs photos and measurements), 2 or 4 layers, the DRV8833 pin map.
`plan.md` is unchanged and its locked pin and power tables are not updated yet.
