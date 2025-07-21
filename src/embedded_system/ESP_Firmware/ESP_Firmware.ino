#include "config.h"

/// Tested on ESP32-S3-USB-OTG

void setup() {
  Serial.begin(BAUD_RATE);

  for(auto i: LED_PINS){
    pinMode(i, OUTPUT);
  }
}

String serialInput(){
  String MyString = "";
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
  String command = serialInput();
  
  if(command.startsWith("C") && command.length() >= 2){ /// C + [Number]
    int finger_count = command.substring(1).toInt();

    if(finger_count >= 0 && finger_count <= LED_COUNT){ /// Valid command
      update_leds(finger_count);
      Serial.print("OK\n");
    }else{ /// Invalid command
      Serial.print("ERROR");
    }
  ///////////////////////////////
  }else if(command == ""){
    /// Do Nothing
  ///////////////////////////////
  }else if(command = "HELLO"){ /// Hello
      Serial.print("READY\n");
  ///////////////////////////////
  }else{ /// unknown command
    Serial.print("ERROR");
  }
}
