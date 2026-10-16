**Current Status:** Phase 1 / Stage 1 (Power) — RESTARTED on Raspberry Pi 5 8GB + ESP32-S3. Motor driver is now TB6612FNG. Old UNO Q / DRV8833 pin table is retired. New pin table locked below. Pending: Pi 5 boots on the hub from the power bank; star ground includes Pi GND and ESP32 GND.

# Abadi Rover — Build Plan

This file is the single source of truth for the rover. Wiring details for soldering are in [wiring.md](wiring.md).

## Rules (for every session, human or AI)

1. Read this file first, starting with the **Current Status** line, before doing anything else.
2. The **Locked pin table** and **Locked power design** below must never be changed, renamed or "cleaned up" without explicit approval from the owner. On any conflict: stop and ask.
3. Work one stage at a time. No code for a later stage until the current stage passes its test on real hardware.
4. Any terminal or git command given to the owner must be written out in full, with an explanation of what it does.
5. Update the **Current Status** line whenever a stage passes or a test result changes.

## Scope

- **Brain:** Raspberry Pi 5 (8GB). Gamepad, later camera. Talks to the ESP32 over USB serial.
- **Hands:** ESP32-S3 (dual USB-C, N16R8 or N8R2). Motors, servos, relays, later screens.
- **Phase 1 — Body:** power, Bluetooth gamepad, drive, neck servos, combined app with kill switch (ultrasonic sensor deferred; GPIO 41/42 reserved). Done when the rover can be fully driven and steered by gamepad with no PC tether.
- **Phase 2 — Face:** both SPI screens showing simple eyes (blinking is enough).
- **Phase 3 — Extras:** camera, USB audio. Not designed until Phases 1 and 2 are done and the owner asks.
- **Out of scope:** Hermes / AI agent on the rover, turret, MAX98357A I2S amp, Arduino UNO Q, App Lab, old DRV8833 board.

## Hardware

- Raspberry Pi 5 8GB (brain)
- ESP32-S3 dual USB-C DevKit (N16R8 or N8R2)
- ELEGOO Conqueror tracked chassis, 2× 1:48 TT-style geared motors
- TB6612FNG dual motor driver (SparkFun-style red board)
- PCA9685 16-channel PWM driver (servos only)
- Servos: TZT MG996R (180°), Miuzei MZ996 (90°, to be confirmed), unlabeled 360° continuous (orange gear)
- HC-SR04 ultrasonic sensor (deferred)
- 2-channel 3.3V relay board (JQC-3F 03VDC) + 2 LED-filament lights
- 2× GMT020-02 2.0" SPI TFT (ST7789, 240×320)
- 20000mAh 45W PD power bank (2× USB-C PD, 1× USB-A)
- Benfei USB-C hub (PD-IN passthrough)
- HW-183B boost converter (motors), HW-133A buck converter (3.3V rail)
- 5V cooling fan, key switch (bulk capacitor: 1000µF already on the PCA9685 board)
- USB webcam SC-012-SN259 (Phase 3)

## Locked power design

| Rail | Source | Feeds |
|---|---|---|
| **Brain** | Power bank USB-C port 2 → hub PD-IN | Raspberry Pi 5 (hub USB-C cable into the Pi USB-C power port) |
| **ESP32** | Pi USB-A → ESP32 **COM** USB-C | ESP32 board only. Do not also feed VIN from another rail |
| **Quiet 5V** | Spare hub USB port → USB-to-screw adapter | HC-SR04, input of Rail C |
| **Rail C (3.3V)** | HW-133A set to 3.3V, fed from Quiet 5V | Both screens, relay board, both lights (each light via ~10Ω through the relay contacts), TB6612 **VCC** (logic only) |
| **Noisy 5V** | Power bank USB-A → USB-to-screw adapter → key switch | Fan (required keep-awake load), PCA9685 V+ (with bulk capacitor), HW-183B input |
| **Motor 7V** | HW-183B set to 7.0V **under load, on the power bank** | TB6612 **VM** only |
| **Charging** | Power bank USB-C port 1 | Kept free; unplug and charge with robot off |
| **Fallback** | 2S 5200mAh LiPo + 5A UBEC | Motors and servos only, if Noisy 5V fails a test. Power wiring changes only, never signal pins |

- **Common ground:** one star point. Every rail's minus goes there, plus **one wire from a Pi 5 header GND** and **one extra wire from an ESP32 GND pin**. Do not rely on USB ground alone for motors.
- **Key switch:** cuts Noisy 5V only (motors, servos, fan). The Pi and ESP32 keep running.
- **Never** feed power into the Pi 5 GPIO 5V pins, or into the ESP32 5V/VIN pin. The Pi is powered only through its USB-C port. The ESP32 is powered only through USB from the Pi.
- **Pi 5 power:** official need is about 5V / 5A. If the Pi shows a lightning bolt or reboots, the hub is not passing enough power.

## Locked pin table

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
| USB-C power | Hub USB-C cable | Only power for the Pi |
| USB-A | ESP32 COM USB-C | Power + commands |
| Header GND | Star ground (one wire) | Do not use header 5V |
| Bluetooth | PS5-style gamepad | Software, no extra wire |

