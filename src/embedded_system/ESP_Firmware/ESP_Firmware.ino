#include "config.h"

/// Tested on ESP32-S3-USB-OTG

void setup() {
  Serial.begin(BAUD_RATE);

  for(auto i: LED_PINS){
    pinMode(i, OUTPUT);
  }

  



}

String serialInput(){
  String MyString;
  char Cache;

  while(Serial.available()){
    Cache = Serial.read();
    if(Cache == '\n'){
      break;
    }
    MyString += Cache;
  }

  return MyString; 
}


void update_leds(int count){
  for(int i = count; i < LED_COUNT; i++){
    digitalWrite(LED_PINS[i], 0);
  }
  for(int i = 0; i < count; i++){
    digitalWrite(LED_PINS[i], 1);
  }
}

void loop() {
  String A = serialInput();


  if(A == "HELLO") { /// HELLO

    Serial.print("READY\n");
  }//////////////////////
  else if (A == "C0") {
    update_leds(0);
    Serial.print("OK\n");
  }//////////////////////
  else if (A == "C1") { /// LED 1
    update_leds(1);
    Serial.print("OK\n");
  }//////////////////////
  else if (A == "C2") { /// LED 2
    update_leds(2);
    Serial.print("OK\n");
  }//////////////////////
  else if (A == "C3") { /// LED 3
    update_leds(3);
    Serial.print("OK\n"); 
  }//////////////////////
  else if (A == "C4") { /// LED 4
    update_leds(4);
    Serial.print("OK\n");
  }//////////////////////
  else if (A == "C5") { /// LED 5
    update_leds(5);
    Serial.print("OK\n");
  }//////////////////////
  else if (A == ""){    /// NO DATA
    /// ...DO NOTHING...
  }//////////////////////
  else{                 /// ERROR
    Serial.print("ERROR\n");
  }





}
