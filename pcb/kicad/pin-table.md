# Pin table (generated from the board file - PROVISIONAL)

Everything here follows the module pin orders I assumed. Check each one against your real module before ordering.

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

- **DRV8833 A (2 rows: inputs row first, then power/outputs row)** (DRVA): 1=IN1A, 2=IN2A, 3=IN3A, 4=IN4A, 5=GND, 6=VBAT, 7=M1A, 8=M1B, 9=M2A, 10=M2B
- **DRV8833 B** (DRVB): 1=IN1B, 2=IN2B, 3=IN3B, 4=IN4B, 5=GND, 6=VBAT, 7=M3A, 8=M3B, 9=M4A, 10=M4B
- **PCA9685 header at its LEFT short end (top to bottom)** (PCA): 1=GND, 2=-, 3=SCL, 4=SDA, 5=ESP3V3, 6=SERVO5
- **GY-521 (left to right as printed on the module)** (GYRO): 1=-, 2=-, 3=-, 4=-, 5=SDA, 6=SCL, 7=GND, 8=ESP3V3
- **Screen L** (SCR_L): 1=RAILC, 2=GND, 3=CS_L, 4=LCD_RST, 5=LCD_DC, 6=MOSI, 7=SCK
- **Screen R** (SCR_R): 1=RAILC, 2=GND, 3=CS_R, 4=LCD_RST, 5=LCD_DC, 6=MOSI, 7=SCK
- **Spare IO (GPIO numbers are printed on the board)** (SPARE): 1=GND, 2=ESP3V3, 3=SPARE3, 4=SPARE46, 5=SPARE45, 6=SPARE48, 7=SPARE38, 8=SPARE21
- **Relay 1** (RLY1H): 1=RAILC, 2=RLY1_H, 3=GND
- **Relay 2** (RLY2H): 1=RAILC, 2=RLY2_H, 3=GND
- **Relay 3** (RLY3H): 1=RAILC, 2=RLY3_H, 3=GND
- **Sonar 1** (SON1): 1=CLEAN5, 2=TRIG, 3=ECHO1_5V, 4=GND
- **Sonar 2** (SON2): 1=CLEAN5, 2=TRIG, 3=ECHO2_5V, 4=GND
- **I2C sensor** (I2C): 1=ESP3V3, 2=GND, 3=SDA, 4=SCL
- **UART** (UART): 1=GND, 2=UART_TX, 3=UART_RX
- **SERVO 5V IN (output of the servo buck)** (TL0): 1=SERVO5, 2=GND
- **BATT IN (battery pack, for the motors)** (TL1): 1=VBAT, 2=GND
- **CLEAN 5V IN (output of the clean 5V buck)** (TL2): 1=CLEAN5, 2=GND
- **3.3V IN (output of the 3.3V buck)** (TL3): 1=RAILC, 2=GND
- **POWER OUT: upper row = clean 5V, clean 5V, 3.3V, 3.3V (from the bucks); lower row = GND x4** (PWR): 1=CLEAN5, 2=CLEAN5, 3=RAILC, 4=RAILC, 5=GND, 6=GND, 7=GND, 8=GND
- **MOTOR 1** (TM1): 1=M1A, 2=M1B
- **MOTOR 2** (TM2): 1=M2A, 2=M2B
- **MOTOR 3** (TM3): 1=M3A, 2=M3B
- **MOTOR 4** (TM4): 1=M4A, 2=M4B

Terminals (all 5.08 mm pitch): the lower/first pin is **+**, marked on the board. Motor terminals: M1 = DRV A out 1/2, M2 = DRV A out 3/4, M3/M4 = DRV B.
