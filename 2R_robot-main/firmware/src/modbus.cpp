#include "modbus.h"

ModbusIP mb;

void vModbusInit(void){
    mb.server();
    mb.addHreg(REG_THETA1);
    mb.addHreg(REG_THETA2);
    mb.addHreg(REG_TRIGGER);
}