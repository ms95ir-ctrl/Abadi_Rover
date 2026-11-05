# DRAFT: new plan.md for Robot 1 on the motherboard (v5)

**Status: PROPOSAL, NOT APPLIED (version 2, after an independent check).** `plan.md` and `wiring.md` are unchanged until the owner says "approved".
After approval: the text under "PROPOSED plan.md" replaces `plan.md` and this draft is deleted. `wiring.md` (the TB6612 / power-bank build) and `HANDOVER.md` (the UNO Q / App Lab text) get a short rewrite; the new `wiring.md` keeps the old safety items (capacitor polarity, servo plug colours, relay and light wiring). The old pictures (`wiring-map.png`, `wiring-map.svg`, `wiring-map-unoq.png`, `relay-wiring.png`, `relay-wiring.svg`) show the old build and are replaced or removed. Three more small edits, each only with your approval: `.cursor/rules/plan-first.mdc` (its example names the old screen pins), the Robot 1 and board rows of the top-level `README.md`, and the sentence in `pcb/kicad/README.md` that says plan.md is not updated.
Sources (nothing invented): `plan.md` and `wiring.md` (old), `pcb/kicad/README.md`, `pin-table.md`, `shopping-list.md`, `parts-list.md`, `power-wiring.png`, `battery-wiring.png`, `relay-wiring.svg`. **(V)** = written in one of those files. **(A)** = my suggestion or assumption, to be tested.

## 1. What changes compared with the old plan.md

| Topic | Old plan.md (retired) | New (board v5) |
|---|---|---|
| Motor driver | TB6612FNG, 1 module, STBY pin | 2 x DRV8833 (HW-627) **on the board**; Robot 1 uses driver A only (left track = M1, right track = M2 (A)). No STBY pin (V). |
| Power | power bank + USB hub, HW-183B boost (7 V), HW-133A buck (3.3 V), keep-awake fan | 2S Li-ion pack, BMS, USB-C charger board, main switch, splice, one fuse per branch, bucks (V) |
| Pi 5 power | power bank through the hub | its own XL4016 set to 5.1 V, 5 A fuse, USB-C plug with bare wires (V) |
| ESP32 power | only from the Pi's USB, never the 5 V pin | the board feeds the ESP32 5 V pin through diode D1 from the clean 5 V buck (V); the USB cable from the Pi must be tested (Decision 3) |
| Pin table | GPIO 4,5,6,7,15,16,17; relays 1/2; I2C 8/9; screens 10-14, 21; sonar 41/42 | completely new, see "Locked pin table" below. GPIO 1 and 2 were relays; now GPIO 1 is a motor input and GPIO 2 the left screen CS. Do not reuse old wires or old code. |
| Hardware kill | key switch cuts motors, servos and fan only; the Pi stays on | the main switch cuts everything, including the Pi (Decision 2) |
| Extras on the board | none | gyro GY-521 socket, 2 sonar headers, 3 relay headers, SPARE IO header, I2C SENSOR header, UART header, 4 motor spots |
| Scope | sonar deferred | sonar stays deferred (pins reserved); the gyro is a later extra |

**Decisions to approve** (full text in the proposed plan.md, section "Decisions"): 1 motor driver and motor voltage limit; 2 main switch is the kill switch and the Pi is shut down first; 3 ESP32 power and the USB cable tests; 4 fan; 5 old files.

## --- PROPOSED plan.md starts here ---

**Current Status:** Phase 1 / Stage 0 (Build the board). Robot 1 moves to the motherboard v5 (ESP32-S3 + 2 x DRV8833 + 2S Li-ion power). The old TB6612 / power-bank pin table and power design are retired. Pending: check that the board says v5, test-fit of the real modules on the real board, soldering, then the Stage 1 power tests.

# Abadi Rover: Build Plan

This file is the single source of truth for the rover. The board's own documents are in `pcb/kicad/` (pin table: `pcb/kicad/pin-table.md`; power: `pcb/kicad/README.md`, `pcb/kicad/power-wiring.png`, `pcb/kicad/battery-wiring.png`; parts: `pcb/kicad/shopping-list.md`). Soldering and wiring steps: `wiring.md` (rewritten for the board). If it disagrees with this file, this file wins; report the mismatch.

