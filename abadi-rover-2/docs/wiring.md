# Abadi Rover 2: wiring (the final table and the decisions behind the diagram)

Diagram: `../diagrams/wiring-robot2.png` (and `.svg`). Battery part only: `../../pcb/kicad/battery-wiring.png`. Power part of the motherboard: `../../pcb/kicad/power-wiring.png`.
Pin numbers come from `../../pcb/kicad/pin-table.md` (locked). Nothing here changes the motherboard or robot 1.

**Words.** SBC = the Raspberry Pi. Buck = a module that lowers a voltage. Splice = the lever connector where every branch takes its plus (+) from the switched battery. Pack = the 2S Li-ion battery, 6.0 to 8.4 V.
**Marks.** VERIFIED = seen in a file or source. ASSUMED = my choice or guess, test it. Everything below is a plan; no part has been built or measured yet.

---

## 1. What the diagram shows, in one minute

- **One battery pack, one main switch, one splice.** From the splice, **four branches**, each with its own fuse. Black wires all go back to one minus lever connector.
- **Branch 1, BATT IN (5 A slow-blow):** raw pack voltage to the motherboard terminal BATT IN. It feeds only the DRV8833 motor driver, so the two drive motors get the pack voltage.
- **Branch 2, servo buck (5 A fuse, XL4016 set to 5.0 V):** to the terminal SERVO 5V IN. It feeds the PCA9685 and the pan and tilt servos only.
- **Branch 3, clean 5 V (2 A fuse, fixed 1.8 A buck):** to the terminal CLEAN 5V IN. It feeds the ESP32 (through diode D1), the two sonars, and nothing noisy.
- **Branch 4, Raspberry Pi (5 A fuse, second XL4016 set to 5.1 V):** goes to the Pi's USB-C power input through a USB-C plug with bare wires, with a 1000 uF capacitor at the Pi end. From the same 5.1 V wire a second wire runs through a **1 A fuse** to the 7 inch screen's power lead (and the speaker amplifier, if route B sound is used).
- **The 3.3 V terminal and the second motor driver are not used** in robot 2. No SPI screens, no relays.
- **Data cables:** HDMI Pi to screen; USB webcam; USB audio adapter; USB touch (data only); USB Pi to ESP32 COM socket (data only, section 3).

---

## 2. Decisions I made on the helpers' conflicts

| # | Question | Decision | Reason |
|---|---|---|---|
| C1 | Where does the screen get its power? | From the **5.1 V Pi buck**, through its own **1 A slow-blow fuse**. Not from POWER OUT. | Keeps the backlight noise off the ESP32's clean 5 V and leaves the 1 A POWER OUT budget alone. The diagram shows it. |
| C2 | HDMI cable length | **0.8 m**, flat and thin | The mast route needs about 0.65 m. |
| C7 | 3.3 V buck, fuse count | Buy **one** fixed buck (5 V). **Five** fuse holders: BATT IN, servo buck, clean 5 V, Pi buck, screen. | Robot 2 does not use 3.3 V rails. |
| C9 | Two 5 V sources on the ESP32 USB cable and on the touch cable | **Data-only cables** (or tape the 5 V contact of the USB-C plug), for the ESP32 link and the touch link. | The ESP32 is already fed from CLEAN 5V IN. Two 5 V sources that are not joined by a diode can fight. ASSUMED: I did not check the devkit schematic; the data-only cable is the safe side. |
| C6 | Motor voltage setting in the software | `mot_vmax` about **8 V** for the Pololu 12 V motors (not the 6 V default) | It is a setting, not a wiring change. Speed is about 0.29 m/s at 6 V and 0.36 m/s at 7.4 V. |
| C10 | LED dimming on the PCA9685 | Camera LED **on or off only** | All PCA9685 channels share one PWM speed (50 Hz); dimming would flicker. |
| C3, C4, C5, C8, C12 | Charging while on, runtime, mass, the place for speaker and button, Pi 5 USB limit | **Not decided here.** They are the open questions in section 6. | They need the owner's answer or a bench measurement. |

---

## 3. The wiring table (every electrical part)

"Pack" = after the main switch. All grounds are one common ground.

