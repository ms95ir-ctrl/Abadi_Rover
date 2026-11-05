# Robot 2: screen, camera, sound, sensors and the small electronics

Written 5 November 2026 for the telepresence robot. This file explains the choices behind `parts-list.md`. It covers the parts that sit between the small computer (SBC) or the motherboard and the world: screen, camera, microphone and speaker, sonar, cliff sensors, battery monitor, LEDs, button. It ends with the conflicts I found between the other specialists' files.

**Words used here.** SBC = single board computer (the Raspberry Pi). Motherboard = your 100 x 100 mm ESP32 board. ESP32 = the small controller on it. GPIO = a numbered signal pin of the ESP32. PCA9685 = the 16-channel servo board on the motherboard. ADC = analog-to-digital converter (turns a voltage into a number). I2C = a two-wire bus (SDA and SCL) that many small boards share. UVC = the standard "no driver needed" USB camera type. AEC = acoustic echo cancelling (removes the loudspeaker sound from the microphone signal). BMS = the battery protection board. Buck = a module that lowers a voltage. Strapping pin = an ESP32 pin whose level at power-on changes how it starts. Carry-on = hand luggage.

**How sure am I.** VERIFIED = I saw it in a file or web source (listed at the end). ASSUMED = my own knowledge, calculation or guess; check it. All prices are EUR, "about", from web search snapshots and not from shop pages I could open (my tool could not open most shops). Check the live price when you buy.

---

## 1. The short answer

| Part | Decision | Why |
|---|---|---|
| **Screen** | **Waveshare 7 inch HDMI LCD (C)**, 1024x600, touch, about 58 EUR. A no-name 7 inch with the same specs (about 45 EUR) is the cheap version. | Verified size 164.9 x 107 x 8 mm, 5 V at 0.5 A, 2.5 W. It fits the head pocket in `mechanical-design.md`. |
| **Screen power** | From the **5.1 V SBC buck**, through its own 1 A fuse. Not from the motherboard's POWER OUT. | Keeps backlight noise off the ESP32's clean 5 V. Section 2.3. |
| **Camera** | **Try your SC-012-SN259 first** with the 10 minute test in section 3. If it fails, a cheap wide-angle 1080p UVC webcam with microphone (about 22 EUR). | I could not find any page for the model number SC-012-SN259, so its size, view angle and microphone are unknown. |
| **Sound** | **Start with route B**: webcam microphone + USB audio adapter + small speaker in the base (about 12 EUR) and the browser's own echo cancelling. **Keep route A** (USB speakerphone, about 75 EUR) as the upgrade if the echo test fails. | Route B is the cheapest that has a real chance to work. Route A is the only one with echo cancelling built into the device. Section 4. |
| **Sonar** | 2 x HC-SR04, 5 V type. | The motherboard already has the 1k/2k divider for the echo signal. |
| **Cliff sensors** | 2 x TCRT5000-type IR modules, powered from **3.3 V**, on GPIO21 and GPIO3. | Follows the draft wiring diagram and the software plan. |
| **Battery monitor** | ADS1115 on the I2C header; divider 47 kOhm / 27 kOhm with 100 nF. | 3.07 V at 8.4 V pack: safe for the chip. Section 5.3. |
| **LEDs and button** | Camera-live LED on PCA9685 channel 2, button light on channel 3, call button on GPIO45. | No free ESP32 pins are left. Section 5.4. |
| **USB ports on the SBC** | All 4 are used (webcam, sound, ESP32, touch). No hub needed. | Pi 4 and Pi 5 both have 4. Section 6. |

**What is not settled and needs you:** the real webcam (test), the real screen's HDMI socket type, a place for the speaker, and the charging-versus-always-on question (section 8, conflict C3).

---

## 2. The screen

### 2.1 What I chose and why

| | Waveshare 7 inch HDMI LCD (C) | No-name 7 inch HDMI IPS with touch |
|---|---|---|
| About price (Germany) | **58 EUR** (seen 45 to 62 EUR: exp-tech.de 44.95 EUR without VAT = about 53.50 EUR with VAT, elecena.pl 58, elty.pl 62.26, melopero.com 48.47, opencircuit.shop 60.75) (V) | **45 EUR** (eBay.de listings 43 to 57 EUR) (V) |
| Size | 164.90 x 106.96 x 8 mm, visible 154.2 x 85.9 mm (V, Waveshare wiki) | Often about 165 x 100 x 10 mm: check the listing (A) |
| Picture | 1024x600 IPS, 170 degree viewing angle, 300 cd/m2 (V) | usually the same (A) |
| Touch | 5-point capacitive, over USB (V) | check "capacitive", not "resistive" (A) |
| Power | **5 V, 500 mA typical, 2.5 W** (V, Waveshare wiki) | similar (A) |
| Weight | 320 g item weight in one shop listing, 200 to 250 g in other sources (V, conflicting) | unknown (A) |
| Why | Known data, widely used on Raspberry Pi, driver-free | Saves about 13 EUR; the risk is a wrong size or HDMI socket |

The head pocket is 166 x 108 x 10 mm (mechanical design), so both fit. **Buy the Waveshare unless money is tight.** If you buy a no-name one, read the listing for: 1024x600, IPS, HDMI socket type, 5 V micro-USB power, USB touch.

### 2.2 Cables and connectors

