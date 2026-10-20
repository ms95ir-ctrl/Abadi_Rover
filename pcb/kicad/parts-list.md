# Parts list (generated from the board file)

| Qty | Item | Pads | Refs |
|---|---|---|---|
| 1 | 470 uF electrolytic capacitor, 16 V or higher (25 V is fine), radial, 3.5 mm lead spacing; long leg / no stripe = + (square pad) | 2 | C1 |
| 1 | 100 uF electrolytic capacitor, 10 V or higher, radial, 2.5 mm lead spacing; long leg / no stripe = + (square pad) | 2 | C2 |
| 1 | 100 nF ceramic capacitor (marked 104), 16 V or higher, 2.54 mm lead spacing, no polarity | 2 | C3 |
| 1 | 100 nF ceramic capacitor (marked 104), 16 V or higher, 2.54 mm lead spacing, no polarity | 2 | C4 |
| 1 | 1N5819 Schottky diode; the stripe end = K, goes to the hole marked K | 2 | D1 |
| 1 | two 1x6 female sockets, 2.54 mm (or solder the module's pins straight in) | 12 | DRVA |
| 1 | two 1x6 female sockets, 2.54 mm (or solder the module's pins straight in) | 12 | DRVB |
| 1 | 1x8 female socket, 2.54 mm | 8 | GYRO |
| 4 | M3 mounting hole (screw + nut), 3.2 mm | 1 | H1, H2, H3, H4 |
| 1 | 4-pin 2.54 mm male header or JST-XH socket (I2C SENSOR) | 4 | I2C |
| 1 | 22-pin female socket, 2.54 mm (the ESP32-S3 devkit's pins plug in) | 22 | J1 |
| 1 | 22-pin female socket, 2.54 mm (the ESP32-S3 devkit's pins plug in) | 22 | J3 |
| 1 | 1x6 pin header (pins down, plastic on the module's underside) plus a 1x6 socket on the board, or solder straight in | 6 | PCA |
| 1 | 2x4 pin header, 2.54 mm | 8 | PWR |
| 2 | 1 kOhm resistor, 1/4 W, stands upright | 2 | RD1a, RD2a |
| 2 | 2 kOhm resistor, 1/4 W, stands upright | 2 | RD1b, RD2b |
| 1 | 3-pin 2.54 mm male header or JST-XH socket (RELAY 1) | 3 | RLY1H |
| 1 | 3-pin 2.54 mm male header or JST-XH socket (RELAY 2) | 3 | RLY2H |
| 1 | 3-pin 2.54 mm male header or JST-XH socket (RELAY 3) | 3 | RLY3H |
| 1 | 7-pin 2.54 mm male header or JST-XH socket (SCREEN L) | 7 | SCR_L |
| 1 | 7-pin 2.54 mm male header or JST-XH socket (SCREEN R) | 7 | SCR_R |
| 1 | 4-pin 2.54 mm male header or JST-XH socket (SONAR 1) | 4 | SON1 |
| 1 | 4-pin 2.54 mm male header or JST-XH socket (SONAR 2) | 4 | SON2 |
| 1 | 8-pin 2.54 mm male header or JST-XH socket (SPARE IO) | 8 | SPARE |
| 1 | screw terminal, 2-pole, 5.08 mm pitch (hole 1.3 mm) | 2 | TL0 |
| 1 | screw terminal, 2-pole, 5.08 mm pitch (hole 1.3 mm) | 2 | TL1 |
| 1 | screw terminal, 2-pole, 5.08 mm pitch (hole 1.3 mm) | 2 | TL2 |
| 1 | screw terminal, 2-pole, 5.08 mm pitch (hole 1.3 mm) | 2 | TL3 |
| 1 | 2-pin 2.54 mm header or JST socket for the motor plug | 2 | TM1 |
| 1 | 2-pin 2.54 mm header or JST socket for the motor plug | 2 | TM2 |
| 1 | 2-pin 2.54 mm header or JST socket for the motor plug | 2 | TM3 |
| 1 | 2-pin 2.54 mm header or JST socket for the motor plug | 2 | TM4 |
| 1 | 3-pin 2.54 mm male header or JST-XH socket (UART) | 3 | UART |

Cable ports (relay, sonar, screen, I2C, UART, SPARE IO): standard 2.54 mm male pin headers, or JST-XH sockets (2.5 mm pitch; the owner's plugs fit this spacing). Power outputs and ground on the POWER OUT header: about 2 A per rail at most. The two resistors per sonar stand upright (holes 2.54 mm apart); D1 lies flat (holes 7.62 mm apart). See shopping-list.md for the parts that are not on the board (bucks, BMS, charger, fuses, connectors).
