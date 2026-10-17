# PCB draft for review

The picture in `layout.png` is the real board, to scale, 133 mm by 93 mm. `board-draft.png` is only the earlier sketch. The file to upload for a quote is `abadi-rover-body.zip`. See `QUOTE.md`. `plan.md` still has the older TB6612 pin table until the owner approves a change.

## Board

- 2 copper layers, 1.6 mm thick.
- Top side: the modules, screw terminals, and capacitors.
- Bottom side: one solid ground plane. Every GND pin on the board joins that plane.
- The Raspberry Pi is not on this board. A USB cable from the Pi powers the ESP32 and carries commands.

## What plugs in

- ESP32-S3 development board, in a socket. Its 5V pin is left unconnected.
- DRV8833 for the two track motors. Same module type as the old one. Sleep jumper closed on the module. Fault pin unused.
- A second DRV8833 socket with its own four motor screws, for later. Same wiring pattern.
- PCA9685 servo board. Channels 0, 1, and 2 are the three neck servos. The 1000µF capacitor already on that board stays there.
- GY-521 gyro (MPU6050) on the same two I2C wires as the servo board.
- Two identical 3.3V two-channel relay boards. Board A is the two lights. Board B is spare.
- The larger adjustable buck from the photo, in place of the HW-133A. It is set to 3.3V.
- HW-183B boost, screw input, set to 7.0V under load. It feeds both motor drivers.
- Two 7-pin headers for the eye screens, and one 4-pin header for the ultrasonic sensor. Both are fitted and left unused for now.

## Power

- Quiet 5V from the power bank enters the buck. The buck's 3.3V output feeds both relay boards, the relay common terminals, the screen headers, and the light resistors.
- Noisy 5V, after the key switch, feeds the fan, the PCA9685 servo power terminal, and the HW-183B input.
- A 100µF capacitor and a 100nF capacitor sit on the buck's 3.3V output.
- A 100µF capacitor and a 100nF capacitor sit on the 7V output of the HW-183B.
- The ESP32 3.3V pin feeds only the PCA9685 logic pin and the gyro. It is not tied to the buck.
- One ground screw on the board is where the Pi's ground wire lands.

## Proposed ESP32 connections

These are not locked yet.

- GPIO 4, 5, 6, 7: track driver IN1, IN2, IN3, IN4.
- GPIO 15, 16, 17, 18: spare driver IN1, IN2, IN3, IN4.
- GPIO 8 SDA and GPIO 9 SCL: PCA9685 (address 0x40) and gyro (address 0x68).
- GPIO 1 and 2: relay board A.
- GPIO 38 and 39: relay board B.
- GPIO 13 left screen select, GPIO 14 right screen select, GPIO 21 data/command, GPIO 10 reset, GPIO 11 shared data, GPIO 12 shared clock.
- GPIO 41 ultrasonic trigger, GPIO 42 ultrasonic echo. Two resistors on the echo wire drop 5V down to 3.3V.
- GPIO 40: spare, broken out to a pin and nothing else.

## Small parts soldered by the factory

- Four capacitors listed above.
- Two 10Ω resistors for the existing lights, and two more 10Ω spots for the spare relay.
- Two resistors for the ultrasonic echo divider.

## Check these

- Track driver outputs: OUT1 and OUT2 are the left track. OUT3 and OUT4 are the right track.
- Servo plugs: brown or black is ground, red is the noisy 5V, orange is the signal.
- The ESP32 socket hole order must match the printing on the ESP32 board that is actually purchased.
- The buck footprint must match the module in the photo. Its part number was not readable.
