# import RPi.GPIO as GPIO
import pigpio
from time import sleep


class Servo:
    def __init__(self, pin):
        self.motor = pin
        # GPIO.setwarnings(False)
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.motor, GPIO.OUT)
        # self.servo = GPIO.PWM(self.motor, 50)
        self.servo = pigpio.pi()
        self.servo.set_mode(self.motor, pigpio.OUTPUT)
        #self.angle2duty = lambda angle: (angle/18.0) + 2.5
        # self.servo.start(self.angle2duty(0))
        
    def write(self, angle):
        self.servo.hardware_PWM(self.motor, 50, self.angle2duty(angle))
        #duty = self.angle2duty(angle)
        #self.servo.ChangeDutyCycle(duty)
        #self.servo.stop()
        #GPIO.cleanup()
        
    def angle2duty(self,angle):
        return int((angle*611.111) + 20.000)
        
if __name__ == "__main__":
    servo = Servo(19)


    while True:
        
        for i in range(110, 120, 1):
            servo.write(117)
            print(i)
            sleep(.5)
            
        for i in range(120, 110, -1):
            servo.write(120)
            sleep(.5)
            print(i)
            
        servo.write(180)
        print("18000000")
        
