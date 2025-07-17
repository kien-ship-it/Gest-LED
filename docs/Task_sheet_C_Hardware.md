# Task Sheet for Engineer C (Bảo)

**Your Team:** Team Bravo - Embedded/Hardware Squad  
**Your Role:** Hardware Engineer  
**Your Partner:** Engineer D (Firmware Developer)

## 1. Your Mission

Design and build the physical LED display system. You'll create a reliable, well-documented circuit that can be controlled by an ESP8266 microcontroller. Your hardware will be the visual output that brings the project to life.

## 2. Your Deliverables

1. **Physical Circuit** - Fully assembled breadboard with ESP8266 and 5 LEDs
2. **Circuit Diagram** - Clear documentation (Fritzing, photo, or hand-drawn)
3. **`hardware_test.ino`** - Test firmware to verify all connections
4. **`config.h`** - Pin configuration file for your partner
5. **Hardware Documentation** - Connection guide and parts list

## 3. Required Components

### Essential Parts List
| Component | Quantity | Specifications |
|-----------|----------|----------------|
| ESP8266 NodeMCU | 1 | v2 or v3 |
| LEDs | 5 | Any color (red/green/blue recommended) |
| Resistors | 5 | 220Ω (red-red-brown) or 330Ω |
| Breadboard | 1 | Half-size (400 points) minimum |
| Jumper Wires | ~15 | Male-to-male |
| USB Cable | 1 | Micro-USB for NodeMCU |

### Tools Needed
- Computer with Arduino IDE installed
- USB port for programming
- Optional: Multimeter for testing
- Optional: Wire strippers/cutters

## 4. Pin Assignments (MANDATORY)

You MUST use these exact pins for compatibility with Engineer D's firmware:

| LED Number | Function | NodeMCU Pin | GPIO Number | Physical Location |
|------------|----------|-------------|-------------|-------------------|
| LED 1 | First finger | D1 | GPIO5 | Right side, top |
| LED 2 | Second finger | D2 | GPIO4 | Right side |
| LED 3 | Third finger | D5 | GPIO14 | Right side |
| LED 4 | Fourth finger | D6 | GPIO12 | Right side |
| LED 5 | Fifth finger | D7 | GPIO13 | Right side, bottom |

## 5. Circuit Design Specifications

### 5.1 Wiring Diagram

```
NodeMCU ESP8266 Pinout:
                    ┌─────────┐
               D0 ──┤         ├── D1 → LED1 (with 220Ω) → GND
               A0 ──┤         ├── D2 → LED2 (with 220Ω) → GND
              RST ──┤         ├── D3
              GND ──┤ ESP8266 ├── D4
               3V ──┤ NodeMCU ├── D5 → LED3 (with 220Ω) → GND
              GND ──┤         ├── D6 → LED4 (with 220Ω) → GND
               TX ──┤         ├── D7 → LED5 (with 220Ω) → GND
               RX ──┤         ├── D8
                    └─────────┘
                      USB Port
```

### 5.2 LED Connection Detail

Each LED must be connected as follows:
```
NodeMCU Pin ──→ Resistor (220Ω) ──→ LED Anode (+) ──→ LED Cathode (-) ──→ GND
```

**Important:** 
- LED Anode (longer leg) connects to resistor
- LED Cathode (shorter leg) connects to ground
- All 5 LEDs share common ground

### 5.3 Breadboard Layout Guide

```
     A B C D E     F G H I J
   ┌─────────────────────────┐
 1 │ ○ ○ ○ ○ ○  |  ○ ○ ○ ○ ○ │ ← Power Rails (optional)
 2 │ ○ ○ ○ ○ ○  |  ○ ○ ○ ○ ○ │
 3 │ R ○ ○ ○ ○  |  ○ ○ ○ ○ ○ │ ← Resistor for LED1
 4 │ ○ L ○ ○ ○  |  ○ ○ ○ ○ ○ │ ← LED1
 5 │ ○ ○ ○ ○ ○  |  ○ ○ ○ ○ ○ │
...│                         │
30 │ ○ ○ ○ ○ ○  |  ○ ○ ○ ○ ○ │
   └─────────────────────────┘

R = Resistor, L = LED, Wire from NodeMCU to resistor
```

## 6. Test Firmware Specifications

### 6.1 File: `hardware_test.ino`

