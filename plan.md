**Current Status:** Phase 1 / Stage 1 (Power) — passed 8 Nov 2026. Owner: every power rail meters correctly and the grounds are common. Next: Stage 2, solder the motherboard with the key off. The pin table further down is still the old TB6612 table. Do not solder signal wires from that table onto the printed board.

# Abadi Rover — Build Plan

This file is the single source of truth for the rover. Wiring details for soldering are in [wiring.md](wiring.md).

## Rules (for every session, human or AI)

1. Read this file first, starting with the **Current Status** line, before doing anything else.
2. The **Locked pin table** and **Locked power design** below must never be changed, renamed or "cleaned up" without explicit approval from the owner. On any conflict: stop and ask.
3. Work one stage at a time. No code for a later stage until the current stage passes its test on real hardware.
4. Any terminal or git command given to the owner must be written out in full, with an explanation of what it does.
5. Update the **Current Status** line whenever a stage passes or a test result changes.

## What finished looks like

The rover is bolted together, powered from its own battery, and driven by the gamepad with no PC attached. The Pi is the brain. The ESP32 moves the motors, servos, and lights. A camera lets it see people, faces, and objects, and tell which room of the house it is in after the rooms have been shown to it. It can speak, and be spoken to, in Arabic and English.

## Scope

- **Brain:** Raspberry Pi 5 (8GB). Gamepad, camera, speech. Talks to the ESP32 over USB serial.
- **Hands:** ESP32-S3 (dual USB-C, N16R8 or N8R2), seated on the printed motherboard. Motors, servos, relays, screens.
- **Phase 1 — Body:** power, solder the board, gamepad, drive, neck servos, lights, kill switch. Done when the rover can be driven around the room by gamepad with no PC.
- **Phase 2 — Face:** both screens showing simple eyes.
- **Phase 3 — See and talk:** camera, person / face / object detection, room recognition, Arabic and English speech. The owner asked for this on 7 Nov 2026.
- **Out of scope:** a general AI agent (Hermes or anything that browses or runs the computer on its own), a turret, the MAX98357A I2S amplifier, Arduino UNO Q, App Lab.

## Hardware

- Raspberry Pi 5 8GB (brain)
- ESP32-S3 dual USB-C DevKit (N16R8 or N8R2)
- Printed board: **Abadi Motherboard v5**, two layers, 100 mm by 100 mm. This is the board on the bench.
- ELEGOO Conqueror tracked chassis, 2× 1:48 TT-style geared motors
- Two DRV8833 modules in the sockets marked DRV8833 A and DRV8833 B
- PCA9685 16-channel PWM driver (servos only)
- Servos: TZT MG996R (180°), Miuzei MZ996 (90°, to be confirmed), unlabeled 360° continuous (orange gear)
- GY-521 gyro on the board
- HC-SR04 ultrasonic sensors (two footprints; still deferred)
- Relay channels on the board (three headers) + LED-filament lights
- 2× GMT020-02 2.0" SPI TFT (ST7789, 240×320)
- Two Li-ion cells, a 2S protection board (B−, BM, B+, P−, P+), and a USB-C charger
- XL4016 buck (Pi only), one buck for CLEAN 5V IN (label still to be read), LM2596 HW-411 (servos), one 3.3 V module
- Key switch on the P+ wire, before the five fuses. Off kills the whole robot. The charger stays on the battery side of the key.
- 5V cooling fan
- USB webcam SC-012-SN259
- A speaker the Pi can drive (USB speaker, or the headphone jack into a powered speaker)
- A microphone if the webcam does not have one

The power bank, hub, HW-183B, and HW-133A were retired by the owner on 7 Nov 2026.

## Locked power design

Owner decisions, 7 Nov 2026. Each buck has its own two wires onto the protection board. The outputs stay separate.

