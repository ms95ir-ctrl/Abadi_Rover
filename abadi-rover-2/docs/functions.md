# Abadi Rover 2: what the robot can do (function list)

This is the list you asked for, in plain words. "Must" = needed for the first version you take on the trip. "Should" = planned, can finish later. "Nice" = only if time is left.
Details: software in `software-plan.md`, the USB language in `esp32-serial-protocol.md`, the body in `mechanical-design.md`, parts in `parts-list.md`.

## A. For you, in Germany

| # | Function | How it works, short | Priority |
|---|---|---|---|
| 1 | **Video call both ways** | You open a link on your phone or laptop. You see the room through the robot's camera and your sister sees you on the robot's 7 inch screen. | Must |
| 2 | **Drive the robot** | Joystick on the page (or keys, or the gamepad you own): forward, back, turn. | Must |
| 3 | **Move the head** | Pan (look left and right) and tilt (nod up and down) with the two servos. | Must |
| 4 | **Call the robot** | Your call rings on the robot; the family answers or lets you in (their choice). | Must |
| 5 | **Emergency stop** | A big button on your page. Also a button on the robot's screen and the main switch on the body. | Must |
| 6 | **Battery and health on your page** | Battery voltage and percent, Wi-Fi quality, delay of the link, warnings. | Should |
| 7 | **Speed modes** | Creep, Normal, Fast. The speed limit drops by itself when the link is slow. | Should |
| 8 | **Remote updates and recovery** | You can log in from Germany to fix the software. A second, independent path exists in case the first fails. | Must |

## B. For your sister and the family

| # | Function | How it works, short | Priority |
|---|---|---|---|
| 9 | **One big CALL button** | Pressing it rings your phone. | Must |
| 10 | **Answer and hang up** | Big buttons; hanging up also switches driving off. | Must |
| 11 | **Privacy** | Camera and microphone are on only during a call. A light shows when the camera is live. There is a camera-off mode, a do-not-disturb mode and no recording. | Must |
| 12 | **Family STOP** | Version 1: hanging up the call stops the robot (about 0.5 s) and so does the main switch. A physical STOP / call button on the body is a Must before the trip. A STOP button on the screen during the call is added only if the overlay test passes (`software-plan.md`, section 3.3). | Must |
| 13 | **Starts by itself** | Switch on, wait about a minute, the idle screen shows. No keyboard needed. | Must |
| 14 | **Connects to the home Wi-Fi** | First choice: the Wi-Fi is stored before the trip. Fallbacks: your phone's hotspot, then a network cable. | Must |

## C. Safety, done by the robot itself

| # | Function | How it works, short | Priority |
|---|---|---|---|
| 15 | **Stops when the connection drops** | Four independent timers (250, 300, 500 and 1000 ms); the wheels stop in about 0.4 s, or about 0.6 s if the ESP32 program hangs (ASSUMED, measured in Stage 5 and 7). | Must |
| 16 | **Driving needs an extra switch** | After every reconnect, driving is off until you switch it on again, and only one person controls the robot at a time. | Must |
| 17 | **Stops before obstacles** | Two sonars in front. | Should |
| 18 | **Stops at stair edges** | Two floor-facing IR sensors (cliff sensors). Required before the trip, because remote driving stays off until they pass. They protect only driving forwards, and only at low speed. | Must (before the trip) |
| 19 | **Stops if lifted or tipped** | The gyro board (GY-521) on the motherboard; stops at 10 degrees of tilt. Required before the trip. | Must (before the trip) |
| 20 | **Safe shutdown** | At low battery the robot warns, then the Pi shuts down cleanly before the pack runs empty. | Should |

## D. Version 2 and extras

| # | Function | Priority |
|---|---|---|
| 21 | One own web page with video and controls together (instead of the public Jitsi service) | Nice, after the trip works |
| 22 | Gamepad driving in the browser | Nice |
| 23 | Camera slide cover (the 3D design now has a slot for it; the physical call/STOP button is already a Must, see rows 9 and 12) | Nice |
| 24 | Bumper switches | Optional |

Out of scope unless you ask: AI agent on the robot, turret, mapping, self-docking.

## What does the work (one sentence each)

- **Raspberry Pi 5:** runs the browser for the call, the small robot service (buttons, rooms, notifications) and the link to the ESP32.
- **ESP32 on the motherboard:** drives the motors, pan/tilt servos, reads sonar, cliff sensors, gyro and battery, and stops everything by itself if the Pi stops talking.
- **Tailscale:** the private link that lets you reach the robot through the sister's router without changing any router setting.
- **Jitsi (first version):** the free video call service the call runs on. Replaced later by an own page.
