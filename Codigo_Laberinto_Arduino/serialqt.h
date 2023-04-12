#include "Arduino.h"


class serialQT{
  public:
  serialQT();//CONSTRUCCTOR
  int serialY(char dato);
  int serialX(char dato);

  private:
  const byte led = 2;
};