## Rules (for every session, human or AI)

1. Read this file first, starting with the **Current Status** line, before doing anything else.
2. The **Locked pin table** and **Locked power design** below must never be changed, renamed or "cleaned up" without explicit approval from the owner. On any conflict: stop and ask.
3. Work one stage at a time. No code for a later stage until the current stage passes its test on real hardware.
4. Any terminal or git command given to the owner must be written out in full, with an explanation of what it does.
5. Update the **Current Status** line whenever a stage passes or a test result changes.

**Words used.** BMS = the battery protection board for the two cells. Buck = a small board that lowers the battery voltage to a steady lower one. Splice = the two lever connectors where all battery wires meet. Rail = one power line. PWM = fast on/off pulses that set motor speed or servo position. GPIO = a numbered ESP32 pin. I2C = a two-wire link (SDA data, SCL clock) to the PCA9685 and the gyro. SPI = the link to the screens (MOSI data, SCK clock, CS chip select, DC data/command, RST reset). UART = the serial console header. EEP = the DRV8833 sleep pin. OE = the PCA9685 output-enable pin. Multimeter = the tester that reads volts and beeps for connections. (V) = written in the board files. (A) = my assumption, to be tested.

## Scope

- **Brain:** Raspberry Pi 5 (8GB). Gamepad, later camera. Talks to the ESP32 over USB serial.
- **Hands:** ESP32-S3 (dual USB-C, N16R8 or N8R2) plugged into the motherboard. Motors, servos, relays, later screens.
- **Phase 1: Body.** Power, Bluetooth gamepad, drive, neck servos, combined app with kill switch (ultrasonic sensors deferred). Done when the rover can be fully driven and steered by gamepad with no PC tether.
- **Phase 2: Face.** Both SPI screens showing simple eyes (blinking is enough).
- **Phase 3: Extras.** Camera, USB audio, gyro (later). The sonar stays deferred as in the old plan: pins 12/13/14 are reserved, no stage yet. Not designed until Phases 1 and 2 are done and the owner asks.
- **Out of scope:** Hermes / AI agent on the rover, turret, MAX98357A I2S amp, Arduino UNO Q, App Lab, TB6612 and the old power-bank power design.

## Hardware

- Raspberry Pi 5 8GB (brain)
- ESP32-S3 dual USB-C DevKit (N16R8 or N8R2)
- Motherboard v5 (100 x 100 mm, 2 layers) with 2 x DRV8833 modules (HW-627; Robot 1 uses driver A only), PCA9685 16-channel PWM driver, GY-521 gyro (later)
- ELEGOO Conqueror tracked chassis, 2 x 1:48 TT-style geared motors, 2-pin JST plugs for the motors (V: parts list)
- Servos: TZT MG996R (180°), Miuzei MZ996 (90°, to be confirmed), unlabeled 360° continuous (orange gear)
- 2-channel 3.3V relay board (JQC-3F 03VDC) + 2 LED-filament lights, about 10 Ω resistors for them
- 2 x GMT020-02 2.0" SPI TFT (ST7789, 240x320)
- HC-SR04 ultrasonic sensors (deferred)
- Power: 2 x 18650 cells (2S) in a holder, 2S balancing BMS (HX-2S-JH20 type), 2S USB-C charger board (IP2326), main switch (10 A or more), XL4016 buck (servos, 5.0 V), second XL4016 (Pi, 5.1 V), fixed 5 V 1.8 A buck, fixed 3.3 V 2 A buck, 5 fuses with holders, Wago 221 lever connectors, wire 1.0 to 1.5 mm² (AWG 16 to 18) for the battery and motor branches (V)
- USB-C plug breakout board with solder pads, or a thick 5 A USB-C cable to cut, plus AWG 18 to 20 wire (A), for the Pi 5 power
- Multimeter (A); data-only USB adapter ("power blocker") and an ordinary USB-A to USB-C cable (A); a USB power meter, only if Stage 1 test 7 part B fails (A)
- 5V cooling fan (see Decision 4)
- USB webcam SC-012-SN259 (Phase 3)
- Retired from this build (kept in the drawer): 20000mAh power bank, Benfei USB-C hub, HW-183B boost, HW-133A buck, TB6612 board, key switch (unless it is rated 10 A or more and used as the main switch)

