#include "esp32-hal-gpio.h"
#include "SensorT.h"

// Inicialización del constructor
SensorT::SensorT(int _pinled, int _capacitancia)
{
	pinled = _pinled;
	capacitancia = _capacitancia;
}

/* INICIALIZACIÓN DE MÉTODOS */

//Método de sensar capacitancia:
void SensorT::sensar()
{	 
	Serial.print("Capacitancia: ");
	Serial.println(touchRead(capacitancia));	// Lee capacitancia
	//delay(1000);
}

//Método poner pin en alto: 
void SensorT::pinalto()
{
  pinMode(pinled, OUTPUT);

	if(capacitancia < 50 || capacitancia > 55){   //Si se sale del rango...
    digitalWrite(pinled, HIGH);
    //delay(200);
    digitalWrite(pinled, LOW);
  }
  else{
    digitalWrite(pinled, LOW);
  }
}
	