| Part | Connects to | Voltage | Current (ASSUMED unless marked) | Connector |
|---|---|---|---|---|
| Battery cells (2 in series, or 4 as 2S2P) | BMS B-, BM, B+ in that order (see `battery-wiring.png`) | 6.0 to 8.4 V | 2 to 4 A typical, up to 10 A peak | holder wires or solder tags |
| BMS, charger board, main switch | pack plus through the switch to the splice; minus to the splice minus; charger board between BMS and splice | 6.0 to 8.4 V | 10 A max (BMS) | wires, spade lugs |
| Fuse, BATT IN | splice plus to the BATT IN terminal (+) | 6.0 to 8.4 V | 5 A slow-blow | 5 x 20 mm in-line holder, 5.08 mm screw terminal |
| XL4016 #1, servos | in from splice through a 5 A fuse; out to SERVO 5V IN | out 5.0 V | up to 5 A | lever and screw terminal |
| Fixed 5 V buck | in from splice through a 2 A fuse; out to CLEAN 5V IN | out 5.0 V | 0.5 A typical | lever and screw terminal |
| XL4016 #2, Pi | in from splice through a 5 A fuse; out to the Pi pigtail and the screen lead | out **5.1 V**, set with a meter at the Pi under load | 1 to 1.5 A typical, 3 A (Pi 4) or 5 A (Pi 5) peak | lever; wire to the pigtail |
| Raspberry Pi 5 | USB-C pigtail from XL4016 #2, 1000 uF capacitor across 5.1 V and GND at the Pi end | 5.1 V | see above | USB-C plug with bare wires, AWG 18, under 40 cm |
| 7 inch screen | 5.1 V through a 1 A fuse to its micro-USB power lead; HDMI to the Pi HDMI0 | 5.1 V | 0.5 A (VERIFIED for the Waveshare 7 inch (C)) | micro-USB pigtail, micro-HDMI to HDMI-A |
| Screen touch | Pi USB port | data only | 0 | micro-USB to USB-A, data only |
| USB webcam | Pi blue USB 3 port | 5 V from the Pi | 0.2 to 0.3 A | USB-A |
| USB audio adapter or speakerphone | Pi USB 2 port | 5 V from the Pi | 0.05 to 0.5 A | USB-A |
| Speaker amplifier (route B) | 5.1 V after the screen fuse; input from the USB audio adapter | 5.1 V | up to 0.6 A | 2 wires, 3.5 mm plug |
| ESP32 devkit | motherboard J1 and J3 sockets; 5 V via D1 from CLEAN 5V IN; **COM USB-C** to the Pi | 5 V | 0.15 to 0.3 A | sockets; USB-A to USB-C data-only |
| Left motor | terminal **M1** (DRV A out 1 and 2; IN1A GPIO4, IN2A GPIO16) | pack voltage, pulsed | 0.2 to 0.4 A working, 1.26 A stall at 8.4 V | JST 2-pin |
| Right motor | terminal **M2** (DRV A out 3 and 4; IN3A GPIO1, IN4A GPIO5) | pack voltage, pulsed | same | JST 2-pin |
| Pan servo | PCA9685 channel 0 | 5.0 V | 0.1 to 0.5 A, stall about 2.5 A | 3-pin servo plug and extension cable |
| Tilt servo | PCA9685 channel 1 | 5.0 V | same | same |
| Camera-live LED | PCA9685 channel 2 signal, 220 Ohm, LED, GND pin | 3.3 V logic | 6 mA | servo-type 3-pin plug (signal and GND used) |
| Button light (optional) | PCA9685 channel 3 | 3.3 V logic | 6 mA | same |
| Sonar 1 and 2 | SONAR 1 and 2 headers (5 V, TRIG GPIO12, ECHO GPIO13 and GPIO14, GND) | 5 V | 15 mA each | 4-pin 2.54 mm or JST-XH |
| Cliff sensor left | SPARE IO pin 8 (GPIO21), 3V3 pin 2, GND pin 1 | 3.3 V | 20 to 30 mA | 3-wire plug |
| Cliff sensor right | SPARE IO pin 3 (GPIO3), 3V3, GND | 3.3 V | 20 to 30 mA | 3-wire plug |
| Call button | SPARE IO pin 5 (GPIO45) to GND pin 1 | 3.3 V logic | about 0 | 2-wire plug |
| Bump switches (optional) | SPARE IO pin 4 (GPIO46), 10 kOhm to 3V3, other side GND | 3.3 V logic | about 0 | 2-wire plug |
| ADS1115 battery monitor | I2C SENSOR header: 3V3, GND, SDA (GPIO7), SCL (GPIO6); ADDR to GND (address 0x48) | 3.3 V | 0.2 mA | 4-pin JST-XH |
| Battery divider | 47 kOhm from the splice plus to ADS1115 A0; 27 kOhm and 100 nF from A0 to GND | 3.07 V at A0 when the pack is 8.4 V | 0.11 mA | solder or a small terminal |
| Fan (Pi 5 Active Cooler or Pi 4 fan) | Pi fan header or 5 V header pins | 5 V | 0.1 to 0.2 A | 2-pin |

