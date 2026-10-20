# Shopping list (v5 board)

The parts for the board and the power system. Values and ratings are minimums; a higher voltage rating is always fine.

## Soldered on the board

| What | How many | Notes |
|---|---|---|
| Female socket 1x22, 2.54 mm | 2 | for the ESP32-S3 devkit. The devkit's pins must be soldered in first if it came loose. |
| Female socket 1x6, 2.54 mm | 4 | for the two DRV8833 modules (each module has two rows of 6 pins; solder pins into the module first if it has none) |
| Pin header 1x6 plus socket 1x6 | 1 each | PCA9685: the header goes on the module (pins down, plastic on its underside), the socket on the board; or solder the module straight in |
| Female socket 1x8, 2.54 mm | 1 | GY-521 gyro |
| 2.54 mm male header or JST-XH socket | 3-pin x3 (relays), 4-pin x2 (sonars), 7-pin x2 (screens), 4-pin (I2C), 3-pin (UART), 2-pin x4 (motors), 8-pin (SPARE IO) | your JST plugs fit this spacing |
| 2x4 pin header | 1 | POWER OUT (2 x 5 V, 2 x 3.3 V, 4 x GND; about 2 A per rail at most) |
| Screw terminal, 2-pole, 5.08 mm | 4 | SERVO 5V IN, BATT IN, CLEAN 5V IN, 3.3V IN |
| Electrolytic capacitor 470 uF, 16 V or higher | 1 | C1, + = square pad |
| Electrolytic capacitor 100 uF, 10 V or higher | 1 | C2, + = square pad |
| Ceramic capacitor 100 nF (marked 104), 16 V or higher | 2 | C3, C4 |
| Resistor 1 kOhm, 1/4 W | 2 | sonar echo dividers (upright, "1k") |
| Resistor 2 kOhm, 1/4 W | 2 | sonar echo dividers (upright, "2k") |
| Diode 1N5819 (Schottky) | 1 | D1: stripe = K = the hole marked K |
| M3 screws + nuts | 4 | mounting |

## Off the board (power)

| What | Notes |
|---|---|
| Buck 1: XL4016 module | servo 5 V. Set to 5.0 V (not 6 V). Check that it regulates down to a 6 V pack (test it at 6.0 V in). Heatsink and some airflow. Measure before connecting; lock the adjust screw with a drop of glue. |
| Buck 2: fixed 5 V buck, 1.8 A | clean 5 V (ESP32, sonars, POWER OUT 5 V). Check its input range covers 6-8.4 V. |
| Buck 3: fixed 3.3 V buck, 2 A | relays, screens, POWER OUT 3.3 V. Check its input range covers 6-8.4 V. |
| Buck 4 (only with a Raspberry Pi 5): second XL4016, set to 5.1 V | check its input range and test it at 6.0 V in; own 5 A fuse, thick short wires, lock the adjust screw. A bare USB-C cable end gives the Pi no 5 A negotiation (it limits its USB ports); the 5 V header pins are the alternative but bypass its protection. |
| BMS 2S, balancing (HX-2S-JH20 type) | "20 A" is a peak rating, about 10 A continuous is realistic. Overcharge 4.25 V, over-discharge 2.9-3.0 V per cell is best for old cells. |
| 2S USB-C charger board (balancing if possible) | charge with the robot switched off |
| 2 x 18650 cells (or more in 2S x N) in a holder | similar capacity, no damaged cells, same charge level before joining |
| Fuses with holders (5 or 6) | one per branch: BATT IN 5 A slow-blow (6 A at most: the board's 2 mm battery copper is a roughly 6 A design), servo buck 5 A, clean 5 V buck 2 A, 3.3 V buck 2 A, Pi buck 5 A. The BMS is about 10 A continuous in total. |
| Main switch, 10 A or more | in the battery + lead |
| Lever connectors (Wago 221), x2 | one for battery +, one for battery -. The battery lead plus BATT IN and three bucks is 5 wires; with the Pi buck it is 6 (use 6-way, or two connectors joined) |
| Wire | 1.0-1.5 mm2 (AWG 16-18) for the battery and motor branches |

## First power-up (before anything plugged in)

1. With nothing on the board, power each buck from the battery alone and set it: servo 5.0 V, clean 5.0 V, 3.3 V buck 3.3 V (Pi buck 5.1 V).
2. Connect BATT IN only, with a fuse, and check with a multimeter that nothing is hot.
3. Connect the three buck outputs, then the ESP32. Run Wi-Fi transmitting on the clean 5 V buck only (USB unplugged): the ESP32's 3.3 V pin should stay at 3.2 V or higher.
