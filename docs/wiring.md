# Abadi Rover — Wiring Reference

![Phase 1 wiring map](wiring-map.png)

Soldering and assembly reference. Pin assignments come from the **Locked pin table** in [plan.md](../plan.md); if this file and `plan.md` ever disagree, `plan.md` wins and the mismatch must be reported.

Items marked **(wire later)** belong to Phase 2 or later. Their pins are reserved now; leave them unconnected until that stage.

## Wire colours and sizes

| Colour | Use |
|---|---|
| Red | Noisy 5V (after key switch) |
| Orange | Motor 7V (HW-183B output) |
| Purple | Quiet 5V (hub port) |
| Yellow | Rail C 3.3V |
| Black | GND |
| Any other colour | Signals |

- Power wires: 20–22 AWG. Signal wires: 24–26 AWG.
- Keep motor wires away from screen and sensor signal wires where possible.

## 1. Power diagram

```mermaid
flowchart LR
    subgraph bank [Power bank 20000mAh 45W]
        C2["USB-C port 2 PD"]
        UA["USB-A port"]
        C1["USB-C port 1 - charging only"]
    end

    C2 --> HubIn["Hub PD-IN"]
    HubIn --> Hub["Benfei hub"]
    Hub -->|"hub USB-C cable"| UnoQ["UNO Q"]
    Hub -->|"USB port"| Cam["Camera - Phase 3"]
    Hub -->|"USB port"| Audio["USB audio - Phase 3"]
    Hub -->|"USB port + screw adapter"| Quiet["Quiet 5V - purple"]

    Quiet --> Sonar["HC-SR04 VCC"]
    Quiet --> Buck["HW-133A set to 3.3V"]
    Buck --> RailC["Rail C 3.3V - yellow"]
    RailC --> ScrL["Left screen VCC - wire later"]
    RailC --> ScrR["Right screen VCC - wire later"]
    RailC --> Relay["Relay board VCC + COM1 + COM2"]

    UA -->|"screw adapter"| Key["Key switch"]
    Key --> Noisy["Noisy 5V - red"]
    Noisy --> Fan["Fan - keep-awake load"]
    Noisy --> Cap["Bulk cap 1000-2200uF"]
    Noisy --> PCAVplus["PCA9685 V+ terminal"]
    Noisy --> Boost["HW-183B screw input"]
    Boost --> Motor7["Motor 7V - orange"]
    Motor7 --> DRV["DRV8833 VCC"]

    UnoQ -->|"3.3V pin"| PCAVcc["PCA9685 VCC logic"]
```

### Ground (star point)

All of these go to **one** star point (a screw-terminal bus bar or lever connector):

```mermaid
flowchart TB
    Star["STAR GROUND POINT"]
    UAneg["USB-A adapter minus"] --> Star
    Quietneg["Quiet 5V adapter minus"] --> Star
    BuckNeg["HW-133A IN- and OUT-"] --> Star
    BoostNeg["HW-183B IN- and OUT-"] --> Star
    CapNeg["Bulk cap minus stripe"] --> Star
    FanNeg["Fan minus"] --> Star
    DRVg["DRV8833 GND"] --> Star
    PCAg["PCA9685 GND terminal"] --> Star
    SonarG["HC-SR04 GND"] --> Star
    RelayG["Relay board GND"] --> Star
    LightsG["Lights minus"] --> Star
    ScreensG["Screens GND - wire later"] --> Star
    UnoG["UNO Q GND screw - one wire"] --> Star
```

## 2. Signal diagram

