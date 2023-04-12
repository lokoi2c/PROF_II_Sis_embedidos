#include"Motores.h"

/*Motor::Motor()
{
¿que sucede? ¿por que me dice que estoy redefiniendo el constructor
}**/
  Servo servoX, servoY;//creo los objetos servo
  int gradosy = equilibrioY;
  int gradosx = equilibrioX;
  

void Motor::moverlaberintoY(int valor){
  if(valor > 2900){ 
    gradosy = gradosy + sensibility;
    Serial.println("im here "+ String(gradosy));
    if(gradosy > (equilibrioY + 10)) gradosy=(equilibrioY + 10);
    }
  else if(valor < 800){ 
    gradosy = gradosy - sensibility;
    Serial.println("im there "+ String(gradosy));
    if(gradosy < (equilibrioY - 10)) gradosy=(equilibrioY - 10);
    }
  else {
    Serial.println("im Y " + String(gradosy));
    if(gradosy<equilibrioY){
      for(gradosy; gradosy<equilibrioY; gradosy = gradosy + sensibility){
        Serial.println(gradosy);
        servoY.write(gradosy);
        delay(80);
      
      }
    }
    else{
      for(gradosy; gradosy>equilibrioY; gradosy = gradosy - sensibility){
        Serial.println(gradosy);
        servoY.write(gradosy);
        delay(80);
      }
    }
  }
  Serial.println("\n \n ");
  servoY.write(gradosy); Serial.println("grados y: " + String(gradosy));
}
void Motor::moverlaberintoX(int valor){
   if(valor > 2800){ 
    gradosx = gradosx + sensibility;
    if(gradosx > (equilibrioX+10)) gradosx=(equilibrioX+10);
    }
  else if(valor < 900){ 
    gradosx =gradosx - sensibility;
    if(gradosx < (equilibrioX-10)) gradosx=(equilibrioX-10);
    }
  else {
    Serial.println("im X " + String(gradosx));
    if(gradosx<equilibrioX){
      for(gradosx; gradosx<equilibrioX; gradosx = gradosx + sensibility){
        Serial.println(gradosx);
        servoX.write(gradosx);
        delay(80);
      }
    }
    else{
      for(gradosx; gradosx>equilibrioX; gradosx =gradosx - sensibility){
        Serial.println(gradosx);
        servoX.write(gradosx);
        delay(80);
      }
    }
  }
  Serial.println("\n \n  ");

  servoX.write(gradosx); Serial.println("grados x: " + String(gradosx));

}

void Motor::begin(){
  servoX.attach(pinMotorX);
  servoY.attach(pinMotorY);
  delay(100);
  servoX.write(90);
  servoY.write(90);
}

  void Motor::begin(uint8_t pinmx, uint8_t pinmy, uint8_t sensibilidad){
    pinMotorX = pinmx;
    pinMotorY = pinmy;
    sensibility = sensibilidad;
    servoX.attach(pinMotorX);
    servoY.attach(pinMotorY);
    delay(100);
    servoX.write(90);
    servoY.write(90);
  }
