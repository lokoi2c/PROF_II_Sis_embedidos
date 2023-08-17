import servo
from time import sleep

'''
for you can move the maze, you might send codes at this class. 
Codes:
valorx or valory:   201 Move maze +x or +y
                    49 Move maze -x or -y
'''

class Motor:
    def __init__(self, pinmx, pinmy, sensibilidad=1, retraso_ms=80):
        self.pinmx = pinmx
        self.pinmy  = pinmy
        self.sensibilidad = sensibilidad
        self.retraso = retraso_ms/1000
        self.servoy = servo.Servo(self.pinmy)
        self.servox = servo.Servo(self.pinmx)
        self.equilibriox = 129
        self.equilibrioy = 118
        self.maximaaperturagrados = 20
        self.servox.write(self.equilibriox)
        self.servoy.write(self.equilibrioy)
        self.gradosx = self.equilibriox
        self.gradosy = self.equilibrioy
        
    def MoverLaberintoX(self, valorX):
        valorX = int(valorX)
        
        if valorX > 200:
            self.gradosx += self.sensibilidad
            if self.gradosx > (self.equilibriox + (self.maximaaperturagrados//2)):
                self.gradosx = self.equilibriox + (self.maximaaperturagrados//2)
            
        elif valorX < 50:
            self.gradosx -= self.sensibilidad
            if self.gradosx < (self.equilibriox - (self.maximaaperturagrados//2)):
                self.gradosx = self.equilibriox - (self.maximaaperturagrados//2)
                
        '''else:
            if self.gradosy < self.equilibrioy:#este if hace que el laberinto vaya a su punto de requilibrio de una forma amortiguada,
                for grad in range(self.gradosy, self.equilibrioy + 1, self.sensibilidad):#inicio, fin, paso
                    self.servoy.write(grad)
                    sleep(self.retraso)
                self.gradosy =self.equilibrioy
                
            else:#este if hace que el laberinto vaya a su punto de requilibrio de una forma amortiguada,
                self.gradosy > self.equilibrioy
                for grad in range(self.gradosy, self.equilibrioy - 1, -self.sensibilidad):#inicio, fin, paso
                    self.servoy.write(grad)
                    sleep(self.retraso)
                self.gradosy =self.equilibrioy
        #print(f'grados en x {self.gradosx}')'''
        self.servoy.write(self.gradosy)#finalmente escribo al servo
        
        
    def MoverLaberintoY(self, valorY):
        valorY = int(valorY)
        if valorY > 200:
            self.gradosy += self.sensibilidad
            if self.gradosy > (self.equilibrioy + (self.maximaaperturagrados//2)):
                self.gradosy = self.equilibrioy + (self.maximaaperturagrados//2)
            
        elif valorY < 50:
            self.gradosy -= self.sensibilidad
            if self.gradosy < (self.equilibrioy - (self.maximaaperturagrados//2)):
                self.gradosy = self.equilibrioy - (self.maximaaperturagrados//2)
                
        '''else:
            #self.gradosy =117
            if self.gradosx < self.equilibriox:#este if hace que el laberinto vaya a su punto de requilibrio de una forma amortiguada,
                for grad in range(self.gradosx, self.equilibriox + 1, self.sensibilidad):#inicio, fin, paso
                    self.servox.write(grad)
                    sleep(self.retraso)
                self.gradosx =self.equilibriox
                
            else:#este if hace que el laberinto vaya a su punto de requilibrio de una forma amortiguada,
                self.gradosx > self.equilibriox
                for grad in range(self.gradosx, self.equilibriox - 1, -self.sensibilidad):#inicio, fin, paso
                    self.servox.write(grad)
                    sleep(self.retraso)
                self.gradosx =self.equilibriox
        #print(f'grados en Y {self.gradosy}')'''
        self.servox.write(self.gradosx)#finalmente escribo al servo
                

'''if __name__ == "__main__":
    laberinto = Motor(15,18,1,80)


    while True:
        
        for i in range(0, 180, 1):
            laberinto.MoverLaberintoY("201")
            sleep(.05)
            print("+X")
            
        for i in range(180, 0, -1):
            laberinto.MoverLaberintoY(45)
            sleep(.05)
            print("-X")
            
        for i in range(180, 0, -1):
            laberinto.MoverLaberintoY(112)
            sleep(.05)
            print('CENTROim')'''