```cpp
/*
 * hardware_test.ino - Hardware verification for Gest-LED
 * Author: Engineer C
 * Purpose: Test all LED connections independently
 */

// Pin definitions - MUST match your wiring
#define LED1_PIN 5   // D1
#define LED2_PIN 4   // D2
#define LED3_PIN 14  // D5
#define LED4_PIN 12  // D6
#define LED5_PIN 13  // D7

// Test parameters
#define CHASE_DELAY 200  // milliseconds between LEDs

void setup() {
  // Initialize serial for debugging
  Serial.begin(115200);
  Serial.println("Hardware Test Starting...");
  
  // Configure all LED pins as outputs
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  pinMode(LED3_PIN, OUTPUT);
  pinMode(LED4_PIN, OUTPUT);
  pinMode(LED5_PIN, OUTPUT);
  
  // Turn all LEDs off initially
  allLEDsOff();
  
  Serial.println("Setup complete. Starting LED chase...");
}

void loop() {
  // Test pattern 1: Chase sequence
  Serial.println("Pattern 1: Chase");
  chasePattern();
  
  // Test pattern 2: All on/off
  Serial.println("Pattern 2: All flash");
  allFlashPattern();
  
  // Test pattern 3: Binary count
  Serial.println("Pattern 3: Binary count");
  binaryCountPattern();
}

void chasePattern() {
  // Light each LED in sequence
  for(int i = 0; i < 5; i++) {
    allLEDsOff();
    setLED(i, HIGH);
    delay(CHASE_DELAY);
  }
}

void allFlashPattern() {
  // Flash all LEDs together
  for(int i = 0; i < 3; i++) {
    allLEDsOn();
    delay(300);
    allLEDsOff();
    delay(300);
  }
}

void binaryCountPattern() {
  // Count from 0 to 31 in binary
  for(int count = 0; count <= 31; count++) {
    displayBinary(count);
    delay(200);
  }
}

void setLED(int ledNumber, int state) {
  // Control individual LED (0-4)
  switch(ledNumber) {
    case 0: digitalWrite(LED1_PIN, state); break;
    case 1: digitalWrite(LED2_PIN, state); break;
    case 2: digitalWrite(LED3_PIN, state); break;
    case 3: digitalWrite(LED4_PIN, state); break;
    case 4: digitalWrite(LED5_PIN, state); break;
  }
}

void allLEDsOff() {
  digitalWrite(LED1_PIN, LOW);
  digitalWrite(LED2_PIN, LOW);
  digitalWrite(LED3_PIN, LOW);
  digitalWrite(LED4_PIN, LOW);
  digitalWrite(LED5_PIN, LOW);
}

void allLEDsOn() {
  digitalWrite(LED1_PIN, HIGH);
  digitalWrite(LED2_PIN, HIGH);
  digitalWrite(LED3_PIN, HIGH);
  digitalWrite(LED4_PIN, HIGH);
  digitalWrite(LED5_PIN, HIGH);
}

void displayBinary(int number) {
  // Display number in binary on LEDs
  digitalWrite(LED1_PIN, (number & 0x01) ? HIGH : LOW);
  digitalWrite(LED2_PIN, (number & 0x02) ? HIGH : LOW);
  digitalWrite(LED3_PIN, (number & 0x04) ? HIGH : LOW);
  digitalWrite(LED4_PIN, (number & 0x08) ? HIGH : LOW);
  digitalWrite(LED5_PIN, (number & 0x10) ? HIGH : LOW);
}
```

### 6.2 File: `config.h`

Create this file for Engineer D to use:

```cpp
/*
 * config.h - Hardware configuration for Gest-LED
 * Author: Engineer C
 * Date: [Current Date]
 * 
 * This file defines the pin mappings for the LED circuit.
 * These values MUST match the physical wiring.
 */

#ifndef CONFIG_H
#define CONFIG_H

// Serial communication settings
#define BAUD_RATE 115200

// LED pin definitions (GPIO numbers)
#define LED_COUNT 5

// Array of LED pins in order (finger 1 to 5)
const int LED_PINS[LED_COUNT] = {5, 4, 14, 12, 13};

// Pin labels for reference
// LED_PINS[0] = GPIO5  = D1 = LED for 1 finger
// LED_PINS[1] = GPIO4  = D2 = LED for 2 fingers
// LED_PINS[2] = GPIO14 = D5 = LED for 3 fingers
// LED_PINS[3] = GPIO12 = D6 = LED for 4 fingers
// LED_PINS[4] = GPIO13 = D7 = LED for 5 fingers

// LED behavior settings
#define LED_ACTIVE_HIGH true  // LEDs turn on with HIGH signal

// Debug settings
#define DEBUG_MODE true       // Enable serial debug messages

#endif // CONFIG_H
```

