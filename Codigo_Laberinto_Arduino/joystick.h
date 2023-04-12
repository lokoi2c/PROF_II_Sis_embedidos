#include <Arduino.h>

class Joystick {
  private:
  uint8_t pinjx = 25;
  uint8_t pinjy = 26;
  
  public:
  void attach();
  void attach(uint8_t pjx, uint8_t pjy);
  int lecturaY();
  int lecturaX();
};