#include "joystick.h"


/*Joystick::Joystick(){
  attach();
}*/
/*Creacion de metodo de clase con parametros de entrada
1. definir 2 metodos, uno con parametros de entrada y el otro sin nada, son una estrategia, por si el usrurio no entrega parametros de entrada
2. sed deben especificar el tipo de dato especificando el tamaño fijo en bits uint8_t */

//Metodo sin paametros de entrada
void Joystick::attach(){
  pinMode(pinjx, INPUT);
  pinMode(pinjy, INPUT);
  }
//Metodo con parametros de entrada
  void Joystick::attach(uint8_t pjx, uint8_t pjy){
    //reasigno las variables por defecto a las entregadas por el usuario
    pinjx = pjx;
    pinjy = pjy;
    pinMode(pinjx, INPUT);
    pinMode(pinjy, INPUT);
  }
    
  
  
  int Joystick::lecturaY(){
    int valAntY = 0, axisy=0;
    //for que promedia la lectura en Y
    for(int i =0; i<6; i++) valAntY = valAntY + analogRead(pinjy);

    axisy = valAntY/6;
    Serial.println("Valores en Y: " + String(axisy));
    return axisy;
  }

  int Joystick::lecturaX(){
    int valAntX = 0, axisx=0;
    //for que promedia la lectura en X
    for(int i =0; i<6; i++) valAntX = valAntX + analogRead(pinjx);
    
    axisx = valAntX/6;
    Serial.println("Valores en X: " + String(axisx));
    return axisx;
  }
