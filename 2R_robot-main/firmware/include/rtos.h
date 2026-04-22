#ifndef RTOS_H
#define RTOS_H

#include <Arduino.h>

void vRtosInit(void);
void vControlTask(void *pvParameters);
void vComTask(void *pvParameters);

#endif