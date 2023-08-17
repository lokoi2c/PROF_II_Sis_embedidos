""" 
CÓDIGO PRINCIPAL:
Algunos código en esta carpeta son librerías dentro de librerías. 
Ejemplo: ElADCDivino.py reúne el Adc (Joystick) y el motor.py, en un solo archivo,
que a su vez, tiene a servo.py importado.

"""

#import ElADCDivino as Eladc
import mpu5050, math
import RPi.GPIO as GPIO
from time import sleep
import motor
import adc
import socket
from threading import Thread


# - - - - - - - - - - - - - - - - - - - -  COMUNICACIÓN DE PROCESO - - - - - - - - - - - - - - - - - -

run = True 
delay = 0.5
mode = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 65432))    # Se conecta a la raspberry
s.listen()  # Escucha conexiones entrantes

def hilosock():
    global mode
    while run:
        try:
            client, address = s.accept()
            print('Ciente conectado')
            data = client.recv(1024)
            if data == b'manual':
                mode = True
            elif data == b'auto':
                mode = False  
            print(data)
            # client.send("hola".encode('utf-8'))
            
        except KeyboardInterrupt:
            break
        
    print('End server')

    """
                        Ahora tengo un par de preguntas... ¿Debería poner una función
                que ejecute toodo este código en respuesta a la solicitud de la interfaz?
 """       

# - - - - - - - - - - - - - - - - - - - - # Lo del ADCDivino: # - - - - - - - - - - - - - - - - - - - - - - 

adc = adc.ADC()
laberinto = motor.Motor(12,19,1,80)
adc.setup()

def ADCDivino():
    global mode
    while True:
        if mode:
            try:
                valory = adc.read(0)
                valorx = adc.read(1)
                #print('ch0 valor y: {}, ch1 valor x:{}'.format(valory, valorx))
                laberinto.MoverLaberintoX(valorx)
                laberinto.MoverLaberintoY(valory)
                sleep(.08)
                
                
            except KeyboardInterrupt:
                break

# - - - - - - - - - - - - - - - - - - - # Lo del MPU # - - - - - - - - - - - - - - - - - - - - - - - - -
'''def mpu6050():
        mpu = mpu5050.MPU6050(0x68)
        mpu.begin()

        while True:
            accel = mpu.getAcceleration()
            gyro = mpu.getRotation()

            
            #print("ax:{}, ay:{}, az:{}".format(accel['x'], accel['y'], accel['z']))
            #print("gx:{}, gy:{}, gz:{}".format(gyro['x'], gyro['y'], gyro['z']))
            
            # Conversión matemática a inclinación:
            
            Ix = math.atan(accel['x'] / math.sqrt(math.pow(accel['y'], 2) + math.pow(accel['z'], 2)))*(180.0 / 3.14)
            
            Iy = math.atan(accel['y'] / math.sqrt(math.pow(accel['x'], 2) + math.pow(accel['z'], 2)))*(180.0 / 3.14)
            
            print("Inclix:{}, Incliy:{}".format(Ix, Iy))'''
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

hilo_adcdivino = Thread(target=ADCDivino)
hilo_adcdivino.start()

hilo_sock = Thread(target = hilosock)
hilo_sock.start()