| Rail | Source | Set to | Lands on |
|---|---|---|---|
| **Pack** | Cells through the BMS. Charger on **P+** and **P−** | About 6 V empty to 8.4 V full | **BATT IN +** and **BATT IN −** |
| **Pi** | XL4016 input from **P+** and **P−** | **5.10 V** | Pi USB-C power port only |
| **Clean 5V** | Its own buck, input from **P+** and **P−** | **5.00 V** | **CLEAN 5V IN +** and its minus pad |
| **Servo 5V** | LM2596 HW-411, input from **P+** and **P−** | **5.00 V** | **SERVO 5V IN +** and its minus pad |
| **3.3V** | 3.3 V module, input from **P+** and **P−** | **3.30 V** | **3.3V IN +** and its minus pad |
| **ESP32** | Pi USB-A → ESP32 **COM** USB-C | — | ESP32 only. Leave the ESP32 5V pin on the motherboard empty |

Fuses, set 7 Nov 2026 from the five fuses on hand. Every fuse is on a plus wire. P- has no fuse. There is no main fuse: the red jumper from P+ to the five fuses stays short. The picture is [power-cabling.png](power-cabling.png).

| Fuse on hand | Where it sits | Wire |
|---|---|---|
| **6.3 A** | XL4016 input plus (the Pi) | 18 AWG |
| **5 A** | BATT IN + | 18 AWG |
| **5 A** | LM2596 input plus | 20 AWG |
| **2 A** | Clean 5 V buck input plus | 22 AWG |
| **2 A** | 3.3 V module input plus | 22 AWG |

The charger stays on P+ and P- with no fuse of its own, on the battery side of the key. The key is the next thing on the P+ wire. Everything to the right of the key — Pi, clean 5 V, 3.3 V, motors, and servos — dies when the key is off. The 6.3 A fuse is on the Pi because that rail is the heavy one. One 5 A fuse is on the motor wire because a stalled track is the big fault. The other 5 A is on the servo buck: it opens if that wire shorts. The LM2596 itself stops around 3 A, so the fuse is not what limits a stall.

What each board pad feeds:

- **BATT IN** feeds the motor-driver power pins and the 470 µF capacitor. Two cells is the highest this board takes. DRV8833 power must stay under 10.8 V.
- **CLEAN 5V IN** feeds the sonar VCC pins and the POWER OUT 5 V pins.
- **SERVO 5V IN** feeds the PCA9685 V+ pin. The LM2596 is a 3 A converter. Normal neck moves are fine. If all three servos stall, it will get hot and the voltage will sag.
- **3.3V IN** feeds both screens, the three relay VCC pins, the gyro, and the POWER OUT 3.3 V pins.
- The ESP32 makes its own 3.3 V when the USB cable from the Pi is plugged in. That 3.3 V feeds the PCA9685 logic pin and the I2C header.
- **POWER OUT** is a tap for later. Converters land on the **IN** pads.

Rules that stay in force:

- Set every buck with the meter **before** the output wire touches the Pi or the board. These modules often wake up near the full pack voltage.
- The Pi is powered only through its USB-C power port. Do not use the Pi header 5 V pins. The USB-C plug needs a **5.1 kΩ** resistor from the CC pin to ground, or the Pi can stay off.
- Do not feed the ESP32 5V/VIN pin from a buck.
- All minus wires join the board ground. Add one wire from a Pi header GND and one extra wire from an ESP32 GND pin. Do not rely on the USB cable alone for motor ground.
- The key switch sits in the single **P+** wire, next to the BMS, before the five fuses. Off kills the whole robot. **B−**, **BM**, and **B+** stay soldered to the cells. Shut the Pi down from its menu when you can. The key is the hard off, and it cuts the Pi too. The gamepad kill button is the one that stops the motors while the Pi stays on.
- Measure 3.30 V on the 3.3 V rail **before** any relay IN wire is connected. A wandering 3.3 V rail already killed the old controller.
- Charge with the key switch off. Unplug the charger when a cell reaches 4.20 V or the pack reaches 8.40 V. Unplug if the cells drift more than about 0.1 V apart, or if a cell gets hot.

## Locked pin table

This table is still the TB6612 table from before the printed board. The board on the bench is Motherboard v5. It has two DRV8833 sockets. The silk on that board is the map for those sockets. **Do not solder the signal wires in this table onto that board.** Power pads are already settled above. Signal pins get a new lock only after we read the silk together, and only before the drive stage.

### ESP32-S3 pins (hands)

Pins chosen so both N16R8 and N8R2 boards work. Do not use GPIO 19/20 (USB), GPIO 0/45/46 (boot), GPIO 43/44 (USB-serial), or GPIO 33–37 (flash on N16R8).