## Decisions (made when Robot 1 moved to the board; approved by the owner on ______)

1. **Motor driver and motor voltage.** The TB6612 is replaced by the DRV8833. No STBY: stop = both inputs of a motor low (A). The old plan ran the TT motors at 7.0 V; the pack is 6.0 to 8.4 V. The DRV8833 is rated 1.5 A continuous, 2 A peak per channel (A: seller figure, check the module's datasheet). A stalled TT motor draws about 1.5 A at 6 V (A: shop figure, not measured) and more at a higher voltage. **Default: the software limits the PWM duty to 6.0 V / battery voltage (never above 100 %).** Raise it towards 7.0 V only after Stage 3 shows the stall current is acceptable. First measure each motor's winding resistance with the multimeter, motors unplugged: about 4 Ω is expected (6 V / 1.5 A); a lower reading means a higher stall current. Never hold a track against a wall.
2. **Kill switch.** The old key switch left the Pi running. The new main switch cuts everything, including the Pi, which can damage the SD card. **Default: the main switch is the on/off switch and the hardware kill; shut the Pi down first (until the app has a Shut down button, type `sudo shutdown -h now` in a terminal on the Pi and press Enter: this halts Linux; wait about 10 seconds until the Pi's green LED stops flashing); the gamepad kill button is the software kill. No second switch for now.**
3. **ESP32 power and the USB cable.** The board feeds the ESP32 5 V pin; the old plan said "never feed the 5 V pin". Whether the Pi's USB cable may also carry 5 V is not known (A). **Default: until Stage 1 test 7 passes, use a data-only USB cable between the Pi and the ESP32 COM port.**
4. **Fan.** The fan was only needed to keep the power bank awake. The Pi 5 may still want cooling. **Default: if the fan is the Pi's own Active Cooler, plug it into the Pi 5's fan header (A). Otherwise leave the fan out and check the Pi's temperature after a long run: type `vcgencmd measure_temp` and press Enter (prints the chip temperature). A fan is a small motor; if one is put on a board 5 V pin (about 1 A is available for your own parts, V) and the ESP32 resets when it starts, move it (A).**
5. **Old files.** `wiring.md` and `HANDOVER.md` are rewritten short for the board; the old pictures are replaced or removed.

## Locked power design

Pack alone first, then each branch one at a time (Stage 1). Wiring diagram: `pcb/kicad/power-wiring.png`; battery only: `pcb/kicad/battery-wiring.png`.

| Rail | Source | Feeds |
|---|---|---|
| **Pack** | 2 x 18650 (6.0 to 8.4 V): cell wires B-, BM, B+ go to the BMS; the BMS output P+ → main switch → splice plus. Two lever connectors, one for + and one for -; each needs 6 inputs with the Pi buck (use a 6-way or two joined) | every branch below |
| **Charging** | USB-C charger board, output set to 8.4 V, wired to the BMS pads P+ and P- (the charger's own pads are also called B+ / B-; the BMS pad B- is never used for charging) | charge with the robot switched off |
| **BATT IN** | splice → 5 A slow-blow fuse (6 A at most) → board terminal BATT IN | DRV8833 supply (motors) only |
| **Servo 5 V** | splice → 5 A fuse → XL4016 set to **5.0 V** → board terminal SERVO 5V IN | PCA9685 V+ (servos). For big servos also run a second short AWG 18 pair from the SAME servo buck OUT+ and OUT- to the PCA9685 module's own V+ screw terminal (never from the clean 5 V buck) (V: board README, A: wire gauge) |
| **Clean 5 V** | splice → 2 A fuse → fixed 5 V 1.8 A buck → board terminal CLEAN 5V IN | ESP32 5 V pin (through D1), both sonars, POWER OUT 5 V pins |
| **3.3 V** | splice → 2 A fuse → fixed 3.3 V 2 A buck → board terminal 3.3V IN | relay boards, screens, both lights (see "Relay and lights"), POWER OUT 3V3 pins |
| **Brain** | splice → 5 A fuse → second XL4016 set to **5.1 V** → thick short wires (AWG 18 to 20, under 40 cm, A) → USB-C plug → Pi USB-C power port | Raspberry Pi 5 only. Does not touch the board |

- **Common ground:** the ground is joined at the splice minus lever connector. With the Pi buck it takes 6 wires: BMS P-, BATT IN minus, and the minus INPUT (IN-) of each of the four buck modules, as drawn in `pcb/kicad/power-wiring.png`. The cells are not on this connector: cell 1 minus goes only to BMS B-, and no wire of the robot or the charger ever goes on B-. Each buck's minus OUTPUT goes to its own board terminal minus (SERVO 5V IN, CLEAN 5V IN, 3.3V IN) or, for the Pi buck, to the Pi cable. The bucks are not isolated, so IN- and OUT- of a module are the same ground (A). On the board all GND pads are one piece (V). The old "star ground" wires from the Pi and ESP32 are dropped (A): the Pi's minus reaches the splice through the Pi buck, and the ESP32's GND is the board ground, which reaches the splice through the BATT IN minus wire (checked in Stage 0c). Do not rely on USB ground alone for motors.
- **Main switch OFF** whenever you connect, move or unplug a wire, a buck, the ESP32 or a DRV module. The board has no reverse-polarity protection (V): before the first connection of each board terminal and of the Pi plug, check + and - with the multimeter. Screw terminals on the left edge: + is the lower hole with the square pad, marked + on the board (V).
- **Board limits (V):** no fuse and no reverse-polarity protection on the board. Each POWER OUT rail is good for about 1 A of your own parts. The battery copper on the board is a roughly 6 A design. The BMS is about 10 A continuous in total ("20 A" is only a peak): the five fuses add up to 19 A, so a rare peak of everything at once could make the BMS cut off, which switches off everything including the Pi (A). Typical use is far lower (A).
- **Never** feed power into the Pi 5 GPIO 5V pins. The Pi is powered only through its USB-C port. The ESP32 gets its 5 V from the board (CLEAN 5V IN through D1); the USB cable between the Pi and the ESP32 follows Decision 3 and Stage 1 test 7.
- **Set every adjustable buck (the two XL4016) on its own, powered from the battery, with a multimeter before it touches the board;** the fixed bucks only have to read 5.0 V and 3.3 V. Lock the two XL4016 adjust screws with a drop of glue after the load tests (A).
- **Pi 5 power:** official need is about 5 V / 5 A. A bare USB-C cable end gives the Pi no 5 A negotiation, so it limits its USB ports (V: shopping list). If the Pi shows a yellow lightning-bolt warning or reboots, the Pi buck or its wires are not good enough.
- **Fallback (old):** the 2S 5200 mAh LiPo + 5 A UBEC fallback of the old plan is not part of this design.

## Locked pin table

Source: `pcb/kicad/pin-table.md` (generated from the board file; PROVISIONAL until Stage 0a has passed, then locked). Pin numbers are ESP32 GPIO numbers. Do not use GPIO 19/20 (USB) or GPIO 43/44 (UART header = console) for anything else.

### ESP32-S3 pins (hands)

| GPIO | Signal on the board | Connects to | Phase |
|---|---|---|---|
| 4 | IN1A | DRV A IN1 → motor M1 (left track, A), PWM | 1 |
| 16 | IN2A | DRV A IN2 → motor M1 (left track, A), PWM | 1 |
| 1 | IN3A | DRV A IN3 → motor M2 (right track, A), PWM | 1 |
| 5 | IN4A | DRV A IN4 → motor M2 (right track, A), PWM | 1 |
| 6 | SCL | PCA9685, (later GY-521) | 1 |
| 7 | SDA | PCA9685, (later GY-521) | 1 |
| 15 | RLY1 | relay header 1 (light 1, A) | 1 |
| 18 | RLY2 | relay header 2 (light 2, A) | 1 |
| 17 | RLY3 | relay header 3 (spare) | spare |
| 12 | TRIG | HC-SR04 TRIG, both sonar headers | deferred |
| 13 | ECHO1 | sonar 1 echo (1k/2k divider on the board) | deferred |
| 14 | ECHO2 | sonar 2 echo (1k/2k divider on the board) | deferred |
| 2 | CS_L | left screen CS | 2 |
| 42 | CS_R | right screen CS | 2 |
| 41 | LCD_RST | both screens RST | 2 |
| 40 | LCD_DC | both screens DC | 2 |
| 39 | MOSI | both screens SDA | 2 |
| 47 | SCK | both screens SCL | 2 |
| 8, 11, 9, 10 | IN1B, IN2B, IN3B, IN4B | DRV B (not used in Robot 1, reserved) | spare |
| 3, 46, 45, 48, 38, 21 | SPARE IO header: pin 1 = GND, pin 2 = the ESP32's own 3V3, then these six GPIOs in this order | GPIO 3, 45, 46 are boot-strapping pins and GPIO 46 is input-only; 38 and 48 drive the devkit's RGB LED. Leave unused in Phase 1 (A). The 3V3 pin here and on the I2C SENSOR header is the ESP32 devkit's own 3V3, a different source from the POWER OUT 3V3 pins (3.3 V buck): never join them (V) | spare |
| 43, 44 | UART header (console TX/RX) | unplug it while flashing | spare |
| 0, 19, 20, 35, 36, 37 | not connected | do not use | none |

(A) Left track = M1, right track = M2, RLY1 = light 1, RLY2 = light 2 and "leave SPARE IO unused in Phase 1" are my choices carried over from the old plan. The board only fixes M1 = DRV A OUT1+OUT2 (IN1A GPIO4, IN2A GPIO16) and M2 = DRV A OUT3+OUT4 (IN3A GPIO1, IN4A GPIO5).

Screens are wired in the header order **CS DC RST SDA SCL VCC GND** (pin 1 = square pad = CS); VCC is the 3.3 V rail. Sonar header: 5 V TRIG ECHO GND. Relay header: pin 1 = 3.3 V (square pad), pin 2 = IN, pin 3 = GND.

### Relay and lights (A, carried over from the old build; to be re-tested)

Your relay board has ONE 4-pin control header (drawn in `relay-wiring.svg` as VCC GND IN1 IN2), but the motherboard has THREE 3-pin relay headers in the order VCC IN GND. Do not plug a 3-wire cable straight across (GND and the signal would swap). First compare the names printed on your relay board with the board print, then use single Dupont wires: relay VCC → RELAY 1 pin 1; relay IN1 → RELAY 1 pin 2; relay IN2 → RELAY 2 pin 2; relay GND → RELAY 1 pin 3. Pins 1 and 3 of RELAY 2 stay empty (same nets). Light contacts: relay COM1 and COM2 → a POWER OUT 3V3 pin; relay NO1 / NO2 → about 10 Ω → light 1 / light 2 plus; both light minus wires → a POWER OUT GND pin. LED filaments have polarity (marked +, a dot or a notch): test each light briefly on 3.3 V with its resistor before installing. The lights are a load on the 3.3 V buck (2 A fuse).

### Raspberry Pi 5 (brain)

| Pi connection | Connects to | Notes |
|---|---|---|
| USB-C power | the 5.1 V Pi buck cable | Only power for the Pi |
| USB-A | ESP32 COM USB-C (the one marked COM, not USB) | Serial commands (cable: Decision 3, Stage 1 test 7) |
| Bluetooth | PS5-style gamepad | Software, no extra wire |

### PCA9685 (I2C address 0x40, OE not connected, PWM frequency 50Hz)

Plugs into its 1x6 socket on the board (V: shopping list: header pins down, plastic on the module's underside; or solder it straight in). Header at the LEFT short end, servo plugs facing the bottom edge (V: board print). Header order top to bottom: GND, OE (not connected), SCL, SDA, VCC (logic, from the ESP32 devkit's own 3V3), V+ (servo 5 V branch) (V: pin-table.md). The board has no I2C pull-up resistors: the PCA9685 and GY-521 modules must bring their own (V). Servo plugs: brown or black = GND, red = V+, orange or yellow = signal; match the labels printed on the PCA9685 before plugging in (a reversed plug puts 5 V on the signal pin, A).

| Channel | Servo | Role |
|---|---|---|
| CH0 | TZT MG996R (180°) | Decided in Stage 4 |
| CH1 | Miuzei MZ996 (90°?) | Decided in Stage 4 |
| CH2 | Unlabeled 360° continuous (orange gear) | Decided in Stage 4 |
| CH3-CH15 | Spare | none |

### DRV8833 A outputs

| On the board | Connects to |
|---|---|
| MOTOR 1 spot (2-pin header or JST, DRV A OUT1+OUT2) | Left track motor (A) |
| MOTOR 2 spot (DRV A OUT3+OUT4) | Right track motor (A) |
| DRV A module VCC pin | Already tied to the BATT IN terminal by the board copper (V): no wire needed |

If a track runs backwards, swap that motor's two wires at its M1 or M2 spot and note it in the calibration table. This does not change the pin table.

## Calibration table (editable, not locked)

| Item | Value | Date / notes |
|---|---|---|
| Servo buck output (XL4016) | 5.0 V | Stage 1 test 3 |
| Clean 5 V buck output (fixed) | 5.0 V | Stage 1 test 3 (measure only) |
| 3.3 V buck output (fixed) | 3.3 V | Stage 1 test 3, relay board still unplugged; a relay board is plugged in only after this reads 3.3 V |
| Pi buck output (XL4016) | 5.1 V | Stage 1 test 3; measure again at the Pi plug under load (test 6) |
| Motor duty limit (6.0 V / battery) | TBD | Stage 3 (Decision 1) |
| Motor winding resistance (each) | TBD | Stage 3, before the first drive |
| DRV8833 EEP pin tied high? | TBD | Stage 3 (if the motors do not run, EEP needs a wire to the ESP32's own 3V3: SPARE IO pin 2 or I2C SENSOR pin 1, main switch OFF, never to a pin next to VBAT) |
| USB data-only cable tests A and B | TBD | Stage 1 test 7 |
| CH0 MG996R min / max pulse (µs) | TBD | Stage 4 |
| CH0 role | TBD | Stage 4 |
| CH1 MZ996 min / max pulse (µs) | TBD | Stage 4 (confirm 90° vs 180°) |
| CH1 role | TBD | Stage 4 |
| CH2 360° stop pulse (µs) | TBD | Stage 4 (around 1500) |
| CH2 role | TBD | Stage 4 |
| Left motor wires swapped? | TBD | Stage 3 |
| Right motor wires swapped? | TBD | Stage 3 |
| Obstacle stop distance (cm) | TBD | Later |
| Relay trigger (active high / low) | TBD | When the lights are wired (no stage yet) |

## Phase 1 stages

### Stage 0: Build the board (new)

**0a. Check and test-fit (no soldering).** First look at the board itself: the text "v5" is printed on it. If it says another version, stop and tell Claude: the pin table below does not match that board. Then lay the real modules on the real board and check (V: board README, "Still to confirm"): the two DRV8833 rows fall in the holes (row gap about 16 mm); EEP sits across from IN1; with the white plug toward the bottom edge the top row reads IN1 IN2 VCC GND IN3 IN4 from the left and the module's VCC pin is over the printed "VCC"; the screen cable's pin 1 is CS; the ESP32 fits with its USB-C ends toward the right edge; the PCA9685 header, the gyro and a terminal fit. Also compare the pin names printed on your relay board, sonar sensor, PCA9685 and GY-521, pin by pin, with the names printed on the board (V: these orders are only the usual orders, not read from your modules; the I2C SENSOR and UART headers have no module behind them). Tell Claude anything that does not line up before any soldering. (The paper template `pcb/kicad/fit-template-1to1.pdf` was for the check before ordering; if you still print it, print at 100 % so its 50 mm ruler measures 50 mm.)

**0b. Solder.** Parts list: `pcb/kicad/parts-list.md` and `pcb/kicad/shopping-list.md` ("Soldered on the board"). Polarity (V): D1 stripe end = K = the hole marked K; C1 (470 µF) and C2 (100 µF): long leg / no stripe = + (square pad); reversed, an electrolytic capacitor can burst. Order (A, normal practice): resistors and diode, then the ceramic capacitors, then sockets and headers, then the screw terminals, last the two electrolytic capacitors. Solder the pins into the devkit and the modules first if they came loose. Do **not** insert the DRV8833 modules yet.

**0c. Check before any power (A).** With the multimeter on the beeper or ohm range, nothing plugged in and the main switch off: no short between GND and each of the four terminals' plus (BATT IN, SERVO 5V IN, CLEAN 5V IN, 3.3V IN); the minus of each of the three board terminals beeps to the splice minus once the wires are connected. Look at the solder joints under a light.

- **Stage pass:** 0a all fit, 0b done, 0c no short.

### Stage 1: Power (restarted on the board)

In this order. Nothing on the signal pins yet. DRV8833 modules stay out until Stage 3.

| Test | Result |
|---|---|
| 1. Pack, following `pcb/kicad/battery-wiring.png`, one wire at a time, every bare end taped: (a) both cells within about 0.1 V of each other (A); (b) join cell 1 + to cell 2 - (series link); (c) BMS wires in the order B-, then BM, then B+; (d) measure BMS P+ to P-: 6.0 to 8.4 V; (e) charger board with the USB adapter unplugged: its output must read about 8.4 V; if it reads far more, do NOT connect it; (f) connect the charger output to BMS P+ and P-; (g) main switch OFF, plug in the USB adapter and watch the voltage: it must stop rising at 8.4 V | **Pending** |
| 2. Main switch on, nothing else connected: voltage at the splice is 6.0 to 8.4 V. Stop driving when the splice reads about 6.4 V (A); the BMS cuts at about 5.8 to 6.0 V (V: shopping list, 2.9 to 3.0 V per cell), and that also switches the Pi off hard | **Pending** |
| 3. Each buck alone, from the splice through its own fuse, loads disconnected, multimeter on its OUT+ and OUT-. Servo XL4016: turn the screw to 5.0 V. Pi XL4016: turn the screw to 5.1 V. The fixed 5 V and 3.3 V bucks have no screw: they only have to read 5.0 V and 3.3 V (about 0.1 V). Pi cable: with the buck on and the plug NOT in the Pi, put the multimeter on the two wires at the USB-C plug: +5.1 V on the 5 V wire, 0 V on the ground wire; if reversed, do not plug it in. The "also at 6.0 V in" check needs an adjustable bench power supply (A): with one, feed each XL4016 at 6.0 V and confirm the output holds; without one, do it under load in test 6 with the pack at about 6.4 V and again at 6.0 V, measured at the USB-C plug | **Pending** |
| 4. BATT IN only, with its fuse, no DRV module: nothing hot | **Pending** |
| 5. Connect the three board buck outputs (SERVO 5V IN, CLEAN 5V IN, 3.3V IN), then plug the ESP32 (USB-C ends toward the right edge). Flash a tiny Wi-Fi test program written only for this test (A: no code for later stages) with the clean 5 V fuse OUT so only the USB powers the devkit; then unplug the USB and put the fuse back. The program joins Wi-Fi and sends for 5 minutes. Pass: the ESP32 3V3 pin never reads below 3.2 V (V: board README) and the chip does not reboot (a multimeter shows an average and can miss short dips, so a reboot is the real fail sign, A) | **Pending** |
| 6. Pi 5 boots on the Pi buck and stays up 5 min. No yellow lightning-bolt warning on the screen. In a terminal type `vcgencmd get_throttled` and press Enter (it asks the Pi whether it ever had too little power): the answer must be `throttled=0x0` (never) | **Pending** |
| 7. The Pi can see the ESP32 (Pi running, a terminal open). Cable = a data-only USB adapter plus an ordinary USB-A to USB-C cable (A). **A (no 5 V on the cable):** pull the clean 5 V branch's 2 A fuse out of its holder (do NOT use the main switch: it also switches the Pi off). Plug the cable from a Pi USB-A port into the devkit's COM USB-C socket (not the one marked USB). The devkit power LED must stay dark; if it lights, the cable carries 5 V: stop and fix the cable. **B (the chip appears):** put the fuse back, same cable. Type `lsusb` and press Enter (lists the USB devices): one line must contain `10c4:ea60`, `1a86:7523` or `1a86:55d3`. Then type `ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null` and press Enter (lists the serial ports and hides the harmless "No such file" message): one device, for example `/dev/ttyUSB0`, must be listed. **If B fails:** use an ordinary cable with a USB power meter in line; about 0 mA must leave the Pi port while the clean 5 V buck feeds the ESP32; if the Pi port delivers current, STOP and ask before the robot is run that way | **Pending** |
| 8. Servo rail under servo movement | **Pending** (Stage 4) |

- **Stage pass:** tests 1 to 7 pass, common ground per the power design, no signal pin used.

### Stage 2: Gamepad test (no motors)

- Pair the PS5-style controller to the **Pi 5 Bluetooth**.
- A small program on the Pi that only prints stick and button values.
- **Pass:** each stick axis and the chosen buttons change the printed values; after turning the controller off and on, it reconnects without restarting the Pi.

### Stage 3: Drive

- Main switch OFF and the BATT IN fuse out of its holder. Insert DRV A only now, with the thick white-plug bar toward the bottom edge (board print "white plug v"). A module inserted 180° rotated fits the holes and would put battery voltage on GPIO1 / GPIO16 (V). Check the bar once more, then put the fuse back and switch on. Motors on the MOTOR 1 (left) and MOTOR 2 (right) spots. Measure each motor's winding resistance first (Decision 1). If the motors do not run, check the EEP pin of the module (calibration table).
- DRV8833 driven from ESP32 GPIO 4, 16 (left) and 1, 5 (right). Speed = PWM on one input of a motor with the other low; reverse = swap; stop = both low (A). Pi sends stick values over USB serial. Left stick controls both tracks.
- Gradual speed ramping. ESP32 safety stop: motors stop if no command arrives for 300 ms. Duty limit: 6.0 V / battery voltage (Decision 1).
- **Pass (tracks lifted first, then on the floor):** forward, back, left and right turns; motors stop within 0.5 s when the controller is switched off.

### Stage 4: Neck servos

- Calibrate each servo on its PCA9685 channel (CH0 to CH2). Record in the calibration table.
- Check the servo plug colours against the PCA9685 labels before plugging in (see the PCA9685 section).
- Right stick moves the neck. The 360° servo uses speed/direction, not angle.
- Run power test 8 (servo rail under movement) here.
- **Pass:** smooth movement, no buzzing or stalling at the limits, no Pi reboot.

### Stage 5: Integration and kill switch

- One combined app on the Pi: drive + neck, talking to the ESP32.
- Sonar still deferred (GPIO 12/13/14 stay reserved).
- Gamepad kill button: motors stop and servos hold until re-armed. The main switch remains the hardware kill; it cuts everything including the Pi, so shut the Pi down first (Decision 2).
- Shutdown (A): a button in the app shuts the Pi down cleanly (runs `sudo shutdown -h now`). Switch the main switch off only after the Pi has stopped. Cutting power on a running Pi can damage the SD card.
- App starts automatically at boot (no PC needed).
- **Pass:** drive the rover around the room by gamepad with no PC; kill button works.

### Stage 6: Phase 2: Screens

- Both ST7789 screens on shared SPI (GPIO 39 MOSI, GPIO 47 SCK), CS GPIO 2 left / GPIO 42 right, shared DC GPIO 40 and RST GPIO 41, powered from the 3.3 V buck.
- **Pass:** both screens show simple eyes that blink.

## Lessons learned

- Lock the pinout early, and treat this file as the only source of truth.
- Validate every part against real datasheets and bench tests before writing code.
- Keep servo and motor power separate from logic and screen power.
- One phase at a time; confirm on real hardware before moving on.
- Set each adjustable buck on the battery it will actually run from, alone first with a multimeter, then check it again under its real load.
- ESP32 pins are **not** 5V-tolerant. Relay IN pins sit at the relay board's VCC: that VCC must be a steady 3.3 V *before* the relay inputs are connected. The sonar ECHO divider is already on the board.
- The UNO Q STM32 died after the 3.3 V rail wandered while relay IN pins were attached. Do not repeat that on the ESP32.
- A DRV8833 module pushed in 180° rotated fits the holes. Check the plug-side bar before every insertion.
- The ESP32 fits the holes both ways round, but only one way is correct: USB-C ends toward the right edge, antenna end (the square pad, pin 1 of each row) at the left. Turned around, its 3V3 pins land on GND pads and its GND pins on the 3V3 pads.
- The UART header is the ESP32 console: unplug it while flashing.
