#include "rtos.h"
#include "modbus.h"
#include "motor.h"

bool trigger_last = false;
float theta1 = 0;
float theta2 = 0;

TaskHandle_t controlTaskHandle = NULL;
TaskHandle_t comTaskHandle = NULL;

void vRtosInit(void){

  xTaskCreate(
      vControlTask,
      "Control Task",
      4096,
      NULL,
      1,
      &controlTaskHandle
    );

    xTaskCreate(
      vComTask,
      "Communication Task",
      4096,
      NULL,
      1,
      &comTaskHandle
    );
}

void vControlTask(void *pvParameters) {
    while (true) {
        vRunMotors(); // Roda sempre para não perder passos

        if (ulTaskNotifyTake(pdTRUE, 0)) {
            vMoveRobo(mb.Hreg(REG_THETA1), mb.Hreg(REG_THETA2));
        }

        // Lógica de liberação
        bool parado = (motorBase.distanceToGo() == 0 && motorCotovelo.distanceToGo() == 0);
        
        if (parado) {
            // Se chegou no alvo, libera o Python mudando Trigger para 0
            if (mb.Hreg(REG_TRIGGER) == 1) {
                mb.Hreg(REG_TRIGGER, 0); 
                Serial.println("Fim do movimento físico.");
            }
        } else {
            // Se está se mexendo, garante que o Trigger fique em 1
            // Isso evita que o Python ache que acabou antes de começar
            mb.Hreg(REG_TRIGGER, 1);
        }

        vTaskDelay(1);
    }
}

void vComTask(void *pvParameters){
  
  while(true){
    mb.task();
    bool trigger_now = mb.Hreg(REG_TRIGGER);

    // Detecta borda de subida (0 -> 1)
    if (trigger_now && !trigger_last) {
        Serial.println("Comando recebido!");
        xTaskNotifyGive(controlTaskHandle);
    }

    trigger_last = trigger_now;
    vTaskDelay(pdMS_TO_TICKS(10));
  }
}
