# Robot 2: the full parts list

Written 5 November 2026 for the telepresence robot. This is everything you need to buy to build robot 2 **from the motherboard onwards**, with prices, shops, weights and a shopping split. The same list is in `parts-list.csv` (one line per part, same rows, same words, for a spreadsheet; section 2 says how to add up a build). The reasons behind the choices are in `peripherals.md` (screen, camera, sound, sensors) and in the other files named below.

**Words used here.** SBC = single board computer (the Raspberry Pi). Motherboard = your 100 x 100 mm ESP32 board (version v5; you report 5 boards ordered: confirm they are v5, see group 8). Buck = a module that lowers a voltage. BMS = the battery protection board. Carry-on = hand luggage. EUR prices are "about" prices for Germany, from web search snapshots; I could not open most shop pages. Check the live price when you buy.

**How sure am I.** (V) = I saw it in a web source or file. For a web page whose text I could not open this means "search summary only, re-check the page". (A) = assumed or my own guess. The "Note" column says which. Prices without (V) are estimates.

---

## 1. The short answer

| | **Cheap build** (works, no frills) | **Comfortable build** (what I would buy) |
|---|---|---|
| SBC | Raspberry Pi 4 Model B 2 GB | Raspberry Pi 5 2 GB with Active Cooler |
| Screen | no-name 7 inch HDMI touch | Waveshare 7 inch HDMI LCD (C) |
| Camera | your own SC-012-SN259 (if it passes the test) | a new wide-angle 1080p webcam with microphone |
| Sound | USB audio adapter + small speaker + amplifier with its own fuse (route B, about 15 EUR) | USB speakerphone with echo cancelling (route A, about 75 EUR) |
| Battery | 2 cells (2S) | 4 cells (2S2P): double the runtime |
| Extras | spare SD card, LAN cable, small keyboard and card pouches (24.00 EUR, needed by stage 9); the data-only adapters, the right-angle USB adapters and the call / STOP button are in both builds | spares, tools, travel kit |
| **Price, everything bought new** | **581.60 EUR** | **820.80 EUR** |
| of which the robot itself (groups 1 to 8) | 553.60 EUR | 707.80 EUR |
| of which tools, spares and travel kit (groups 9 and 10) | 28.00 EUR | 113.00 EUR |
| **Cash needed if you already have the "maybe-spare" items** (old cells, wire, screws, tools, cables) **and the board-order parts** | **416.50 EUR** | **614.20 EUR** |
| Cash needed if robot 1 also waits (you take its Pi 5, servos, BMS, charger, bucks, switch, sonar and fan) | 365.50 EUR | 486.70 EUR |
| Parts to buy in Germany **before the trip** | 389.70 EUR | 579.90 EUR |
| Parts easy to buy **anywhere** | 191.90 EUR | 240.90 EUR |
| In-line fuse holders (5 x 20 mm) | 6 (5 + one for the amplifier, route B) | 5 |
| **Weight of the finished robot** (sum of this list; the CAD says 2.6 and 3.0 kg, see section 7) | **2.8 kg** | **3.3 kg** |
| Carried extras (spares, tools, charger, box, keyboard) | 0.6 kg | 1.7 kg |

Optional parts that are in no total (bump switches, clip-on microphone, 8.4 V charger adapter, TVS diode, servo tester, 6.3 A fuses, bench power supply): 64.10 EUR.

**Four things to know:**

1. **The three biggest costs are the motors (about 72 EUR for two Pololu motors including shipping and VAT), the SBC (72 to 83 EUR) and the screen (45 to 58 EUR).** In the cheap build these three come to 189 EUR, about a third of 581.60 EUR.
2. **You can lower the cost by taking robot 1's parts.** Your own Pi 5 8 GB saves 72 EUR (cheap) or 82.50 EUR (comfortable) but leaves robot 1 without a brain during the trip. Old 18650 cells save 12 to 24 EUR (test them; matched cells only, same voltage within 0.05 V before joining).
3. **The comfortable build is above the 3.0 kg that the motors were sized for:** 3.03 kg by the CAD, about 3.3 kg by the sum of this list (the list weighs every pack and cable in full, section 7). The cheap build is 2.61 kg by the CAD and about 2.8 kg by this list. See `peripherals.md` section 8, conflict C4.
4. **The runtime on two cells is short: about 1.1 to 1.4 hours of calling, and about 1 hour or less if the robot also drives; four cells give about 2.2 to 2.8 hours of calling** (my sums, all ASSUMED, `peripherals.md` section 6.3; Stage 3 measures them). The buy decision (2 or 4 cells) assumes about 1 hour. That is why the comfortable build has four cells. Family routine: switch the robot on at the agreed call times and charge it with the robot off.

---

## 2. How to read the tables