### PCA9685 (I2C address 0x40, OE not connected, PWM frequency 50Hz)

| Channel | Servo | Role |
|---|---|---|
| CH0 | TZT MG996R (180°) | Decided in Stage 4 |
| CH1 | Miuzei MZ996 (90°?) | Decided in Stage 4 |
| CH2 | Unlabeled 360° continuous (orange gear) | Decided in Stage 4 |
| CH3–CH15 | Spare | — |

### TB6612FNG outputs

| TB6612 pin | Connects to |
|---|---|
| AO1, AO2 | Left track motor |
| BO1, BO2 | Right track motor |
| VM | Motor 7V (HW-183B output) |
| VCC | Rail C 3.3V |
| All GND pins | Star ground |
| STBY | ESP32 GPIO 17 |
| PWMA, AIN1, AIN2 | ESP32 GPIO 4, 5, 6 |
| PWMB, BIN1, BIN2 | ESP32 GPIO 7, 15, 16 |

If a track runs backwards, swap that motor's two wires at AO1/AO2 or BO1/BO2 and note it in the calibration table. This does not change the pin table.

## Calibration table (editable — not locked)

| Item | Value | Date / notes |
|---|---|---|
| HW-183B output under load | 7.0V | Set on power bank, both motors running (bench). Re-check under load in Stage 3 |
| HW-133A Rail C output | 3.3V | Set with relay board connected |
| CH0 MG996R min / max pulse (µs) | TBD | Stage 4 |
| CH0 role | TBD | Stage 4 |
| CH1 MZ996 min / max pulse (µs) | TBD | Stage 4 (confirm 90° vs 180°) |
| CH1 role | TBD | Stage 4 |
| CH2 360° stop pulse (µs) | TBD | Stage 4 (around 1500) |
| CH2 role | TBD | Stage 4 |
| Left motor wires swapped? | TBD | Stage 3 |
| Right motor wires swapped? | TBD | Stage 3 |
| Obstacle stop distance (cm) | TBD | Later |
| Relay trigger (active high / low) | TBD | Stage 5 |

## Phase 1 stages

### Stage 1 — Power

Old bank / hub / fan / 7V / 3.3V tests already passed on this power hardware. New checks:

| Test | Result |
|---|---|
| 1. Pi 5 boots on hub from power bank USB-C 2; stays up 5 min; ESP32 enumerates on Pi USB | **Pending** |
| 2–5. Bank USB-A, motors, fan keep-awake, HW-183B 7.0V | Passed earlier (same rails) |
| 6. Servo rail under servo movement | **Pending** (Stage 4) |

- **Stage pass:** test 1 passes, TB6612 VM/VCC/GND wired, common ground includes Pi + ESP32, no signal pins to the TB6612 until Stage 3.

### Stage 2 — Gamepad test (no motors)

- Pair the PS5-style controller to the **Pi 5 Bluetooth**.
- A small program on the Pi that only prints stick and button values.
- **Pass:** each stick axis and the chosen buttons change the printed values; after turning the controller off and on, it reconnects without restarting the Pi.

### Stage 3 — Drive

- TB6612 driven from ESP32 GPIO 4, 5, 6, 7, 15, 16, 17. Pi sends stick values over USB serial. Left stick controls both tracks.
- Gradual speed ramping. ESP32 safety stop: motors stop if no command arrives for 300 ms. STBY goes low on stop.
- **Pass (tracks lifted first, then on the floor):** forward, back, left and right turns; motors stop within 0.5 s when the controller is switched off.

### Stage 4 — Neck servos

- Calibrate each servo on its PCA9685 channel. Record in the calibration table.
- Right stick moves the neck. The 360° servo uses speed/direction, not angle.
- Run power test 6 here.
- **Pass:** smooth movement, no buzzing or stalling at the limits, no Pi reboot.

### Stage 5 — Integration and kill switch

- One combined app on the Pi: drive + neck, talking to the ESP32.
- HC-SR04 still deferred (GPIO 41/42 stay reserved).
- Gamepad kill button: motors stop and servos hold until re-armed. Key switch remains the hardware kill.
- App starts automatically at boot (no PC needed).
- **Pass:** drive the rover around the room by gamepad with no PC; kill button works.

### Stage 6 — Phase 2: Screens

- Both ST7789 screens on shared SPI (GPIO 11/12), CS GPIO 13 left / GPIO 14 right, shared DC GPIO 21 and RST GPIO 10, powered from Rail C (3.3V).
- **Pass:** both screens show simple eyes that blink.

## Lessons learned

- Lock the pinout early, and treat this file as the only source of truth.
- Validate every part against real datasheets and bench tests before writing code.
- Keep servo and motor power separate from logic and screen power.
- One phase at a time; confirm on real hardware before moving on.
- Set boost and buck converters on the source they will actually run from, with the real load connected.
- ESP32 pins are **not** 5V-tolerant. Relay IN pins sit at the relay board's VCC — that VCC must be a steady 3.3V *before* IN1/IN2 are connected. HC-SR04 ECHO needs a divider.
- The UNO Q STM32 died after the 3.3V rail wandered while relay IN pins were attached. Do not repeat that on the ESP32.
