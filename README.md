# Abadi Rover

Two robots, one shared motherboard. Each robot has its own files, so they do not get mixed up.

| | Robot | Where its files are | Status |
|---|---|---|---|
| **Abadi Rover 1** | The tracked rover: ELEGOO tracked chassis, Raspberry Pi 5, ESP32-S3 motherboard, camera, audio. | The files at the **top level** of this repository: [`plan.md`](plan.md) (the locked build plan), [`wiring.md`](wiring.md), [`HANDOVER.md`](HANDOVER.md), [`wiring-map.png`](wiring-map.png), [`wiring-map.svg`](wiring-map.svg), [`wiring-map-unoq.png`](wiring-map-unoq.png), [`relay-wiring.png`](relay-wiring.png), [`relay-wiring.svg`](relay-wiring.svg) | In progress (still being built) |
| **Abadi Rover 2** | The telepresence robot: round base, 7 inch screen and camera on a pan/tilt head, Raspberry Pi 5 for video calls. It will be built abroad, so the owner can call family and drive the robot around the house from Germany. | The folder [`abadi-rover-2/`](abadi-rover-2/) (start with its [`README.md`](abadi-rover-2/README.md)) | First design draft |
| **Shared motherboard** | The 100 x 100 mm ESP32-S3 board (KiCad 7, 2 layers) used by both robots. The owner reports that five boards were ordered, for five different robots. | The folder [`pcb/kicad/`](pcb/kicad/) (start with its [`README.md`](pcb/kicad/README.md); locked pin table: [`pin-table.md`](pcb/kicad/pin-table.md)) | v5 designed and checked. Order only after the paper test-fit in `pcb/kicad/README.md` passes. If the owner has already ordered, he must confirm the ordered files are v5 (they must match `pin-table.md`) |

## Rules that keep the two robots apart

- Robot 1's files stay where they are. Other tools (for example Cursor) read `plan.md` at the top level, so they are not moved.
- Robot 2 is written only inside `abadi-rover-2/`. It does not change `plan.md`, `wiring.md`, `HANDOVER.md` or anything else of robot 1.
- The motherboard folder is shared. Its pin table and power design are **locked**; a change needs the owner's explicit approval, because both robots depend on it.
- One stage at a time. A robot's code is only written for the stage that is being built and tested.
