# Pin table (generated from the board file - PROVISIONAL)

Everything here follows the module pin orders I assumed. Check each one against your real module before ordering.

## ESP32-S3 DevKit: which signal each pin carries

| Header | Pin | GPIO / pin | Signal |
|---|---|---|---|
| J1 | 1 | 3V3 | ESP3V3 |
| J1 | 2 | 3V3 | ESP3V3 |
| J1 | 3 | RST | - |
| J1 | 4 | 4 | RLY1 |
| J1 | 5 | 5 | SCL |
| J1 | 6 | 6 | IN2A |
| J1 | 7 | 7 | IN4A |
| J1 | 8 | 15 | SDA |
| J1 | 9 | 16 | IN3A |
| J1 | 10 | 17 | RLY2 |
| J1 | 11 | 18 | RLY3 |
| J1 | 12 | 8 | IN1B |
| J1 | 13 | 3 | TOUCH1 |
| J1 | 14 | 46 | TOUCH2 |
| J1 | 15 | 9 | IN2B |
| J1 | 16 | 10 | IN3B |
| J1 | 17 | 11 | IN4B |
| J1 | 18 | 12 | TRIG |
| J1 | 19 | 13 | ECHO1_3V |
| J1 | 20 | 14 | ECHO2_3V |
| J1 | 21 | 5V | ESP5V |
| J1 | 22 | G | GND |
| J3 | 1 | G | GND |
| J3 | 2 | TX(43) | UART_TX |
| J3 | 3 | RX(44) | UART_RX |
| J3 | 4 | 1 | CS_L |
| J3 | 5 | 2 | IN1A |
| J3 | 6 | 42 | LCD_DC |
| J3 | 7 | 41 | CS_R |
| J3 | 8 | 40 | LCD_RST |
| J3 | 9 | 39 | MOSI |
| J3 | 10 | 38 | SPARE38 |
| J3 | 11 | 37 | - |
| J3 | 12 | 36 | - |
| J3 | 13 | 35 | - |
| J3 | 14 | 0 | - |
| J3 | 15 | 45 | SPARE45 |
| J3 | 16 | 48 | SPARE48 |
| J3 | 17 | 47 | SCK |
| J3 | 18 | 21 | - |
| J3 | 19 | 20 | - |
| J3 | 20 | 19 | - |
| J3 | 21 | G | GND |
| J3 | 22 | G | GND |

## Other connectors (pin 1 = square pad)

- **DRV8833 A (2 rows: inputs row first, then power/outputs row)** (DRVA): 1=IN1A, 2=IN2A, 3=IN3A, 4=IN4A, 5=GND, 6=VBAT, 7=M1A, 8=M1B, 9=M2A, 10=M2B
- **DRV8833 B** (DRVB): 1=IN1B, 2=IN2B, 3=IN3B, 4=IN4B, 5=GND, 6=VBAT, 7=M3A, 8=M3B, 9=M4A, 10=M4B
- **PCA9685 control socket** (PCA): 1=GND, 2=-, 3=SCL, 4=SDA, 5=ESP3V3, 6=-
- **GY-521** (GYRO): 1=ESP3V3, 2=GND, 3=SCL, 4=SDA, 5=-, 6=-, 7=-, 8=-
- **Screen L** (SCR_L): 1=RAILC, 2=GND, 3=CS_L, 4=LCD_RST, 5=LCD_DC, 6=MOSI, 7=SCK
- **Screen R** (SCR_R): 1=RAILC, 2=GND, 3=CS_R, 4=LCD_RST, 5=LCD_DC, 6=MOSI, 7=SCK
- **Spare IO** (SPARE): 1=GND, 2=ESP3V3, 3=SPARE3, 4=SPARE46, 5=SPARE45, 6=SPARE48
- **Relay 1** (RLY1H): 1=RAILC, 2=RLY1_H, 3=GND
- **Relay 2** (RLY2H): 1=RAILC, 2=RLY2_H, 3=GND
- **Relay 3** (RLY3H): 1=RAILC, 2=RLY3_H, 3=GND
- **Sonar 1** (SON1): 1=CLEAN5, 2=TRIG, 3=ECHO1_5V, 4=GND
- **Sonar 2** (SON2): 1=CLEAN5, 2=TRIG, 3=ECHO2_5V, 4=GND
- **I2C sensor** (I2C): 1=ESP3V3, 2=GND, 3=SDA, 4=SCL
- **UART** (UART): 1=GND, 2=UART_TX, 3=UART_RX
- **Touch 1** (TCH1): 1=RAILC, 2=TOUCH1, 3=GND
- **Touch 2** (TCH2): 1=RAILC, 2=TOUCH2, 3=GND
- **BATT IN** (TL0): 1=VBAT, 2=GND
- **TO BUCK 1 (servo 5V)** (TL1): 1=VBAT, 2=GND
- **TO BUCK 2 (clean 5V)** (TL2): 1=VBAT, 2=GND
- **TO BUCK 3 (3.3V)** (TL3): 1=VBAT, 2=GND
- **CLEAN 5V IN** (TR_5V): 1=CLEAN5, 2=GND
- **3.3V IN** (TR_33): 1=RAILC, 2=GND
- **MOTOR 1** (TM1): 1=M1A, 2=M1B
- **MOTOR 2** (TM2): 1=M2A, 2=M2B
- **MOTOR 3** (TM3): 1=M3A, 2=M3B
- **MOTOR 4** (TM4): 1=M4A, 2=M4B

Terminals: the lower/first pin is **+**, marked on the board. Motor terminals: M1 = DRV A out 1/2, M2 = DRV A out 3/4, M3/M4 = DRV B.
