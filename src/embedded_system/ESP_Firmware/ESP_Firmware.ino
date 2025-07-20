#include "config.h"

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


void loop() {
  String A = serialInput();


  if(A == "HELLO") { /// HELLO
    
    Serial.print("READY\n");
  }//////////////////////
  else if (A == "C0") {

    Serial.print("OK\n");
  }//////////////////////
  else if (A == "C1") { /// LED 1
    
    Serial.print("OK\n");
  }//////////////////////
  else if (A == "C2") { /// LED 2

    Serial.print("OK\n");
  }//////////////////////
  else if (A == "C3") { /// LED 3
    
    Serial.print("OK\n"); 
  }//////////////////////
  else if (A == "C4") { /// LED 4
    
    Serial.print("OK\n");
  }//////////////////////
  else if (A == "C5") { /// LED 5
    
    Serial.print("OK\n");
  }//////////////////////
  else if (A == ""){    /// NO DATA
    /// ...DO NOTHING...
  }//////////////////////
  else{                 /// ERROR
    Serial.print("ERROR\n");
  }





}
