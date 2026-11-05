# Robot 2: which small computer (SBC) goes in the head

Written 5 November 2026 for the telepresence robot. This file only chooses the small computer. Screen, camera, wiring and software are in other files.

**Words used here.** SBC = single board computer, the small "brain" board (a Raspberry Pi is an SBC). CPU = the processor. RAM = working memory. WebRTC = the technology browsers use for video calls (Google Meet, Jitsi and most call web pages use it). Chromium = the free browser that comes with Raspberry Pi OS. Hardware video = a small special part of the chip that decodes or encodes video without using the CPU. OTG = a USB port that can act as a plug for a keyboard or hub. DP Alt Mode = a USB-C port that can also send a screen picture.

**How sure am I.** VERIFIED = I saw it in a web source (listed at the bottom). ASSUMED = my own knowledge or a sensible guess; check it. In the tables, (V) = verified, (A) = assumed.

---

## 1. The short answer

| | Board | About price (Germany) | Why |
|---|---|---|---|
| **Recommended** | **Raspberry Pi 5, 2 GB** (4 GB if you can afford it) | 2 GB about 82 EUR; 4 GB about 115 to 150 EUR (sources disagree, check live) | The CPU is strong enough to do the whole video call in software. Same family as robot 1, so the same OS and the same ESP32 serial code. Sold everywhere in the world. |
| **Free option** | The **Raspberry Pi 5 8 GB you already own** (it is robot 1's brain) | 0 EUR | If you can leave robot 1 unfinished while you travel, take its Pi. Buy a new one for robot 1 afterwards. |
| **1. Cheapest that really works** | **Raspberry Pi 4 Model B 2 GB** | about 72 EUR | Works for a simple 1-to-1 call. Runs hot and busy; needs a fan. About 10 EUR cheaper than a Pi 5 2 GB, but a lot slower. |
| **3. Avoid** | Pi Zero 2 W, Orange Pi Zero 2W / Zero 3 / Zero 3W, Radxa Zero 3W, Radxa Cubie A7Z / A7A / **A7S** | 15 to 85 EUR | Too weak, or too little proven software, or hard to buy in Germany right now. Details in section 6. |

The cheap boards you named (Orange Pi Zero 2W, Radxa Cubie A7S) look 2 to 3 times cheaper than a Pi. They are not a good deal for a trip: you cannot afford days of fiddling at your sister's house. The A7S has a second problem: it has **no HDMI port at all** (section 4).

**The one honest unknown.** I found **no test of a 720p Chromium video call on any of these boards**, only hints. Nobody has proven that a call is smooth on the Pi 4 or the Pi 5 either. The plan therefore includes a short test at home before you leave (section 10).

---

## 2. What the SBC must do (the checklist)

1. Show the video call on an **HDMI screen** (the person's face, full screen).
2. Run a **USB camera** and a **microphone** (the webcam has one, assumed) and play **sound** (screen speakers over HDMI, or a small USB speaker).
3. Join **Wi-Fi** at your sister's house. Dual-band (2.4 and 5 GHz) is a big plus in crowded flats.
4. Talk to the **ESP32 over USB** (drive and pan/tilt commands). The ESP32 sits on the motherboard.
5. Run on **5 V** from a buck converter on the 2S pack (6.0 to 8.4 V), without brown-outs when the motors start.
6. Be **as cheap as sensible** and easy to get in Germany before you leave.

**Ports we need:** HDMI out, 2 USB ports (camera and ESP32). A third USB port (speaker) is nice.

---

## 3. The big question: hardware video or not?

In a PC, the browser uses the graphics chip to decode video. On these small boards, **Chromium does not use the chip's video hardware for a WebRTC call**. So the CPU does all the work: it decodes the other person (about 720p), compresses your camera (about 720p), decodes the webcam's JPEG pictures, and draws the screen. The stronger the CPU, the smoother the call. This is the main reason the ranking below follows CPU speed and not the "4K video" claims on the boxes.

What I found, board family by board family:

| Chip | Video hardware on paper | Does a Chromium call use it today? |
|---|---|---|
| Pi 5 (BCM2712) | Hardware decode for H.265 only. **No H.264 hardware at all.** (V, community gist) | No. A user report shows Chromium on the Pi 5 decoding video in software. (V) |
| Pi 4 (BCM2711) | H.264 decode and encode blocks exist. Chromium on Raspberry Pi OS can use the decoder for video files. (V, 2021 guide) | **Probably not for calls.** A Chromium developer thread (2021; it does not clearly name the board) says a call's incoming H.264 stream still went through the software decoder while video files used the hardware. I found no 2026 proof either way. (V for 2021, otherwise unknown) |
| Pi Zero 2 W (BCM2710) | H.264 hardware encode/decode exists, used by special apps. | Not by Chromium calls. (A) |
| Allwinner H618 (Orange Pi Zero 2W, Zero 3) | Decoder exists on paper (H.265, VP9). | **No.** Armbian forum threads (2024, 2025) say video encode/decode does not work in Linux on this chip. (V) |
| Rockchip RK3566 (Radxa Zero 3W, Orange Pi 3B) | H.264/H.265 decode 4K60, encode 1080p60 per vendors. (V) | Not by standard Chromium. I found no source showing it works in a browser call. (unknown) |
| Allwinner A733 (Cubie A7Z, A7A, A7S, Orange Pi Zero 3W) | Vendor claims 8K H.265 decode. (V) | **No.** A Radxa forum post says Chromium on the A7A reports hardware decoding disabled. (V) |

**What this means for the software plan (for the other specialists):**
- Plan for **software VP8 or H.264 at 720p, 1-to-1, with the frame rate capped at about 24 to 30 fps**. A plain peer-to-peer call page is much lighter than Jitsi or Google Meet, which are built for many people.
- The webcam should be set to **720p, not 1080p** (a Balena forum user got lag with a 1080p webcam on a Pi). (V)
- The CPU should be set to its "performance" mode, because Raspberry Pi OS does not always do it by itself. (V, Balena forum)
- A special app (not Chromium) can use the Pi 4 or Zero 2 W hardware H.264 encoder. A project does that on a Zero 2 W (one-way, about 1 second delay). (V) That is a possible later upgrade, not a reason to pick a board.

---

## 4. Comparison tables

Prices are EUR, delivered to Germany, "about", from news articles and shop snapshots seen through web search. **I could not open the shop pages themselves** (my tool could not reach several sites), so check the live price at purchase.

### 4a. The boards

| Board | Chip, CPU | RAM options | About price (Germany) | Size (mm) |
|---|---|---|---|---|
| **Raspberry Pi 5** | Broadcom BCM2712, 4x Cortex-A76 at 2.4 GHz (A). Geekbench 6 single-core about 800 to 850 (V) | 1, 2, 4, 8, 16 GB | 2 GB about **82.50** (V, Notebookcheck, 1 Oct 2026). 4 GB: the sources disagree on the US list price (85 USD in one table, 110 USD in two others; 110 fits the April 2026 rise of 25 USD) (V); German shop snapshots 141 to 149 EUR (V, undated). Plan on **115 to 150 EUR** | 85 x 56 (A) |
| **Raspberry Pi 4 Model B** | BCM2711, 4x Cortex-A72 at 1.5 GHz (A). Roughly 2 to 3 times slower than a Pi 5 (A) | 1, 2, 3, 4, 8 GB | 2 GB about **71.90** (V, Notebookcheck, 1 Oct 2026). 3 GB: 83.75 USD at launch (V). 4 GB: 75 or 100 USD (sources disagree) (V), German snapshots 114 to 129 EUR (V) | 85 x 56 (A) |
| **Raspberry Pi Zero 2 W** | BCM2710, 4x Cortex-A53 at 1 GHz (A). Browser speed about one third of a Pi 4 (V, Hackster) | 512 MB only (A) | 15 USD official, unchanged in 2026 (V). A German guide says it has been **sold out almost everywhere for months** (V, Sept 2026). Old German deals 16 to 24 EUR (V, expired) | 65 x 30 |
| **Orange Pi Zero 2W** | Allwinner H618, 4x Cortex-A53 up to 1.5 GHz (V) | 1, 1.5, 2, 4 GB (V) | 2023 list price 12.9 to 23.9 USD (V). European shop neven7: 1 GB 29.10 EUR (V, out of stock). China bundles with shipping about 32 to 59 EUR (V). Budget **25 to 45 EUR** (A) | 65 x 30 (V) |
| **Orange Pi Zero 3** | Allwinner H618, same CPU (V) | 1, 2, 4 GB | 1 GB about 40 USD on Amazon US (V). German price not found (A: 30 to 50 EUR) | about 55 x 50 (A) |
| **Orange Pi Zero 3W** | Allwinner A733, 2x A76 + 6x A55 (V) | 1 to 16 GB | **65 to 86 USD** for 4 GB, small RAM sizes unavailable (V). Software support is the main complaint (V) | 65 x 32 (V) |
| **Radxa Zero 3W** | Rockchip RK3566, 4x Cortex-A55 at 1.6 GHz (V) | 1, 2, 4, 8 GB | neven7 (EU): 2 GB with 16 GB eMMC 54.40 EUR, 4 GB with 32 GB eMMC 75.20 EUR, **both out of stock** (V). Allnet.de (DE) lists it, not available (V). Ameridroid 61.95 USD, out of stock (V) | 65 x 30 (V) |
| **Radxa Cubie A7Z** | Allwinner A733, 2x Cortex-A76 + 6x A55 (V). Geekbench 6: 519 single, 1181 multi (V) | 1 to 16 GB | From 15 USD (1 GB) at launch (V). About 17 EUR for 1 GB on AliExpress, about 60 EUR for 8 GB (V). 2 and 4 GB prices not found. Ameridroid out of stock (V) | 65 x 30 (V) |
| **Radxa Cubie A7S** (the "Radexa QB A7S" you named) | Allwinner A733, same chip (V) | 4 to 16 GB (V) | About **31 EUR plus shipping** on AliExpress, 4 GB about 22 to 25 USD at Araca Tech (V). **No German shop found** (V). Ameridroid out of stock (V). Radxa promises supply to Dec 2030 (V) | 51 x 51 (V) |
| **Radxa Cubie A7A** | Allwinner A733, same chip (V) | 2 to 16 GB | Launch 28.70 USD (2 GB) and 39.90 USD (4 GB) per LinuxGizmos, or 35.74 USD for 2 GB per CNX (V). Current EU price not found | 85 x 56 (V) |
| **Orange Pi 3B** (extra) | Rockchip RK3566, 4x A55 up to 1.8 GHz (V) | 2, 4, 8 GB | 2 GB 47.20 EUR at an EU shop, 4 GB out of stock (V) | about 85 x 56 (A) |

### 4b. Screen, USB, Wi-Fi, power

| Board | HDMI connector | USB we can use | Wi-Fi / Bluetooth | Power input (5 V) |
|---|---|---|---|---|
| **Pi 5** | 2x **micro** HDMI (A) | 2x USB 3.0 + 2x USB 2.0 (A). Total only 600 mA unless the supply negotiates 5 A or you set a flag (section 7) (V) | Wi-Fi 5 dual-band, BT 5.0 (A) | USB-C, **5.1 V 5 A** official (V). Also 5 V GPIO pins (V) |
| **Pi 4** | 2x **micro** HDMI (A) | 2x USB 3.0 + 2x USB 2.0 (A) | Wi-Fi 5 dual-band, BT 5.0 (A) | USB-C, 5 V 3 A (A). Also 5 V GPIO pins (A). 3.5 mm audio jack (A) |
| **Pi Zero 2 W** | 1x **mini** HDMI (A) | **One** micro-USB data port (OTG), so a hub is needed (A) | Wi-Fi **2.4 GHz only**, BT 4.2 (A) | micro-USB, 5 V 2.5 A advised (A) |
| **Orange Pi Zero 2W** | **mini** HDMI (most sources; a few shops say micro, check the board) (V) | 2x USB-C (power + OTG). 2 more USB 2.0 only via the extra "expansion board" on a flat cable (V) | Wi-Fi 5, BT 5.0 (V) | USB-C, about 5 V 2 A (A) |
| **Orange Pi Zero 3** | **micro** HDMI (V) | 1x USB-A 2.0 + 1 USB-C OTG, 2 more via expansion board (V) | Wi-Fi 5, BT 5.0 (V) | USB-C, 5 V 3 A (V) |
| **Radxa Zero 3W** | **micro** HDMI (V) | 1x USB 3.0 USB-C "host" limited to **500 mA** + 1x USB 2.0 USB-C that is also the power port (V) | Wi-Fi 6; Bluetooth 5.0 or 5.4 (sources disagree) (V) | USB-C OTG port, 5 V 2 A, or GPIO pins 2 and 4 (V) |
| **Cubie A7Z** | **micro** HDMI (V) | USB-C only (one has DP Alt Mode) (V) | Wi-Fi 6, BT 5.4 (V) | USB-C 5 V 2 A (V, one listing) |
| **Cubie A7S** | **NONE.** Picture comes out of a **USB-C port with DP Alt Mode** (V). You need a USB-C to HDMI cable that is built for DisplayPort (about 10 to 15 EUR, A) | 1x USB-A 2.0 host, 1x USB-C 3.2 (video port), 1x USB-C 2.0 (power) (V) | Wi-Fi 6, BT 5.4, socket for an external antenna (V) | USB-C: 5 V **1 A** per Radxa's brief, 3 A or more per CNX (V, sources disagree) |
| **Cubie A7A** | 1x **full-size** HDMI (A: Radxa's page is named "HDMI Interface", the A7Z's is "Micro HDMI") | 1x USB 3 + 3x USB 2.0 type A + 1 USB-C (V) | Wi-Fi 6, BT 5.4 (A) | USB-C 5 V 3 to 4 A (V, sources disagree) |
| **Orange Pi 3B** | **full-size** HDMI (V) | 1x USB 3.0 + 3x USB 2.0 (V) | Wi-Fi 5, BT 5.0 (V) | 5 V USB-C or barrel (A) |

### 4c. Power draw, heat, operating system

"Idle" = desktop doing nothing. "Call" = my estimate for a 720p call with USB camera and the SBC only (no screen backlight, no servos). **I found no measured call figures for any board.** The estimates are ASSUMED and are for sizing the buck and the fuse, not for battery-life promises.

| Board | Idle (measured) | Heavy load (measured) | 720p call (estimate, 5 V) | Heat | OS you can use |
|---|---|---|---|---|---|
| **Pi 5** | 2.7 to 3.6 W (about 0.6 to 0.7 A) (V) | 7 to 8.8 W (1.4 to 1.8 A) (V) | 5 to 7 W, **1.0 to 1.5 A** (A) | Hot. Needs the Active Cooler or a heatsink with fan | Raspberry Pi OS 64-bit (Debian-based), Chromium included (V) |
| **Pi 4** | 2.7 to 2.9 W (about 0.55 A) (V) | 6.2 to 6.4 W (1.3 A) (V) | 5 to 6 W, **1.0 to 1.3 A** (A). Peaks to 3 A with USB devices | Warm to hot; throttles near 80 degrees C without a fan (A) | Raspberry Pi OS 64-bit, Chromium included (V) |
| **Zero 2 W** | 0.4 to 1.3 W (V) | 1.2 to 3.4 W (V) | 2 to 3 W (A) | Warm | Raspberry Pi OS (V) |
| **Orange Pi Zero 2W / Zero 3** | not found | not found | 3 to 5 W (A) | Warm | Orange Pi's own Debian/Ubuntu images; Armbian is community-made and a reviewer's Armbian Trixie image did **not** work with the expansion board (V) |
| **Radxa Zero 3W** | not found | not found | 3 to 5 W (A) | Warm | Radxa OS (Debian-based) (A) |
| **Cubie A7Z** | 2.9 W (V) | 5.4 W (V) | 3 to 5 W (A) | Throttles hard, see below | Radxa OS **Debian 11**, old kernel (V) |
| **Cubie A7S** | not found | not found | 3 to 6 W (A) | See below | Radxa OS Debian, Android 13 (V) |
| **Cubie A7A** | 3.9 W (V) | 9 W (V) | 4 to 7 W (A) | See below | Radxa OS Debian 11 (V) |

**Cubie heat warning (V):** A Radxa forum thread says a recent Radxa software update makes the A733 boards drop to about **400 MHz once the chip reaches 60 degrees C**. Radxa staff answered that this is unavoidable. A user also reports the A7S staying stuck at 416 MHz after cooling down (GitHub issue). A call keeps the CPU busy, so a Cubie would likely crawl in the middle of a call. A forum user says changing the thermal policy turns this off, but I did not verify that.

---

## 5. Short verdict on each board you named

- **Raspberry Pi.** Pick the right model: Pi 5 or Pi 4. Not the Zero. (Section 6.)
- **Orange Pi Zero 2W.** It exists, and it is cheap. But it has the same weak kind of CPU as the Pi Zero 2 W, Linux video hardware does not work on this chip (V), it has no normal USB-A ports on the board, and the HDMI is the small "mini" type. I would not rely on it for a call at 720p. It might do 480p. I found no test either way.
- **Radxa Cubie A7S** ("Radexa QB A7S"). It exists (launched February 2026) and it is the best-looking cheap board on paper: a very fast CPU (two big A76 cores), Wi-Fi 6, 31 EUR. But (1) **no HDMI port**, only USB-C DisplayPort, and I found no report that anybody tested a USB-C to HDMI cable on it; (2) the Cubie family runs an **old Debian 11 image** and has reports of **no HDMI picture on the A7A under Linux** (V), **Chromium without hardware decode** (V) and the **60 degree throttling** (V); (3) **no German shop** (AliExpress delivery takes weeks, risky before a trip). I would not take an experiment to your sister's house.

---

## 6. The three picks

### Pick 1: the cheapest that really works well enough: Raspberry Pi 4 Model B, 2 GB (about 72 EUR)

- **Why.** Every part of the job is proven on it: HDMI, camera, ESP32 over USB, Wi-Fi, Chromium, Raspberry Pi OS. Millions of people use it, so any problem has an answer on the internet. 4 USB ports, no adapters. It takes a plain 5 V supply on a bare USB-C cable end without any trouble (A).
- **Limit.** It is at the edge. Reports say a 720p call in Chromium can push it to almost full CPU, and it gets hot. It needs a fan, the performance CPU mode, and a simple 1-to-1 call page. 2 GB of RAM is enough for one Chromium call but not roomy (A). The 3 GB model costs more (83.75 USD at launch); the 4 GB much more.
- **Cheaper still?** A used Pi 4 on eBay or Kleinanzeigen may be 40 to 60 EUR (A, **not checked**). Only buy used if you can test it before you leave.

### Pick 2: the comfortable one: Raspberry Pi 5 (2 GB; 4 GB if you can afford it), or the Pi 5 you already own

- **Why.** The CPU is about 2 to 3 times faster than a Pi 4 (A), so a software call has room to spare. A call should not make it throttle if it has a cooler. Same OS and the same ESP32 serial code as robot 1.
- **Cost.** 2 GB about 82.50 EUR, only about 10 EUR more than a Pi 4 2 GB. The 4 GB costs about 115 to 150 EUR in German shop snapshots, 35 to 65 EUR more for memory a single Chromium call should not need (A). Buy 2 GB unless the 4 GB is under about 100 EUR on the day. During the home test (section 10) watch the memory: if the call plus the system stays under about 1.5 GB, 2 GB is enough.
- **Costs of power.** 1.0 to 1.5 A in a call (A) and up to 5 A peak. The fuse and the wire must be sized for 5 A (the shopping list already plans this). A bare USB-C cable end makes it limit USB power to 600 mA unless you set one flag (section 7).
- **Free version.** Take the **Pi 5 8 GB from robot 1**. It saves 80 to 150 EUR. The price is that robot 1 has no brain during your trip.

### Pick 3: avoid, and why

| Board | Why not |
|---|---|
| **Raspberry Pi Zero 2 W** | 512 MB RAM and a 1 GHz CPU: Chromium gets only about a third of Pi 4 speed (V). One USB port. Wi-Fi 2.4 GHz only. **Sold out almost everywhere** (V). |
| **Orange Pi Zero 2W, Zero 3** | The H618 chip is the same class as the Zero 2 W. No working video hardware in Linux (V). USB only through an extra board. Orange Pi's own images are the only ones that work well (V). |
| **Orange Pi Zero 3W** | Costs 65 to 86 USD for 4 GB, so the "cheap" argument is gone. Software support described as "not there" (V). |
| **Radxa Zero 3W** | 55 to 75 EUR **and** out of stock at every shop I found (V). Only 500 mA on the USB host port (V). Chromium cannot use its video hardware. |
| **Radxa Cubie A7Z / A7A / A7S** | Fast CPU, but old software image, throttling at 60 degrees C, reports of no HDMI picture (A7A) and no hardware decode, hard to buy in Germany. The A7S needs a special USB-C video cable and has one weak USB-A port. Look at them again in 2027. |
| **Raspberry Pi 3 B+ / 3 A+** | Old, same class as the Zero. A 720p call was reported to lag on a Pi 3 (V). Not worth buying new. |
| **Raspberry Pi 4 1 GB** | Too little RAM for Chromium plus a call (A). |

---

## 7. What each pick needs besides the board

| Item | Pi 4 2 GB | Pi 5 (own or new) |
|---|---|---|
| **HDMI cable** | **micro-HDMI** to the screen's connector. Which end the screen needs is decided in the screen file. Use the HDMI0 port, the one closest to the USB-C power port (A). Cable must bend through the neck: pick a **thin, flexible, 30 to 50 cm** cable. About 6 to 10 EUR (A). | The same: 2x micro-HDMI, use HDMI0 (A). |
| **Storage** | microSD 32 GB, A1 or A2 rating, a known brand (SanDisk, Samsung). About 8 to 12 EUR (A). Buy **two** and clone the first as a spare. | The same. A 64 GB card is fine. |
| **Cooling** | Heatsink plus a small 5 V fan. You own a 5 V fan. Without it the Pi 4 may throttle in a long call (A). | **Official Active Cooler** for the Pi 5, about 5 to 6 EUR (A, check). It plugs into the fan connector on the board. |
| **Power cable** | USB-C plug with bare wires (a "pigtail"), or a cut USB-C cable. About 3 to 8 EUR (A). | Same, plus the config flag below. |
| **USB** | Webcam on a blue USB 3.0 port, ESP32 on a USB 2.0 port. No hub. | Same. |
| **Audio out** | 3.5 mm jack on the board, or HDMI sound to the screen, or a small USB speaker (A). | **No 3.5 mm jack on a Pi 5.** HDMI sound or a USB speaker (A). |

### How to power the SBC safely from the 5.1 V buck (applies to all Raspberry Pi picks)

This follows the power design in the motherboard documents: a second XL4016 buck set to 5.1 V, its own fuse, straight to the SBC. It does **not** go through the motherboard.

1. **Use the USB-C plug end, not the 5 V header pins.** The USB-C input goes through the board's own protection parts. The header pins skip them (the project's shopping list says the same). Use the header pins only if the USB-C route fails.
2. **Pi 4:** a bare USB-C cable end works. The board does not need a power negotiation (A).
3. **Pi 5:** a bare cable end boots, but the Pi 5 expects a 5 A supply that "talks" to it. Without that it limits all USB ports together to **600 mA** and shows a warning (V). Your webcam and the ESP32 together may use more. The fix is the line `usb_max_current_enable=1` in the file `/boot/firmware/config.txt`. It tells the Pi to allow more USB power anyway. A third-party guide gives this setting (V); **check it in the official Raspberry Pi docs before relying on it**. Only turn it on if the buck and the wire really can give 5 A.
4. **Wire.** Short (under 40 cm) and thick: 1.0 mm² (AWG 18) for the Pi 5; 0.75 mm² (AWG 20) is enough for the Pi 4. Thin USB cable wires (AWG 24) lose about 0.17 V at 2 A over 1 m round trip (A, my calculation). Set the buck to **5.1 V measured at the Pi end with the Pi busy**, not on the bench.
5. **Fuse.** 3 A for the Pi 4. 5 A for the Pi 5 (as in the shopping list). Slow-blow type.
6. **Capacitor.** Put a 470 to 1000 uF, 10 V or higher, capacitor across the 5 V and ground at the Pi end (A). It helps when the motors pull the battery down.
7. **XL4016 warning.** This module needs about 1 to 1.5 V more input than output at higher currents (A). With the 2S pack near empty (6.0 V) a 5.1 V output may sag. Test it at 6.0 V in, with the Pi busy, before the trip. The simple fix is to set the battery cutoff a little higher (about 6.4 V, 3.2 V per cell).
8. **Ground.** Join the SBC ground to the robot's star ground like the other parts. One wire is enough.

### The ESP32 USB cable: a power question for the wiring file

The ESP32 devkit gets 5 V from the motherboard (clean 5 V, through diode D1). If you also plug it into the SBC's USB port, there are **two 5 V sources** on the same pin through a USB cable. The diodes make this probably harmless, but it also joins the two grounds and lets USB current flow back and forth (A). Safest: use a **data-only USB cable or adapter** (no 5 V wire), about 5 EUR (A), so the ESP32 is powered only by the motherboard. The wiring specialist should confirm.

Also, some Allwinner/Radxa kernels may lack the USB-serial driver for the chip on the ESP32's "COM" port (CP2102 or CH340). The Pi's kernel has them (A). If a non-Pi board is ever used, test `ls /dev/ttyUSB*` (it lists connected USB serial adapters) before anything else.

---

## 8. Expected call quality (my estimates, ASSUMED)

| Pick | You see (their face) | They see (your robot's camera) | Notes |
|---|---|---|---|
| **Pi 5** | 720p, 24 to 30 fps, smooth | 720p, 24 to 30 fps | CPU about half used. Keeps up in a 30-minute call if cooled. |
| **Pi 4 2 GB** | 720p at 24 to 30 fps if you use a simple page | 480p to 720p; the browser lowers the quality by itself when the CPU is full | Fan and performance mode are a must. A busy CPU can also make the video lag after 10 to 20 minutes in a warm room. |
| **Cubie / Orange Pi / Radxa Zero** | 480p at best; stutter likely | 360p to 480p | Not tested by anybody I could find. |
| **Pi Zero 2 W** | Not usable in Chromium | | |

Wi-Fi quality matters as much as the board: put the SBC's antenna away from the metal chassis and the battery. 5 GHz is better where the sister's neighbours crowd 2.4 GHz.

---

## 9. Setup notes that differ between boards

| Board | What is different |
|---|---|
| **Pi 4 and Pi 5** | Write the card with **Raspberry Pi Imager** (free program from raspberrypi.com). In it, choose "Raspberry Pi OS (64-bit)", and use the settings button to fill in a user name, password, Wi-Fi name and password, and "enable SSH". This is the easiest start of all the boards. For a robot with no keyboard the OS can start Chromium in full-screen "kiosk" mode (software file, not here). Pi 5 only: add `usb_max_current_enable=1` (section 7), and plug in the Active Cooler. The remote screen from Germany can be reached with the official Raspberry Pi Connect or with Tailscale (A, both free for personal use). Pre-load a **phone hotspot** as a second Wi-Fi so you can always get online. |
| **Orange Pi Zero 2W / Zero 3** | Use the images from orangepi.com, not Armbian, if you ever try one (V). The mini or micro HDMI cable is a different type from the Pi's. Power and the USB data port are both USB-C: do not swap them. Camera and ESP32 need the expansion board or an OTG adapter plus a hub. |
| **Radxa Zero 3W** | Radxa OS image. Power goes into the USB 2.0 OTG USB-C port only (V). The USB 3.0 host port gives only 500 mA (V), so the camera must be on a **powered** hub or it will fail. |
| **Cubie A7S** | The picture comes from the USB 3.2 USB-C port (the one marked DisplayPort); the power goes into the other USB-C port (V). It needs a DP-capable USB-C to HDMI cable, in the right direction (source to HDMI). An HDMI to USB-C adapter is the wrong way and does not work (V). Camera and ESP32 share one USB-A port, so a small hub is needed. Check CPU temperature in the first hour. |

---

## 10. A test at home before the trip (about 1 hour)

Do this with the parts you will actually take: board, microSD, cooler, camera, screen, the buck on the real battery.

1. Boot, join your Wi-Fi, open a free test call (for example a 1-to-1 meeting on Jitsi) with your phone as the other person. Set the camera to 720p.
2. Run the call for **30 minutes**. Look at: CPU use (the system monitor), whether the picture stutters, whether the fan is needed.
3. In a terminal, type `vcgencmd measure_temp`. It prints the board's temperature. Under 80 degrees C is fine. Then type `vcgencmd get_throttled`. It prints a code. `0x0` means no power or heat trouble so far. Any other value means the board has been short of power or too hot (Raspberry Pi boards only).
4. In Chromium, open `chrome://webrtc-internals`. It shows which video encoder and decoder the call really uses ("software" or "hardware"). This also answers the open question in section 3.
5. Drive the motors (wheels lifted) while the call runs. If the board reboots or the picture freezes, the 5.1 V branch is too weak.
6. Note the result in the project log. If the Pi 4 fails, you know you need the Pi 5 before you leave.

---

## 11. Final recommendation and what to buy before the trip

**Take a Raspberry Pi 5.** Your own Pi 5 8 GB is the best choice if robot 1 can wait. Otherwise buy a new Pi 5 with 2 GB (about 82.50 EUR), or 4 GB only if it is under about 100 EUR on the day. Run the one-hour test first. If the test shows the Pi 4 is smooth enough, a Pi 4 2 GB at about 72 EUR is an acceptable cheaper second choice.

Do not buy the Orange Pi Zero 2W or the Cubie A7S for this trip. Their lower price is not worth the risk and the lost time. If you are curious about the A7S, buy one *after* the trip as a bench experiment.

### Buy in Germany (stock and price are sure)

| Item | Shop | About price | Note |
|---|---|---|---|
| Raspberry Pi 5, 2 GB (or 4 GB) | Berrybase, Reichelt, Welectron | 2 GB about 82.50 EUR; 4 GB about 115 to 150 EUR (check live) | Skip if you take your own. A Pi is easy to find abroad, but prices and stock vary. |
| Active Cooler for Pi 5 | same shop | about 5 to 6 EUR (A) | |
| 2 microSD cards 32 or 64 GB, A2 | any | about 20 to 25 EUR for both (A) | Flash one, clone to the second |
| micro-HDMI to HDMI cable, thin, 30 to 50 cm | any | 6 to 10 EUR (A) | Adjust to the screen's connector |
| USB-C pigtail or USB-C cable to cut | any | 3 to 8 EUR (A) | |
| Data-only USB adapter ("power blocker") or cable | any | about 5 EUR (A) | For the ESP32 link |
| Small USB 2.0 hub | any | 6 to 10 EUR (A) | Only if a third device is added |
| Small USB keyboard, or phone hotspot plan | any | about 10 EUR (A) | For first Wi-Fi setup at your sister's |

### Easy to buy anywhere (can wait)

microSD card, HDMI cable, USB cables, USB speaker, hub, keyboard.

### Already owned / in the existing lists

Second XL4016 buck (set to 5.1 V), a 3 A or 5 A fuse and holder, thick wire, a 5 V fan, the USB webcam, the 2S pack and charger.

### Luggage rule

The 2S pack, old 18650 cells and any power bank go in **carry-on luggage only**, never in checked luggage. The SBC, cables and cards are fine anywhere.

---

## 12. Open questions and risks

1. **No tested 720p call result** for any board. The home test (section 10) decides it.
2. **Prices are from news articles and snapshots**, not from the shop pages. The Pi 4 4 GB and Pi 5 4 GB list prices are reported differently by different sources (75 or 100 USD, and 85 or 110 USD), so look at the live shop price.
3. **Is the Pi 5 8 GB free for the trip?** Your decision about robot 1.
4. **Screen connector type** decides the micro-HDMI cable end. Screen file must say.
5. **Sound** (speaker) is not decided yet; the Pi 5 has no headphone jack.
6. **ESP32 power over USB** (section 7): data-only cable or not. The wiring file decides.
7. **The Pi 5 flag** `usb_max_current_enable=1` is from a third-party guide. Check the official docs.
8. **XL4016 at 6.0 V input** may not hold 5.1 V under load. Test it.
9. **Raspberry Pi stock and prices keep changing** because of the memory shortage (four rounds of price rises in 2026). Buy early.
10. **Trip details** (date, country, the sister's Wi-Fi type, hotel or home power plug) are unknown.

---

## Sources (all seen through web search; page text for several was not reachable)

- Cubie A7S: CNX Software, 5 Feb 2026, https://www.cnx-software.com/2026/02/05/cubie-a7s-a-compact-allwinner-a733-sbc-with-usb-c-displayport-gbe-wifi-6-pcie-gen3-ffc-connector-gpio-headers ; Radxa product brief https://dl.radxa.com/cubie/a7s/docs/radxa_cubie_a7s_product_brief.pdf ; Notebookcheck (German price, AliExpress 31 EUR) https://www.notebookcheck.com/Mit-PCIe-Guenstige-Raspberry-Pi-Alternative-startet-mit-mehrmals-USB-Typ-C.1221811.0.html ; Ameridroid https://ameridroid.com/products/radxa-cubie-a7s
- Cubie A7A / A7Z: https://www.cnx-software.com/2025/08/19/radxa-cubie-a7a-powerful-allwinner-a733-sbc-cortex-a76-a55-ai-soc-16gb-ram/ ; https://linuxgizmos.com/cubie-a7a-with-allwinner-a733-lpddr5-ram-launches-starting-at-28-70/ ; https://liliputing.com/radxa-cubie-a7z-is-a-raspberry-pi-zero-sized-allwinner-a33-octa-core-pc-for-15-and-up/ ; https://www.linuxlinks.com/radxa-cubie-a7z-single-board-computer-running-linux-introduction/ ; power: https://www.linuxlinks.com/radxa-cubie-a7z-single-board-computer-running-linux-power-consumption/ and https://www.linuxlinks.com/radxa-cubie-a7a-single-board-computer-running-linux-power-consumption/
- Cubie trouble reports: throttling https://forum.radxa.com/t/extreme-throttling-introduced-on-a733/30688 ; no HDMI on A7A https://forum.radxa.com/t/a7a-no-hdmi-output-in-linux/29039 ; Chromium hardware decode off on A7A https://forum.radxa.com/t/hardware-decoding-for-video-not-enabled-on-a7a/29836
- Raspberry Pi prices: Notebookcheck DE, 1 Oct 2026 (Pi 4 2 GB 71.90 EUR, Pi 5 2 GB about 82.50 EUR) https://www.notebookcheck.com/Raspberry-Pi-Pi-4-und-Pi-5-mit-2-GB-RAM-werden-teurer.1413592.0.html ; OMG Ubuntu https://www.omgubuntu.co.uk/2026/10/raspberry-pi-2gb-costs-how-much-now ; Tom's Hardware price table https://www.tomshardware.com/raspberry-pi/component-shortages-drive-raspberry-pi-prices-up-by-up-to-23-percent-escalating-lpddr4-lpddr5-costs-trigger-the-third-price-hike-of-the-year ; Phoronix https://www.phoronix.com/news/Raspberry-Pi-5-2GB-Price-77.50 ; Pi 4 3 GB https://www.cnx-software.com/2026/04/01/raspberry-pi-4-3gb-launched-for-83-75-further-price-increases-announced-across-the-board-for-4gb-ram-hardware/ ; German shop snapshots (Pi 4 4 GB, Pi 5 4 GB) https://raspberry.tips/raspberrypi-einsteiger/raspberry-pi-5-vs-pi-4-vergleich
- Pi power use: https://raspberry.tips/en/?p=9083 ; Pi 5 USB limit and 5 V pins: https://www.yahboom.net/public/upload/upload-html/1703664332/3.%20Powering%20the%20Raspberry%20PI%205.html and https://structables.lunar.icu/Raspberry-Pi-5-Power-USB-Current-Management ; https://groups.google.com/g/hermes-lite/c/9hhEYJg3UoU
- Pi Zero 2 W: Hackster review https://www.hackster.io/news/raspberry-pi-zero-2-w-review-hands-on-with-the-fastest-zero-ever-b85b155905a5 ; availability guide https://raspberry.tips/faq/raspberry-pi-zero-oft-gestellte-fragen ; one-way WebRTC project https://www.hackster.io/news/tzu-huan-tai-s-webrtc-camera-stack-turns-a-raspberry-pi-zero-2-w-into-a-low-latency-streamer-30a49006f181
- Orange Pi: Zero 2W https://www.cnx-software.com/2023/09/09/orange-pi-zero-2w-raspberry-pi-zero-2w-alternative-4gb-ram/ ; https://linux-sunxi.org/Xunlong_Orange_Pi_Zero2W ; price https://www.neven7.eu/p/orange-pi-2w ; Zero 3 https://www.cnx-software.com/2023/07/03/orange-pi-zero-3-allwinner-h618-sbc-ships-with-up-to-4gb-ram/ ; Zero 3W https://www.cnx-software.com/2026/04/15/orange-pi-zero-3w-an-allwinner-a733-sbc-in-raspberry-pi-zero-form-factor/ ; Orange Pi 3B https://www.cnx-software.com/2023/08/05/orange-pi-3b-a-rockchip-rk3566-sbc-with-an-m-2-nvme-sata-ssd-socket-up-to-8gb-ram/ and https://www.neven7.eu/p/orange-pi-3b
- H618 video not working in Linux: https://forum.armbian.com/topic/37759-state-of-the-things-related-to-video-decoding-and-encoding-in-opi-zero-23/ ; https://forum.armbian.com/topic/50617-x264-hw-encoding-on-orange-pi-zero-2w/
- Radxa Zero 3W: product brief https://dl2.radxa.com/zero3/docs/hw/3w/radxa_zero_3w_product_brief.pdf ; https://www.neven7.eu/p/radxa-zero-3w ; https://shop.allnet.de/detail/index/sArticle/359780
- Chromium and video calls: Pi 4 Chromium hardware accel (video files) https://linuxuprising.com/2021/04/how-to-enable-hardware-acceleration-in.html ; WebRTC H.264 hardware decode thread https://groups.google.com/a/chromium.org/g/chromium-dev/c/D9LsobXOfN8 ; Pi 5 H.264 hardware missing, Chromium software only https://gist.github.com/schickling/089f4faf412b5267508f758408f0645f ; Pi video call box on Balena https://forums.balena.io/t/turn-a-raspberry-pi-a-webcam-and-a-tv-into-a-video-call-device/209644
- Geekbench Browser entries (scores differ from run to run, so treat them as rough): Pi 5 (796 to 846 single-core in the entries I saw) https://browser.geekbench.com/v6/cpu/baseline/12933706 ; Cubie A7Z (519 single, 1181 multi) https://browser.geekbench.com/v6/cpu/baseline/15776780
- Not reachable by my tool (so only search summaries were used): cnx-software.com article text, docs.radxa.com, omgubuntu.co.uk page text, and all shop pages. If you need those pages fetched, they have to be allowed in the session's network settings.