| ESP32 pin | Connects to | Rail / notes |
|---|---|---|
| GPIO 4 | TB6612 PWMA (left speed) | PWM |
| GPIO 5 | TB6612 AIN1 (left dir) | Digital out |
| GPIO 6 | TB6612 AIN2 (left dir) | Digital out |
| GPIO 7 | TB6612 PWMB (right speed) | PWM |
| GPIO 15 | TB6612 BIN1 (right dir) | Digital out |
| GPIO 16 | TB6612 BIN2 (right dir) | Digital out |
| GPIO 17 | TB6612 STBY | Must be HIGH to move. Leave unconnected until code runs (stays off) |
| GPIO 8 | PCA9685 SDA | I2C |
| GPIO 9 | PCA9685 SCL | I2C |
| GPIO 1 | Relay IN1 (light 1) | Digital out |
| GPIO 2 | Relay IN2 (light 2) | Digital out |
| GPIO 11 | Both screens SDA (SPI MOSI, shared) | Hardware SPI (Phase 2) |
| GPIO 12 | Both screens SCL (SPI SCK, shared) | Hardware SPI (Phase 2) |
| GPIO 13 | Left screen CS | Digital out (Phase 2) |
| GPIO 14 | Right screen CS | Digital out (Phase 2) |
| GPIO 21 | Both screens DC (shared) | Digital out (Phase 2) |
| GPIO 10 | Both screens RST (shared) | Digital out (Phase 2) |
| GPIO 41 | HC-SR04 TRIG | Digital out (deferred) |
| GPIO 42 | HC-SR04 ECHO | **3.3V only.** Use a voltage divider. ESP32 is not 5V-tolerant |
| 3.3V pin | PCA9685 VCC (logic only) | A few mA |
| GND | Star ground (extra wire) | Plus the USB ground to the Pi |
| COM USB-C | Raspberry Pi 5 USB-A | Power + serial |

### Raspberry Pi 5 (brain)

| Pi connection | Connects to | Notes |
|---|---|---|
| USB-C power | XL4016 output, 5.10 V, with the 5.1 kΩ CC resistor | Only power for the Pi |
| USB-A | ESP32 COM USB-C | Power + commands |
| USB-A | Webcam | Phase 3 |
| Audio | Speaker, and a microphone if the camera has none | Phase 3 |
| Header GND | Board ground (one wire) | Do not use header 5V |
| Bluetooth | PS5-style gamepad | Software, no extra wire |

### PCA9685 (I2C address 0x40, OE not connected, PWM frequency 50Hz)

| Channel | Servo | Role |
|---|---|---|
| CH0 | TZT MG996R (180°) | Decided in the servo stage |
| CH1 | Miuzei MZ996 (90°?) | Decided in the servo stage |
| CH2 | Unlabeled 360° continuous (orange gear) | Decided in the servo stage |
| CH3–CH15 | Spare | — |

On the printed board the PCA9685 V+ pin is the SERVO 5V rail. The VCC logic pin is the ESP32's own 3.3 V. Servo plugs face the bottom edge. The power terminal faces up.

### Motor outputs on the printed board

DRV8833 A feeds M1 and M2. DRV8833 B feeds M3 and M4. The chassis has two track motors. Which pair is the left track and which is the right track is decided in the drive test. If a track runs backwards, swap that motor's two wires and write it in the calibration table.

The pin marked VCC on each DRV8833 outline is already tied to BATT IN. No extra power wire goes there.

## Calibration table (editable — not locked)

