'''
    Based on: https://www.electronicwings.com/raspberry-pi/mpu6050-accelerometergyroscope-interfacing-with-raspberry-pi
'''

import smbus, math
from time import sleep

PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

class MPU6050:
    def __init__(self, address, device = 1):
        self.address = address
        self.bus = smbus.SMBus(device)

    def begin(self):
        #write to sample rate register
        self.bus.write_byte_data(self.address, SMPLRT_DIV, 7)
        #Write to power management register
        self.bus.write_byte_data(self.address, PWR_MGMT_1, 1)
        #Write to Configuration register
        self.bus.write_byte_data(self.address, CONFIG, 0)
        #Write to Gyro configuration register
        self.bus.write_byte_data(self.address, GYRO_CONFIG, 24)
        #Write to interrupt enable register
        self.bus.write_byte_data(self.address, INT_ENABLE, 1)

    def read_raw_data(self, addr):
        #Accelero and Gyro value are 16-bit
        high = self.bus.read_byte_data(self.address, addr)
        low = self.bus.read_byte_data(self.address, addr+1)

        #concatenate higher and lower value
        value = ((high << 8) | low)

        #to get signed value from mpu6050
        if(value > 32768):
            value = value - 65536
        return value

    def getAcceleration(self):
        acc_x = self.read_raw_data(ACCEL_XOUT_H)
        acc_y = self.read_raw_data(ACCEL_YOUT_H)
        acc_z = self.read_raw_data(ACCEL_ZOUT_H)

        ax = acc_x/16348.0
        ay = acc_y/16348.0
        az = acc_z/16348.0

        return {'x': ax, 'y': ay, 'z': az}
    
    def getRotation(self):
        gyro_x = self.read_raw_data(GYRO_XOUT_H)
        gyro_y = self.read_raw_data(GYRO_YOUT_H)
        gyro_z = self.read_raw_data(GYRO_ZOUT_H)

        gx = gyro_x/131.0
        gy = gyro_y/131.0
        gz = gyro_z/131.0

        return {'x': gx, 'y': gy, 'z': gz}
    

# Lo mismo que está en el main:

if __name__ == "__main__":
    mpu = MPU6050(0x68)
    mpu.begin()

    while True:
        accel = mpu.getAcceleration()
        gyro = mpu.getRotation()

        
        #print("ax:{}, ay:{}, az:{}".format(accel['x'], accel['y'], accel['z']))
        #print("gx:{}, gy:{}, gz:{}".format(gyro['x'], gyro['y'], gyro['z']))
        
        # Conversión matemática a inclinación:
        
        Ix = math.atan(accel['x'] / math.sqrt(math.pow(accel['y'], 2) + math.pow(accel['z'], 2)))*(180.0 / 3.14)
        
        Iy = math.atan(accel['y'] / math.sqrt(math.pow(accel['x'], 2) + math.pow(accel['z'], 2)))*(180.0 / 3.14)
        
        print("Inclix:{}, Incliy:{}".format(Ix, Iy))
    