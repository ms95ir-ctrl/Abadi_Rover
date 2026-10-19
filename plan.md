**Current Status:** Phase 1 / Stage 1 (Power) — all wired; tests 1–5 passed (fan keep-awake confirmed 15 min). Remaining: servo 5V test (done in Stage 4), HW-183B 7.0V re-check under motor load (done in Stage 3). Stage 2 (gamepad): controller paired via Claude in App Lab; pending stick-value print test and reconnect test. Handover note for App Lab Claude: [HANDOVER.md](docs/HANDOVER.md).

# Abadi Rover — Build Plan

This file is the single source of truth for the rover. Wiring details for soldering are in [wiring.md](docs/wiring.md).

## Rules (for every session, human or AI)

1. Read this file first, starting with the **Current Status** line, before doing anything else.
2. The **Locked pin table** and **Locked power design** below must never be changed, renamed or "cleaned up" without explicit approval from the owner. On any conflict: stop and ask.
3. Work one stage at a time. No code for a later stage until the current stage passes its test on real hardware.
4. Any terminal or git command given to the owner must be written out in full, with an explanation of what it does.
5. Update the **Current Status** line whenever a stage passes or a test result changes.

## Scope

- **Phase 1 — Body:** power, Bluetooth gamepad, drive, neck servos, combined app with kill switch (ultrasonic sensor deferred to later; pins D2/D4 reserved). Done when the rover can be fully driven and steered by gamepad with no PC tether.
- **Phase 2 — Face:** both SPI screens showing simple eyes (blinking is enough).
- **Phase 3 — Extras:** App Lab AI functions, camera, USB audio. Not designed until Phases 1 and 2 are done and the owner asks.
- **Out of scope:** Hermes / AI agent on the rover, turret (Nerf X/Y, flywheel, solenoid), MAX98357A I2S amp (replaced by USB audio in Phase 3), ESP32-S3 (fallback only).

## Hardware

- Arduino UNO Q 2GB with screw-terminal shield
- ELEGOO Conqueror tracked chassis, 2× 1:48 TT-style geared motors
- DRV8833 dual H-bridge (J2 soldered: EEP/sleep permanently enabled)
- PCA9685 16-channel PWM driver (servos only)
- Servos: TZT MG996R (180°), Miuzei MZ996 (90°, to be confirmed), unlabeled 360° continuous (orange gear)
- HC-SR04 ultrasonic sensor
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
| **Brain** | Power bank USB-C port 2 → hub PD-IN | UNO Q (via hub USB-C cable), camera, USB audio |
| **Quiet 5V** | Spare hub USB port → USB-to-screw adapter | HC-SR04, input of Rail C |
| **Rail C (3.3V)** | HW-133A set to 3.3V, fed from Quiet 5V | Both screens, relay board, both lights (each light via ~10Ω through the relay contacts) |
| **Noisy 5V** | Power bank USB-A → USB-to-screw adapter → key switch | Fan (required keep-awake load), PCA9685 V+ (with bulk capacitor), HW-183B input |
| **Motor 7V** | HW-183B set to 7.0V **under load, on the power bank** | DRV8833 motor supply (VCC/VM) |
| **Charging** | Power bank USB-C port 1 | Kept free; unplug and charge with robot off |
| **Fallback** | 2S 5200mAh LiPo + 5A UBEC | Motors and servos only, if Noisy 5V fails a test. Power wiring changes only, never signal pins |

- **Common ground:** one star point. Every rail's minus goes there, plus one wire to a UNO Q GND screw.
- **Key switch:** cuts Noisy 5V only (motors, servos, fan). The UNO Q keeps running.
- **Never** feed power into the UNO Q's 5V, 3.3V or IOREF header pins.

## Locked pin table

### UNO Q pins

| UNO Q pin | Connects to | Rail / notes |
|---|---|---|
| D0 | Reserved (not used) | UART RX, kept for debugging |
| D1 | Reserved (not used) | UART TX, kept for debugging |
| D2 | HC-SR04 ECHO | 5V-tolerant input; ECHO must only ever go here |
| D3 | DRV8833 IN1 (left motor) | PWM |
| D4 | HC-SR04 TRIG | Digital out |
| D5 | DRV8833 IN2 (left motor) | PWM |
| D6 | DRV8833 IN3 (right motor) | PWM |
| D7 | Right screen CS | Digital out (Phase 2) |
| D8 | Both screens DC (shared) | Digital out (Phase 2) |
| D9 | DRV8833 IN4 (right motor) | PWM |
| D10 | Left screen CS | Digital out (Phase 2) |
| D11 | Both screens SDA (SPI MOSI, shared) | Hardware SPI (Phase 2) |
| D12 | Reserved (not used) | SPI MISO, claimed by SPI hardware |
| D13 | Both screens SCL (SPI SCK, shared) | Hardware SPI (Phase 2) |
| A0 | Both screens RST (shared) | Digital out (Phase 2) |
| A1 | Spare | — |
| A2 | Relay IN1 (light 1) | Digital out |
| A3 | Relay IN2 (light 2) | Digital out |
| A4 | Spare | — |
| A5 | Spare | — |
| D20 (SDA) | PCA9685 SDA | I2C |
| D21 (SCL) | PCA9685 SCL | I2C |
| 3.3V pin | PCA9685 VCC (logic only) | Output from UNO Q, a few mA |
| GND | Star ground point | Common ground |

