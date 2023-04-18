#importar dependencias necesarias para ejecutar qt
import sys # libreria que habilita funcionaliades del sistema
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import  uic
from PyQt5 import QtCore, QtGui
#from PyQt5.Qt import Qt#CA
#modulos asociados al serial
import serial #dwddl
import serial.tools.list_ports as list_ports


#leer datos disponibles en el puerto, cuando los halla se genera una señal, llamda update
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
                        data = self.serial.read()
                        data = data.replace(b'\r', b'')
                        text = data.decode('iso-8859-1')
                        self.update.emit(text)
                except:
                    pass
                
#creacion de la clase principalll
class laberinto(QMainWindow):#herencia
    def __init__(self):
        super().__init__()#(laberinto, self).__init__()
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
            
        #se crea el hilo
        self.thread = QtCore.QThread()

        self.readPort = ReadPort(self.serial)
        
        self.readPort.moveToThread(self.thread)#se entrega el metodo readport a el hilo principal
        self.thread.started.connect(self.readPort.run)
        self.readPort.update.connect(self.updateText)
        
        # Connect signals - slots
        #eventos asociados a una funcion, llevan nombre del boton  y la funcion a ejecutar
        #self.ui.max.clicked.connect(self.click_max)
        self.ui.max.clicked.connect(self.click_max('d'))
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
        
#metodos llamados como eventos al presionar los botones  
    def click_enviar(self, letraEnviar):
        self.letraEnviada = letraEnviar
        if self.letraEnviada == self.letraPrevia:
            pass
        else:
            serial.write(b'd')
        self.letraPrevia = self.letraEnviada
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
            self.ui.sendButton.setEnabled(True)
            self.ui.connectButton.setText('Disconnect')
            self.ui.inputEdit.setEnabled(True)
        else:
            self.thread.quit()
            self.serial.close()
            # self.readTimer.stop()
            self.ui.sendButton.setEnabled(False)
            self.ui.connectButton.setText('Connect')
            self.ui.inputEdit.setEnabled(False)
        
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
