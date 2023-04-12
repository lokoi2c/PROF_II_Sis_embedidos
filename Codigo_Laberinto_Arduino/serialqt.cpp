#include "serialqt.h"


serialQT::serialQT(){
    pinMode(led, OUTPUT);
}

int serialQT::serialY(char dato){
  int valor = 2000;
    if(dato== 'w'){
      digitalWrite(led, 1);
      delay(50);
      digitalWrite(led, 0);
      valor =700;
    }
    else if(dato== 's'){
      digitalWrite(led, 1);
      delay(50);
      digitalWrite(led, 0);
      valor = 3000;
    }
    else{
      digitalWrite(led, 1);
      delay(50);
      digitalWrite(led, 0);
      valor = 2000;
    }
    return valor;
}

int serialQT::serialX(char dato){
  int valor = 2000;
     if(dato== 'a'){
      digitalWrite(led, 1);
      delay(50);
      digitalWrite(led, 0);
      valor = 700;
    }
    else if(dato== 'd'){
      digitalWrite(led, 1);
      delay(50);
      digitalWrite(led, 0);
      valor = 3000;
    }
    else{
      digitalWrite(led, 1);
      delay(50);
      digitalWrite(led, 0);
      valor = 2000;
    }
    return valor;
}