| Link | Cable | Notes |
|---|---|---|
| SBC to screen picture | **micro-HDMI plug (SBC end) to full-size HDMI-A plug (screen end), flat and slim, 0.8 m**, about 12 EUR | The Pi 4 and Pi 5 have micro-HDMI sockets (`sbc-selection.md`; I know this to be true, but it is marked ASSUMED there). The screen's socket is ASSUMED to be full-size HDMI-A: look at the shop photo. If it is mini or micro, change one end. **Length:** the mast route needs about 0.65 m (120 mm along the deck, 215 mm up the mast, 120 mm loop, 60 mm in the head, plus pan slack). `sbc-selection.md` said 30 to 50 cm. That is too short (conflict C2). |
| Screen power | micro-USB plug with bare wires, power only, about 30 cm | Wires go to the 5.1 V buck output through a 1 A fuse. Cut an old micro-USB cable if you have one. |
| Touch | micro-USB to USB-A, **data only (no 5 V)**, into one SBC USB port | If the touch cable also carried 5 V, the screen would have two power sources (the buck and the SBC's USB). Use a data-only cable or tape over the 5 V pin of the USB-A plug. |

### 2.3 Why the screen takes its power from the SBC buck

The mechanical design says "screen power from the POWER OUT 5 V pins on the motherboard (the wiring file decides)". The draft wiring diagram (`abadi-rover-2/diagrams/wiring-robot2.png`) draws it from the 5.1 V buck. I follow the diagram, for three reasons:

1. The POWER OUT 5 V rail comes from the clean 5 V buck (1.8 A) and is "about 1 A usable" (V, board README). The ESP32 and the sonars already use some of it. The screen would take half of the rest.
2. A screen backlight can put noise on a supply. The ESP32 is the safety brain; it should have the quietest rail.
3. The 5.1 V XL4016 module has plenty of spare current (the Pi 4 needs about 3 A at most; the Pi 5 up to 5 A, the screen 0.5 A).

**The screen lead needs its own small fuse.** The 5 A fuse on the buck input does not protect a thin micro-USB wire. Use a **1 A slow-blow fuse in an in-line holder** at the buck end. About 1.20 EUR.

**Idea, not in the totals:** the screen uses 2.5 W even when nobody is calling. A relay module that switches the screen's 5 V off when idle would save about a third of the idle power (A). The motherboard has relay headers (RLY1 = GPIO15), but they are powered by the 3.3 V buck, which robot 2 does not otherwise use. Ask the power and software specialists before buying anything.

### 2.4 Is the screen too heavy for the servos? No.

The mechanical document estimates 833 g for the head and a tilt-servo load of 11 to 22 percent with a 230 g screen. Take the worst listing (320 g) and a balance point 25 mm off the tilt axis: static torque is about 0.92 kg x 9.81 x 0.025 m = 0.23 N·m, plus about 0.04 N·m for motion and friction. That is about 0.27 N·m against about 0.92 N·m for an MG996R at 4.8 V (A), about 29 percent. **No conflict.** A 10.1 inch screen (+0.55 kg) is a different story and is not planned.

---

## 3. The camera

### 3.1 Your SC-012-SN259: unknown, so test it

I searched the web for "SC-012-SN259" and found **no product page, no data sheet, no size**. It is only named in your `plan.md` for robot 1. So everything about it is ASSUMED. The mechanical design assumed a body of 60 x 30 x 28 mm, a lens window of 16 mm and a 1.5 m cable.

**What the camera must do (pass test):**

| Need | Pass if | Why |
|---|---|---|
| Works without a driver | Appears as a UVC camera in the list below | The SBC runs Linux; UVC is built in. |
| 720p at 30 fps | The list shows `MJPG` (motion-JPEG, a compressed picture format) with 1280x720 at 30 fps | The SBC document says to run the call at 720p, not 1080p (the CPU decodes the camera's JPEG pictures too). |
| A microphone (for route B) | `arecord -l` shows a capture device | Otherwise buy a clip-on USB microphone (about 8 EUR) or use route A. |
| View angle 70 degrees or more, 90 better | Measured with the wall test below | A robot at about 0.5 m height must see a person and a bit of the room. |
| Fits the brow | Body at most 60 x 30 x 28 mm, lens near the middle | The head brow is printed for that size. If it is bigger, the brow gets re-printed. |

**The ten minute test.** Plug the camera into the Pi (or any Linux computer). Type these commands in a terminal, one at a time. In full:

1. `lsusb` lists all USB devices. Look for a line that looks like your camera.
2. `sudo apt install v4l-utils` installs a small tool that talks to cameras. It needs internet. "sudo" means "do this as administrator".
3. `v4l2-ctl --list-devices` lists the cameras and their names (for example `/dev/video0`).
4. `v4l2-ctl -d /dev/video0 --list-formats-ext` lists every picture size and speed the camera offers. Look for `MJPG` and `1280x720` with `30.000 fps`.
5. `arecord -l` lists the sound recording devices. A webcam with a microphone shows up as a "card" with the camera's name.

**The wall test for the view angle.** Put the camera 1.5 m from a wall. Measure how wide the picture is on the wall. The horizontal view angle is 2 x arctan(half the width / 1.5 m). A width of 1.5 m is about 53 degrees (too narrow), 2.5 m is about 80 degrees (good), 3.0 m is 90 degrees (very good).

### 3.2 If it fails: the fallback

A cheap **wide-angle 1080p UVC webcam with a microphone**, about 15 to 30 EUR (A; I found no single model with all of these in one listing, so I do not name one). Rules for the buy:

- It must say UVC or "plug and play on Linux and Raspberry Pi".
- It must have a microphone if you use route B.
- Its view angle is "90 to 110 degrees". Many listings claim 130 degrees and the real value is lower (one review of a 130 degree camera measured about half). Check the picture.
- Check the body size against the brow (60 x 30 x 28 mm) before you print the head.

Bare USB camera modules (about 38 x 38 mm, no case) are the smallest, but most have no microphone.

**Buy-twice note.** The SC-012-SN259 belongs to robot 1's phase 3, which has not started. If robot 2 takes it, robot 1 needs another camera later.

### 3.3 Mounting and privacy

- The webcam sits in the **brow** above the screen (mechanical design) so the remote person looks into the camera.
- Plug it into a **blue USB 3 port** (SBC document). Keep the cable's extra length coiled in the head (the cable is about 1.5 m).
- Set the camera to **720p, 30 fps** in the call software.
- The software plan wants a **camera-live LED** that follows the truth (is `/dev/video0` open?) and a **physical cover**. The mechanical design has **no hole for the LED and no cover** (conflict C5). A 5 mm LED hole next to the camera window and a small sliding cover are cheap additions.

---

## 4. Sound: speaker, microphone and echo

### 4.1 The problem

When the family hears the owner, the speaker plays his voice. The robot's microphone hears that sound and sends it back. The owner then hears himself a moment later. That is echo. His side (headphones) never echoes (software plan). The fix is echo cancelling (AEC). It exists in two places: in the browser (Chromium has it on by default, VERIFIED for Jitsi's defaults in the software plan) and, in some products, inside the USB device.

I found **no tested report of this exact setup** (Chromium on a Pi, webcam microphone, separate small speaker, 10 cm apart). It is the normal setup of millions of laptops, so I expect it to work at moderate volume, but I cannot prove it. That is why the plan has a test.

### 4.2 The three routes

| | **A. USB speakerphone** (Jabra Speak 410 class) | **B. USB audio adapter + small speaker** | B2. One-cable USB mini speaker |
|---|---|---|---|
| What it is | One case: microphone + speaker + echo cancelling chip. One USB plug. | USB sound adapter (7 EUR) + PAM8403 amplifier board (2.50 EUR) + 40 mm 3 W speaker (2.50 EUR). The microphone is the webcam's. | A ready speaker with a USB plug and its own sound chip. The microphone is the webcam's. |
| About price | **60 to 85 EUR.** Seen: eBay.de new 59.99 EUR plus shipping; a Latvian shop 84.99 EUR (June 2026); other shops 92 to 154 EUR (V). Budget 75 EUR. | **about 12 EUR** (A) | about 8 to 12 EUR (A) |
| Echo cancelling | In the device **and** in the browser | In the browser only | In the browser only |
| Why it can work | Microphone and speaker share one clock and one case; the maker tuned them together (A) | Common setup; needs distance and a modest volume | Same as B |
| Weak points | Size and weight (I assume 100 to 125 mm wide and about 350 g; I could not verify). Its own microphone is on the base, far from faces. Motor noise. USB current 0.3 to 0.5 A (A). | Echo in a small robot is the worst case if speaker and microphone are close | Same, and the speaker is bigger than the head lid grille |
| Mechanical fit | **No place for it in the design.** It needs a flat spot on top of the cover behind the mast. | The 40 mm speaker fits the lid grille, **but that grille faces backward and sits about 10 cm from the camera microphone (C5).** Better: put the speaker in the base facing forward and down. | No place |
| Weight | about 350 g (A), but it sits low and works as ballast (the mechanical design suggests 400 g of ballast) | about 30 g | 100 to 200 g (A) |

**Cheap no-name "conference speakers" at 17 to 31 EUR** (seen on eBay and Fruugo) say nothing about echo cancelling or Linux. I would not trust them. Buy a speakerphone only if the seller says "echo cancellation" (AEC), "full duplex" and USB audio class (works without a driver).

### 4.3 Which is cheapest that really works?

- **Cheapest with a real chance: route B, about 12 EUR.** The webcam microphone is free (if the camera has one), the browser cancels the echo, and you keep the speaker away from the microphone.
- **Cheapest with a guarantee in the device: route A, about 75 EUR.** About six times the price.
- **My plan:** build route B first. Run the echo test (section 4.4). If you hear yourself, buy route A before the trip. It is the same 3-minute test every time, and it costs 75 EUR only if needed. The **cheap build** in `parts-list.md` uses B; the **comfortable build** uses A.

### 4.4 The echo test (3 minutes, at home, with the real robot)

1. Start a call between the robot and your laptop. You wear headphones on the laptop.
2. Talk normally on the laptop. Ask a helper to talk in the robot's room at a normal volume.
3. You pass if you hear no echo of your own voice at the volume the family would use. Watch for echo when the helper stops talking.
4. Repeat with the robot's speaker volume at 100 percent. The software plan caps the volume (for example at 70 percent), so check at the cap.
5. Fail: move the speaker farther from the microphone, lower the cap, or buy route A.

Do **not** switch on a second echo canceller in the operating system at the same time as the browser's. Two cancellers can sound worse (software plan, ASSUMED).

### 4.5 Where the speaker goes

Placement matters more than price:

- **Speaker low, microphone high.** Put the speaker in the base (cover or front rim, facing forward or down) and keep the webcam microphone in the head. That gives 40 cm of distance and a body between them.
- **Not in the lid.** The lid is at the back of the head. The speaker would face the wall behind the robot and sit about 10 cm from the microphone.
- **Route A:** the speakerphone sits on top of the cover behind the mast. Its microphone then also hears motors. Turn the robot's own drive noise down (slow ramps) when the owner talks.
- Mechanical decision needed: a speaker grille in the base, or a speakerphone shelf. See C5.

### 4.6 Wiring of route B (for the wiring diagram)

USB audio adapter plugs into a SBC USB port. Its green 3.5 mm output goes to the PAM8403 input (through a 3.5 mm plug and 2 wires). The PAM8403 board takes **5 V from the 5.1 V buck branch** (it can draw about 0.6 A at full volume with a 3 W speaker; the speaker volume cap keeps it much lower) and its output goes to the speaker. All grounds join at the 5.1 V buck's minus. The Pi 5 has no 3.5 mm audio jack, so the adapter is needed (`sbc-selection.md`). The Pi 4 has a jack, but its sound quality is poor and noisy.

The operating system must be told to use the USB device (not the screen's HDMI sound) as the default speaker, and the webcam (or speakerphone) as the default microphone. That is a software task (stage 1).

---

## 5. Sensors, battery monitor, LEDs and button

### 5.1 Pin map (all from `pcb/kicad/pin-table.md` and `esp32-serial-protocol.md`)

| Function | Where on the motherboard | Pin | Voltage | Parts |
|---|---|---|---|---|
| Sonar 1 and 2 | SONAR 1 and SONAR 2 headers (4-pin: 5 V, TRIG, ECHO, GND) | TRIG = GPIO12 (shared), ECHO = GPIO13 and GPIO14 through the board's 1k/2k dividers | 5 V supply, 3.3 V signals at the ESP32 | 2 x HC-SR04 (5 V type) |
| Cliff sensor left | SPARE IO header pin 8 | GPIO21 | **3.3 V** supply from SPARE pin 2 | IR module |
| Cliff sensor right | SPARE IO header pin 3 | GPIO3 (strapping pin; harmless after start) | 3.3 V | IR module |
| Call button | SPARE IO header pin 5 and pin 1 (GND) | GPIO45 (strapping pin; pulled low by default, so a button to GND is safe) | 3.3 V logic | arcade button |
| Bump switches (optional) | SPARE IO header pin 4 and a GND pin | GPIO46 (input only, strapping pin) | 3.3 V, **needs a 10 kOhm pull-up to 3V3** | 2 micro switches in parallel |
| Battery monitor | I2C SENSOR header (1 = 3V3, 2 = GND, 3 = SDA, 4 = SCL) | SDA = GPIO7, SCL = GPIO6, ADS1115 address 0x48 | 3.3 V | ADS1115 board + divider |
| Camera-live LED | PCA9685 channel 2 (servo header: signal and GND pins) | none: the PCA9685 drives it | 3.3 V logic, about 6 mA | LED + 220 Ohm |
| Button light | PCA9685 channel 3 | none | 3.3 V logic | LED ring + 220 Ohm |
| Gyro | GY-521 socket | I2C 0x68 | 3.3 V | on the board |
| Pan servo / tilt servo | PCA9685 channel 0 / 1 | I2C 0x40 | 5.0 V servo power | 2 x MG996R |

### 5.2 Sonar and cliff sensors

- **Sonar:** HC-SR04 boards are 45 x 20 x 15 mm (V, mechanical doc). They run on 5 V and need the **5 V type**, not the "HC-SR04P" 3.3 V type: the motherboard's divider (1 kOhm + 2 kOhm) expects a 5 V echo. About 15 mA each (A). Sonar misses soft cushions and thin legs, so it is a helper, not the safety.
- **Cliff sensor:** a reflective infrared module (TCRT5000 type with a small comparator and a digital output). It shines IR at the floor and looks for the reflection. The mechanical design points them at the floor from 12 mm. **Power them from 3.3 V, never from 5 V:** a 5 V output on GPIO21 or GPIO3 can damage the ESP32 (not 5 V tolerant, V). About 20 to 30 mA each (A), so about 50 mA on the ESP32's 3.3 V pin, which is fine (the dev kit regulator gives about 500 mA, A). Black or very dark carpet absorbs IR and can look like "no floor". **Buy 4 modules, test on your floors, keep the best two.** The module's pot (small screw) sets the switching level.

### 5.3 The battery monitor (ADS1115 and its divider)

**Why a divider.** The pack is 6.0 to 8.4 V. The ADS1115 is powered at 3.3 V and its input pins must stay below 3.3 V + 0.3 V = 3.6 V. So the pack voltage is divided down first. (The ESP32's own ADC is noisy, so the software plan uses the ADS1115.)

**The divider.** 47 kOhm from pack plus to input A0, 27 kOhm from A0 to ground, 100 nF across the 27 kOhm. Use 1 percent metal-film resistors.

| Pack | Voltage at A0 (= pack x 27 / 74) |
|---|---|
| 8.4 V (full) | **3.07 V** |
| 8.5 V (BMS overcharge limit) | 3.10 V (safe, under 3.6 V) |
| 7.4 V | 2.70 V |
| 6.4 V (software "critical") | 2.33 V |
| 6.0 V | 2.19 V |

- **Drain:** 8.4 V / 74 kOhm = 0.11 mA. **Connect the divider after the main switch**, so it drains nothing when the robot is off.
- **Resolution:** with the +/-4.096 V range one count is 0.125 mV at the pin, which is 0.34 mV on the pack. The resistor tolerance is removed by one reading against a multimeter (`bat_cal`, software plan).
- **Source impedance:** the divider looks like 17 kOhm to the chip; the 100 nF smooths it. Fine for a 128-samples-per-second reading (A).
- **Wires:** ADS1115 VDD to I2C pin 1 (3V3), GND to pin 2, SDA to pin 3, SCL to pin 4, ADDR to GND (address 0x48), A0 to the divider middle. The boards come with their own pull-up resistors; with the PCA9685 and GY-521 also having theirs, the bus ends up with about 2 to 3 kOhm in parallel, which is fine at 3.3 V (A).
- **Optional A1 (charger present):** two 10 kOhm in series from the charger's 5 V input to ground, tap to A1: 2.5 V when plugged in. Leave out unless the power design lets the robot run while charging (C3).

### 5.4 LEDs, button, bump switches

- **Camera-live LED (and button light).** A red 5 mm LED needs about 2.0 V. The PCA9685 channel gives 3.3 V. With a 220 Ohm resistor: (3.3 - 2.0) / 220 = **5.9 mA**. That is bright enough and within the chip's limit (A). Wire: signal pin, then the resistor, then the LED plus; LED minus to the GND pin of the same servo header plug. **Use red, amber or orange.** A white, green or blue LED needs about 3 V and will be dim at 3.3 V. Do not use the V+ pin of that header: it carries 5 V.
- **The PCA9685 has one PWM speed for all channels** (set to 50 Hz for the servos). A dimmed LED at 50 Hz can visibly flicker. **Use the LED fully on or fully off**, not dimmed or pulsing (conflict C10; the software protocol offers pulse and brightness).
- **After an ESP32 reset the camera LED comes on** (software plan): the safe direction. A PCA9685 keeps its last setting if the ESP32 dies (A).
- **Call button:** an arcade button 30 mm, normally open, between GPIO45 and GND. The firmware uses the internal pull-up. The software plan says short press and long press. **The mechanical design has no hole for it** (C5). Optional: the button's LED ring on channel 3.
- **Bump switches (optional):** two lever micro switches in parallel between GPIO46 and GND, with a 10 kOhm resistor from GPIO46 to 3V3. GPIO46 is input-only and may have no internal pull-up (A), so the outside resistor is needed. **The software plan has no event for it yet** (C11).

### 5.5 PCA9685 channel plan

| Channel | Use | Load | Notes |
|---|---|---|---|
| 0 | Pan servo (turn) | MG996R | power from V+ (5.0 V buck) |
| 1 | Tilt servo (nod) | MG996R | same |
| 2 | Camera-live LED | 6 mA | 3.3 V logic, resistor 220 Ohm |
| 3 | Button light | 6 mA | optional |
| 4 to 15 | free | | keep unused |

The servo plug order is brown or black = GND, red = V+, orange or yellow = signal (`wiring.md`); match the row labels printed on the board before plugging in. Each servo extension cable goes up the mast (3 cables: pan, tilt, LED). The mechanical cable list shows only 2; see C5.

MG996R facts: 40.7 x 19.7 x 42.9 mm, 55 g (V). Stall current about 2 to 2.5 A each (A). Datasheet torque numbers differ by seller (9.4 kg·cm at 4.8 V or "15 kg"); I use 9.4 (A). The PCA9685 header pins are good for 2 to 3 A (board README). Two servos that move seldom stay far below that.

---

## 6. USB ports, power use and runtime

### 6.1 USB devices on the SBC

| Device | Port | Power | Cable |
|---|---|---|---|
| Webcam | blue USB 3 port | about 0.2 to 0.3 A (A) | the camera's own cable |
| Sound (route A speakerphone, or route B adapter) | USB 2 port | route A 0.3 to 0.5 A, route B 0.05 A (A) | the device's cable |
| ESP32 COM socket | USB 2 port | **none** (data-only cable) | USB-A to USB-C, 20 cm, data only |
| Touch (screen) | USB 2 port | **none** (data-only cable) | micro-USB to USB-A, data only |

That is **4 devices on 4 ports**: no hub. If you add a fifth, you need a small powered hub.

**Data-only means no 5 V wire.** The ESP32 already gets 5 V from the motherboard (through diode D1). A second 5 V through the USB cable would put two power sources on one supply rail. It would use up part of the Pi's USB current budget, and it could push current back into the Pi's USB port while the Pi is off or rebooting (how much depends on the dev kit's diodes, which I could not check). The same logic holds for the screen. Buy a "USB power blocker" or "data only" cable (a "data blocker" does the opposite). **Free trick:** put a piece of Kapton tape over the outer pin of the USB-A plug (pin 1 is the 5 V pin).

**Pi 5 USB limit (from `sbc-selection.md`).** On a bare USB-C power cable the Pi 5 allows only 600 mA for all its USB ports unless the line `usb_max_current_enable=1` is set in `/boot/firmware/config.txt`. A webcam (0.3 A) and a speakerphone (0.3 to 0.5 A) can exceed 600 mA. The setting comes from a third-party guide; **check it in the official Raspberry Pi documentation** and set it only if the buck and the wire can deliver 5 A. The Pi 4 has no such limit (A); its four USB ports share about 1.2 A.

### 6.2 Power budget (ASSUMED; measure in stage 3)

Typical and peak current of every branch. 5 V figures except the motors.

| Branch (fuse) | What is on it | Typical | Peak |
|---|---|---|---|
| BATT IN (5 A slow-blow) | 2 Pololu motors at 7.4 V | 0.2 to 0.4 A | 2.2 A both stalled (1.11 A each; 1.26 A at 8.4 V) (mechanical doc) |
| Servo buck, 5.0 V (5 A) | 2 MG996R | 0.1 to 0.5 A | 4 to 5 A if both stall (A) |
| Clean 5 V buck (2 A) | ESP32 (no Wi-Fi), 2 sonars, LEDs | 0.2 to 0.3 A | 0.5 A |
| SBC buck, 5.1 V (5 A) | Pi + webcam + sound | 1.0 to 1.5 A in a call (V, SBC document) | 3 A (Pi 4), 5 A (Pi 5) |
| Same branch, own 1 A fuse | screen | 0.5 A (V) | 0.6 A |

On paper, if everything peaked at once, the battery would give 10 to 11 A, a little above the BMS's realistic 10 A continuous. That does not happen in use; typical is 2 to 4 A.

**The 5.1 V buck on a low pack.** The XL4016 needs about 1 to 1.5 V more input than output at higher current (A, SBC document). At the software's critical level of 6.4 V (3.2 V per cell) it has about 1.3 V of headroom at rest, and less while the motors or servos pull the pack down. The BMS itself cuts at 5.8 to 6.0 V. So the 6.4 V shutdown level in the software plan is the right one; **test the 5.1 V output with the Pi busy at 6.4 V and 6.0 V input on a bench supply.** If the 5 A buck-input fuse blows when a Pi 5 boots with all USB devices on a nearly empty pack (5.1 V x 5 A / 0.88 / 6.4 V = 4.5 A), try a 6.3 A slow-blow fuse for that branch only (A).

### 6.3 Runtime (my estimate disagrees with the software plan)

| In a call | Watts at 5 V | Note |
|---|---|---|
| Pi 5 plus webcam and sound | 5 to 7 W | `sbc-selection.md` (A) |
| Screen | 2.5 W | Waveshare (V) |
| ESP32, sonars, servos holding | 1.5 W | (A) |
| **Sum at 5 V** | **9 to 11 W** | |
| From the battery (88 percent buck efficiency, A) | **10 to 12.5 W** | |

Two 2500 mAh cells in 2S hold 7.2 V x 2.5 Ah = 18 Wh. About 14 Wh is usable between 8.2 V and 6.4 V. That gives **about 1.1 to 1.4 hours of calling** and about 1.6 to 1.8 hours with the screen on and no call. The software plan says "2 to 3 hours of calling, 4 to 6 hours idle" for the same pack; I get about half. The difference is the screen, the ESP32 and the buck losses. A 2S2P pack (4 cells) doubles these numbers; 3500 mAh cells add 40 percent. **Measure it in stage 3** and write the real number on the family card. See C3.

---

## 7. Wiring table (inputs for the wiring diagram)

Every electrical part, where it connects, voltage, current and connector. "Pack" means the 2S pack after the main switch (6.0 to 8.4 V). All grounds are one common ground.

| Part | Connects to | Voltage | Current | Connector |
|---|---|---|---|---|
| Battery cells | 2-cell holder, wired in series, to the BMS (B+, BM, B-) | 6.0 to 8.4 V | 2 to 4 A typical, up to 10 A peak | holder wires or solder tags |
| BMS, charger board, main switch | pack lead to the splice plus through the main switch; minus to the splice minus | 6.0 to 8.4 V | 10 A continuous max | wire, spade lugs for the switch |
| Splice plus and minus | Wago 221-415 levers | 6.0 to 8.4 V | up to 10 A | lever connector |
| Fuse, BATT IN | splice plus, then the motherboard terminal BATT IN (+) | 6.0 to 8.4 V | 5 A slow-blow | in-line 5 x 20 mm, 5.08 mm screw terminal |
| XL4016 #1 (servo) | IN from splice through a 5 A fuse; OUT to terminal SERVO 5V IN | in 6.0 to 8.4 V, out 5.0 V | 5 A | lever and screw terminal |
| Fixed 5 V buck | IN from splice through a 2 A fuse; OUT to terminal CLEAN 5V IN | in 6.0 to 8.4 V, out 5.0 V | 0.5 A typical | lever and screw terminal |
| XL4016 #2 (SBC) | IN from splice through a 5 A fuse; OUT to the SBC pigtail and the screen lead | in 6.0 to 8.4 V, out **5.1 V** (set with a meter at the Pi) | 2 to 3 A typical, 5 A peak | lever; wire to the pigtail |
| SBC | USB-C pigtail from XL4016 #2; 1000 uF capacitor across 5.1 V and GND at the Pi end | 5.1 V | 1 to 1.5 A, peak 3 A (Pi 4) or 5 A (Pi 5) | USB-C plug with bare wires (AWG 18) |
| Screen | 5.1 V through a 1 A fuse to its micro-USB power lead; HDMI to the SBC HDMI0 | 5.1 V | 0.5 A | micro-USB pigtail, micro-HDMI to HDMI-A |
| Screen touch | SBC USB port | data only | 0 A | micro-USB to USB-A, data only |
| Webcam | SBC blue USB 3 port | 5 V from the SBC | 0.2 to 0.3 A | USB-A |
| Speakerphone or USB audio adapter | SBC USB 2 port | 5 V from the SBC | 0.05 to 0.5 A | USB-A |
| Speaker amplifier (route B) | 5 V from the SBC buck branch; input from the USB audio adapter | 5.1 V | up to 0.6 A | 2 wires, 3.5 mm plug |
| ESP32 devkit | motherboard J1 and J3 sockets; 5 V via D1 from CLEAN 5V IN; COM USB-C to the SBC | 5 V | 0.15 to 0.3 A | sockets; USB-A to USB-C data only |
| Left motor | terminal M1 (DRV A out 1 and 2) | 6.0 to 8.4 V pulsed | 0.2 to 0.4 A, stall 1.1 to 1.3 A | JST 2-pin |
| Right motor | terminal M2 (DRV A out 3 and 4) | 6.0 to 8.4 V pulsed | same | JST 2-pin |
| Pan servo | PCA9685 channel 0 | 5.0 V | 0.1 to 0.5 A, stall about 2 A | 3-pin servo plug and extension cable |
| Tilt servo | PCA9685 channel 1 | 5.0 V | same | same |
| Camera-live LED | PCA9685 channel 2 signal, 220 Ohm, LED, GND pin | 3.3 V logic | 6 mA | servo-type 3-pin plug (signal, GND used) |
| Button light (optional) | PCA9685 channel 3 | 3.3 V logic | 6 mA | same |
| Sonar 1 and 2 | SONAR 1 and 2 headers (5 V, TRIG, ECHO, GND) | 5 V | 15 mA each | 4-pin JST-XH |
| Cliff sensor left | SPARE pin 8 (GPIO21), 3V3 from pin 2, GND from pin 1 | 3.3 V | 20 to 30 mA | 3-wire plug |
| Cliff sensor right | SPARE pin 3 (GPIO3), 3V3, GND | 3.3 V | 20 to 30 mA | 3-wire plug |
| Call button | SPARE pin 5 (GPIO45) and GND pin 1 | 3.3 V logic | about 0 | 2-wire plug |
| Bump switches (optional) | SPARE pin 4 (GPIO46), 10 kOhm to 3V3, other side GND | 3.3 V logic | about 0 | 2-wire plug |
| ADS1115 | I2C SENSOR header: 3V3, GND, SDA (GPIO7), SCL (GPIO6); ADDR to GND | 3.3 V | 0.2 mA | 4-pin JST-XH |
| Battery divider | 47 kOhm from pack plus (after the main switch) to A0; 27 kOhm and 100 nF from A0 to GND | 0 to 3.07 V at A0 | 0.11 mA | solder or small terminal |
| Fan (Pi 4 only) | Pi 5 V header pins, or the Pi 5 fan header (Active Cooler) | 5 V | 0.1 to 0.2 A | 2-pin |

---

## 8. Conflicts between the specialists' files (and what I recommend)

| # | The conflict | Files | My recommendation | Who decides |
|---|---|---|---|---|
| **C1** | **Screen power source.** Mechanical: POWER OUT 5 V on the motherboard. Draft wiring diagram: 5.1 V SBC buck. | `mechanical-design.md` 6.2, `diagrams/wiring-robot2.png` | The SBC buck, with a 1 A fuse. Section 2.3. | wiring specialist |
| **C2** | **HDMI cable length.** SBC file says 30 to 50 cm; the mast route needs about 0.65 m. | `sbc-selection.md` 7, `mechanical-design.md` 6.2 | Buy 0.8 m, flat, slim, ideally right-angle at the screen end. | already in the parts list |
| **C3** | **Charge while on, and runtime.** Power list: charge with the robot off. Software plan wants a robot that can be called, and estimates 2 to 3 h in a call. My sum gives 1.1 to 1.4 h on 2 cells (section 6.3). A robot that is off cannot be called. | `pcb/kicad/shopping-list.md`, `software-plan.md` R3 and 7.8 | Use 2S2P (4 cells) in the comfortable build. Decide how the family charges it: switch on at agreed call times, or a charge-while-on design (power specialist). | owner and power specialist |
| **C4** | **Mass.** Mechanical: 2.6 kg, motors sized for 3.0 kg. Cheap build with a Pi 4 weighs about 2.7 kg; the comfortable build with 4 cells and a speakerphone about 3.2 kg. A 4-cell pack also needs a cradle about 77 x 80 x 21 mm instead of 77 x 40 x 21. | `mechanical-design.md` 5.3, 8 | The speakerphone (350 g) in the base works as the suggested ballast. Check the motor margin: the 5 degree ramp at 3.2 kg needs about 1.0 kg·cm per wheel, about 31 percent of the estimated stall torque of 3.2 kg·cm (29 percent at 3.0 kg in the mechanical doc). Still workable, but there is little extra. Update the cradle in the CAD if 4 cells are used. | mechanical specialist |
| **C5** | **Things the design has no place for:** the speaker (the lid grille faces backward, 10 cm from the microphone), a speakerphone, the camera-live LED hole, the call button hole, the camera cover, a third servo-type cable for the LED up the mast. | `mechanical-design.md` 6.2, 7.1; `software-plan.md` 3.5, 5.1 | Speaker in the base. 5 mm LED hole beside the camera window. A shelf or a flat spot for route A. A 3rd cable in the mast bundle (the bundle is 25 x 12 mm, plenty of room). | mechanical specialist |
| **C6** | **Motor voltage setting.** The software plan's default `mot_vmax` = 6 V assumes 3 to 6 V motors. The mechanical choice is a 12 V Pololu motor run from 6 to 8.4 V. | `software-plan.md` 7.3, `mechanical-design.md` 5.5 | Set `mot_vmax` to about 8 V (the pack's full level). At 6 V the speed is about 0.29 m/s instead of 0.36 m/s at 7.4 V. A setting only. | software specialist |
| **C7** | **3.3 V buck and fuse count.** Mechanical assumes two fixed bucks (clean 5 V and 3.3 V) and 5 fuse holders. Robot 2 does not use the 3.3 V buck (SPI screens and relays are not fitted). | `mechanical-design.md` 5.3, `diagrams/wiring-robot2.png` | Buy one fixed buck (5 V). Keep 5 fuse holders: BATT IN, servo, clean 5 V, SBC, screen. The free place in the base is harmless. | wiring specialist |
| **C8** | **The SBC's power draw vs the buck.** The Pi 5 can pull 5 A at peak. A 5 A input fuse sits at 4.5 A at the Pi's worst peak with a 6.4 V pack. The XL4016 needs headroom at a low pack. | `sbc-selection.md` 7, `pcb/kicad/shopping-list.md` | Not a conflict for typical use (2 to 3 A). Test at 6.4 V and 6.0 V input (section 6.2). | owner (bench test) |
| **C9** | **Two 5 V sources on the ESP32 USB link and the touch cable.** | `sbc-selection.md` 7, `software-plan.md` Stage 4 | Data-only cables for both, or tape. | wiring specialist |
| **C10** | **LED dimming on a servo board.** One PWM speed for all PCA9685 channels (50 Hz); dimmed or pulsing LEDs flicker. | `esp32-serial-protocol.md` 5.9 | Use on and off only for the camera LED. | software specialist |
| **C11** | **Bump switches have no pin and no event.** | `mechanical-design.md` 5.6, `software-plan.md` 7.6 | Optional: GPIO46 with a 10 kOhm pull-up. Or skip the switches; sonar and cliff sensors are enough for a first build. | software specialist |
| **C12** | **Pi 5 USB 600 mA limit** with a webcam and a speakerphone on a bare USB-C cable. | `sbc-selection.md` 7 | Set the config flag (check the official docs first). | owner |
| **C13** | **Price of the Pi 5.** `sbc-selection.md` says about 82.50 EUR (2 GB, Notebookcheck, 1 Oct 2026). A Berrybase snapshot in my search shows 68.90 EUR (2 GB) and 118.50 EUR (4 GB), probably from before the 2026 rises. | | Use 82.50 EUR. Check live. | owner |

**Checked and fine:** (a) the head's servos can carry even the heaviest screen listing (section 2.4); (b) the Pololu motors' 1.26 A stall at 8.4 V stays under the DRV8833's 1.5 A (mechanical doc); (c) the ADS1115 stays under 3.6 V (section 5.3); (d) four USB ports for four devices (section 6.1); (e) the Pi 5 with its Active Cooler fits under the cover (95 mm against 102.6 mm).

---

## 9. What is verified and what is assumed

**Verified (V), seen in a file or a web source:** Waveshare 7 inch (C) size 164.90 x 106.96 x 8 mm, 1024x600 IPS, 5-point capacitive touch, 5 V at 500 mA, 2.5 W; Eckstein item weight 0.32 kg; screen prices from five shops (45 to 62 EUR); Welectron Active Cooler 5.90 EUR; Pololu motor 3229 at US$29.95; Jabra Speak 410 prices (59.99 to 154 EUR); cell prices (3.99 to 10 EUR); XL4016 modules 3.25 to 11 EUR; PETG 9.75 to 13.45 EUR per kg; MG996R 4.50 to 13.29 EUR; pin table and header orders (`pin-table.md`); the software plan's divider values and levels; the SBC document's power draws and Pi 5 USB rule (third-party source).

**Assumed (A):** everything about the SC-012-SN259 (no information found); the screen's HDMI socket type and whether the touch and power are one or two micro-USB sockets; the speakerphone's size and weight; all small-part prices not listed above; the TCRT5000-type module at 12 mm from the floor; 220 Ohm LED current; GPIO46 pull-up; servo stall current; buck efficiency 88 percent; the runtime figures; the echo performance of route B.

**Not checked at all:** any call on the real hardware. The home test in `sbc-selection.md` section 10 and stages 1 and 3 in the software plan decide the open points.

---

## Sources

- Waveshare 7inch HDMI LCD (C) specifications: https://www.waveshare.com/wiki/Template:7inch_HDMI_LCD_C_Spec and https://waveshare.com/wiki/7inch_HDMI_LCD_(C)
- Screen prices: https://exp-tech.de/en/products/waveshare-7-capacitive-touch-screen-lcd-c-1024-x-600 , https://elecena.pl/product/29572644/waveshare-7inch-capacitive-touch-screen-lcd-c-with-bicolor-case-1024-600-hdmi-ips-low-power , https://elty.pl/en_US/p/LCD-display-7-1024x600-IPS-HDMI-housing/1714 , https://www.melopero.com/en/?p=115049 , https://opencircuit.shop/product/7inch-capacitive-touch-screen-lcd-c-1024-600 , Eckstein weight: https://eckstein-shop.de/Tier1_1__7_4?qf=6 , eBay.de no-name 7 inch listings (42.99 to 56.99 EUR).
- Jabra Speak 410 prices: https://www.ebay.de/itm/286702464437 , https://aio.lv/en/product--jabra-7410-109--333442.md (84.99 EUR, June 2026), https://www.galaxus.de/en/s1/product/jabra-speak-410-conference-devices-268588 . Cheap speakerphone listing at 16.99 EUR (eBay) and Nearity A20S (Linux listed, no price).
- Software echo cancelling on Linux (background): https://github.com/rhasspy/echo-canceller
- Pololu 25D 47:1 MP 12 V (item 3229): https://www.pololu.com/product/3229/resources
- Pi 5 Active Cooler: https://welectron.com/Official-Raspberry-Pi-Active-Cooler-Cooler-for-Pi-5
- Cells: Kaufland (Samsung 25R 6.00 and 9.00 EUR, Molicel P28A 8.96 EUR, LG MJ1 5.95 to 10.05 EUR), Nkon (P28A 3.99 EUR incl. VAT), https://www.nkon.nl/default/molicel-inr18650-p28a-2800mah-35a.html
- XL4016 prices: eBay.de listings (3.25 to 4.50 EUR), a Dutch shop 6.01 to 6.95 EUR, AZ-Delivery via https://elecena.pl/product/20759922/xl4016e1-dc-dc-step-down-converter-adjustable-5-40v-to-1-2-36v-12a-compatible-with-arduino
- Wago 221: https://www.berrybase.de/wago-221-412-verbindungsklemme-2-fach and Hornbach listings
- PETG: https://www.mydealz.de/deals/amazon-prime-sunlu-4-x-1kg-petg-filament-bundle-175mm-975eurkg-2795450
- MG996R: eBay.de listings; datasheet at roboter-bausatz.de (https://roboter-bausatz.de/media/pdf/15/f5/87/RBS10997-MG996R-Datenblatt.pdf)
- Project files read: `00-brief.md`, `sbc-selection.md`, `software-plan.md`, `esp32-serial-protocol.md`, `mechanical-design.md`, `pcb/kicad/pin-table.md`, `shopping-list.md`, `parts-list.md`, `README.md`, `diagrams/draw_wiring.py` and `wiring-robot2.png`.
- Not reachable or not found: any page for SC-012-SN259; any shop page for Berrybase or Reichelt; a tested Chromium echo report for this setup.
