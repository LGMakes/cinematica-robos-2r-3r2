#include "apwifi.h"

void vAcessPointInit(void){
    Serial.println("Iniciando Access Point...");
    WiFi.softAP("ESP32_ROBOT", "12345678");
    Serial.println("Acess Point iniciado!");
    Serial.print("IP: ");
    Serial.println(WiFi.softAPIP());
}
    