## 7. Assembly Instructions

### Step 1: Prepare the Breadboard
1. Place NodeMCU on breadboard (spanning the center channel)
2. Ensure USB port is accessible
3. Leave space for LEDs and resistors

### Step 2: Connect Ground Rail
1. Connect a jumper from NodeMCU GND to breadboard ground rail
2. This creates a common ground for all LEDs

### Step 3: Install LEDs (Repeat for each LED)
1. Insert LED with anode (long leg) in one row
2. Insert cathode (short leg) in adjacent row
3. Space LEDs evenly for clear visual display

### Step 4: Add Resistors
1. Connect resistor from NodeMCU pin row to LED anode row
2. Ensure firm connection (push fully into breadboard)

### Step 5: Complete Ground Connections
1. Connect jumper from each LED cathode to ground rail
2. Double-check all ground connections

### Step 6: Verify Before Power
1. Check no shorts between power and ground
2. Verify correct LED orientation
3. Confirm resistor values (220Ω or 330Ω)

## 8. Testing Procedure

### 8.1 Initial Hardware Check
1. **Visual Inspection**
   - All components firmly seated
   - No exposed wire ends touching
   - Correct LED orientation

2. **Continuity Test** (if multimeter available)
   - Test ground connections
   - Verify no shorts

### 8.2 Firmware Test
1. **Upload Test Firmware**
   ```
   - Open hardware_test.ino in Arduino IDE
   - Select Tools → Board → NodeMCU 1.0
   - Select correct COM port
   - Click Upload
   ```

2. **Observe LED Patterns**
   - Chase: Each LED lights in sequence
   - Flash: All LEDs blink together
   - Binary: LEDs count in binary

3. **Verify Serial Output**
   - Open Serial Monitor (115200 baud)
   - Should see pattern descriptions

### 8.3 Success Criteria
✓ All 5 LEDs light up individually  
✓ No LEDs are dim or flickering  
✓ Patterns run continuously without stopping  
✓ Serial monitor shows status messages

## 9. Troubleshooting Guide

| Problem | Possible Cause | Solution |
|---------|----------------|----------|
| LED won't light | Wrong polarity | Flip LED around |
| LED very dim | Resistor too high | Use 220Ω instead of 330Ω |
| All LEDs dead | No ground connection | Check ground rail |
| Random flashing | Loose connection | Push components firmly |
| Upload fails | Wrong board selected | Select NodeMCU 1.0 |
| No serial output | Wrong baud rate | Set to 115200 |

## 10. Documentation Requirements

### 10.1 Circuit Diagram
Create one of the following:
- Fritzing diagram (preferred)
- Clear photo with labels
- Hand-drawn schematic

Must clearly show:
- All connections
- Component values
- Pin numbers

### 10.2 Parts List
Document exact components used:
```
Parts Used:
- NodeMCU v3 (CP2102 USB chip)
- 5x Red LEDs (5mm)
- 5x 220Ω resistors
- 1x Half-size breadboard
- 10x Male jumper wires
```

### 10.3 Handoff Checklist
Before passing to Engineer D:
- [ ] All LEDs tested working
- [ ] config.h file created
- [ ] Circuit diagram complete
- [ ] Test firmware demonstrates all LEDs
- [ ] No loose connections
- [ ] Ground rail properly connected
- [ ] Serial output verified

## 11. Safety Notes

- Never connect LEDs directly to pins (always use resistors)
- Don't exceed 12mA per GPIO pin
- Unplug USB before modifying circuit
- Handle NodeMCU by edges to avoid static damage

## 12. Tips for Success

1. **Label Everything**: Use tape to label LED numbers
2. **Color Code**: Use same color wire for all grounds
3. **Test Often**: Check each LED as you connect it
4. **Document Well**: Your partner needs to understand your circuit
5. **Keep It Neat**: Tidy wiring prevents errors

Remember: Your hardware is the foundation of the project. A solid, well-tested circuit makes everyone's job easier. Take your time and build it right!