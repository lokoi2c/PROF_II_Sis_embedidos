import RPi.GPIO as GPIO
from time import sleep
import motor

PIN_CLK = 17
PIN_CS  = 27
PIN_DI  = 22
PIN_DO  = 10    

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class ADC:
    def setup(self):
        GPIO.setup(PIN_CLK, GPIO.OUT)
        GPIO.setup(PIN_CS, GPIO.OUT)
        GPIO.setup(PIN_DI, GPIO.OUT)
        GPIO.setup(PIN_DO, GPIO.IN)

        GPIO.output(PIN_CLK, GPIO.LOW)
        GPIO.output(PIN_CS, GPIO.HIGH)

    def pulseClock(self):
        GPIO.output(PIN_CLK, GPIO.HIGH)
        GPIO.output(PIN_CLK, GPIO.LOW)

    def read(self, channel):
        # initial
        GPIO.output(PIN_CS, GPIO.LOW)
        GPIO.output(PIN_DI, GPIO.HIGH)

        # start bit, sgl/dif
        self.pulseClock()
        self.pulseClock()
        
        # odd/sign
        GPIO.output(PIN_DI, (channel & 1))
        self.pulseClock()

        # select bits
        GPIO.output(PIN_DI, ((channel//2) & 1))
        self.pulseClock()
        GPIO.output(PIN_DI, ((channel//2) & 2))
        self.pulseClock()
        
        value = 0

        for bit in range(8):
            self.pulseClock()
            value = value<<1 | int(GPIO.input(PIN_DO))

        GPIO.output(PIN_CLK, GPIO.LOW)
        GPIO.output(PIN_CS, GPIO.HIGH)

        return value

if __name__ == "__main__":
    adc = ADC()
    adc.setup()
    laberinto = motor.Motor(12,19,1,80)#morado es x, rojo es y
# o <-----130 ----> 180

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