- **Build:** `both` = in both builds. `cheap` = only in the cheap build. `comfort` = only in the comfortable build. `opt` = optional, in no total.
- **Owned?** `no` = you do not own it. `maybe-spare` = probably in your drawer (old cells, wire, screws, tools, cables). `maybe-robot1` = **you own one for robot 1; robot 2 needs its own: buy twice** (or take robot 1's and wait). `maybe-board` = comes from the parts order for the boards (you report 5 boards ordered); check what you ordered and that it is version v5.
- **Trip:** `DE` = **buy in Germany before the trip** (special part, slow delivery, or it must be tested at home). `any` = easy to buy abroad too (it is still needed for the build at home, so buy it in time).
- **g** (grams) are in `parts-list.csv` and in the weight tables in section 7.
- Prices are for the whole line (quantity times price each).
- **The CSV file** has the same rows, in the same order, with the same words in the Build, Owned? and Trip columns. Its columns are: `group`, `item`, `quantity`, `unit_price_eur`, `total_eur`, `build`, `already_owned_maybe`, `buy_where`, `buy_before_trip`, `weight_g`, `on_robot` (`yes` = counts in the robot's weight, `no` = carried in the luggage) and `notes`.
- **How to add up a build in a spreadsheet.** In the CSV, `total_eur` is column E, `build` is column F, `already_owned_maybe` is column G and `buy_before_trip` is column I. **Do not just double-click the CSV file.** A German-language Excel expects semicolons and may put everything into column A (known Excel behaviour; I could not test it here), so the figures would sit in the wrong columns. In Excel use Data > From Text/CSV, set the delimiter to Comma and, if it offers a language or locale choice, English (United States). In LibreOffice Calc use File > Open, tick Comma as the only separator and set the number columns to English (USA). (A: menu names differ a little between versions.) Otherwise the decimal points are misread. Then type the formulas with those column letters. Cheap build = `=SUMIF(F:F,"both",E:E)+SUMIF(F:F,"cheap",E:E)` = 581.60 EUR. Comfortable build = `=SUMIF(F:F,"both",E:E)+SUMIF(F:F,"comfort",E:E)` = 820.80 EUR. Before the trip, cheap build: `=SUMIFS(E:E,F:F,"both",I:I,"DE")+SUMIFS(E:E,F:F,"cheap",I:I,"DE")` = 389.70 EUR. Cash needed, cheap build: `=SUMIFS(E:E,F:F,"both",G:G,"no")+SUMIFS(E:E,F:F,"both",G:G,"maybe-robot1")+SUMIFS(E:E,F:F,"cheap",G:G,"no")+SUMIFS(E:E,F:F,"cheap",G:G,"maybe-robot1")` = 416.50 EUR (this leaves out the `maybe-spare` and `maybe-board` lines); leave out the two `maybe-robot1` terms for the lowest figure, 365.50 EUR. For the comfortable build use `"comfort"` instead of `"cheap"` (before the trip 579.90 EUR; cash needed 614.20 EUR; lowest 486.70 EUR). In a German-language spreadsheet the functions are called `SUMMEWENN` and `SUMMEWENNS` and the separator is a semicolon, for example `=SUMMEWENN(F:F;"both";E:E)+SUMMEWENN(F:F;"cheap";E:E)` and `=SUMMEWENNS(E:E;F:F;"both";I:I;"DE")+SUMMEWENNS(E:E;F:F;"cheap";I:I;"DE")`. Never add the `opt` lines. A plain sum of the whole column is wrong (it counts both builds and the optional parts).

---

## 3. The list

Robot 2 is built at home, before the trip. **Required before the trip:** stages 1 to 5, 7 and 9 of the software plan, plus the safety part of stage 8 (cliff sensors, tilt and pick-up detection, family STOP). Stage 6 (pan and tilt) is strongly recommended: it is a Must function. The rest of stage 8 (sonar tuning, the wall-stop test, camera-off at USB level) is recommended; the bump switches are not in the first build. Remote driving stays switched off in the software until the cliff and tilt tests pass, and the first drives at the destination are with your sister next to the robot, away from stairs. The required stages take about 8 evenings (A: stages 1 to 5, 7 and 9, plus the safety part of stage 8; more with stage 6 and the rest of stage 8). So nearly everything has to be bought in Germany first.

#### Group 1 Brain and screen

| Item | Qty | EUR each | EUR total | Build | Owned? | Buy where | Trip | Note |
|---|---|---|---|---|---|---|---|---|
| Raspberry Pi 4 Model B, 2 GB (the cheapest board that really works) | 1 | 72.00 | 72.00 | cheap | no | Berrybase, Reichelt, Welectron | DE | About 71.90 EUR on 1 Oct 2026 (Notebookcheck). Runs near full load in a 720p call, so the first call is asked at 480p. Fan and performance mode needed (sbc-selection.md, section 3). |
| Raspberry Pi 5, 2 GB (recommended board) | 1 | 82.50 | 82.50 | comfort | maybe-robot1 | Berrybase, Reichelt, Welectron | DE | About 82.50 EUR (Notebookcheck, 1 Oct 2026). 4 GB costs about 115-150 EUR. Free option: take your own Pi 5 8 GB if robot 1 can wait. |
| Raspberry Pi 5 Active Cooler (official) | 1 | 5.90 | 5.90 | comfort | no | Welectron (5.90 EUR incl. VAT, art. RP9-111480) | DE | Pi 5 only. Fits under the cover (cooler 13.7 mm high). |
| Heatsink plus small 5 V fan for the Pi 4 | 1 | 6.00 | 6.00 | cheap | maybe-robot1 | Amazon.de, Berrybase | DE | You own a 5 V fan for robot 1; robot 2 needs its own. About price (ASSUMED). |
| microSD card 32 GB, A1 or A2, SanDisk or Samsung (main card) | 1 | 9.00 | 9.00 | both | no | any shop | any | About price (ASSUMED). Buy a known brand, not an unnamed one. |
| microSD card 32 GB (clone = spare card) | 1 | 9.00 | 9.00 | both | no | any shop | any | Clone the finished card onto it (stage 9; the spare card is a pass test there). Packed in the luggage, not in the robot. |
| 7 inch HDMI screen, 1024x600 IPS, touch: no-name type | 1 | 45.00 | 45.00 | cheap | no | eBay.de, Amazon.de | DE | Listings 43-57 EUR (eBay.de search). Check outline about 165x100-107 mm, full-size HDMI, 5 V micro-USB. Weight varies. |
| Waveshare 7 inch HDMI LCD (C), 1024x600 IPS, 5-point touch (recommended screen) | 1 | 58.00 | 58.00 | comfort | no | exp-tech.de, Eckstein, Welectron, elecena.pl, melopero.com | DE | Seen 48-62 EUR incl. VAT depending on shop (exp-tech.de 44.95 EUR is without VAT, about 53.50 with VAT; search summaries, re-check the shop page). 164.9x107x8 mm, 5 V 500 mA (Waveshare wiki). Stock varies: order early. |
| HDMI cable, micro-HDMI to HDMI-A, flat and slim, 0.8 m | 1 | 12.00 | 12.00 | both | no | Amazon.de, Reichelt | DE | Needs about 0.65 m (mast route); sbc-selection.md now says the same. Right-angle plug at the screen end is better. |
| Screen power lead: micro-USB plug with bare wires, power only | 1 | 3.00 | 3.00 | both | maybe-spare | any (cut an old micro-USB cable) | any | Wires go to the 5.1 V SBC buck branch (not to the clean 5 V). Via the 1 A fuse. |
| USB-C plug breakout board with solder pads, for the SBC power pigtail (you solder your own AWG 18-20 silicone wire to ALL the VBUS and GND pads) | 1 | 5.00 | 5.00 | both | no | Amazon.de, eBay.de | DE | Or cut a thick 5 A USB-C cable and read the wire gauge printed on its jacket. If the wire is thinner than AWG 20, use a 3 A fuse on this branch (the fuse assortment in group 4 should have one: check the listing) and accept a Pi 5 peak limit; with a Pi 4 get thicker wire instead (sbc-selection.md, section 7, points 4 and 5). Short: under 40 cm. The wire is the silicone wire line in group 4. About price (ASSUMED). |
| Capacitor 1000 uF, 16 V, low-ESR (at the SBC power input) | 1 | 0.60 | 0.60 | both | maybe-spare | Reichelt | any | Across 5.1 V and GND at the Pi end. 470 uF also fine. |
| USB-A to USB-C cable, short (20 cm), ordinary (has the 5 V wire), for the ESP32 COM socket | 1 | 4.00 | 4.00 | both | maybe-spare | any | any | Plug it into the data-only adapter below. It is also the one spare ordinary cable: if bench test B fails (the two bench tests are written out in peripherals.md, 6.1), use it on its own. Taping the 5 V contact (pin 1 of the USB-A plug) is a backup only. |
| USB data-only adapter (power blocker, no 5 V wire), for the ESP32 link and for touch | 2 | 5.00 | 10.00 | both | no | Amazon.de (search: USB power blocker / Stromsperre) | DE | One for the ESP32 link, one for the touch cable. Not the same as a 'data blocker' (that blocks data). Check the ESP32 one with bench test A (the devkit's LED stays dark, peripherals.md, 6.1) and the touch one with the screen-dark check (peripherals.md, 2.2). About price (ASSUMED). |
| Touch cable, micro-USB to USB-A, thin, about 1 m, data (the screen box may already contain one: check that it reaches the SBC through the mast, about 0.65 m plus slack) | 1 | 3.00 | 3.00 | both | maybe-spare | any (or the one from the screen box) | any | It goes into the second data-only adapter. Keep it uncut: the screen power lead is a separate cable. About price (ASSUMED). |
| USB-A right-angle adapter (90 degrees, male plug to female socket), for the webcam, the ESP32 link, the touch cable and the sound adapter or speakerphone | 4 | 2.50 | 10.00 | both | no | Amazon.de, eBay.de | DE | The USB ports face the rear wall and only 20 to 42 mm of room is left (mechanical-design.md, 5.2), so straight plugs and the data-only adapters would press on the wall. Dry-fit with the real parts before you print the base. If the webcam gets the extension cable below, its adapter is a spare. About price (ASSUMED). |
| USB-A extension cable, about 1 m, male right-angle plug to female socket (for a webcam whose cable is fixed to the camera) | 1 | 4.00 | 4.00 | both | no | Amazon.de, eBay.de | DE | mechanical-design.md, 6.2: the camera's own plug joins it inside the head. Needed if the camera cable cannot be unplugged (most cannot). About price (ASSUMED). |
| **Group total** | | | | | | | | **cheap build 192.60 EUR, comfortable build 216.00 EUR** |

#### Group 2 Camera and audio

| Item | Qty | EUR each | EUR total | Build | Owned? | Buy where | Trip | Note |
|---|---|---|---|---|---|---|---|---|
| Webcam: your own SC-012-SN259, if it passes the test | 1 | 0.00 | 0.00 | cheap | maybe-robot1 | from robot 1 (phase 3 has not started) | DE | Model not found on the web: size, view angle and microphone are ASSUMED. Test first (peripherals.md). Buy another for robot 1 later. |
| Wide-angle USB webcam, 1080p, UVC, with microphone (fallback or comfort) | 1 | 22.00 | 22.00 | comfort | no | Amazon.de | DE | About 15-30 EUR (ASSUMED). Check body fits the brow 60x30x28 mm and view angle 90-110 degrees. |
| USB audio adapter (3.5 mm speaker out) | 1 | 7.00 | 7.00 | cheap | no | Amazon.de, eBay.de | any | Cheap audio route B. Not needed with route A (speakerphone). |
| Speaker 40 mm, 4 ohm, 3 W | 1 | 2.50 | 2.50 | cheap | no | Reichelt, eBay.de | any | Goes in the cover top, right of the mast, facing up; not in the head lid (echo). The CAD has the grille and the pocket (mechanical-design.md, 7.1); the 15 mm depth is ASSUMED, measure yours. |
| PAM8403 amplifier board, 5 V | 1 | 2.50 | 2.50 | cheap | no | eBay.de, AZ-Delivery | any | Powered from the 5.1 V Pi-buck output through its OWN 1 A fuse (6th fuse holder, group 4), not through the screen fuse. Input from the USB audio adapter through the audio cable below. |
| Audio cable, 3.5 mm plug to bare wires (or a cut aux cable), for the amplifier input | 1 | 1.50 | 1.50 | cheap | maybe-spare | any (cut an old aux cable) | any | Route B only. Two wires (signal and ground) go to the amplifier input; the plug goes into the green socket of the USB audio adapter. |
| USB speakerphone with real echo cancelling (Jabra Speak 410 class) | 1 | 75.00 | 75.00 | comfort | no | Amazon.de, Galaxus.de, eBay.de | DE | Seen 60-85 EUR (eBay new 59.99, a shop 84.99 in Jun 2026). Cheaper ones (17-31 EUR) do not say 'echo cancellation': do not trust them. Weight and size ASSUMED. Doubles as ballast. The CAD has a flat spot of 115 mm diameter on the cover top, behind the mast (mechanical-design.md, 7.1). |
| LEDs 5 mm red, 5 pieces, plus 220 ohm resistors | 1 | 2.00 | 2.00 | both | maybe-spare | Reichelt, any | any | Plain red LEDs that light at 3.3 V. Camera-live LED on PCA9685 channel 2 (and button light on channel 3). If every PCA9685 output already has a 220 ohm resistor (small SMD parts marked 221), connect the LED with NO extra resistor and check the brightness. |
| USB clip-on microphone (only if the webcam has no microphone) | 1 | 8.00 | 8.00 | opt | no | Amazon.de | any | Only needed if the webcam test finds no microphone and you use route B. |
| **Group total** | | | | | | | | **cheap build 15.50 EUR, comfortable build 99.00 EUR** |

#### Group 3 Sensing

| Item | Qty | EUR each | EUR total | Build | Owned? | Buy where | Trip | Note |
|---|---|---|---|---|---|---|---|---|
| HC-SR04 ultrasonic sensor, 5 V type (not the 3.3 V HC-SR04P) | 2 | 2.00 | 4.00 | both | maybe-robot1 | AZ-Delivery, Berrybase, eBay.de | DE | The board's 1k/2k divider expects a 5 V echo. |
| HC-SR04 spare | 1 | 2.00 | 2.00 | comfort | no | AZ-Delivery, Berrybase, eBay.de | DE | Spare. |
| IR floor sensor module, TCRT5000 type, digital output, 3.3-5 V (cliff) | 2 | 1.50 | 3.00 | both | no | eBay.de, Amazon.de | DE | About 31x14 mm per mechanical doc (ASSUMED). Must work at 12 mm from the floor. |
| IR floor sensor spares, to find a pair that reads your floor | 2 | 1.50 | 3.00 | both | no | eBay.de, Amazon.de | DE | Dark carpet can fool IR sensors. Buy 4 modules in both builds, test them on your floors and keep the best two (peripherals.md, 5.2): the cliff sensors are part of the required safety stage. |
| ADS1115 16-bit analog-to-digital board (battery monitor) | 1 | 4.50 | 4.50 | both | no | eBay.de, AZ-Delivery, Reichelt | DE | 3.5-5 EUR on eBay.de, up to about 13 EUR in local shops (software-plan listing check). |
| ADS1115 spare | 1 | 4.50 | 4.50 | comfort | no | eBay.de, AZ-Delivery, Reichelt | DE | Spare. |
| Resistor and capacitor kit: 47k x2, 27k x2 (1 %), 10k x4, 100 nF x4 | 1 | 5.00 | 5.00 | both | maybe-spare | Reichelt, any | any | Battery divider 47k/27k + 100 nF (the 47k sits on the splice-plus wire, the 27k and 100 nF at the ADS1115). Charger sense 2 x 10k (optional). A 10k is also the bump-switch pull-down (optional). |
| Call / STOP button, arcade type 30 mm (optionally with a 3.3 V LED ring) | 1 | 3.50 | 3.50 | both | no | Amazon.de, Reichelt | DE | GPIO45 to GND. A physical STOP / call button is a Must before the trip (functions.md, rows 9 and 12), so it is in both builds. The CAD has a 30 mm hole on the cover top, left of the mast (mechanical-design.md, 7.1; size ASSUMED, measure your button). A button light must work at 3.3 V: not a 12 V arcade ring. |
| Micro switch with lever (KW12-3 type), 2 pieces, bumper | 1 | 2.00 | 2.00 | opt | no | Amazon.de, eBay.de | any | Optional, not in the first build. If fitted: switches between GPIO46 and 3V3, plus a 10k pull-DOWN from GPIO46 to GND (peripherals.md, 5.4). The protocol lists GPIO46 as 'optional bump input' (event ev btn id:bump). |
| **Group total** | | | | | | | | **cheap build 23.00 EUR, comfortable build 29.50 EUR** |

#### Group 4 Power

| Item | Qty | EUR each | EUR total | Build | Owned? | Buy where | Trip | Note |
|---|---|---|---|---|---|---|---|---|
| 18650 Li-ion cell, genuine Samsung 25R / LG MJ1 / Molicel P28A class | 2 | 6.00 | 12.00 | both | maybe-spare | Akkuman, Akkuteile.de, Nkon | DE | Seen 3.99-10 EUR per cell. You own old cells: test them first and use a matched pair (same voltage within 0.05 V before joining). Carry-on only. |
| 18650 cells, 2 more (the 4-cell option, 2S2P: double runtime) | 2 | 6.00 | 12.00 | comfort | maybe-spare | Akkuman, Akkuteile.de, Nkon | DE | All four cells from the same batch and the same model, brought to the same voltage within 0.05 V before joining. Build 2P, then 2S, one BMS only: see wiring.md, section 'Four-cell option (2S2P)' and diagrams/battery-4cell.png. Needs a bigger battery cradle in the base (about 77 x 80 x 21 mm). The robot then weighs about 3.3 kg by the sum of this list (3.03 kg by the CAD). |
| Battery holder for 2 x 18650 | 1 | 2.00 | 2.00 | both | no | Amazon.de, Reichelt | any | 77x40x21 mm per mechanical doc. The BMS needs a wire at the point between the two cells (BM): use a 2-cell holder where you can reach that point, or two single-cell holders. 4-cell option: four single-cell holders in total, or two 2-cell holders whose middle point you can reach and join (next line). |
| Battery holder, 2nd set for the 4-cell option (four single-cell holders in total, or two 2-cell holders whose middle point you can reach and join) | 1 | 2.00 | 2.00 | comfort | no | Amazon.de, Reichelt | any | This line is one more 2-cell holder or two more single-cell holders (about 2 EUR either way, ASSUMED). A 2-cell holder that is wired in series inside has no middle wire and cannot make the pairs: check this when it arrives, and if there is no middle wire or tag, use single-cell holders. How to join them (2P, then 2S): wiring.md, section 7 'Four-cell option (2S2P)' and diagrams/battery-4cell.png. |
| 2S BMS (HX-2S-JH20 type), balancing | 1 | 3.00 | 3.00 | both | maybe-robot1 | Amazon.de, eBay.de | DE | Buy twice if robot 1 keeps its own. One BMS only, also with 4 cells. |
| 2S USB-C charger board (IP2326 type, 5 V in, 8.4 V out) | 1 | 5.00 | 5.00 | both | maybe-robot1 | Amazon.de, eBay.de | DE | Charge with the robot off (power list). See conflict C3 in peripherals.md. |
| USB-C wall charger 5 V, at least 2 A (for the charger board) | 1 | 9.00 | 9.00 | both | maybe-spare | any (plug type of the destination) | any | Buy it where you stay if the plug differs. |
| USB-A to USB-C charging cable, 1 m | 1 | 4.00 | 4.00 | both | maybe-spare | any | any |  |
| Main switch, round rocker, 10 A or more, 19 mm hole | 1 | 2.50 | 2.50 | both | maybe-robot1 | Amazon.de, Reichelt | any | You own a key switch for robot 1. This one is for the rear wall. |
| In-line fuse holder for 5 x 20 mm fuses | 5 | 1.20 | 6.00 | both | no | Reichelt, Amazon.de | DE | Five branches: BATT IN, servo buck, clean 5 V buck, SBC buck, screen. The 3.3 V buck is not used in robot 2. |
| In-line fuse holder for 5 x 20 mm fuses, 6th holder (route B: own 1 A fuse for the speaker amplifier) | 1 | 1.20 | 1.20 | cheap | no | Reichelt, Amazon.de | DE | Route B (cheap build) only. The amplifier gets its own tap from the 5.1 V Pi-buck output through its own 1 A fuse; the screen keeps its own 1 A fuse. With the speakerphone (route A) there is no amplifier and five holders are enough. The 1 A fuse comes from the assortment below. |
| Slow-blow fuses 5 x 20 mm, assortment (1 A, 2 A, 3 A, 5 A) | 1 | 5.00 | 5.00 | both | no | Reichelt, Amazon.de | DE | Needs: 5 A x3 (BATT IN, servo buck, Pi buck), 2 A x1 (clean 5 V buck), 1 A x2 (screen, and the amplifier in route B), plus spares. The 3 A is only for a Pi pigtail wire thinner than AWG 20 (it replaces the 5 A on the Pi branch). Check that the assortment you buy lists 3 A; if it does not, buy one single 3 A slow-blow only if your wire turns out to be thin. The optional 6.3 A slow-blow for the Pi branch is the next line. |
| Slow-blow fuse 5 x 20 mm, 6.3 A (spare for the Pi branch, only if the 5 A fuse blows in rare peaks) | 2 | 0.30 | 0.60 | opt | no | Reichelt, Amazon.de | DE | Optional, not in the totals. Use it only with AWG 18 to 20 wire (peripherals.md, 6.2). About price (ASSUMED). |
| Lever connector Wago 221-415 (5-way) | 4 | 1.20 | 4.80 | both | no | Berrybase, Reichelt, Hornbach | any | Splice plus and splice minus: two connectors per side, each pair joined by a 10 cm jumper wire in a free slot of each. The plus side has 6 wires, the minus side up to 7. Budget 1.20 EUR each (ASSUMED): 2-way pieces were seen at 0.39 to 0.55 EUR, no 5-way price was seen. |
| XL4016 buck module with heatsink (servo 5.0 V, and SBC 5.1 V) | 2 | 6.00 | 12.00 | both | maybe-robot1 | eBay.de 3-5 EUR, Amazon.de or AZ-Delivery 8-11 EUR | DE | Two are needed. You own one for robot 1: buy two new. After setting each one with a multimeter, lock the adjust screw with a drop of glue or nail varnish. |
| Fixed 5 V buck, 1.8 A (clean 5 V) | 1 | 2.50 | 2.50 | both | maybe-robot1 | eBay.de, Amazon.de | DE | Input range must cover 6-8.4 V. After any luggage trip, re-measure all three buck outputs with nothing connected before you plug in the Pi or the ESP32. |
| Silicone wire 1.0 mm2 (AWG 18), red and black, 3 m each | 1 | 7.00 | 7.00 | both | maybe-spare | Amazon.de, Reichelt | any | Battery, buck and SBC branches, the 10 cm jumpers between the lever connectors, and the second servo feed to the PCA9685 screw terminal. Weight = what is used. |
| Wire 0.5 mm2 and thinner, several colours | 1 | 8.00 | 8.00 | both | maybe-spare | Amazon.de, Reichelt | any | Sensors, LED, screen power. |
| JST-XH plug kit 2/3/4-pin with crimped wires | 1 | 9.00 | 9.00 | both | maybe-spare | Amazon.de | any | Board headers are JST-XH / 2.54 mm. You said your plugs fit. |
| Wire end ferrules, assortment | 1 | 5.00 | 5.00 | comfort | no | Amazon.de | any | For the screw terminals and lever connectors. |
| Servo extension cable 50 cm, 3-wire | 3 | 2.00 | 6.00 | both | no | Amazon.de, eBay.de | DE | Pan, tilt, and the camera LED up the mast. For the LED use a 3-pin plug with the red (V+) wire cut off or taped. |
| Spade lugs (flat crimp terminals), 6.3 mm, small assortment, for the main switch | 1 | 3.00 | 3.00 | both | maybe-spare | Amazon.de, Reichelt | any | The main switch has spade tabs (wiring.md, peripherals.md section 7). Check the tab width of your switch: 6.3 mm is common (ASSUMED). About price (ASSUMED). |
| Single-cell 18650 charger (TP4056 type) | 1 | 3.00 | 3.00 | comfort | maybe-spare | Amazon.de, eBay.de | any | 4-cell option only: to bring the lower cells up to the same voltage (within 0.05 V) before they are joined (wiring.md, section 7, Four-cell option). Also handy for old cells. About price (ASSUMED). |
| TVS diode SMBJ5.0A (optional protection across the Pi supply wires) | 1 | 0.50 | 0.50 | opt | no | Reichelt, eBay.de | any | Optional, not in the totals. |
| 8.4 V 2 A charger adapter with DC jack (idea for charging while on) | 1 | 10.00 | 10.00 | opt | no | Amazon.de | DE | Only if the power design decides to charge while the robot runs. Not decided: conflict C3. |
| **Group total** | | | | | | | | **cheap build 102.00 EUR, comfortable build 122.80 EUR** |

#### Group 5 Drive

| Item | Qty | EUR each | EUR total | Build | Owned? | Buy where | Trip | Note |
|---|---|---|---|---|---|---|---|---|
| Pololu 25D metal gearmotor 12 V, medium power, 47:1 (item 3229) | 2 | 36.00 | 72.00 | both | no | Pololu.com, or an EU reseller (Eckstein, Botland) | DE | Pololu US$29.95 each (search summary only, re-check the page). Plus shipping, 19 % VAT, maybe a courier fee: about 30-45 EUR each delivered (ASSUMED). 2-3 weeks. When they arrive, measure the winding resistance with a multimeter: about 6.7 ohm is expected (12 V / 1.8 A). If it reads well below 5 ohm, do not fit them to the DRV8833 (peripherals.md, section 8). |
| Robot wheels 65 mm, rubber tyre, hub for 4 mm D-shaft (pair) | 1 | 10.00 | 10.00 | both | no | Amazon.de, eBay.de, robot shops | DE | Bore is ASSUMED to fit the Pololu 4 mm D-shaft: check before buying. |
| Hub adapters 4 mm D-shaft for wheels (only if the wheel bore does not fit) | 1 | 8.00 | 8.00 | comfort | no | Pololu, Amazon.de | DE | Insurance. |
| Steel ball 16 mm (or 5/8 inch) for the caster | 1 | 1.50 | 1.50 | both | no | hardware store, Amazon.de | any |  |
| Steel ball 16 mm, spare | 1 | 1.50 | 1.50 | comfort | no | hardware store, Amazon.de | any |  |
| **Group total** | | | | | | | | **cheap build 83.50 EUR, comfortable build 93.00 EUR** |

#### Group 6 Pan/tilt

| Item | Qty | EUR each | EUR total | Build | Owned? | Buy where | Trip | Note |
|---|---|---|---|---|---|---|---|---|
| MG996R servo, metal gear (pan and tilt) | 2 | 8.00 | 16.00 | both | maybe-robot1 | Amazon.de, eBay.de (4.50-7 EUR), Waveshare 13 EUR | DE | PCA9685 channel 0 = pan, channel 1 = tilt. Buy twice if robot 1 keeps its servos. |
| Aluminium servo horn 25T, 20 mm disc, 4 x M3 holes | 2 | 3.50 | 7.00 | both | no | Amazon.de, AliExpress | DE | Hard to find locally. The kit's plastic horn is not used. |
| MG996R spare | 1 | 8.00 | 8.00 | comfort | no | Amazon.de, eBay.de | DE | Spare. |
| **Group total** | | | | | | | | **cheap build 23.00 EUR, comfortable build 31.00 EUR** |

#### Group 7 Mechanical hardware

| Item | Qty | EUR each | EUR total | Build | Owned? | Buy where | Trip | Note |
|---|---|---|---|---|---|---|---|---|
| Heat-set insert assortment M2-M5, brass | 1 | 11.00 | 11.00 | both | no | Amazon.de | DE | Needs 37 x M3 and 8 x M4 (plus 20 % spare). Mechanical doc, section 10. |
| Screw and nut assortment M2.5/M3/M4/M5 hex socket, 6-30 mm | 1 | 16.00 | 16.00 | both | maybe-spare | Amazon.de, Reichelt | any | Counts in mechanical doc section 10: about 64 x M3, 12 x M4, 4 x M2.5. The 4 motherboard screws are M3 x 6. |
| M5 x 30 bolt with lock nut and 2 washers | 1 | 1.00 | 1.00 | both | maybe-spare | any | any | Head pivot. |
| PTFE adhesive tape 0.2 mm (turntable glide ring) | 1 | 6.00 | 6.00 | both | no | Amazon.de | DE | About price (ASSUMED). |
| PETG filament 1 kg spool, 1.75 mm (printed parts weigh about 1.13 kg) | 2 | 13.00 | 26.00 | both | no | Amazon.de, eBay.de | any | Seen 9.75-13.45 EUR per kg (deals Jun 2026). Weight = printed parts of the first build without the bumper (3d/tools/results/numbers.txt). Buy the filament first, so that printing (about 44 hours) can start. No tube needed: the mast is printed. |
| Super glue plus 2-part epoxy | 1 | 6.00 | 6.00 | both | maybe-spare | any | any | Base seams. |
| Double-sided foam mounting tape | 1 | 4.00 | 4.00 | both | maybe-spare | any | any | Modules, screen, webcam. |
| Zip ties 2.5 x 100 mm, 100 pieces | 1 | 3.00 | 3.00 | both | maybe-spare | any | any | About 25 needed. |
| Self-adhesive cable tie mounts, 10 pieces (2 to 4 needed) | 1 | 2.00 | 2.00 | both | maybe-spare | any | any | One low in the mast or on the deck, one in the head (mechanical-design.md, 6.3). About price (ASSUMED). |
| Foam pads 3 mm and Kapton tape | 1 | 3.00 | 3.00 | both | maybe-spare | any | any | Screen retention. The Kapton tape is the backup for the USB 5 V contact (pin 1 of the USB-A plug). |
| **Group total** | | | | | | | | **cheap build 78.00 EUR, comfortable build 78.00 EUR** |

#### Group 8 Motherboard fit-out

| Item | Qty | EUR each | EUR total | Build | Owned? | Buy where | Trip | Note |
|---|---|---|---|---|---|---|---|---|
| Motherboard v5 bare PCB (5 pieces; order only after the paper test-fit passes, see pcb/kicad/README.md) | 1 | 0.00 | 0.00 | both | maybe-board | JLCPCB (confirm the order status) | DE | Bare board. You report 5 boards ordered: confirm they are version v5 (pcb/kicad/pin-table.md). If they are not v5, the pin numbers in these files do not apply. |
| ESP32-S3 DevKitC-1, N16R8, dual USB-C, headers soldered | 1 | 12.00 | 12.00 | both | maybe-board | Amazon.de, AZ-Delivery, AliExpress | DE | About price (ASSUMED). Check it has two USB-C sockets. |
| DRV8833 motor driver module HW-627 (driver A only) | 1 | 2.50 | 2.50 | both | maybe-board | Amazon.de, eBay.de | DE | Robot 2 uses M1 and M2 only, so driver B can stay empty. |
| DRV8833 HW-627 spare | 1 | 2.50 | 2.50 | comfort | no | Amazon.de, eBay.de | DE | Spare. |
| PCA9685 16-channel servo driver board | 1 | 6.00 | 6.00 | both | maybe-board | Amazon.de, AZ-Delivery | DE | Check that it has its own V+ screw terminal: a second AWG 18 feed from the servo buck goes there (peripherals.md, 5.5). |
| GY-521 gyro board (MPU-6050) | 1 | 3.50 | 3.50 | both | maybe-board | Amazon.de, AZ-Delivery | DE |  |
| Sockets, headers and 5.08 mm screw terminals for the board | 1 | 9.00 | 9.00 | both | maybe-board | Reichelt, AZ-Delivery | DE | Full list in pcb/kicad/parts-list.md. Robot 2 fits 3 of the 4 terminals (not 3.3V IN). |
| Capacitors 470 uF and 100 uF, 2 x 100 nF, 1N5819 diode, 4 resistors 1k/2k | 1 | 3.00 | 3.00 | both | maybe-board | Reichelt | any |  |
| **Group total** | | | | | | | | **cheap build 36.00 EUR, comfortable build 38.50 EUR** |

#### Group 9 Tools and consumables

| Item | Qty | EUR each | EUR total | Build | Owned? | Buy where | Trip | Note |
|---|---|---|---|---|---|---|---|---|
| Heat-shrink tubing assortment | 1 | 6.00 | 6.00 | both | maybe-spare | any | any |  |
| Solder 1 mm, 100 g | 1 | 7.00 | 7.00 | both | maybe-spare | any | any | Tool: you probably own an iron and a multimeter. |
| Digital caliper | 1 | 12.00 | 12.00 | comfort | no | Amazon.de | DE | To check servo, webcam and screen sizes before printing. Weight is a guess (A). |
| Precision screwdriver and hex key set | 1 | 10.00 | 10.00 | comfort | maybe-spare | any | any | Weight is a guess (A). |
| Wire stripper and flush cutter | 1 | 10.00 | 10.00 | comfort | maybe-spare | any | any | Weight is a guess (A). |
| USB-C power meter (voltage and current) | 1 | 10.00 | 10.00 | comfort | no | Amazon.de | DE | Handy for the power tests in stage 3, and needed for the fallback of bench test B (peripherals.md, 6.1). Get an in-line meter with a USB-C plug on one side and a USB-C socket on the other (or two sockets and a short USB-C to USB-C cable). It goes between the ordinary cable's USB-C end and the devkit's COM socket, not at the Pi (the Pi's port is USB-A, so it does not fit there). Comfortable build: in the list. Cheap build: not in the total. Do bench test B at home first; only if it fails, buy one (about 10 EUR) or borrow one before the trip. Weight is a guess (A). |
| Servo tester | 1 | 3.00 | 3.00 | opt | no | Amazon.de, eBay.de | any | Only for the pan-servo bench test in mechanical-design.md (assembly step 10: power the servo from a tester and check that the turntable turns freely). Optional, not in the totals. About price (ASSUMED). |
| Adjustable bench power supply, 0 to 15 V or more, at least 3 A (5 A is better), with a volt display and a current limit | 1 | 40.00 | 40.00 | opt | maybe-spare | borrow one, or Amazon.de | any | Needed for the tests before the trip: the Pi under load with the pack voltage at 6.4 V and at 6.0 V (wiring.md, step 4) and the low-battery test at 6.7 V and 6.3 V (software-plan.md, Stage 4, pass 9). Borrow one if you can. The price is a guess (ASSUMED): simple adjustable ones with 3 A cost about 25 to 35 EUR, 5 A ones about 40 to 60 EUR. In no total. |
| **Group total** | | | | | | | | **cheap build 13.00 EUR, comfortable build 55.00 EUR** |

#### Group 10 Travel and spares

| Item | Qty | EUR each | EUR total | Build | Owned? | Buy where | Trip | Note |
|---|---|---|---|---|---|---|---|---|
| Spare ESP32-S3 DevKitC-1 | 1 | 12.00 | 12.00 | comfort | no | Amazon.de, AZ-Delivery | DE |  |
| LAN cable 2 m (Wi-Fi plan D) | 1 | 3.00 | 3.00 | both | no | any | any | Stage 9 rehearses Wi-Fi plan D (software-plan.md). |
| Small USB keyboard (Wi-Fi plan E) | 1 | 10.00 | 10.00 | both | maybe-spare | any | any | Stage 9 tries Wi-Fi plan E once (software-plan.md). |
| Travel plug adapter | 1 | 8.00 | 8.00 | comfort | no | any | any | Country not known yet. |
| Spare USB cables (USB-A to USB-C, ordinary, with data and 5 V) | 2 | 4.00 | 8.00 | comfort | maybe-spare | any | any |  |
| Laminating pouches for the family card | 1 | 2.00 | 2.00 | both | no | any | any | For the family card (stage 9). |
| Hard box or organiser for the trip (about 30 x 25 x 20 cm) | 1 | 15.00 | 15.00 | comfort | no | any | any | Printed parts stack into this size. |
| **Group total** | | | | | | | | **cheap build 15.00 EUR, comfortable build 58.00 EUR** |


**Not on the list, because you probably own them:** soldering iron, multimeter, 3D printer, a computer with a microSD card reader, a phone, and a normal Raspberry Pi USB-C power supply (robot 1 has one) for the bench tests. **You also need an adjustable bench power supply** for the Pi test at 6.4 V and 6.0 V (stage 3) and the low-battery test at 6.7 V and 6.3 V (stage 4). It is the last line of group 9, marked optional so that it is in no total: borrow one if you can, or buy one. Robot 1's TB6612 driver, 20000 mAh power bank, relay board and SPI screens are not used in robot 2.

**What changed against the draft shopping lists.** The motherboard's `shopping-list.md` has a 3.3 V fixed buck and a sixth fuse holder; robot 2 has **no 3.3 V buck** (no SPI screens, no relays) and uses five fuse holders: BATT IN, servo buck, clean 5 V buck, SBC buck, screen. The cheap build with route B sound adds a sixth holder with its own 1 A fuse for the speaker amplifier (`peripherals.md` conflict C7). The DRV8833 driver B is not needed either: robot 2 uses motors M1 and M2 only.

**The splice.** The plus side has 6 wires (switch in, four fused branches, the divider resistor). The minus side has up to 7 wires (battery minus, BATT IN return, servo buck, clean buck, Pi buck, screen return, amplifier return). That is why the list has four 5-way Wago 221-415 connectors: two per side, each pair joined by a 10 cm jumper wire. The 2-way connectors of the first draft are dropped.

### The PCA9685 channels (servo board)

| Channel | Use |
|---|---|
| 0 | pan servo (turn left and right) |
| 1 | tilt servo (nod) |
| 2 | camera-live LED |
| 3 | call button light (optional) |
| 4 to 15 | free |

---

## 4. What must be bought twice

These are parts you own for robot 1 but robot 2 needs its own. If robot 1 can wait, you may take them and buy replacements later.

| Part | Qty | EUR total | Build |
|---|---|---|---|
| Raspberry Pi 5, 2 GB (recommended board) | 1 | 82.50 | comfort |
| Heatsink plus small 5 V fan for the Pi 4 | 1 | 6.00 | cheap |
| Webcam: your own SC-012-SN259, if it passes the test | 1 | 0.00 | cheap |
| HC-SR04 ultrasonic sensor, 5 V type (not the 3.3 V HC-SR04P) | 2 | 4.00 | both |
| 2S BMS (HX-2S-JH20 type), balancing | 1 | 3.00 | both |
| 2S USB-C charger board (IP2326 type, 5 V in, 8.4 V out) | 1 | 5.00 | both |
| Main switch, round rocker, 10 A or more, 19 mm hole | 1 | 2.50 | both |
| XL4016 buck module with heatsink (servo 5.0 V, and SBC 5.1 V) | 2 | 12.00 | both |
| Fixed 5 V buck, 1.8 A (clean 5 V) | 1 | 2.50 | both |
| MG996R servo, metal gear (pan and tilt) | 2 | 16.00 | both |

Total to buy twice: **51.00 EUR** in the cheap build, **127.50 EUR** in the comfortable build (included in the totals above).

Your own Raspberry Pi 5 8 GB is the free option for the Pi 5 line above: it is not bought, but robot 1 then has no brain during the trip. Your robot 1 fan and key switch are not used in robot 2: robot 2 has its own (the heatsink and fan line and the main switch line in the table). The ELEGOO chassis is not used (the mechanical design uses a new printed base).

---

## 5. Shopping split: before the trip, or anywhere

### Buy in Germany **before** the trip

Order the **Pololu motors first**: 2 to 3 weeks from the US (A), or ask an EU reseller (Eckstein, Botland). Then the screen (stock varies), the SBC, the ESP32 and small modules, the aluminium horns and heat-set inserts, and the right-angle USB adapters (dry-fit them before you print the base).

- **1 Brain and screen:** Raspberry Pi 4 Model B, 2 GB (the cheapest board that really works) x1 [cheap build only]; Raspberry Pi 5, 2 GB (recommended board) x1 [comfortable build only]; Raspberry Pi 5 Active Cooler (official) x1 [comfortable build only]; Heatsink plus small 5 V fan for the Pi 4 x1 [cheap build only]; 7 inch HDMI screen, 1024x600 IPS, touch: no-name type x1 [cheap build only]; Waveshare 7 inch HDMI LCD (C), 1024x600 IPS, 5-point touch (recommended screen) x1 [comfortable build only]; HDMI cable, micro-HDMI to HDMI-A, flat and slim, 0.8 m x1; USB-C plug breakout board with solder pads, for the SBC power pigtail (you solder your own AWG 18-20 silicone wire to ALL the VBUS and GND pads) x1; USB data-only adapter (power blocker, no 5 V wire), for the ESP32 link and for touch x2; USB-A right-angle adapter (90 degrees, male plug to female socket), for the webcam, the ESP32 link, the touch cable and the sound adapter or speakerphone x4; USB-A extension cable, about 1 m, male right-angle plug to female socket (for a webcam whose cable is fixed to the camera) x1
- **2 Camera and audio:** Webcam: your own SC-012-SN259, if it passes the test x1 [cheap build only; from robot 1, 0.00 EUR]; Wide-angle USB webcam, 1080p, UVC, with microphone (fallback or comfort) x1 [comfortable build only]; USB speakerphone with real echo cancelling (Jabra Speak 410 class) x1 [comfortable build only]
- **3 Sensing:** HC-SR04 ultrasonic sensor, 5 V type (not the 3.3 V HC-SR04P) x2; HC-SR04 spare x1 [comfortable build only]; IR floor sensor module, TCRT5000 type, digital output, 3.3-5 V (cliff) x2; IR floor sensor spares, to find a pair that reads your floor x2; ADS1115 16-bit analog-to-digital board (battery monitor) x1; ADS1115 spare x1 [comfortable build only]; Call / STOP button, arcade type 30 mm (optionally with a 3.3 V LED ring) x1
- **4 Power:** 18650 Li-ion cell, genuine Samsung 25R / LG MJ1 / Molicel P28A class x2; 18650 cells, 2 more (the 4-cell option, 2S2P: double runtime) x2 [comfortable build only]; 2S BMS (HX-2S-JH20 type), balancing x1; 2S USB-C charger board (IP2326 type, 5 V in, 8.4 V out) x1; In-line fuse holder for 5 x 20 mm fuses x5; In-line fuse holder for 5 x 20 mm fuses, 6th holder (route B: own 1 A fuse for the speaker amplifier) x1 [cheap build only]; Slow-blow fuses 5 x 20 mm, assortment (1 A, 2 A, 3 A, 5 A) x1; XL4016 buck module with heatsink (servo 5.0 V, and SBC 5.1 V) x2; Fixed 5 V buck, 1.8 A (clean 5 V) x1; Servo extension cable 50 cm, 3-wire x3
- **5 Drive:** Pololu 25D metal gearmotor 12 V, medium power, 47:1 (item 3229) x2; Robot wheels 65 mm, rubber tyre, hub for 4 mm D-shaft (pair) x1; Hub adapters 4 mm D-shaft for wheels (only if the wheel bore does not fit) x1 [comfortable build only]
- **6 Pan/tilt:** MG996R servo, metal gear (pan and tilt) x2; Aluminium servo horn 25T, 20 mm disc, 4 x M3 holes x2; MG996R spare x1 [comfortable build only]
- **7 Mechanical hardware:** Heat-set insert assortment M2-M5, brass x1; PTFE adhesive tape 0.2 mm (turntable glide ring) x1
- **8 Motherboard fit-out:** Motherboard v5 bare PCB (5 pieces; order only after the paper test-fit passes, see pcb/kicad/README.md) x1 [0.00 EUR here: you report 5 boards ordered, confirm they are v5]; ESP32-S3 DevKitC-1, N16R8, dual USB-C, headers soldered x1; DRV8833 motor driver module HW-627 (driver A only) x1; DRV8833 HW-627 spare x1 [comfortable build only]; PCA9685 16-channel servo driver board x1; GY-521 gyro board (MPU-6050) x1; Sockets, headers and 5.08 mm screw terminals for the board x1
- **9 Tools and consumables:** Digital caliper x1 [comfortable build only]; USB-C power meter (voltage and current) x1 [comfortable build only]
- **10 Travel and spares:** Spare ESP32-S3 DevKitC-1 x1 [comfortable build only]

### Easy to buy **anywhere** (any shop, no long delivery)

These are still needed for the build at home before the trip: buy them in time. Buy the **PETG filament first**, so that printing (about 44 hours) can start.

- **1 Brain and screen:** microSD card 32 GB, A1 or A2, SanDisk or Samsung (main card) x1; microSD card 32 GB (clone = spare card) x1; Screen power lead: micro-USB plug with bare wires, power only x1; Capacitor 1000 uF, 16 V, low-ESR (at the SBC power input) x1; USB-A to USB-C cable, short (20 cm), ordinary (has the 5 V wire), for the ESP32 COM socket x1; Touch cable, micro-USB to USB-A, thin, about 1 m, data (the screen box may already contain one: check that it reaches the SBC through the mast, about 0.65 m plus slack) x1
- **2 Camera and audio:** USB audio adapter (3.5 mm speaker out) x1 [cheap build only]; Speaker 40 mm, 4 ohm, 3 W x1 [cheap build only]; PAM8403 amplifier board, 5 V x1 [cheap build only]; Audio cable, 3.5 mm plug to bare wires (or a cut aux cable), for the amplifier input x1 [cheap build only]; LEDs 5 mm red, 5 pieces, plus 220 ohm resistors x1
- **3 Sensing:** Resistor and capacitor kit: 47k x2, 27k x2 (1 %), 10k x4, 100 nF x4 x1
- **4 Power:** Battery holder for 2 x 18650 x1; Battery holder, 2nd set for the 4-cell option (four single-cell holders in total, or two 2-cell holders whose middle point you can reach and join) x1 [comfortable build only]; USB-C wall charger 5 V, at least 2 A (for the charger board) x1; USB-A to USB-C charging cable, 1 m x1; Main switch, round rocker, 10 A or more, 19 mm hole x1; Lever connector Wago 221-415 (5-way) x4; Silicone wire 1.0 mm2 (AWG 18), red and black, 3 m each x1; Wire 0.5 mm2 and thinner, several colours x1; JST-XH plug kit 2/3/4-pin with crimped wires x1; Wire end ferrules, assortment x1 [comfortable build only]; Spade lugs (flat crimp terminals), 6.3 mm, small assortment, for the main switch x1; Single-cell 18650 charger (TP4056 type) x1 [comfortable build only]
- **5 Drive:** Steel ball 16 mm (or 5/8 inch) for the caster x1; Steel ball 16 mm, spare x1 [comfortable build only]
- **7 Mechanical hardware:** Screw and nut assortment M2.5/M3/M4/M5 hex socket, 6-30 mm x1; M5 x 30 bolt with lock nut and 2 washers x1; PETG filament 1 kg spool, 1.75 mm (printed parts weigh about 1.13 kg) x2; Super glue plus 2-part epoxy x1; Double-sided foam mounting tape x1; Zip ties 2.5 x 100 mm, 100 pieces x1; Self-adhesive cable tie mounts, 10 pieces (2 to 4 needed) x1; Foam pads 3 mm and Kapton tape x1
- **8 Motherboard fit-out:** Capacitors 470 uF and 100 uF, 2 x 100 nF, 1N5819 diode, 4 resistors 1k/2k x1
- **9 Tools and consumables:** Heat-shrink tubing assortment x1; Solder 1 mm, 100 g x1; Precision screwdriver and hex key set x1 [comfortable build only]; Wire stripper and flush cutter x1 [comfortable build only]
- **10 Travel and spares:** LAN cable 2 m (Wi-Fi plan D) x1; Small USB keyboard (Wi-Fi plan E) x1; Travel plug adapter x1 [comfortable build only]; Spare USB cables (USB-A to USB-C, ordinary, with data and 5 V) x2 [comfortable build only]; Laminating pouches for the family card x1; Hard box or organiser for the trip (about 30 x 25 x 20 cm) x1 [comfortable build only]

**Plug note:** the wall charger for the charger board must have the plug of the country you stay in. Buy it there if you do not know the plug yet.

---

## 6. Luggage rules (flights)

**Li-ion cells, battery packs and power banks go in carry-on only, never in checked luggage.** This is the airline rule for spare batteries (check your own airline's page; I did not look it up).

- Take the cells **out of the robot.** Carry them in a plastic cell case or a small box, each cell in its own pocket, ends covered with tape. Do not carry loose cells in a pocket with coins or keys.
- Your cells are about 9 to 13 Wh each (3.6 V x 2.5 to 3.5 Ah) (A). Four cells are about 36 to 50 Wh, under the usual 100 Wh limit for hand luggage (A).
- The finished 2S pack (BMS and cells) also goes in carry-on.
- **Checked luggage is fine for:** printed parts, motors, screen (padded), SBC, cables, screws, tools, the steel ball. Put sharp tools (hobby knife, side cutters) in checked luggage; check the airline's rule for a soldering iron.
- Pack the printed base pieces flat. They stack into about 30 x 25 x 20 cm (mechanical doc).
- Carry the **screen, SBC and microSD cards** in your hand luggage if you can: they are the parts that hurt most to lose.
- **After any transport in luggage,** measure all three buck outputs again with nothing connected, before you plug in the Pi or the ESP32. A knock can turn the adjust screw. The screws are locked with a drop of glue or nail varnish, but measure anyway.

---

## 7. Weight

| | Cheap build | Comfortable build |
|---|---|---|
| Printed parts (about 1.13 kg of PETG, from the mechanical print list) | 1.13 kg | 1.13 kg |
| Bought parts on the robot | 1.71 kg | 2.14 kg |
| **Finished robot, sum of this list** | **2.8 kg** (2838 g) | **3.3 kg** (3265 g) |
| Mechanical design estimate (CAD, `3d/tools/results/numbers.txt`, for comparison) | 2.61 kg | 3.03 kg |
| Carried extras (spares, tools, charger, box, keyboard) | 0.6 kg | 1.7 kg |
| **Everything you carry on the trip** (robot parts, if you take it apart, plus extras) | about 3.4 kg | about 4.9 kg |

Weight by group (robot parts only):

| Group | Cheap build | Comfortable build |
|---|---|---|
| 1 Brain and screen | 495 g | 487 g |
| 2 Camera and audio | 105 g | 422 g |
| 3 Sensing | 54 g | 54 g |
| 4 Power | 445 g | 543 g |
| 5 Drive | 259 g | 279 g |
| 6 Pan/tilt | 126 g | 126 g |
| 7 Mechanical hardware | 1270 g | 1270 g |
| 8 Motherboard fit-out | 81 g | 81 g |
| 9 Tools and consumables | 3 g | 3 g |
| **Total on the robot** | **2838 g** | **3265 g** |

**Why the list is heavier than the CAD.** The list is about 0.23 kg heavier than the CAD estimate in both builds (2838 g against 2610 g; 3265 g against 3030 g). The reasons (A): the list weighs every cable, adapter, screw pack, glue and tape in full (including about 70 g of USB adapters and cables), where the CAD allows 225 g for wiring, screws and cables; and single parts differ by a few grams. Use the CAD figure for the tip-over numbers, the list figure for the luggage and for the motor margin, and weigh the real robot.

The mechanical design sized the motors for **3.0 kg**. The cheap build is within it (2.61 kg by the CAD, 2.8 kg by this list). The comfortable build is over it: 3.03 kg by the CAD, about 3.3 kg by this list (about 270 g over). The speakerphone (about 350 g, a guess) and two extra cells add most of it. See `peripherals.md` conflict C4. The weights of small parts are my assumptions (A); weigh the real parts and tell me.

---

## 8. Conflicts between the specialists' files (short form)

The long table with recommendations is in `peripherals.md` section 8. The ones that change what you buy:

1. **Screen power:** from the SBC's 5.1 V buck with a 1 A fuse (not from the motherboard's POWER OUT). The list follows the draft wiring diagram. (C1)
2. **HDMI cable length:** 0.8 m (an earlier draft said 30 to 50 cm, which is too short; `sbc-selection.md` now says 0.8 m too). (C2)
3. **Runtime and charging:** two cells give about 1.1 to 1.4 hours of calling (about 1 hour or less if the robot also drives); the power list says "charge only with the robot off"; a robot that is off cannot be called. The comfortable build has four cells (about 2.2 to 2.8 hours) and an optional 8.4 V charger adapter (not in the totals) for the power specialist to judge. All ASSUMED, measured in Stage 3. (C3)
4. **Mass and battery cradle:** four cells need a bigger cradle in the base. (C4)
5. **Places the 3D design needed before the large parts are printed:** the speaker, a speakerphone, the camera LED, the call / STOP button, the camera cover and the third cable up the mast. The CAD now has all of them (`mechanical-design.md` 6.2 and 7.1); the sizes stay ASSUMED until you measure the real parts. (C5)
6. **No 3.3 V buck is needed**, and driver B is not needed. Route B sound adds a sixth fuse holder (the amplifier's own 1 A fuse). (C7)
7. **Motor voltage:** the Pololu motors are 12 V types; the software setting `mot_vmax` is 8.0, a speed cap and not the motor rating. A setting only. (C6)
8. **Pi 5 USB limit** with a webcam and speakerphone on a bare USB-C cable. (C12)
9. **A screen that is too heavy for the servos?** No. Checked in `peripherals.md` section 2.4.
10. **A buck that cannot feed the SBC?** Not for normal use (typical 1.5 to 2 A; worst case on paper 5.5 to 6 A, which is why a 6.3 A slow-blow is allowed on this branch if the 5 A fuse blows). Test with the pack at 6.4 V and at 6.0 V (a bench power supply, group 9). (C8)
11. **The USB link to the ESP32:** a data-only adapter in both builds, checked by two bench tests (`peripherals.md` 6.1). The ordinary cable in the list is the fallback. (C9)
12. **Splice:** four 5-way lever connectors, not three, and no 2-way ones. (`wiring.md`)
13. **The USB ports face the rear wall:** only 20 to 42 mm of room is left behind them, so the list buys right-angle USB-A adapters (four) and a right-angle extension cable for a webcam with a fixed cable. (`mechanical-design.md` 5.2 and 6.2)

---

## 9. Price evidence

All prices are web-search snapshots (shop pages mostly could not be opened). Where I saw a number, the source is named.

| Part | What I saw | Source |
|---|---|---|
| Raspberry Pi 4 2 GB / Pi 5 2 GB | 71.90 EUR / about 82.50 EUR on 1 Oct 2026 | `sbc-selection.md` (Notebookcheck). A Berrybase snapshot shows 68.90 EUR for the Pi 5 2 GB, probably before the 2026 rises. |
| Pi 5 Active Cooler | 5.90 EUR incl. VAT | Welectron (art. RP9-111480); 5.67 to 7.95 EUR elsewhere |
| Waveshare 7 inch (C) | 44.95 EUR without VAT (exp-tech.de), 48.47 EUR (melopero), 58 EUR (elecena.pl), 60.75 EUR (opencircuit.shop), 62.26 EUR (elty.pl) | shop listings |
| No-name 7 inch HDMI touch | 42.99 to 56.99 EUR | eBay.de listings |
| Jabra Speak 410 | 59.99 EUR (eBay, new, plus shipping), 84.99 EUR (June 2026, Latvian shop), 92 to 154 EUR elsewhere. Cheaper no-name "conference speakers" (17 to 31 EUR) are not trustworthy: they say nothing about echo cancelling. | shop listings |
| Pololu 25D MP 47:1 (3229) | US$29.95 each; stall current 1.8 A at 12 V (used for the driver margin) | pololu.com page (search summary only, re-check the page; no copy is in the repository). Check the stall current by measuring the winding resistance (`peripherals.md` section 8). |
| 18650 cells | 3.99 EUR (Nkon NL), 5.95 to 10.05 EUR (Kaufland sellers) | listings |
| XL4016 module | 3.25 to 4.50 EUR (eBay.de), 6.01 to 6.95 EUR (NL shops), 10.99 EUR (AZ-Delivery via elecena.pl) | listings |
| Wago 221 | 0.39 EUR (Berrybase, "from"), about 0.55 EUR (Hornbach, pack of 25) | listings (2-way and mixed packs); single 5-way pieces cost more, I budget 1.20 EUR (A) |
| MG996R | 4.50 to 7 EUR (eBay.de), 13.29 EUR (Waveshare) | listings |
| PETG 1 kg | 9.75 EUR per kg (4-pack deal, June 2026), 12.32 to 13.45 EUR single | mydealz, eBay.de |
| ADS1115 | 3.5 to 5 EUR (eBay.de), up to about 13 EUR (local shops) | `software-plan.md` listing check |
| Everything else | my estimate (A) | |

**Currency:** US dollar prices are converted at about 0.9 EUR per dollar (A).

**The Pololu motors cost most.** Pololu direct: US$29.95 each plus US shipping (about US$15 to 35, A), plus 19 percent import VAT and maybe a courier fee. The delivered price per motor may reach 40 to 45 EUR. An EU reseller (Eckstein sells Pololu parts) may be cheaper once shipping and VAT are counted. I could not confirm a stock or a price for item 3229 at an EU shop (Botland's listing I found was for the encoder version and was withdrawn). I budget 36 EUR each (A).

---

## 10. What is verified and what is assumed

**Verified (V):** prices named in section 9 (search summaries, re-check the shop page); screen size and power; motor model and Pololu price (search summary only, re-check the page); the motherboard's connectors and pins; the SBC's recommended boards and their prices.

**Assumed (A):** every small-part price not named in section 9; all weights except the printed parts (the CAD print list) and the MG996R (55 g, V); the Pololu import cost; the Pololu stall current of 1.8 A (check with a multimeter when the motors arrive); the wheel bore of 4 mm; the screen's HDMI socket; the SC-012-SN259 (no data found); the speakerphone weight; the number of 5 x 20 mm fuses and connectors needed; the price of the USB-C breakout board and the data-only adapters; whether the data-only adapter lets the devkit's USB chip appear on the Pi (bench tests in `peripherals.md` 6.1).

**Open questions that change this list:**

1. Can robot 1 spare the Pi 5 8 GB, the servos, BMS, charger and bucks for the trip? (changes the cash needed)
2. Does the SC-012-SN259 pass the camera test? (saves or costs 22 EUR)
3. Does the echo test pass with route B? (saves about 60 EUR, or not)
4. Which exact screen, and which HDMI socket does it have? (changes the cable)
5. 2 cells or 4 cells? (runtime, cradle, mass; the buy decision assumes about 1 hour of calling while driving, Stage 3 measures it)
6. Which country, and what plug? (charger, travel adapter)
7. Which 3D printer? (the design needs at least a 180 x 180 mm bed)
8. Are the 5 boards you ordered version v5? (if not, the pin numbers in these files do not apply; `pcb/kicad/pin-table.md`)
9. Does the devkit's USB chip appear on the Pi through the data-only adapter? (two bench tests, `peripherals.md` 6.1; the ordinary cable is the fallback)
