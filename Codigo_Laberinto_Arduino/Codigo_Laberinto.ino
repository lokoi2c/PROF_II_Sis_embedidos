#include "Motores.h"
#include "joystick.h"
#include "SensorT.h"
#include "serialqt.h"
#include "MPU6050"


const int mpuAddress = 0x68;  // Puede ser 0x68 o 0x69
MPU6050 mpu(mpuAddress);


int elpinled = 33;  //pin del led touch
int lacap = 32; //pin del sensor touch
char dato;
int modo = 0;

//objetos
Motor Motor;
Joystick joystick;
SensorT SensorT1(elpinled,lacap); 
serialQT serialQT1;

void setup() {
  Serial.begin(115200);
  delay(200);
  Motor.begin();
  joystick.attach();//puedo entrgarle que pines, si no, lo hara por defer¿cto
}

void loop() {
  SensorT1.sensar();
  SensorT1.pinalto();

  if(Serial.available()){
    dato = Serial.read();
    if(dato == 'm') modo = 1; //debemos alamacenar la varible para que mantenga m , y asi modo = 1
  }

  if(modo){
    Motor.moverlaberintoX(serialQT1.serialX(dato));
    Motor.moverlaberintoY(serialQT1.serialY(dato));
    Serial.println("dato: " + String(dato) +" valorx: " + String(serialQT1.serialX(dato)) + "  valorY: " + String(serialQT1.serialY(dato)));

  }
  else{
    Motor.moverlaberintoX(joystick.lecturaX());
    Motor.moverlaberintoY(joystick.lecturaY());
  }  

  delay(80);//si se desea quitar este retraso tambien se deben quitar los de Motores.cpp
  Serial.flush();


// LECTURA DEL GIROSCOPIO: //
  mpu.getAcceleration(&ax, &ay, &az);

	//Calcular los angulos de inclinacion
	float accel_ang_x = atan(ax / sqrt(pow(ay, 2) + pow(az, 2)))*(180.0 / 3.14);
	float accel_ang_y = atan(ay / sqrt(pow(ax, 2) + pow(az, 2)))*(180.0 / 3.14);

	// Mostrar resultados
	Serial.print(F("Inclinacion en X: "));
	Serial.print(accel_ang_x);
	Serial.print(F("\tInclinacion en Y:"));
	Serial.println(accel_ang_y);
	delay(10);
}

