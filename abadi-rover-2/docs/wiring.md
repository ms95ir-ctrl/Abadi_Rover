# Abadi Rover 2: wiring (the final table and the decisions behind the diagram)

Diagram: `../diagrams/wiring-robot2.png` (and `.svg`). Battery part only: `../../pcb/kicad/battery-wiring.png` (2 cells) and `../diagrams/battery-4cell.png` (4 cells, section 7). Power part of the motherboard: `../../pcb/kicad/power-wiring.png`.
Pin numbers come from `../../pcb/kicad/pin-table.md` (locked). Nothing here changes the motherboard or robot 1.
**Board status.** The owner reports 5 boards ordered. Please confirm that the files that were ordered are version v5 (see `../../pcb/kicad/pin-table.md`). The board README says to order only after the paper test-fit passes.

**Words.** SBC = the Raspberry Pi. Buck = a module that lowers a voltage. Splice = the lever connectors where every branch takes its plus (+) from the switched battery. Pack = the 2S Li-ion battery, 6.0 to 8.4 V. 2S = two cells in series. 2S2P = four cells: two pairs, each pair is two cells in parallel, and the two pairs are in series. BMS = the battery protection board. AWG = wire thickness; AWG 18 is about 1 mm2 and AWG 20 about 0.5 mm2 (a bigger number is a thinner wire). ADS1115 = the small chip that measures the battery voltage. EEP = the sleep pin of the DRV8833 motor driver. TVS = a small diode that absorbs short voltage spikes. B-, BM, B+ = the three BMS wires that go to the cells: B- to the minus end, BM (the balance wire) to the point between the cells, B+ to the plus end. VBUS = the 5 V contacts of a USB plug; GND = the 0 V (minus) contacts.
**Marks.** VERIFIED = seen in a file or source. ASSUMED = my choice or guess, test it. Everything below is a plan; no part has been built or measured yet.

---

## 1. What the diagram shows, in one minute

- **One battery pack, one main switch, one splice.** From the splice, **four branches, each with its own fuse**, and one thin unfused wire for the battery monitor (the divider, section 3). Black wires all go back to the minus side of the splice.
- **The splice is four 5-way lever connectors** (Wago 221-415): two for plus and two for minus. Each pair is joined by a 10 cm jumper wire (AWG 18) that sits in one free slot of each connector of the pair. Plus side: 6 wires (switch in, the four fused branches, the divider resistor). Minus side: up to 7 wires (battery minus, BATT IN return, servo buck, clean buck, Pi buck, screen return, and for route B the amplifier return). One way to fill the slots:

| Connector | Wires in it |
|---|---|
| Plus 1 | main switch out (pack plus), the divider resistor wire (section 3), BATT IN fuse, servo buck fuse, jumper to Plus 2 (5 of 5 slots) |
| Plus 2 | jumper from Plus 1, clean 5 V fuse, Pi buck fuse (3 of 5 slots) |
| Minus 1 | pack minus (BMS P-), BATT IN terminal minus, servo buck IN-, jumper to Minus 2 (4 of 5 slots) |
| Minus 2 | jumper from Minus 1, clean buck IN-, Pi buck IN-, screen return, amplifier return (route B only; 5 of 5 slots, or 4 without route B) |