### PCA9685 (I2C address 0x40, OE not connected, PWM frequency 50Hz)

| Channel | Servo | Role |
|---|---|---|
| CH0 | TZT MG996R (180°) | Decided in Stage 4 |
| CH1 | Miuzei MZ996 (90°?) | Decided in Stage 4 |
| CH2 | Unlabeled 360° continuous (orange gear) | Decided in Stage 4 |
| CH3–CH15 | Spare | — |

### DRV8833 outputs

| DRV8833 pin | Connects to |
|---|---|
| OUT1, OUT2 | Left track motor |
| OUT3, OUT4 | Right track motor |
| VCC (VM) | Motor 7V (HW-183B output) |
| GND | Star ground |
| EEP | Always on via soldered J2 |
| ULT (fault) | Not connected |

If a track runs backwards, swap that motor's two wires at OUT1/OUT2 or OUT3/OUT4 and note it in the calibration table. This does not change the pin table.

## Calibration table (editable — not locked)

| Item | Value | Date / notes |
|---|---|---|
| HW-183B output under load | 7.0V | Set on power bank, both motors running (bench). After final wiring it read 5.16V no-load; reset to 7.0V no-load, re-check under load in Stage 3 |
| HW-133A Rail C output | 3.3V | Set with relay board connected |
| CH0 MG996R min / max pulse (µs) | TBD | Stage 4 |
| CH0 role | TBD | Stage 4 |
| CH1 MZ996 min / max pulse (µs) | TBD | Stage 4 (confirm 90° vs 180°) |
| CH1 role | TBD | Stage 4 |
| CH2 360° stop pulse (µs) | TBD | Stage 4 (around 1500) |
| CH2 role | TBD | Stage 4 |
| Left motor wires swapped? | TBD | Stage 3 |
| Right motor wires swapped? | TBD | Stage 3 |
| Obstacle stop distance (cm) | TBD | Stage 5 |
| Relay trigger (active high / low) | TBD | Stage 5 |

## Phase 1 stages

### Stage 1 — Power

Results so far:

| Test | Result |
|---|---|
| 1. UNO Q boots on hub from power bank USB-C 2; camera plug/unplug ×3, no reboot | Passed |
| 2. Power bank USB-A gives 5V (after pressing bank button) | Passed |
| 3. Motors on USB-A: spinning and stall, UNO Q no reboot | Passed |
| 4. Fan as keep-awake load | Passed (15 min idle, still running) |
| 5. HW-183B at 7.0V under load on bank, both motors, stall (≈1V drop), warm not hot, no reboot | Passed |
| 6. Servo rail under servo movement | **Pending** |

- **Test 4 pass:** fan on Noisy 5V, motors idle for 5 minutes, then motors respond immediately without pressing the bank button.
- **Test 6 pass:** Noisy 5V stays at 4.5V or above at the PCA9685 V+ terminal while servos move (done during Stage 4).
- **Stage pass:** tests 4 and 6 pass, everything soldered per [wiring.md](docs/wiring.md), common ground checked with multimeter continuity.

### Stage 2 — Gamepad test (no motors)

- Pair the PS5-style controller to the UNO Q's Bluetooth on the Linux side.
- App Lab app with a custom brick that can read the input devices (`/dev/input`); it only prints stick and button values.
- **Pass:** each stick axis and the chosen buttons change the printed values; after turning the controller off and on, it reconnects and values print again without restarting the board.

### Stage 3 — Drive

- DRV8833 driven from UNO Q pins D3, D5, D6, D9; left stick controls both tracks (forward/back + turn mixing).
- Gradual speed ramping (no instant full-power jumps).
- Safety stop on the microcontroller: motors stop if no command arrives for 300 ms.
- **Pass (tracks lifted first, then on the floor):** forward, back, left and right turns respond correctly; motors stop within 0.5 s when the controller is switched off.

### Stage 4 — Neck servos

- Calibrate each servo on its PCA9685 channel: safe min/max pulse, 360° stop point, then decide pan/tilt roles. Record everything in the calibration table.
- Right stick moves the neck, with software limits just inside each servo's real range. The 360° servo uses speed/direction control, not angle.
- Run power test 6 here.
- **Pass:** smooth movement at moderate speed, no buzzing or stalling at the limits, no reboots.

### Stage 5 — Integration and kill switch

- One combined app: drive + neck.
- HC-SR04 deferred out of Phase 1 by owner decision (pins D2/D4 stay reserved). Obstacle stop will be added when it is wired.
- Gamepad kill button: motors stop and servos hold until re-armed. The key switch remains the hardware kill for everything that moves.
- App starts automatically at boot (no PC needed).
- **Pass:** drive and steer the rover around the room by gamepad with no PC connected; kill button works.

### Stage 6 — Phase 2: Screens

- Both ST7789 screens on the shared SPI bus (D11/D13), separate CS (D10 left, D7 right), shared DC (D8) and RST (A0), powered from Rail C (3.3V).
- **Pass:** both screens show simple eyes that blink.

## Lessons learned

- Lock the pinout early, and treat this file as the only source of truth.
- Validate every part against real datasheets and bench tests before writing code.
- Keep servo and motor power separate from logic and screen power.
- One phase at a time; confirm on real hardware before moving on.
- Set boost and buck converters on the source they will actually run from, with the real load connected.