| Item | Value | Date / notes |
|---|---|---|
| Cell A / cell B on the BMS | 3.83 V / 3.84 V, pack about 7.7 V | 7 Nov 2026, before charge |
| Charger open-circuit | 8.5 V | 7 Nov 2026 |
| Charge check | 3.84 V / 3.84 V / 7.69 V, then 3.87 V / 3.87 V / 7.74 V | 7 Nov 2026, cells matched |
| XL4016 output | 5.10 V | Set with the meter before it touches the Pi |
| Clean 5 V buck output | 5.00 V | Module label still to be read |
| LM2596 HW-411 output | 5.00 V | Set with the meter before it touches SERVO 5V IN |
| 3.3 V module output | 3.30 V | Set with the meter before it touches 3.3V IN |
| Rails on the board | Match the set points, common ground | 8 Nov 2026, owner confirmed. Stage 1 passed |
| CH0 MG996R min / max pulse (µs) | TBD | Servo stage |
| CH0 role | TBD | Servo stage |
| CH1 MZ996 min / max pulse (µs) | TBD | Servo stage (confirm 90° vs 180°) |
| CH1 role | TBD | Servo stage |
| CH2 360° stop pulse (µs) | TBD | Servo stage (around 1500) |
| CH2 role | TBD | Servo stage |
| Left motor wires swapped? | TBD | Drive stage |
| Right motor wires swapped? | TBD | Drive stage |
| Obstacle stop distance (cm) | TBD | Later |
| Relay trigger (active high / low) | TBD | Lights stage |
| HW-183B output under load | 7.0 V | Old power-bank setup. Retired 7 Nov 2026 |
| HW-133A Rail C output | 3.3 V | Old power-bank setup. Retired 7 Nov 2026 |

## Stages

One stage at a time. Do not start the next until the current one has passed on the real robot.

### Stage 1 — Finish power (next, when you are back)

The charger can still be running. Outputs of the bucks stay free until the meter is right.

1. Read the label on the clean 5 V buck and on the 3.3 V module.
2. Wire each buck input, plus to **P+** and minus to **P−**, with its own pair of wires. The charger stays on those posts.
3. Meter each output and turn the screw until it reads: XL4016 **5.10 V**, clean buck **5.00 V**, LM2596 **5.00 V**, 3.3 V module **3.30 V**.
4. Then connect the outputs: XL4016 to the Pi USB-C plug (with the 5.1 kΩ resistor), clean buck to **CLEAN 5V IN**, LM2596 to **SERVO 5V IN**, 3.3 V module to **3.3V IN**. Each minus goes to that pair's minus pad.
5. The key switch is the plus wire from **P+** to the five fuses. **BATT IN** minus and every buck minus go to **P−**.
6. Turn the key on. Meter the four IN pads on the board. They must match the table. Nothing gets hot.

**Pass:** on the board, BATT IN reads the pack voltage, CLEAN 5V IN and SERVO 5V IN read 5.00 V, and 3.3V IN reads 3.30 V. The Pi is connected only after the XL4016 meter reads 5.10 V. No wire is warm after a minute.

### Stage 2 — Solder the motherboard and test the rails on it

Solder small parts first.

1. The 100 nF capacitors, then C2 100 µF 10 V, then C1 470 µF 16 V. The stripe on a can is the minus leg. The silk plus mark is the plus leg.
2. Pin headers.
3. ESP32, USB-C end on the silk mark, antenna over the empty rectangle.
4. Both DRV8833 modules. The silk says which way the white plug faces.
5. GY-521 on its outline.
6. PCA9685. Servo plugs face the bottom edge. The power terminal faces up.
7. Leave screens, sonars, and relay IN wires off.

Power it from the bucks with the key on. Meter BATT IN, CLEAN 5V IN, SERVO 5V IN, and 3.3V IN again on the board. Meter the DRV8833 VCC pin: it must read the pack voltage, not 5 V and not 3.3 V.

**Pass:** rails still correct with the modules seated, no part hot, ESP32 5V pad still empty.

### Stage 3 — Pi and ESP32

1. XL4016 at 5.10 V into the Pi USB-C power port.
2. Pi USB-A into the ESP32 COM USB-C.
3. One ground wire from a Pi header GND to the board. One extra ground wire from an ESP32 GND pin to the board.
4. Leave the Pi header 5 V pin empty.

**Pass:** the Pi stays up for 5 minutes and the ESP32 shows up. Key off, the Pi goes dark. Key on, it boots again.

### Stage 4 — Gamepad (no motors)

- Pair the PS5-style controller to the Pi 5 Bluetooth.
- A small program on the Pi that only prints stick and button values.
- **Pass:** each stick and the chosen buttons change the printed values. After the controller is switched off and on, it reconnects without restarting the Pi.

### Stage 5 — Drive

Confirm the signal pin lock against the motherboard silk before any motor signal is soldered. The ESP32 stops the motors if no command arrives for 300 ms.