- **Fuse holders:** the four branches plus the screen fuse = **5 holders**. Route B sound (the cheap build) adds the amplifier fuse = **6 holders**. Fuses: 5 A slow-blow for BATT IN, the servo buck and the Pi buck; 2 A for the clean buck; 1 A slow-blow for the screen (and a second 1 A for the amplifier in route B).
- **Branch 1, BATT IN (5 A slow-blow):** raw pack voltage to the motherboard terminal BATT IN. It feeds only the DRV8833 motor driver, so the two drive motors get the pack voltage.
- **Branch 2, servo buck (5 A fuse, XL4016 set to 5.0 V):** to the terminal SERVO 5V IN. It feeds the PCA9685 and the pan and tilt servos only. A **second short AWG 18 pair** runs from the same buck OUT+ and OUT- to the PCA9685 module's own V+ screw terminal, in parallel with the board's header pin. Reason: two servos stalled together can pull about 5 A, and one header pin is good for only about 2 to 3 A (board README).
- **Branch 3, clean 5 V (2 A fuse, fixed 1.8 A buck):** to the terminal CLEAN 5V IN. It feeds the ESP32 (through diode D1), the two sonars, and nothing noisy.
- **Branch 4, Raspberry Pi (5 A fuse, second XL4016 set to 5.1 V):** goes to the Pi's USB-C power input through a USB-C plug with your own thick wires, with a 1000 uF capacitor at the Pi end. From the same 5.1 V output two more wires leave, **each with its own 1 A fuse**: one to the 7 inch screen's power lead, and (route B sound only) one to the speaker amplifier.
- **The battery monitor is not a fused branch.** Its 47 kOhm resistor is soldered at the splice, so the thin wire that runs on to the ADS1115 carries at most 8.4 V / 47 kOhm = 0.18 mA, even in a short.
- **The 3.3 V terminal and the second motor driver are not used** in robot 2. No SPI screens, no relays.
- **Data cables:** HDMI Pi to screen; USB webcam; USB audio adapter; USB touch (data only); USB Pi to ESP32 COM socket (data-only adapter, section 2 C9 and section 6 question 7).

---

## 2. Decisions I made on the helpers' conflicts

