# PROFUNDIZACIÓN I Sistemas Embedidos
## Proyecto Laberinto Inteligente
La practicidad y el potencial de los sistemas embebidos permite realizar 
construcciones muy interesantes, desde juegos didácticos, hasta sistemas 
automatizados e inteligencias artificiales. Esta propuesta pretende hacer un 
sistema que pase por todas estas etapas, realizando un modelo de laberinto 
que tendrá que resolverse de manera automática, valiéndose del 
funcionamiento de sistemas embebidos como el SoC ESP32 y finalmente 
Raspberry Pi. El laberinto tendrá la función de notificar cuando sea resuelto.

## Circuito esquematico
El laberinto automático C4RL052 es la fusión de 2 sistemas que utiliza la ESP32 para el 
control del Hardware y demás componentes que hacen el laberinto funcional. Y la 
Raspberry Pi 3 que se encarga de llevar el sistema a una interfaz digital, además de 
automatizarlo.
La integración de la Raspberry al sistema es simplemente la conexión de esta, a la 
computadora. Sin embargo, si desea transportar el laberinto, reemplazar piezas o por 
algún motivo accidental desconectó partes del circuito de la ESP32, deberá tener en 
cuenta las siguientes conexiones
![image](https://github.com/lokoi2c/PROF_II_Sis_embedidos/assets/71717504/b84b9625-7a5d-4463-94c3-fba522d0611c)
### Esp32
![image](https://github.com/lokoi2c/PROF_II_Sis_embedidos/assets/71717504/6a148df5-3ead-41ea-8849-4c396e46c0a6)
### Servos
: Dado el calibre de los 
servomotores, estos necesitan una fuente de 
alimentación externa, concretamente de 12V.
Los pines señalados en la ilustración 3 
corresponden a los pines de comunicación de 
los servomotores (cables amarillos en la 
ilustración 4), no olvide dirigir los cables VCC
(rojo) y GND (negro) a una fuente de 
alimentación externa al sistema.
#
![image](https://github.com/lokoi2c/PROF_II_Sis_embedidos/assets/71717504/889db8cf-b9b7-4672-8659-4348fc85a712)
### Joystick:
El joystick suministrado con el 
laberinto posee 5 salidas para conectar; las mismas que 
se muestran en la ilustración 5: VCC o 5V (cable rojo) 
GND (cable negro), conexión eje X (Cable naranja),
conexión eje Y (Cable amarillo), y SELECCIÓN (Cable 
azul). Todas son importantes a excepción de 
SELECCIÓN, dado que la función de oprimir el joystick 
no tiene acciones asignadas. Cabe recalcar que las 
conexiones del eje X y eje Y van dirigidas a los pines que 
muestra la ilustración 3, mientras que VCC y GND beben 
de los pines de alimentación de la ESP32, NO de la fuente externa que alimenta a los 
motores. 
#
![image](https://github.com/lokoi2c/PROF_II_Sis_embedidos/assets/71717504/1c1f038a-91c9-49d0-a9cd-60da1bf80e4e)
### MPU6050
: El MPU6050 es un 
dispositivo que se comunica a través del protocolo i2C. 
Consta de 8 pines pero para el laberinto sólo se utilizan 4. El 
par de pines de alimentación, y los pines SCL y SDA que 
forman parte del protocolo ya mencionado. Estos últimos se 
conectan como se indica en la ilustración 3, mientras que los 
pines de alimentación van a los que suministra la ESP32.

![image](https://github.com/lokoi2c/PROF_II_Sis_embedidos/assets/71717504/6f8bfce0-033a-4801-abd3-98e0153114d6)

fg
## Diseño del sistema
![image](https://github.com/lokoi2c/PROF_II_Sis_embedidos/assets/71717504/5f59cf84-d472-44ad-b9b8-447e10a46abf)
sgsrg
##Laberinto final
![laberinto2](https://github.com/lokoi2c/PROF_II_Sis_embedidos/assets/71717504/df13e8dd-af8d-4b98-87bd-7418dc23e212)
![laberinto](https://github.com/lokoi2c/PROF_II_Sis_embedidos/assets/71717504/32fb4e13-0f13-4f7b-8952-f1f387bd18af)

##Conclusiones:
sdfs
