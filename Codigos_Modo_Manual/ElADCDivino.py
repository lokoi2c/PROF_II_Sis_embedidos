import RPi.GPIO as GPIO
from time import sleep
import servo
import Codigo_Laberinto_Manual.adc as adc
import motor

#servox  = servo.Servo(15)
adc = adc.ADC()
laberinto = motor.Motor(4,15,1,80)
adc.setup()
valorx =0

while True:
    try:
        valory = adc.read(0)
        valorx = adc.read(1)
        print('ch0 valor y: {}, ch1 valor x:{}'.format(valory, valorx))
        laberinto.MoverLaberintoX(valorx)
        laberinto.MoverLaberintoY(valory)
        sleep(.08)
        
        
    except KeyboardInterrupt:
        break