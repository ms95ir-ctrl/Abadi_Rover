# Abadi Rover 2: review log (what was checked, what was changed, what is still open)

Written 5 November 2026, after the first design draft. Nothing here was built or measured; the checks were done by reading the files, recomputing the numbers with scripts, compiling the 3D files and looking at the pictures.

## How the draft was checked

1. **Four independent reviewers** (electrical, mechanical/CAD, software/protocol, completeness) read the whole folder. Every medium or high finding was then attacked by a second reviewer who tried to prove it wrong. Result: **78 findings confirmed, 2 rejected**.
   - Rejected 1: "the headline price is not the price of the recommended parts". The README names the cheap and the comfortable build and points to the parts list, which says what is inside each.
   - Rejected 2: "the word Claude appears in the files". It only names the other design session; there is no rule against it.
2. **Pass 1** applied the findings. Decisions were fixed first so the files agree with each other (tilt guard 10 degrees, motor cap 8 V, runtime 1.1 to 1.4 hours on 2 cells, the stages needed before the trip, the 4-cell wiring, a second power path for the servos, the divider resistor at the splice, a fuse for the speaker amplifier, the USB cable tests and so on). Each group of files was edited by one owner and checked by a separate verifier.
3. **Pass 2** was a cross-file check (power, software, mechanical, parts and arithmetic, the owner's first read). It found 73 more points, mostly stale numbers and statements that did not match after pass 1.
4. **Pass 3** closed the remaining open points (stale weights, the mast stiffness calculation, a picture label, steps in the right order).

## The most important changes for you

- The robot stops at 10 degrees of tilt (it tips at about 22 degrees on a ramp), not 30.
- Four stop timers, not three. The robot stops in about 0.4 s (ASSUMED).
- Before the trip the stair-edge sensors, the tilt/pick-up detection and the family STOP must work, and remote driving stays off until they pass.
- The USB cable between the Pi and the ESP32 has two bench tests (A and B) before you trust a data-only cable.
- Four cells (2S2P) now have wiring rules and their own picture (`../diagrams/battery-4cell.png`).
- The servos get a second power wire to the PCA9685's own screw terminal.
- The 3D design now has places for the call / STOP button, the camera light, the camera cover and the speaker. Their sizes are ASSUMED; measure the real parts before printing the large pieces.
- The parts list grew (right-angle USB adapters, a speaker-amplifier fuse, spare IR sensors, a fuse assortment and more). Cheap build about 582 EUR, comfortable build about 821 EUR; the exact figures are in `parts-list.md`, section 1.

## Still open (nobody can close these without you or without the real parts)

1. Charging while the robot is on (the plan says: switch it on only at agreed call times).
2. 2 cells or 4 cells.
3. The pan cable path in the head is not proven: pan is limited to +/-30 degrees until Stage 6 tests the real bundle.
4. The stair-edge sensors sit about 43 mm in front of the balance point. They give only a short margin and nothing protects driving backwards.
5. The base has no service hatch: reaching the fuses means lifting the cover and taking off the deck (`mechanical-design.md`, section 14, item 10).
6. Whether the devkit's USB chip works with a data-only cable (tests A and B decide).
7. Whether the Pi 5 limits its USB ports to 600 mA on a bare USB-C power cable (check the official documentation).
8. Your pan/tilt design, printer bed size, country and days until the trip (`../README.md`, "What I need from you").
9. Whether the 5 boards are version v5, and the paper test-fit of the DRV8833 row and the screen pin order (`../../pcb/kicad/README.md`).
10. Every weight, tip-over, runtime and stop-time number is a calculation until it is measured.
