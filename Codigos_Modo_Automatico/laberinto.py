#importar dependencias necesarias para ejecutar qt
import sys, json # libreria que habilita funcionaliades del sistema
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import  uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtNetwork import QTcpSocket

#modulos asociados al serial
import serial #dwddl
import serial.tools.list_ports as list_ports
from time import sleep

import cv2
import numpy as np
import sys
from scipy import ndimage
import mpu5050, math
import motor

#-------------->escritorio grande raspberry 192.168.125.205:1

'''class mpulocal(QtCore.QObject):#Metodo necceario para heredar objetos de la interfaz grafica
    aceleraciones = QtCore.pyqtSignal(str)
     #funcion que ejecuta el mpu
    def __init__(self):
        super().__init__()
        self.mpu = mpu5050.MPU6050(0x68)
        self.mpu.begin()
        
    def mpu6050_run(self):
        while True:
            accel = self.mpu.getAcceleration()
            gyro = self.mpu.getRotation()
            
            # Conversión matemática a inclinación:
            
            Ix = math.atan(accel['x'] / math.sqrt(math.pow(accel['y'], 2) + math.pow(accel['z'], 2)))*(180.0 / 3.14)
            
            Iy = math.atan(accel['y'] / math.sqrt(math.pow(accel['x'], 2) + math.pow(accel['z'], 2)))*(180.0 / 3.14)
            self.aceleraciones.emit(str(Ix)) 
            sleep(1)'''


#otra prueba
#leer datos disponibles en el puerto, cuando los haya se genera una señal, llamda update
class ReadPort(QtCore.QObject):
    update = QtCore.pyqtSignal(str)
    #constructor
    def __init__(self, serial):
        super().__init__()
        self.serial = serial 

    def run(self):
        while True:
            if self.serial.is_open:
                try:
                    if self.serial.in_waiting > 0:
                        raw_string_b = self.serial.readline()
                        
                        raw_string_s = raw_string_b.decode('utf-8')
                        
                        raw_string_s = raw_string_s[0:raw_string_s.index("}")+1]
                        raw_string_j = json.loads(raw_string_s)
                        print(raw_string_j)
                        cadenaalienigena = raw_string_j["Value"]
                        self.update.emit(cadenaalienigena) #aqui esta el herror, esta en la forma de como se separa el json
                        print(raw_string_j["Value"])
                        print(raw_string_j["Value2"])
                        
                except:
                    print('error en el jason')
            
            
                