- Tracks lifted off the table first, then on the floor.
- Left stick drives both tracks.
- **Pass:** forward, back, left, and right. Motors stop within 0.5 s when the controller is switched off. Key switch also stops them.

### Stage 6 — Neck servos

- Calibrate each servo. Record the pulses in the table.
- Right stick moves the neck. The 360° servo uses speed and direction, not an angle.
- Watch the LM2596. If it gets hot or the servo rail falls away from 5 V, stop and say so.
- **Pass:** smooth movement, no buzzing at the ends of travel, no Pi reboot.

### Stage 7 — Lights

Relay VCC is the 3.3 V rail. Measure 3.30 V again before the IN wires go on.

- **Pass:** each light turns on and off from the gamepad. The 3.3 V rail stays at 3.30 V.

### Stage 8 — Screens

Both screens on the headers marked SCREEN L and SCREEN R, powered from the 3.3 V rail.

- **Pass:** both screens show simple eyes that blink.

### Stage 9 — Assemble the body

Bolt the board, the Pi, the pack, and the bucks onto the chassis. Keep the cell tabs covered. Keep wires off the tracks and off the pots, so the voltage screws can still be turned. Mount the camera so it looks forward. Mount the speaker. Tie the pack down so it cannot slide into the tracks.

- **Pass:** drive around the room by gamepad, no PC. The gamepad kill button stops the motors and the Pi stays up. The key switch then kills the whole robot.

### Stage 10 — Camera

Plug the webcam into the Pi. A small program shows the live picture.

- **Pass:** the picture is the right way up and updates while the rover sits still.

### Stage 11 — Person, face, and objects

One program on the Pi, using the camera, with no internet required.

- It draws a box on a person.
- It draws a box on a face.
- It names a few ordinary objects it was built to know (a cup, a chair, a person).
- **Pass:** in a lit room it marks you, marks your face, and names at least one object that is really there.

### Stage 12 — Remember a face

Show it your face once and give it your name. Later it greets you by that name when it sees you. A stranger stays "a person."

- **Pass:** it greets you, and it does not use your name for someone else in the same light.

### Stage 13 — Rooms of the house

There is no indoor GPS. The robot learns rooms by being shown them.

- Walk it to a room. Tell it the room name. It saves a few pictures.
- Do that for the rooms you care about.
- It remembers the last room it named, so it can say it moved from one to the next.
- **Pass:** shown three rooms, then taken back without being told the name, it names the room correctly in normal daylight. Expect mistakes in the dark or after the furniture moves. Those misses get written in the calibration table, not patched in silence.

### Stage 14 — Arabic and English

A speaker on the Pi. A microphone, or the camera's microphone if it has one. Speech runs on the Pi, with no website required.

- It says a short sentence in English, then the same sentence in Arabic.
- You speak a short sentence in either language. It answers in the language it heard.
- **Pass:** both directions work in a quiet room. The motors still stop if the Pi is busy and stops sending commands.

### Stage 15 — One robot

One program: gamepad drive and neck, eyes, lights, and the seeing and talking from the stages above. It can say what it sees and which room it is in, in Arabic or English. The gamepad kill button stops motion while the Pi stays on. The key switch cuts power to the whole robot.

- **Pass:** drive it through two rooms, no PC. It names the room, notices a person, and answers one spoken sentence. Kill switch works.

## Lessons learned

- Lock the pinout early, and treat this file as the only source of truth.
- Validate every part against real datasheets and bench tests before writing code.
- Keep servo power, motor power, and the Pi on separate converters.
- One stage at a time. Confirm on real hardware before moving on.
- Set every buck from the pack it will really run on, with the meter, before the output is connected. Check again with the real load.
- ESP32 pins are not 5V-tolerant. Relay IN pins sit at the relay board's VCC. That VCC must be a steady 3.3 V before IN is connected. Sonar ECHO needs a divider. The board already has 1k and 2k resistors beside each sonar for that divider.
- The UNO Q STM32 died after the 3.3 V rail wandered while relay IN pins were attached. Do not repeat that on the ESP32.
- The printed board's motor pins are DRV8833 sockets. The old TB6612 pin names stay in the locked table until the owner replaces them.
