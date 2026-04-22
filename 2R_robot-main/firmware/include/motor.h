#ifndef MOTOR_H
#define MOTOR_H

#include <Arduino.h>
#include <AccelStepper.h>

// Resolução do motor 28BYJ-48 
#define PASSOS_POR_VOLTA 4096 

extern AccelStepper motorBase;
extern AccelStepper motorCotovelo;

// Pinos Motor 1 (Base) - Atualizados para ESP32
#define BASE_IN1 13
#define BASE_IN2 12
#define BASE_IN3 14
#define BASE_IN4 27


// Pinos Motor 2 (Cotovelo) - Atualizados para ESP32
#define COTOVELO_IN1 26
#define COTOVELO_IN2 25
#define COTOVELO_IN3 33
#define COTOVELO_IN4 32

void vMotorInit(void);
void vMoveRobo(float theta1, float theta2);
void vRunMotors(void);
void calibrarHoming(void);

#endif