#creacion de la CLASE PRINCIPAL ----------------------------------
class laberinto(QMainWindow):#herencia
    def __init__(self):
        super().__init__()#(laberinto, self).__init__() inputEdit
        self.ui = uic.loadUi('interfaz_qt.ui', self)#cargar la interfaz grafica
        
        self.serial = serial.Serial()# (puerto, velocidad) objeto tipo serial
        # Fill list with Baudrates 
        for baud in self.serial.BAUDRATES:
            self.ui.baudOptions.addItem(str(baud))
            
        #inicializr variables del laberinto
        self.laberinto = motor.Motor(12,19,1,80)

        # Se invoca el objeto Socket: 
        self.socket = QTcpSocket()

        # Set 115200 as default
        self.baud = 115200
        self.ui.baudOptions.setCurrentIndex(self.serial.BAUDRATES.index(self.baud))

        # Get available ports
        ports = list_ports.comports()
        # if any port exists, open port 
        if ports:
            for port in ports:
                self.ui.portOptions.addItem(port.device)

            self.serial.baudrate = self.baud
            self.serial.port = self.ui.portOptions.currentText()
            self.ui.connectButton.setEnabled(True)
            
         #se crean los hilos
        #self.thread = QtCore.QThread()
       # self.hilo_mpu = QtCore.QThread()

        #objetod de las clases que funcionan con hilos
        #self.readPort = ReadPort(self.serial)
       # self.mpuclase = mpulocal()
        
        #se entrega el metodo readport a el hilo principal __init__
        #self.readPort.moveToThread(self.thread)
        #self.mpuclase.moveToThread(self.hilo_mpu)
        
        #se inicializan los hilos
        #self.thread.started.connect(self.readPort.run)
      #  self.hilo_mpu.started.connect(self.mpuclase.mpu6050_run)
        
        #self.readPort.update.connect(self.updateText)
        #self.mpuclase.aceleraciones.connect(self.escribiraceleraciones)
        
        # Connect signals - slots
        #eventos asociados a una funcion, llevan nombre del boton  y la funcion a ejecutar
        #self.ui.max.clicked.connect(self.click_max)
        self.ui.max.clicked.connect(self.click_max)
        self.ui.mex.clicked.connect(self.click_mex)#
        self.ui.may.clicked.connect(self.click_may)#otro cambio
       # self.modo.stateChanged.connect(self.cambio_modo)#si es  activado cambia el modo de juego
        self.ui.mey.clicked.connect(self.click_mey)#ojala sirva
        self.ui.centro.clicked.connect(self.click_centrar)
        #self.ui.ADusb.clicked.connect(self.click_AcDeUSB) #ADusb traduccion:ActivarDesactivar_usb
        
        self.ui.connectButton.clicked.connect(self.connect) # Clicked connect button -> self.connect
        self.ui.baudOptions.currentIndexChanged.connect(self.changeBaud)# Current index changed -> self.changeBaud
        self.ui.refreshButton.clicked.connect(self.refresh)#activa el puerto seleccionado, en caso de no haberse conectado
        
        #Socket: Al activar el Checkbox se ejecuta Camiomodo
        self.ui.modo.stateChanged.connect(self.Cambiomodo)
        self.timerCam = QTimer()
        self.timerMpu6050 = QTimer()
        
        self.timerCam.timeout.connect(self.updateCamera)
        self.timerMpu6050.timeout.connect(self.mpu6050_run)
        
        #objeto de la camara
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)#640
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)#480
        self.encontrarcaidas = True
        self.modeloFondo = []
        self.contornosPerder = []
        self.pixmap = QPixmap()
        self.enableCam.stateChanged.connect(self.enableCamera)#si es  activado el checkBox llama la funcion enableCamera
        self.show()
        
        #MPU
        self.mpu = mpu5050.MPU6050(0x68)
        self.mpu.begin()    
        self.timerMpu6050.start(1000)
    
    #-----------------------MPU----------------
    def mpu6050_run(self):
        accel = self.mpu.getAcceleration()
        # Conversión matemática a inclinación:
        
        Ix = math.atan(accel['x'] / math.sqrt(math.pow(accel['y'], 2) + math.pow(accel['z'], 2)))*(180.0 / 3.14)
        
        Iy = math.atan(accel['y'] / math.sqrt(math.pow(accel['x'], 2) + math.pow(accel['z'], 2)))*(180.0 / 3.14)
        self.ui.accelX.setText(str(round(Ix, 2)) + " m/s^2")
        self.ui.accelY.setText(str(round(Iy, 2)) + " m/s^2")
        
    #----------------------camara-----------
    def updateCamera(self):
        if self.cam.isOpened():
            ret, frame = self.cam.read()
            frameperder = frame.copy()
            
            if self.encontrarcaidas:
                self.contornosPerder = self.encontrarPerder(frame)
                self.modeloFondo = frame
                self.encontrarcaidas = False
            
            if not ret:#si no se tomo captura de imagen, retorne
                return
            
            diferencia=cv2.absdiff(frame,self.modeloFondo).astype('uint8')
            diferencia=cv2.GaussianBlur(diferencia,(11,11),0)
            diferencia=cv2.cvtColor(diferencia,cv2.COLOR_BGR2GRAY)
            umbral,_=cv2.threshold(diferencia,0,255,cv2.THRESH_OTSU)
            bina=255*np.uint8(diferencia>umbral)
            bina=255*np.uint8(ndimage.binary_fill_holes(bina))
            contours,_=cv2.findContours(bina, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            xbol = []
            ybol =[] 
            wbol = [] 
            hbol = []
            for i in contours:
                rect=cv2.boundingRect(i)
                xb,yb,wb,hb=rect
                
                
                if int(cv2.contourArea(i)>990) and int(cv2.contourArea(i)<3200):
                    aspecto = float(wb/hb)
                    if aspecto > 0.8 and aspecto < 1.4:
                        cv2.putText(frame, 'Bola', (xb,yb-5),1,1,(255,0,0),2)
                        cv2.rectangle(frame,(xb,yb),(xb+wb,yb+hb),(255,0,0),2)
                        xbol.append(xb)
                        ybol.append(yb)
                        wbol.append(wb)
                        hbol.append(hb)
            xperd = [] 
            yperd = []
            wperd = []
            hperd = []
            for c in self.contornosPerder:
                epsilon = 0.012*cv2.arcLength(c, True)
                apro = cv2.approxPolyDP(c, epsilon, True)
                #print(len(apro))
                xf,yf,wf,hf = cv2.boundingRect(apro)
            
                if cv2.contourArea(c)>1800:
                    if len(apro) > 7:
                        xperd.append(xf)
                        yperd.append(yf)
                        wperd.append(wf)
                        hperd.append(hf)
                        cv2.putText(frame, 'Perder', (xf,yf-5),1,1,(0,0,255),2)
                        cv2.rectangle(frame,(xf,yf),(xf+wf,yf+hf),(0,0,255),2)
                        cv2.drawContours(frame, [apro], 0, (0,0,255), 2) 
            rpx = 30#rangoPixeles
            '''if len(xbol) == 0 or len(ybol) == 0:
                pass
            else:
                for p in range(0, len(xperd)):
                    x_centrobola = (xbol[0] + wbol[0]/2)
                    y_centrobola = (ybol[0] + hbol[0]/2)
                    x_centrohueco = (xperd[p] + wperd[p]/2)
                    y_centrohueco = (yperd[p] + hperd[p]/2)
                    if  ((x_centrobola > x_centrohueco + rpx) or (x_centrobola < x_centrohueco - rpx)) and ((y_centrobola > y_centrohueco + rpx) or (y_centrobola < y_centrohueco - rpx)):
                        print("perdiste MTK")
                        cv2.putText(frameperder, 'Game Over Bastard', (320,240),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),2)
                        frame  = frameperder'''
        #cv2.drawContours(imgRecortadai, [apro], 0, (0,0,255), 2)   
        #convierte la imagen capturada con openCV a Qt
        #imagen, anccho, alto, ancho*numerobits por pixel, formato de imagen
        #cv2.imshow('resultado', img_masnegra)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1]*frame.shape[2], QImage.Format_RGB888)
        
        self.pixmap.convertFromImage(image.rgbSwapped())
        self.camLabel.setPixmap(self.pixmap) # se muestra la imagen en la labelCam
    
    def encontrarPerder(self, frame):#encuentra os huecos en el laberinto
        m,n,_ = frame.shape
        imgRecortadai = frame#[np.uint64(0.1*m):np.uint64(0.91*m), np.uint64(0.12*n):np.uint64(0.92*n)]# n=columnas, todas las filas, las columnas desde el >25% de estas hasta <84% np.uint64(0.25*n)
        newimg=cv2.cvtColor(imgRecortadai,cv2.COLOR_BGR2GRAY)
        h, w = newimg.shape
        img_masnegra = newimg.copy()#debo de conservar la variable, sin sobreescribir
        for p in range(0,h):
            for j in range(0, w):
                if int(newimg[p][j]) < 160:#160
                    img_masnegra[p][j]= 0#newimg[p][j]#180
                    
                elif int(newimg[p][j]) > 170:#170
                    img_masnegra[p][j]=newimg[p][j]
                    
                else:
                    img_masnegra[p][j]=newimg[p][j]
        newimg = cv2.GaussianBlur(img_masnegra, ksize=(5,5), sigmaX=0)
        newimg = cv2.GaussianBlur(img_masnegra, ksize=(5,5), sigmaX=0)

        imgcanny = cv2.Canny(newimg, 70, 180)
        imgcanny = cv2.dilate(imgcanny, None, iterations=1)
        imgcanny= cv2.erode(imgcanny, None, iterations=1)
        kernel = np.ones((5,5), np.uint8)
        bordes = cv2.dilate(imgcanny, kernel)
        contornosP,_ = cv2.findContours(bordes, mode=cv2.RETR_EXTERNAL, method= cv2.CHAIN_APPROX_SIMPLE)#Se identifican los contornos
        objetos = bordes.copy()#debo de conservar la variable, sin sobreescribir
        output = cv2.connectedComponentsWithStats(objetos,4,cv2.CV_32S)#con este metodo se hallan el numero de objetos, etiquetas , entroides 
        
          
        return contornosP
                    
    def enableCamera(self, state):
        if state == Qt.Checked:
            self.timerCam.start(30)
            
        else:
            self.pixmap.fill(Qt.transparent)
            self.camLabel.setPixmap(self.pixmap)
            self.timerCam.stop()
    
    
    
#metodos llamados como eventos al presionar los botones  
    def probar(self, state):
        self.camara.enableCamera(state)

    def click_max(self):
        self.laberinto.MoverLaberintoX(210)#el codigo 201 hace que el laberinto se mueva en +x
        '''self.letraEnviada = 'd'
        if self.letraEnviada == self.letraPrevia:
            pass
        else:
            serial.write(b'd')
        self.letraPrevia = self.letraEnviada'''
            
    def click_mex(self):
        self.laberinto.MoverLaberintoX(40)#el codigo 201 hace que el laberinto se mueva en -x
        '''self.letraEnviada = 'a'
        if self.letraEnviada == self.letraPrevia:
            pass#cambio
        else:
            serial.write(b'a')
        self.letraPrevia = self.letraEnviada'''
        
    def click_may(self):
        self.laberinto.MoverLaberintoY(40)#el codigo 201 hace que el laberinto se mueva en +y
        '''self.letraEnviada = 'w'
        if self.letraEnviada == self.letraPrevia:
            pass
        else:
            serial.write(b'w')
        self.letraPrevia = self.letraEnviada'''
        
    def click_mey(self):
        self.laberinto.MoverLaberintoY(210)#el codigo 201 hace que el laberinto se mueva en -y
        '''self.letraEnviada = 's'
        if self.letraEnviada == self.letraPrevia:
            pass
        else:
            serial.write(b's')
        self.letraPrevia = self.letraEnviada'''
        
    def click_centrar(self):
        self.laberinto.MoverLaberintoY(112)#el codigo 112 hace que el laberinto se centre
        self.laberinto.MoverLaberintoX(112)#el codigo 112 hace que el laberinto se centre
        '''self.letraEnviada = 'e'
        if self.letraEnviada == self.letraPrevia:
            pass
        else:
            serial.write(b'e')
        self.letraPrevia = self.letraEnviada'''
    
    '''def cambio_modo(self):
        self.letraEnviada = 'm' #falta modificar este
        if self.letraEnviada == self.letraPrevia:
            pass
        else:
            serial.write(b'm')
        self.letraPrevia = self.letraEnviada'''

#metodos asociados a comunicaion serial 
    '''def click_AcDeUSB(self):
        self.ui.label.setText(str(self.AcDe))
        if(self.AcDe):
            self.ui.ADusb.setText("Desactivar USB")
            self.prenderSerial()
        else:
            self.ui.ADusb.setText("Activar USB")
            self.apagarserial()
            
        self.AcDe = not self.AcDe#niego el estado de a variable activar desactivar
        #self.ui.label.setText(str(self.AcDe))#HAY UN HERROR cuando se llaman las funciones preder y apagar serial

    def prenderSerial(self):
        serial.open()
        
    def apagarserial(self):
        serial.close()'''

#Entrada por teclado      
    def keyPressEvent(self, event):
        #if int(event.key())== Qt.key_a: #este es un metodo mas sofisticado, pero implica un poco mas de trabajo
        if int(event.key())  == 65:#se preciono la a
            self.click_mex()
        elif int(event.key())  == 68:#se preciono la d
            self.click_max()
        elif int(event.key())  == 87:#se preciono la w
            self.click_may()
        elif int(event.key())  == 83:#"se preciono la s"
            self.click_mey()
        else:
            self.click_centrar()

#metodos asociaados a conectar, seleccionar puerto y cambiar baudaje
    #def clear(self):
     #   self.ui.textEdit.clear() --------------------util, es el objeto en el cual se escribira
        
    def connect(self):
        if not self.serial.is_open:
            self.serial.open()       
            # self.readTimer.start(10)
            #self.thread.start()
            #self.ui.sendButton.setEnabled(True)
            self.ui.connectButton.setText('Disconnect')
            #self.ui.inputEdit.setEnabled(True)
        else:
            #self.thread.quit()
            self.serial.close()
            # self.readTimer.stop()
            #self.ui.sendButton.setEnabled(False)
            self.ui.connectButton.setText('Connect')
            #self.ui.inputEdit.setEnabled(False)
        
    def refresh(self):  
        # Get available ports
        ports = list_ports.comports()
        
        self.ui.portOptions.clear()
        # if any port exists, open port 
        if ports:
            for port in ports:
                self.ui.portOptions.addItem(port.device)

            self.serial.baudrate = self.baud
            self.serial.port = self.ui.portOptions.currentText()
            self.ui.connectButton.setEnabled(True)
            
    def changeBaud(self, index):
        self.baud = self.ui.baudOptions.itemText(index)
        if self.serial.is_open:
            self.serial.baudrate = self.baud
            self.serial.close()
            self.serial.open()

    def updateText(self, cadenaalienigena):
        #print(raw_string_j["Value"])
        self.ui.accelX.setText(cadenaalienigena)
        #self.ui.textEdit.moveCursor(QtGui.QTextCursor.End)
        
    def __del__(self):
        if self.serial.is_open:
            self.serial.close()
    
    # - - - - - - -SOCKETS : La interfaz es el cliente - - - - - - - - -
    def Cambiomodo(self, state):
        self.socket.connectToHost('localhost', 65432)
        if state:
            self.socket.write(b'auto')
            #self.hilo_mpu.start()
            print("se envio auto")
        else:
            self.socket.write(b'manual')
            print("se envio manual")
            #self.hilo_mpu.stop() #esto no funciona :(
        
        self.socket.waitForBytesWritten()
        self.socket.disconnectFromHost()
    #metodo que activa el modo manual del laberinto cuando se cierra la interfaz
    def closeEvent(self, event):
        respuesta = QMessageBox.question(self, 'confirmacion', '¿Desea cerrar la interfaz?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if respuesta == QMessageBox.Yes:
            self.socket.write(b'manual')
        event.accept()#se cierra definitivamnete la ventana
        
        
#if que ejecuta, principal   
if __name__ == "__main__":
    app = QApplication(sys.argv)
    laberin = laberinto()
    laberin.show()
    sys.exit(app.exec())
    
    ##lo que falta es la creacion de los hilos sjlbjnaeroibnaroijn
