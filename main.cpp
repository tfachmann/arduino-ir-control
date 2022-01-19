#include "Arduino.h"
#include <IRremote.hpp>

#define IR_PIN 2

void setup() {
    Serial.begin(9600);
    IrReceiver.begin(IR_PIN, ENABLE_LED_FEEDBACK);
}

void loop() {
    if (IrReceiver.decode()) {
        Serial.println(IrReceiver.decodedIRData.decodedRawData, HEX);
        IrReceiver.resume();
    }
}
