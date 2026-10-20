# Pin table (generated from the board file - PROVISIONAL)

The DRV8833 and screen pin orders are the owner's readings of the real modules; the relay, sonar, gyro and PCA9685 orders match the owner's photos and the usual orders; the I2C and UART headers have no module behind them. Compare each printed name with your real module before ordering.

## ESP32-S3 DevKit: which signal each pin carries (pin 1 is the antenna end of each row; row 1 = 3V3 3V3 RST ..., row 2 = GND TX RX ...)

| Header | Pin | GPIO / pin | Signal |
|---|---|---|---|
| J1 | 1 | 3V3 | ESP3V3 |
| J1 | 2 | 3V3 | ESP3V3 |
| J1 | 3 | RST | - |
| J1 | 4 | 4 | IN1A |
| J1 | 5 | 5 | IN4A |
| J1 | 6 | 6 | SCL |
| J1 | 7 | 7 | SDA |
| J1 | 8 | 15 | RLY1 |
| J1 | 9 | 16 | IN2A |
| J1 | 10 | 17 | RLY3 |
| J1 | 11 | 18 | RLY2 |
| J1 | 12 | 8 | IN1B |
| J1 | 13 | 3 | SPARE3 |
| J1 | 14 | 46 | SPARE46 |
| J1 | 15 | 9 | IN3B |
| J1 | 16 | 10 | IN4B |
| J1 | 17 | 11 | IN2B |
| J1 | 18 | 12 | TRIG |
| J1 | 19 | 13 | ECHO1_3V |
| J1 | 20 | 14 | ECHO2_3V |
| J1 | 21 | 5V | ESP5V |
| J1 | 22 | G | GND |
| J3 | 1 | G | GND |
| J3 | 2 | TX(43) | UART_TX |
| J3 | 3 | RX(44) | UART_RX |
| J3 | 4 | 1 | IN3A |
| J3 | 5 | 2 | CS_L |
| J3 | 6 | 42 | CS_R |
| J3 | 7 | 41 | LCD_RST |
| J3 | 8 | 40 | LCD_DC |
| J3 | 9 | 39 | MOSI |
| J3 | 10 | 38 | SPARE38 |
| J3 | 11 | 37 | - |
| J3 | 12 | 36 | - |
| J3 | 13 | 35 | - |
| J3 | 14 | 0 | - |
| J3 | 15 | 45 | SPARE45 |
| J3 | 16 | 48 | SPARE48 |
| J3 | 17 | 47 | SCK |
| J3 | 18 | 21 | SPARE21 |
| J3 | 19 | 20 | - |
| J3 | 20 | 19 | - |
| J3 | 21 | G | GND |
| J3 | 22 | G | GND |

## Other connectors (pin 1 = square pad)

- **DRV8833 A, HW-627 module (pins 1-6 = top row left to right IN1 IN2 VCC GND IN3 IN4, VCC = battery; pins 7-12 = bottom row, the side with the white plug, EEP OUT1 OUT2 OUT3 OUT4 ULT; EEP and ULT are not used)** (DRVA): 1=IN1A, 2=IN2A, 3=VBAT, 4=GND, 5=IN3A, 6=IN4A, 7=-, 8=M1A, 9=M1B, 10=M2A, 11=M2B, 12=-
- **DRV8833 B (same layout as DRV A)** (DRVB): 1=IN1B, 2=IN2B, 3=VBAT, 4=GND, 5=IN3B, 6=IN4B, 7=-, 8=M3A, 9=M3B, 10=M4A, 11=M4B, 12=-
- **PCA9685 header at its LEFT short end (top to bottom)** (PCA): 1=GND, 2=-, 3=SCL, 4=SDA, 5=ESP3V3, 6=SERVO5
- **GY-521 (left to right as printed on the module)** (GYRO): 1=-, 2=-, 3=-, 4=-, 5=SDA, 6=SCL, 7=GND, 8=ESP3V3
- **Screen L (CS DC RST SDA SCL VCC GND)** (SCR_L): 1=CS_L, 2=LCD_DC, 3=LCD_RST, 4=MOSI, 5=SCK, 6=RAILC, 7=GND
- **Screen R (CS DC RST SDA SCL VCC GND)** (SCR_R): 1=CS_R, 2=LCD_DC, 3=LCD_RST, 4=MOSI, 5=SCK, 6=RAILC, 7=GND
- **Spare IO (GPIO numbers are printed on the board)** (SPARE): 1=GND, 2=ESP3V3, 3=SPARE3, 4=SPARE46, 5=SPARE45, 6=SPARE48, 7=SPARE38, 8=SPARE21
- **Relay 1** (RLY1H): 1=RAILC, 2=RLY1, 3=GND
- **Relay 2** (RLY2H): 1=RAILC, 2=RLY2, 3=GND
- **Relay 3** (RLY3H): 1=RAILC, 2=RLY3, 3=GND
- **Sonar 1** (SON1): 1=CLEAN5, 2=TRIG, 3=ECHO1_5V, 4=GND
- **Sonar 2** (SON2): 1=CLEAN5, 2=TRIG, 3=ECHO2_5V, 4=GND
- **I2C sensor** (I2C): 1=ESP3V3, 2=GND, 3=SDA, 4=SCL
- **UART** (UART): 1=GND, 2=UART_TX, 3=UART_RX
- **SERVO 5V IN (output of the servo buck)** (TL0): 1=SERVO5, 2=GND
- **BATT IN (battery pack, for the motors)** (TL1): 1=VBAT, 2=GND
- **CLEAN 5V IN (output of the clean 5V buck)** (TL2): 1=CLEAN5, 2=GND
- **3.3V IN (output of the 3.3V buck)** (TL3): 1=RAILC, 2=GND
- **POWER OUT: upper row = clean 5V, clean 5V, 3.3V, 3.3V (from the bucks); lower row = GND x4** (PWR): 1=CLEAN5, 2=CLEAN5, 3=RAILC, 4=RAILC, 5=GND, 6=GND, 7=GND, 8=GND
- **MOTOR 1 (2-pin, for a JST plug)** (TM1): 1=M1A, 2=M1B
- **MOTOR 2 (2-pin)** (TM2): 1=M2A, 2=M2B
- **MOTOR 3 (2-pin)** (TM3): 1=M3A, 2=M3B
- **MOTOR 4 (2-pin)** (TM4): 1=M4A, 2=M4B

Left-edge screw terminals (5.08 mm pitch): the lower/first pin is **+**, marked on the board. Motor connectors are 2-pin spots on a 2.54 mm grid for JST plugs (motors have no polarity; swap the two wires to reverse): M1 = DRV A OUT1+OUT2 (driven by IN1A/IN2A), M2 = DRV A OUT3+OUT4 (IN3A/IN4A), M3 = DRV B OUT1+OUT2, M4 = DRV B OUT3+OUT4.
