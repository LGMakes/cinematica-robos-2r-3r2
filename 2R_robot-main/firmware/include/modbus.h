#pragma once

    #include <ModbusIP_ESP8266.h>
    #include <Arduino.h>

    #define REG_THETA1 0
    #define REG_THETA2 1
    #define REG_TRIGGER 2

    extern ModbusIP mb;
    
    void vModbusInit(void);