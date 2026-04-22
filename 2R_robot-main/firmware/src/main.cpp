#include "main.h"

void setup() {

    Serial.begin(115200);
    pinMode(2, OUTPUT);

    vRtosInit();
    vMotorInit();
    vAcessPointInit();
    vModbusInit();
}

void loop() {
  vTaskDelete(NULL);
  }