#include "motor.h"

// Instanciação dos motores usando Meio-Passo (HALF4WIRE) [cite: 1, 2]
AccelStepper motorBase(AccelStepper::HALF4WIRE, BASE_IN1, BASE_IN3, BASE_IN2, BASE_IN4);
AccelStepper motorCotovelo(AccelStepper::HALF4WIRE, COTOVELO_IN1, COTOVELO_IN3, COTOVELO_IN2, COTOVELO_IN4);

bool maquinaReferenciada = true;

void vMotorInit(void) {
    // Configurações de velocidade e aceleração
    motorBase.setMaxSpeed(800.0);
    motorBase.setAcceleration(400.0);
    motorCotovelo.setMaxSpeed(800.0);
    motorCotovelo.setAcceleration(400.0);
}

void calibrarHoming() {
    motorBase.setCurrentPosition(0); 
    motorCotovelo.setCurrentPosition(0); 
    maquinaReferenciada = true;
    Serial.println("=> Homing OK.");
}

void vMoveRobo(float theta1, float theta2) {
    if (!maquinaReferenciada) return;

    // Converte os ângulos recebidos em passos
    long passosBase = (theta1 / 360.0) * PASSOS_POR_VOLTA;
    long passosCotovelo = -(theta2 / 360.0) * PASSOS_POR_VOLTA;

    motorBase.moveTo(passosBase); 
    motorCotovelo.moveTo(passosCotovelo); 
}

// Esta função deve ser chamada repetidamente para girar os motores
void vRunMotors(void) {
    motorBase.run();
    motorCotovelo.run();
}