| # | Question | Decision | Reason |
|---|---|---|---|
| C1 | Where does the screen get its power? | From the **5.1 V Pi buck**, through its own **1 A slow-blow fuse**. Not from POWER OUT. | Keeps the backlight noise off the ESP32's clean 5 V and leaves the 1 A POWER OUT budget alone. The diagram shows it. |
| C2 | HDMI cable length | **0.8 m**, flat and thin | The mast route needs about 0.65 m. |
| C7 | 3.3 V buck, fuse count | Buy **one** fixed buck (5 V). Fuse holders: the four branches (BATT IN, servo buck, clean 5 V, Pi buck) **plus the screen fuse plus, for route B, the amplifier fuse**. That is **5 holders** in the comfortable build and **6** in the cheap build (route B). | Robot 2 does not use 3.3 V rails. The amplifier has its own 1 A fuse so that screen and amplifier (0.5 A plus up to 0.6 A, more at peaks) never share one 1 A fuse. |
| C9 | Two 5 V sources on the ESP32 USB cable and on the touch cable | **Plan:** a **data-only adapter** (a "USB power blocker", about 5 EUR, part of the cheap build too) for the ESP32 link. Taping pin 1 (the 5 V pin) of the USB-A plug on the Pi side is a **backup only**. The touch link also uses a data-only cable. Two bench tests before the trip decide whether this works: tests A and B in section 6, question 7. | The ESP32 is already fed from CLEAN 5V IN. Two 5 V sources that are not joined by a diode can fight. **ASSUMED:** it is not known whether the devkit's USB-serial chip needs the cable's 5 V to appear on the Pi. If it does (test B fails), an ordinary cable is used with the extra check in question 7. For touch: if it does not work through a data-only cable, use an ordinary cable (ASSUMED harmless, the screen's 5.1 V and the Pi come from the same buck). |
| C6 | Motor voltage setting in the software | `mot_vmax` = **8.0**: a speed cap, not the motor rating. The motors are Pololu 25D 12 V, run from a 6.0 to 8.4 V pack. | It is a setting, not a wiring change. Stage 5 starts at 8.0 and never goes above the pack voltage (8.4 V); duty is limited to 100 percent. Speed is about 0.36 m/s at 7.4 V (about 0.29 m/s at 6 V, ASSUMED). |
| C10 | LED dimming on the PCA9685 | Camera LED **on or off only** | All PCA9685 channels share one PWM speed (50 Hz); dimming would flicker. |
| C3, C4, C5, C8, C12 | Charging while on, runtime, mass, the place for speaker and button, Pi 5 USB limit | **Not decided here.** They are the open questions in section 6. | They need the owner's answer or a bench measurement. |

---

## 3. The wiring table (every electrical part)

"Pack" = after the main switch. All grounds are one common ground.

| Part | Connects to | Voltage | Current (ASSUMED unless marked) | Connector |
|---|---|---|---|---|
| Battery cells (2 in series; the comfortable build can use 4 as 2S2P, see section 7) | BMS B-, BM, B+ in that order (see `battery-wiring.png`; for four cells see `battery-4cell.png`) | 6.0 to 8.4 V | 2 to 4 A typical, up to 10 A peak | holder wires or solder tags |
| BMS, charger board, main switch | pack plus through the switch to the splice; minus to the splice minus; charger board between BMS and splice | 6.0 to 8.4 V | 10 A max (BMS) | wires, spade lugs |
| Fuse, BATT IN | splice plus to the BATT IN terminal (+) | 6.0 to 8.4 V | 5 A slow-blow | 5 x 20 mm in-line holder, 5.08 mm screw terminal |
| XL4016 #1, servos | in from splice through a 5 A fuse; out to SERVO 5V IN (and the second path, next row) | out 5.0 V | up to 5 A | lever and screw terminal |
| Servo second power path | a short AWG 18 pair from the XL4016 #1 OUT+ and OUT- (the same two wires that go to SERVO 5V IN, or a terminal-block tap beside it) to the PCA9685 module's **own V+ and GND screw terminal**, in parallel with the board header pin. Check the polarity against the marking on the module. | 5.0 V | carries the stall current that one header pin cannot (both servos stalled: about 5 A; one header pin is good for roughly 2 to 3 A; VERIFIED that the board README says so, and it adds that nothing is tested under load) | 2 wires AWG 18, about 20 cm, to the module's screw terminal |
| Fixed 5 V buck | in from splice through a 2 A fuse; out to CLEAN 5V IN | out 5.0 V | 0.5 A typical | lever and screw terminal |
| XL4016 #2, Pi | in from splice through a 5 A fuse; out to the Pi pigtail, the screen lead and (route B) the amplifier lead | out **5.1 V**, set with a meter at the Pi under load | typical 1.5 to 2 A (Pi 1 to 1.5 A plus screen 0.5 A); paper worst case 5.5 to 6 A (see the note under the table); Pi peak 3 A (Pi 4) or 5 A (Pi 5) | lever; wire to the pigtail |
| Raspberry Pi 5 (Pi 4 in the cheap build) | USB-C pigtail from XL4016 #2; 1000 uF capacitor (10 V or more) across 5.1 V and GND at the Pi end, plus to the 5.1 V wire | 5.1 V | see above | USB-C plug breakout board with solder pads and your own AWG 18 to 20 silicone wire on ALL VBUS (the 5 V contacts) and GND (the 0 V contacts) pads, under 40 cm (see the note under the table) |
| 7 inch screen | 5.1 V through its own 1 A fuse to its micro-USB power lead; HDMI to the Pi HDMI0 | 5.1 V | 0.5 A (VERIFIED for the Waveshare 7 inch (C)) | micro-USB pigtail, micro-HDMI to HDMI-A |
| Screen touch | Pi USB port | data only | 0 | micro-USB to USB-A, data only |
| USB webcam | Pi blue USB 3 port | 5 V from the Pi | 0.2 to 0.3 A | USB-A |
| USB audio adapter or speakerphone | Pi USB 2 port | 5 V from the Pi | 0.05 to 0.5 A | USB-A |
| Speaker amplifier (route B only) | its own tap from the 5.1 V Pi buck output (not from the screen wire) through its **own 1 A fuse**; black wire to the minus splice; input from the USB audio adapter | 5.1 V | up to 0.6 A (the speaker volume cap keeps it lower) | 2 power wires; audio cable 3.5 mm plug to bare wires (about 1.50 EUR) |
| ESP32 devkit | motherboard J1 and J3 sockets; 5 V via D1 from CLEAN 5V IN; **COM USB-C** to the Pi | 5 V | 0.15 to 0.3 A | sockets; a small data-only (power blocker) adapter plus a short ordinary USB-A to USB-C cable (C9, question 7) |
| Left motor | terminal **M1** (DRV A out 1 and 2; IN1A GPIO4, IN2A GPIO16) | pack voltage, pulsed | 0.2 to 0.4 A working, 1.26 A stall at 8.4 V | JST 2-pin |
| Right motor | terminal **M2** (DRV A out 3 and 4; IN3A GPIO1, IN4A GPIO5) | pack voltage, pulsed | same | JST 2-pin |
| Pan servo | PCA9685 channel 0 | 5.0 V | 0.1 to 0.5 A, stall 2 to 2.5 A (both servos stalled: about 5 A, which is why the second power path exists) | 3-pin servo plug and extension cable; plug colours below the table |
| Tilt servo | PCA9685 channel 1 | 5.0 V | same | same |
| Camera-live LED | PCA9685 channel 2 signal, LED, GND pin; exactly one 220 Ohm resistor in the path: the module's own, or, if the module has none, your own 220 Ohm resistor in series with the LED (see the note under the table) | 3.3 V logic | 3 to 6 mA | servo-type 3-pin plug with the red (V+) wire cut off or taped (signal and GND used) |
| Button light (optional) | PCA9685 channel 3, same rules as the camera LED | 3.3 V logic | 3 to 6 mA | same |
| Sonar 1 and 2 | SONAR 1 and 2 headers (5 V, TRIG GPIO12, ECHO GPIO13 and GPIO14, GND) | 5 V | 15 mA each | 4-pin 2.54 mm or JST-XH |
| Cliff sensor left | SPARE IO pin 8 (GPIO21), 3V3 pin 2, GND pin 1 | 3.3 V | 20 to 30 mA | 3-wire plug |
| Cliff sensor right | SPARE IO pin 3 (GPIO3), 3V3, GND | 3.3 V | 20 to 30 mA | 3-wire plug |
| Call / STOP button | SPARE IO pin 5 (GPIO45) to GND pin 1 | 3.3 V logic | about 0 | 2-wire plug |
| Bump switches (optional, NOT in the first build) | SPARE IO pin 4 (GPIO46): each switch between GPIO46 and 3V3 (SPARE IO pin 2), plus **one 10 kOhm pull-DOWN resistor from GPIO46 to GND** (SPARE IO pin 1), so the pin idles low like its reset default | 3.3 V logic | about 0.3 mA while pressed (3.3 V / 10 kOhm) | 2-wire plug per switch |
| ADS1115 battery monitor | I2C SENSOR header: 3V3, GND, SDA (GPIO7), SCL (GPIO6); ADDR to GND (address 0x48) | 3.3 V | 0.2 mA | 4-pin JST-XH |
| Battery divider | **47 kOhm (1 %) soldered onto a short wire stub that goes into the plus splice, right at the lever connector, covered with heat-shrink tube.** Only the resistor's far end goes by thin wire (0.14 to 0.25 mm2) to ADS1115 A0. 27 kOhm and 100 nF from A0 to GND sit at the ADS1115 end. | 3.07 V at A0 when the pack is 8.4 V | 0.11 mA; in a short the thin wire sees at most 8.4 V / 47 kOhm = 0.18 mA | soldered resistor with heat-shrink at the splice; solder or a small terminal at the ADS1115 |
| Fan (Pi 5 Active Cooler or Pi 4 fan) | Pi fan header or 5 V header pins | 5 V | 0.1 to 0.2 A | 2-pin |

SPARE IO pin order and GPIO numbers: `../../pcb/kicad/pin-table.md`. GPIO3, GPIO45 and GPIO46 are strapping pins (the ESP32 reads them while it starts); they are fine for a sensor or button that stays open at power-on, which is why the call button is a button to GND and the IR modules must not pull the pin to 3.3 V while the ESP32 starts (check in Stage 8). For the optional bump switches the pull-DOWN keeps GPIO46 low at start; a pull-up could block the download (flashing) mode. The exact boot table is ASSUMED: check it in the ESP32-S3 datasheet before fitting them. The protocol lists GPIO46 as the optional bump input (event `ev btn id:bump`).

**Pi power pigtail.** Use a USB-C plug breakout board with solder pads and solder your own AWG 18 to 20 silicone wire (under 40 cm) to ALL the VBUS pads (VBUS = the 5 V contacts) and ALL the GND pads (GND = the 0 V contacts). A USB-C plug has several of each: join them. Or cut a thick 5 A USB-C cable instead. Read the gauge printed on the jacket. If the wire is thinner than AWG 20, use a **3 A fuse** (5 x 20 mm slow-blow; make sure you own one, your fuse assortment may not have it) on the Pi branch instead of the 5 A fuse and accept that the Pi 5 then gets only about 3 A at its peaks. Ready-made pigtails are often much thinner (ASSUMED). Keep the 1000 uF capacitor at the Pi end (the stripe on the can marks minus).

**Pi branch current and where to measure.** Typical 1.5 to 2 A (Pi 1 to 1.5 A plus screen 0.5 A). Worst case on paper 5.5 to 6 A at the pack side: Pi 5 peak 5 A, screen 0.6 A and amplifier 0.6 A at 5.1 V, buck efficiency 88 percent, pack at 6.4 to 6.0 V. All ASSUMED, measure in Stage 3. This is why the 5 A slow-blow can blow in a rare peak. If it blows for no clear reason, a 6.3 A slow-blow is also allowed for this branch (the branch wires are AWG 18). Test the Pi under load with the pack at **6.4 V and at 6.0 V**. Where to measure the voltage "at the Pi": put the two multimeter probes on the two pigtail wires right at the USB-C plug, or on the Pi's GPIO header pin 2 (5 V) and pin 6 (GND), while a call runs.

**Servo plugs and the LED.** Servo plug colours: **brown or black = GND, red = V+, orange or yellow = signal.** Match the labels printed on the PCA9685 module before you plug in. A plug the wrong way round puts 5 V on the signal pin and can damage the board. The camera LED uses only signal and GND: use a 3-pin plug with the red (V+) wire cut off or taped, the LED's long leg (plus) on the signal wire and the short leg on the GND wire. Look at your PCA9685 module: if every output already has a 220 Ohm resistor (tiny flat parts soldered on the board, marked 221), connect the LED directly with **no extra resistor**. If the module has no such resistors, put **one 220 Ohm resistor in series with the LED**: signal wire, then the resistor, then the LED's long leg. Always exactly one resistor in the path. Check the brightness with the real parts. For the button light buy a plain 3.3 V-capable red LED (5 mm) or a 3.3 V ring, not a 12 V arcade ring.

**Servo second power path.** Wire it before the first servo moves (step 5). Also set the firmware soft limits for pan and tilt well inside the servo end stops, so a servo never presses against its stop and stalls. ASSUMED: the module's screw terminal is joined to the V+ of all the servo outputs; check with the multimeter (continuity between the terminal and a servo V+ pin) before you rely on it.

---

## 4. First power-up order (details in `software-plan.md`, Stage 3 to 5)

Keep the DRV8833 motor driver module OUT of its socket on the motherboard until step 6. If the pack is four cells, build it first by section 7.

1. **Pack alone:** measure the voltage at the splice with the main switch on (6.0 to 8.4 V). Nothing else connected.
2. **Set each buck with a multimeter, loads not connected:** XL4016 #1 to 5.0 V, the fixed buck reads 5.0 V, XL4016 #2 to 5.1 V. Turn the screw slowly. Do not glue yet: each XL4016 is locked after its load test (steps 4 and 5).
3. **CLEAN 5V IN only:** ESP32 alone. Measure its 3V3 pin; it must read 3.2 V or more. (The ESP32 here does no Wi-Fi, which is the case the board README worries about.)
4. **Pi branch:** connect the Pi and the screen. In a call, the voltage at the Pi (probe points: section 3, "Pi branch current and where to measure") must stay above 4.95 V and `vcgencmd get_throttled` must say `0x0`. Then repeat with the pack at **6.4 V and at 6.0 V** (a bench supply) with the Pi busy. When it passes, lock the adjust screw of XL4016 #2 with a drop of glue or nail varnish over the screw head and the little box it sits in. When it is dry, put a dab of paint across the screw and the box: if the paint is cracked later, the screw has turned. Then do the two cable tests A and B of section 6, question 7 (the link to the ESP32).
5. **SERVO 5V IN and the servos.** First wire the second power path: the short AWG 18 pair from the servo buck OUT+ and OUT- to the PCA9685 module's own V+ and GND screw terminal (check the polarity against the marking on the module). Check the servo plug colours (section 3). Then connect the servos one at a time, wheels or head unloaded first, with the firmware soft limits well inside the servo end stops. When it passes, lock the adjust screw of XL4016 #1 the same way (glue or nail varnish, then a dab of paint across the screw and the box).
6. **The DRV8833 and the motors**, with the robot on a stand, wheels in the air (Stage 5):
   - Measure the winding resistance of each motor with the multimeter on its two wires. 12 V / 1.8 A is about 6.7 Ohm. If it reads well below 5 Ohm, stop: the real stall current is higher. Do not fit the motors to the DRV8833 until the figure is rechecked.
   - Insert the DRV A module only now, with the thick bar (the white-plug side) toward the bottom edge of the board (board print: "white plug v"). Check this **before BATT IN is connected**: a module turned by 180 degrees fits the holes and puts battery voltage on the ESP32 pins GPIO1 and GPIO16.
   - Then connect BATT IN and the motors.
   - If the motors do not run, check the EEP pin of the DRV8833 with the multimeter (first pin of the bottom row, the white-plug side). If it is low, wire it to a live 3.3 V point: SPARE IO pin 2 or I2C pin 1 (the ESP32's own 3V3). Do **not** use the POWER OUT 3V3 pins: that rail is unpowered in robot 2 (no 3.3 V buck).

Steps 5 and 6 may be done in either order.

**After ANY transport (luggage, car, a hard knock), every time:** look at the dab of paint on both XL4016 adjust screws. A cracked dab means the screw has turned. Then measure all three buck outputs with **nothing connected to them**:
1. Take a photo of the wiring first. Switch the main switch off. Take every wire off the output side of the three bucks (at the buck's own OUT+ and OUT- terminals, or at the lever connector they share) and tape the bare ends:
   - XL4016 #1 (servo buck): the wires to the SERVO 5V IN terminal **and** the second-path AWG 18 pair that goes to the PCA9685 module's own terminal.
   - Fixed 5 V buck: the wires to the CLEAN 5V IN terminal.
   - XL4016 #2 (Pi buck): the Pi pigtail, the screen lead **and**, in route B, the amplifier lead. The Pi, the screen and the amplifier stay unpowered during the test.
2. Switch the main switch on and measure each output with the multimeter: XL4016 #1 about 5.0 V, the fixed buck about 5.0 V, XL4016 #2 about 5.1 V. If any reading is above 5.3 V, connect nothing and replace or reset that buck.
3. Only if all three readings are right: switch off, put every wire back where it was (use the photo; plus to plus, minus to minus), switch on, and only then let the Pi, the screen and the ESP32 start.

Optional (not in the parts totals): a TVS diode, type SMBJ5.0A, across the Pi supply wires (band toward the plus wire). It only absorbs short spikes. It does not help if a buck fails and passes the battery voltage through, so the re-measuring above stays the main protection. ASSUMED.

---

## 5. What changed

**From the first draft diagram:**
- Raspberry Pi 5 named; the Pi buck feeds the Pi through a USB-C pigtail with a 1000 uF capacitor.
- 1 A fuse added on the screen wire. The screen's black wire goes to the minus lever connector.
- Motors named (Pololu 25D 12 V), battery monitor and cliff sensors named, camera LED and call button added, USB cables marked data-only.

**After the independent review (this version):**
- **Second servo power path** from the servo buck to the PCA9685 module's own screw terminal (one header pin is rated 2 to 3 A; two stalled servos can pull about 5 A). In the table, step 5 and the diagram.
- **Battery divider:** the 47 kOhm resistor now sits at the splice (heat-shrink); only a thin wire runs on, so a short on it is at most 0.18 mA. In the table, the text and the diagram.
- **Speaker amplifier (route B)** has its own tap and its own 1 A fuse. Fuse holders: 5 in the comfortable build, 6 in the cheap build with route B. Shown in the diagram.
- **Splice:** four 5-way lever connectors (two per side, each pair joined by a 10 cm jumper); the 2-way connectors are dropped. The plus side has 6 wires, the minus side up to 7.
- **Pi pigtail** specified (own AWG 18 to 20 wire on all VBUS and GND pads, or a cut thick 5 A cable). **Pi current figures** unified: typical 1.5 to 2 A, paper worst case 5.5 to 6 A, tests at 6.4 V and 6.0 V, probe points named.
- **ESP32 link cable:** the data-only adapter is the plan (also in the cheap build); taping pin 1 of the USB-A plug is a backup. The old question 7 (read the schematic) is replaced by bench tests A and B.
- **Four-cell option (2S2P)** has its own section 7 and a sketch (`battery-4cell.png`), also for the case of two 2-cell holders with a middle wire.
- **Buck safety:** adjust screws are glued after the load tests; re-measure all three buck outputs after any transport; optional TVS diode.
- **Power-up order:** DRV8833 inserted only at step 6 with a check of its direction; EEP check with a safe 3.3 V point; steps 5 and 6 in either order; motor winding resistance measured first.
- **Servo plug colours and the camera LED** (no extra resistor if the module already has one) added. **Bump switches** are wired with a pull-DOWN on GPIO46.
- Motor setting `mot_vmax` = 8.0 (a speed cap); runtime figures unified (section 6, question 2); board status wording added at the top.

---

## 6. Open questions for the owner (they change wiring or parts)

1. **Can the robot be charged while it is on?** The shopping list says charge with the robot off. A robot that is off cannot be called. Choices: the family switches it on at agreed call times and charges it with the robot off (the default for now), or later a charge-while-on design is made. (conflict C3)
2. **2 cells or 4 cells (2S2P)?** About 1.1 to 1.4 hours of video calling on 2 cells (18 Wh), about 1 hour or less if the robot also drives, and about 2.2 to 2.8 hours on 4 cells. All ASSUMED; Stage 3 measures them (the servo holding current, and so the runtime, depends on how well the head is balanced). The buying decision assumes about 1 hour. Four cells weigh about 3.2 kg in all and need a larger battery cradle. How to wire four cells: section 7. (C3, C4)
3. **Which screen exactly?** One or two micro-USB sockets (power and touch)? HDMI socket type? (peripherals)
4. **Does the SC-012-SN259 webcam pass the 10 minute test?** No information about it could be found online. (peripherals.md, section 3)
5. **Where do the speaker, camera LED and call button go?** The first 3D design had no place for them. Before the large parts are printed the 3D design gets a 30 mm button hole, a 5 mm LED hole, a camera-cover slot and a speaker place; the sizes are ASSUMED until the real parts arrive. (C5; mechanical-design.md)
6. **Pi 5 USB 600 mA limit:** with a bare USB-C cable a Pi 5 limits all USB ports together unless a setting is changed; check the official Raspberry Pi documentation before you rely on it. (C12; sbc-selection.md)
7. **Does the devkit's USB-serial chip appear on the Pi through a data-only cable?** ASSUMED: it is not known whether that chip needs the cable's 5 V to appear. You do not need to read a schematic. Do two bench tests (about 5 minutes each) before the trip. You need: the Pi running (with a terminal window open), the ESP32 devkit in the motherboard with the clean 5 V branch built (step 3), and the data-only adapter plus cable from a Pi USB port to the devkit's **COM** USB-C socket (not the one marked USB).
   - **Test A: no 5 V flows through the cable.** Switch the clean 5 V buck off by pulling its 2 A fuse out of the holder. Nothing else may power the devkit. With the Pi on, plug the cable into the devkit COM socket. The devkit's power LED must stay dark. If it lights up, the cable still carries 5 V (with the tape trick you taped the wrong pin: the 5 V pin is pin 1 of the USB-A plug, the GND pin is the other outer one). Fix that first.
   - **Test B: the chip still appears.** Put the 2 A fuse back (clean 5 V buck on), same cable. On the Pi type `lsusb` and press Enter (it lists the USB devices). Look for a line that contains `10c4:ea60` (CP210x chip), `1a86:7523` or `1a86:55d3` (CH340 or CH343 chip). Then type `ls /dev/ttyUSB* /dev/ttyACM*` and press Enter: it must list one device (for example `/dev/ttyUSB0` or `/dev/ttyACM0`). One error line such as `ls: cannot access '/dev/ttyACM*': No such file or directory` is normal: it is for the other name, which matches nothing. What matters is that one device is listed.
   - **If test B fails:** use an ordinary USB cable (the parts list has a spare). Put a USB power meter in line and check that about 0 mA flows out of the Pi port while the clean 5 V buck feeds the ESP32. If the Pi port does deliver current, stop and ask before you run the robot that way.

---

## 7. Four-cell option (2S2P)

The first build uses 2 cells (2S, drawn in `../../pcb/kicad/battery-wiring.png`, which is locked and not changed). The comfortable build can use 4 cells: about 2.2 to 2.8 hours of calling instead of 1.1 to 1.4 (ASSUMED, section 6 question 2), and the robot weighs about 3.2 kg. The sketch for four cells is `../diagrams/battery-4cell.png` (and `.svg`), drawn by `../diagrams/draw_battery_4cell.py`.

**How to build it: 2P first, then 2S.** Name the cells A1, B1, A2, B2.
1. Pair 1: join cell A1 and cell B1, plus to plus and minus to minus.
2. Pair 2: join cell A2 and cell B2 the same way.
3. Put the pairs in series: plus of pair 1 to minus of pair 2. This is the junction between the pairs.
4. BMS wires, one at a time, in this order: **B-** to the minus of pair 1, **BM** (the balance wire to the point between the cells; here it is the junction between the pairs) to that junction, **B+** to the plus of pair 2.

**If you use the two 2-cell holders from the parts list instead of four single-cell holders.** This works only if each holder has a wire or a solder tag at the point between its two cells (check when the holders arrive; if there is none, buy four single-cell holders). Each holder is then a small 2S string with three points: plus end, middle point, minus end. Joining the two strings in parallel gives the same 2S2P pack: the two bottom cells (next to the minus ends) are pair 1, the two top cells are pair 2.
1. With the cells **out** of the holders, put the two holders side by side the same way round. Join the two plus ends, the two minus ends and the two middle points with short AWG 18 wire (three joints). Tape every bare end.
2. Check with the multimeter on its beep (continuity) setting: plus end to minus end must **not** beep.
3. Measure all four cells alone (0.05 V rule below), then put them in, one at a time, each the right way round by the marks in the holder.
4. BMS wires as in step 4 above: **B-** to the joined minus ends, **BM** to the joined middle points, **B+** to the joined plus ends.

**Rules (all of them):**
- All four cells come from the same batch and are the same model. No damaged cells.
- Before any joint, measure every cell alone with the multimeter. All four must be within **0.05 V** of each other. If not, charge the lower cells alone (single-cell charger) until they match. Never join cells of different charge, and never "equalise" by joining them.
- One BMS only, for the whole pack.
- **No fuse between the pairs.** The BMS limit (10 A) and the 5 A branch fuses stay as they are. The wires inside the battery pack have no fuse, so keep them short, use AWG 18 or thicker wire, and tape every bare end.
- Build with the BMS, the charger and the robot disconnected, one wire at a time.
- You must be able to reach every cell end and the point between the cells. Use four single-cell holders (or a holder you can wire yourself), or two 2-cell holders that each have a middle wire (see above). A two-cell holder that is wired in series inside with no middle wire cannot be used.
- After the build, before anything else is connected: B+ to B- must read 7.4 to 8.4 V (charged cells), and B+ to BM and BM to B- must each read about 3.0 to 4.2 V.
