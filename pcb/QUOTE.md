# File to upload for a PCB quote

Upload this zip file:

`pcb/abadi-rover-body.zip`

On the PCB website (JLCPCB or any other):

1. Choose "Add gerber file" and select that zip.
2. Leave the board at **2 layers** and **1.6 mm** thick.
3. Any solder-mask colour is fine. Green is the usual one.
4. Ask for the bare board. The resistors and capacitors are holes you solder later, together with the modules.

The board is **133 mm wide and 93 mm tall**. That is smaller than the 150 mm × 95 mm perfboard.

Open `pcb/layout.png` in the repository to see the real board, to scale, with every hole named. Pin 1 of each row is the left hole.

Each connector is a row of holes. The rows are ESP32-S3, the two DRV8833 sockets, the servo board, the gyro, the two relay boards, the two screens, and the ultrasonic header.

The screw holes along the lower edge are the power wires, the motor wires, and the light wires. Their names are printed on the board.

The buck's 3.3V output and the ESP32's own 3.3V pin are separate. They are not tied together.