```mermaid
flowchart LR
    subgraph uno [UNO Q screw shield]
        D2["D2"]
        D3["D3"]
        D4["D4"]
        D5["D5"]
        D6["D6"]
        D7["D7"]
        D8["D8"]
        D9["D9"]
        D10["D10"]
        D11["D11"]
        D13["D13"]
        A0["A0"]
        A2["A2"]
        A3["A3"]
        D20["D20 SDA"]
        D21["D21 SCL"]
    end

    D3 --> IN1["DRV8833 IN1"]
    D5 --> IN2["DRV8833 IN2"]
    D6 --> IN3["DRV8833 IN3"]
    D9 --> IN4["DRV8833 IN4"]

    D4 --> Trig["HC-SR04 TRIG"]
    Echo["HC-SR04 ECHO"] --> D2

    D20 --> PSDA["PCA9685 SDA"]
    D21 --> PSCL["PCA9685 SCL"]

    A2 --> R1["Relay IN1"]
    A3 --> R2["Relay IN2"]

    D10 --> LCS["Left screen CS - wire later"]
    D7 --> RCS["Right screen CS - wire later"]
    D8 --> DC["Both screens DC - wire later"]
    A0 --> RST["Both screens RST - wire later"]
    D11 --> SDA["Both screens SDA - wire later"]
    D13 --> SCL["Both screens SCL - wire later"]
```

```mermaid
flowchart LR
    PCA["PCA9685"] -->|"CH0"| S0["MG996R 180 deg"]
    PCA -->|"CH1"| S1["MZ996 90 deg"]
    PCA -->|"CH2"| S2["360 deg continuous"]
    DRVout["DRV8833"] -->|"OUT1 + OUT2"| ML["Left track motor"]
    DRVout -->|"OUT3 + OUT4"| MR["Right track motor"]
```

## 3. Per-component checklist

Tick each box once the wire is soldered/screwed and checked.

### Power bank, hub, key switch

| Done | From | To | Colour |
|---|---|---|---|
| [ ] | Bank USB-C port 2 | Hub PD-IN (USB-C cable) | — |
| [ ] | Hub USB-C cable | UNO Q USB-C | — |
| [ ] | Hub spare USB port | USB screw adapter = Quiet 5V | — |
| [ ] | Bank USB-A | USB-A screw adapter | — |
| [ ] | USB-A adapter + | Key switch terminal 1 | Red |
| [ ] | Key switch terminal 2 | Noisy 5V bus | Red |
| [ ] | USB-A adapter − | Star ground | Black |
| [ ] | Quiet 5V adapter − | Star ground | Black |

### HW-183B boost (motor 7V)

| Done | From | To | Colour |
|---|---|---|---|
| [ ] | Noisy 5V bus | HW-183B screw IN+ | Red |
| [ ] | Star ground | HW-183B screw IN− | Black |
| [ ] | HW-183B OUT+ | DRV8833 VCC | Orange |
| [ ] | HW-183B OUT− | Star ground | Black |

Use the **screw input**, not the HW-183B's USB-C socket, so the key switch can cut the motors. Re-check 7.0V under load after wiring, then glue the dial.

### DRV8833

| Done | DRV8833 pin | To | Colour |
|---|---|---|---|
| [ ] | IN1 | UNO Q D3 | Signal |
| [ ] | IN2 | UNO Q D5 | Signal |
| [ ] | IN3 | UNO Q D6 | Signal |
| [ ] | IN4 | UNO Q D9 | Signal |
| [ ] | OUT1, OUT2 | Left motor (2 wires) | — |
| [ ] | OUT3, OUT4 | Right motor (2 wires) | — |
| [ ] | VCC | HW-183B OUT+ (7V) | Orange |
| [ ] | GND | Star ground | Black |
| — | EEP | Not wired (J2 soldered) | — |
| — | ULT | Not connected | — |

### PCA9685 and servos

| Done | PCA9685 pin | To | Colour |
|---|---|---|---|
| [ ] | VCC | UNO Q 3.3V pin | Yellow |
| [ ] | GND (logic header) | UNO Q GND | Black |
| [ ] | SDA | UNO Q D20 | Signal |
| [ ] | SCL | UNO Q D21 | Signal |
| [ ] | V+ (screw terminal) | Noisy 5V bus | Red |
| [ ] | GND (screw terminal) | Star ground | Black |
| — | Bulk cap | Already on the PCA9685 board (1000µF), nothing to wire | — |
| — | OE | Not connected | — |
| [ ] | Channel 0 | MG996R plug | — |
| [ ] | Channel 1 | MZ996 plug | — |
| [ ] | Channel 2 | 360° servo plug | — |

