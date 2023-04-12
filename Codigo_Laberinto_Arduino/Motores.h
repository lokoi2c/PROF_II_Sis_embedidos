#include<Arduino.h>
#include <Servo.h>

#define equilibrioX 76
#define equilibrioY 90

class Motor{
  public:
  void moverlaberintoX(int valor);
  void moverlaberintoY(int valor);
  void begin();
  void begin(uint8_t pinmx, uint8_t pinmy, uint8_t sensibilidad);
  
  private:
  uint8_t pinMotorX = 14;
  uint8_t pinMotorY = 12;
  uint8_t sensibility = 1;
  //uint8_t equilibrioX = 76;
  //uint8_t equilibrioY = 90;
};

