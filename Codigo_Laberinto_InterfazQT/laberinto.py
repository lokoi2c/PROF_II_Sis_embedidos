#importar dependencias necesarias para ejecutar qt
import sys, json # libreria que habilita funcionaliades del sistema
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import  uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
#modulos asociados al serial
import serial #dwddl
import serial.tools.list_ports as list_ports
from time import sleep

import cv2

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
                        data = self.serial.readline()
                        data = data.replace(b'\r', b'')
                        data = data.replace(b'\n', b'')
                        text = data.decode('iso-8859-1')
                        self.update.emit(text.split(','))
                except:
                    pass
                

class camaraInterfaz(QtCore.QObject):#QtCore.QObject
    def __init__(self, camLabel):#constructor
        super().__init__()
        #objeto de la camara
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.camLabel = camLabel
        self.pixmap = QPixmap()  
        self.activarCamara = True       
        #self.show()
        
#Metodo para actualizar la imagen de la camara
    def updateCamera(self):
        while True:
            if self.activarCamara == True:
                if self.cam.isOpened():
                    ret, frame = self.cam.read()
                    magenHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                    if not ret:#si no se tomo captura de imagen, retorne
                        return
                #convierte la imagen capturada con openCV a Qt
                #imagen, anccho, alto, ancho*numerobits por pixel, formato de imagen
                image = QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1]*frame.shape[2], QImage.Format_RGB888)
                
                self.pixmap.convertFromImage(image.rgbSwapped())
                self.camLabel.setPixmap(self.pixmap) # se muestra la imagen en la labelCam
            sleep(0.03)
        
    def enableCamera(self, state):
        if state == Qt.Checked:
            self.activarCamara = True
            
        else:
            self.pixmap.fill(Qt.transparent)
            self.camLabel.setPixmap(self.pixmap)
            self.activarCamara = False
            
            
                
#creacion de la CLASE PRINCIPAL ----------------------------------
class laberinto(QMainWindow):#herencia
    def __init__(self):
        super().__init__()#(laberinto, self).__init__() inputEdit
        self.ui = uic.loadUi('interfaz_qt.ui', self)#cargar la interfaz grafica
        
        self.serial = serial.Serial(timeout=0)# (puerto, velocidad) objeto tipo serial
        # Fill list with Baudrates 
        for baud in self.serial.BAUDRATES:
            self.ui.baudOptions.addItem(str(baud))

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
        self.thread = QtCore.QThread()
        self.hiloCamara = QtCore.QThread()

        #objetod de las clases que funcionan con hilos
        self.readPort = ReadPort(self.serial)
        self.camara = camaraInterfaz(self.ui.camLabel)
        
        #se entrega el metodo readport a el hilo principal
        self.readPort.moveToThread(self.thread)
        self.camara.moveToThread(self.hiloCamara)
        
        #se inicializan los hilos
        self.thread.started.connect(self.readPort.run)
        self.hiloCamara.started.connect(self.camara.updateCamera)
        
        self.readPort.update.connect(self.updateText)
        
        # Connect signals - slots
        #eventos asociados a una funcion, llevan nombre del boton  y la funcion a ejecutar
        #self.ui.max.clicked.connect(self.click_max)
        self.ui.max.clicked.connect(self.click_max)
        self.ui.mex.clicked.connect(self.click_mex)#
        self.ui.may.clicked.connect(self.click_may)#otro cambio
        self.modo.stateChanged.connect(self.cambio_modo)#si es  activado cambia el modo de juego
        self.ui.mey.clicked.connect(self.click_mey)#ojala sirva
        self.ui.centro.clicked.connect(self.click_centrar)
        #self.ui.ADusb.clicked.connect(self.click_AcDeUSB) #ADusb traduccion:ActivarDesactivar_usb
        
        self.ui.connectButton.clicked.connect(self.connect) # Clicked connect button -> self.connect
        self.ui.baudOptions.currentIndexChanged.connect(self.changeBaud)# Current index changed -> self.changeBaud
        self.ui.refreshButton.clicked.connect(self.refresh)#activa el puerto seleccionado, en caso de no haberse conectado
        
       
       # self.AcDe = True
        
        self.letraEnviada = 'e'
        self.letraPrevia = 'e'
        
        #Items relacionados con la camara ---------------------------
    
        self.ui.enableCam.stateChanged.connect(self.probar)#si es  activado el checkBox llama la funcion enableCamera
        self.hiloCamara.start()
        
#el error encontrado es llamar una funcion externa a la presente clase-------------------------------------------------------------
        
#metodos llamados como eventos al presionar los botones  
    def probar(self, state):
        self.camara.enableCamera(state)

    def click_max(self):
        self.letraEnviada = 'd'
        if self.letraEnviada == self.letraPrevia:
            pass
        else:
            serial.write(b'd')
        self.letraPrevia = self.letraEnviada
            
    def click_mex(self):
        self.letraEnviada = 'a'
        if self.letraEnviada == self.letraPrevia:
            pass#cambio
        else:
            serial.write(b'a')
        self.letraPrevia = self.letraEnviada
        
    def click_may(self):
        self.letraEnviada = 'w'
        if self.letraEnviada == self.letraPrevia:
            pass
        else:
            serial.write(b'w')
        self.letraPrevia = self.letraEnviada
        
    def click_mey(self):
        self.letraEnviada = 's'
        if self.letraEnviada == self.letraPrevia:
            pass
        else:
            serial.write(b's')
        self.letraPrevia = self.letraEnviada
        
    def click_centrar(self):
        self.letraEnviada = 'e'
        if self.letraEnviada == self.letraPrevia:
            pass
        else:
            serial.write(b'e')
        self.letraPrevia = self.letraEnviada
    
    def cambio_modo(self):
        self.letraEnviada = 'm' #falta modificar este
        if self.letraEnviada == self.letraPrevia:
            pass
        else:
            serial.write(b'm')
        self.letraPrevia = self.letraEnviada

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
            self.thread.start()
            #self.ui.sendButton.setEnabled(True)
            self.ui.connectButton.setText('Disconnect')
            #self.ui.inputEdit.setEnabled(True)
        else:
            self.thread.quit()
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

    def updateText(self, text):
        self.ui.accelX.setText(text)
        #self.ui.textEdit.moveCursor(QtGui.QTextCursor.End)
        
    def __del__(self):
        if self.serial.is_open:
            self.serial.close()
    
    
#if que ejecuta, principal   
if __name__ == "__main__":
    app = QApplication(sys.argv)
    laberin = laberinto()
    laberin.show()
    sys.exit(app.exec())
    
    ##lo que falta es la creacion de los hilos sjlbjnaeroibnaroijn