Servo plugs: **brown/black = GND, red = V+, orange/yellow = signal (PWM)**. Match the row labels printed on the PCA9685 before plugging in.

### Fan

| Done | From | To | Colour |
|---|---|---|---|
| [ ] | Fan + | Noisy 5V bus | Red |
| [ ] | Fan − | Star ground | Black |

### HC-SR04

| Done | HC-SR04 pin | To | Colour |
|---|---|---|---|
| [ ] | VCC | Quiet 5V | Purple |
| [ ] | TRIG | UNO Q D4 | Signal |
| [ ] | ECHO | UNO Q **D2 only** | Signal |
| [ ] | GND | Star ground | Black |

### HW-133A buck (Rail C 3.3V)

| Done | From | To | Colour |
|---|---|---|---|
| [ ] | Quiet 5V | HW-133A IN+ | Purple |
| [ ] | Star ground | HW-133A IN− | Black |
| [ ] | HW-133A OUT+ | Rail C 3.3V bus | Yellow |
| [ ] | HW-133A OUT− | Star ground | Black |

Set to **3.3V with nothing connected to the output** before wiring any load. Measure again after loads are connected.

### Relay board and lights

| Done | From | To | Colour |
|---|---|---|---|
| [ ] | Relay VCC | Rail C 3.3V | Yellow |
| [ ] | Relay GND | Star ground | Black |
| [ ] | Relay IN1 | UNO Q A2 | Signal |
| [ ] | Relay IN2 | UNO Q A3 | Signal |
| [ ] | Relay COM1, COM2 | Rail C 3.3V | Yellow |
| [ ] | Relay NO1 | ~10Ω resistor → light 1 + | Yellow |
| [ ] | Relay NO2 | ~10Ω resistor → light 2 + | Yellow |
| [ ] | Light 1 −, light 2 − | Star ground | Black |

LED filaments have polarity: one end is usually marked (+, a dot, or a notch). Test each light briefly on 3.3V with the resistor before installing.

### Screens (wire later — Phase 2)

| Done | Screen pin | Left screen | Right screen | Colour |
|---|---|---|---|---|
| [ ] | VCC | Rail C 3.3V | Rail C 3.3V | Yellow |
| [ ] | GND | Star ground | Star ground | Black |
| [ ] | SCL | UNO Q D13 | UNO Q D13 | Signal |
| [ ] | SDA | UNO Q D11 | UNO Q D11 | Signal |
| [ ] | RST | UNO Q A0 | UNO Q A0 | Signal |
| [ ] | DC | UNO Q D8 | UNO Q D8 | Signal |
| [ ] | CS | UNO Q **D10** | UNO Q **D7** | Signal |

Use a 7-pin female connector housing on each screen. The shared lines (SCL, SDA, RST, DC) are joined at the shield's screw terminal, one wire to each screen.

## 4. Safety notes

- **Bulk capacitor polarity:** the stripe on the can marks the **minus** leg. Reversed, it can burst.
- **HC-SR04 ECHO only on D2.** Never on D3 or A0–A5 (not 5V-tolerant).
- **Never feed power into the UNO Q's 5V, 3.3V or IOREF pins.** The UNO Q is powered only through the hub.
- **HW-183B:** must stay at or below 10.8V (DRV8833 limit). Set 7.0V under load on the power bank, then glue the dial.
- **Before first power-on:** with everything off, check continuity (multimeter beep mode) from each rail's minus to the star point, and check that no + rail beeps to ground.
- **Charging:** robot off, unplug USB-C port 1's cable, then charge.
- Lift the tracks off the table for every first motor test.