SPARE IO pin order and GPIO numbers: `../../pcb/kicad/pin-table.md`. GPIO3, GPIO45 and GPIO46 are strapping pins; they are fine for a sensor or button that stays open at power-on, which is why the call button is a button to GND and the IR modules must not pull the pin to 3.3 V while the ESP32 starts (check in Stage 8).

---

## 4. First power-up order (details in `software-plan.md`, Stage 3 to 5)

1. **Pack alone:** measure the voltage at the splice with the main switch on (6.0 to 8.4 V). Nothing else connected.
2. **Set each buck with a multimeter, loads not connected:** XL4016 #1 to 5.0 V, the fixed buck reads 5.0 V, XL4016 #2 to 5.1 V. Turn the screw slowly; mark the setting with a dab of paint.
3. **CLEAN 5V IN only:** ESP32 alone. Measure its 3V3 pin; it must read 3.2 V or more. (The ESP32 here does no Wi-Fi, which is the case the board README worries about.)
4. **Pi branch:** connect the Pi and the screen. In a call, the voltage at the Pi must stay above 4.95 V and `vcgencmd get_throttled` must say `0x0`. Also test with the pack at 6.4 V (a bench supply) with the Pi busy.
5. **SERVO 5V IN and the servos**, one servo at a time, wheels or head unloaded first.
6. **BATT IN and the motors**, with the robot on a stand, wheels in the air (Stage 5).

---

## 5. What changed from the first draft diagram

- Raspberry Pi 5 named; the Pi buck feeds the Pi through a USB-C pigtail with a 1000 uF capacitor.
- 1 A fuse added on the screen wire. The screen's black wire goes to the minus lever connector.
- Motors named (Pololu 25D 12 V), battery monitor and cliff sensors named, camera LED and call button added, USB cables marked data-only.

---

## 6. Open questions for the owner (they change wiring or parts)

1. **Can the robot be charged while it is on?** The shopping list says charge with the robot off. A robot that is off cannot be called. Choices: the family switches it on at agreed times and charges it at night, or later a charge-while-on design is made. (conflict C3)
2. **2 cells or 4 cells (2S2P)?** Two cells give about 1.1 to 1.4 hours of calling by my sum; four cells double it but weigh about 3.2 kg and need a larger battery cradle. (C3, C4)
3. **Which screen exactly?** One or two micro-USB sockets (power and touch)? HDMI socket type? (peripherals)
4. **Does the SC-012-SN259 webcam pass the 10 minute test?** No information about it could be found online. (peripherals.md, section 3)
5. **Where do the speaker, camera LED and call button go?** The first 3D design has no place for them yet. (C5; mechanical-design.md)
6. **Pi 5 USB 600 mA limit:** with a bare USB-C cable a Pi 5 limits all USB ports together unless a setting is changed; check the official Raspberry Pi documentation before you rely on it. (C12; sbc-selection.md)
7. **Is the devkit's 5 V pin joined to its USB 5 V inside the board?** If you can look at the devkit's schematic, tell me; it decides whether the data-only cable is a must or a nicety.
