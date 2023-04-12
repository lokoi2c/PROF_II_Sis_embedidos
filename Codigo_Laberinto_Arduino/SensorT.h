#include "Arduino.h"

//Clasesita del sensor touch...

class SensorT{
	private:	//Atributos del sensor touch
	  int pinled;
	  int capacitancia;

	public:
	  SensorT(int, int);	//Constructor de la clase
	  void sensar();
	  void pinalto();
};