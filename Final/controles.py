from carro import Carro
import socketio
import RPi.GPIO as gpio

class ControlSIO(Carro):
    def __init__(self, conexion: socketio.Client):
        self.coneccion = conexion
        
        @self.conexion.on("/instruccion")
        def instruccion(self, data):
            if data == 0:
                self.parar()
            elif data == 1:
                self.__adelante()
            elif data == 2:
                self.__reversa()
            elif data == 3:
                self.__izquierda()
            elif data == 4:
                self.__derecha()
                
    def __adelante(self):
        gpio.output(self.FORW_I, gpio.HIGH)
        gpio.output(self.BACK_I, gpio.LOW)
        gpio.output(self.FORW_D, gpio.HIGH)
        gpio.output(self.BACK_D, gpio.LOW)
        self.PWM["I"].ChangeDutyCycle(100)
        self.PWM["D"].ChangeDutyCycle(100)
        
    
    def __reversa(self):
        gpio.output(self.FORW_I, gpio.LOW)
        gpio.output(self.BACK_I, gpio.HIGH)
        gpio.output(self.FORW_D, gpio.LOW)
        gpio.output(self.BACK_D, gpio.HIGH)
        self.PWM["I"].ChangeDutyCycle(100)
        self.PWM["D"].ChangeDutyCycle(100)
    
    def parar(self):
        self.PWM["I"].ChangeDutyCycle(0)
        self.PWM["D"].ChangeDutyCycle(0)
    
    def __izquierda(self):
        gpio.output(self.FORW_I, gpio.HIGH)
        gpio.output(self.BACK_I, gpio.LOW)
        gpio.output(self.FORW_D, gpio.HIGH)
        gpio.output(self.BACK_D, gpio.LOW)
        self.PWM["I"].ChangeDutyCycle(0)
        self.PWM["D"].ChangeDutyCycle(100)
    
    def __derecha(self):
        gpio.output(self.FORW_I, gpio.HIGH)
        gpio.output(self.BACK_I, gpio.LOW)
        gpio.output(self.FORW_D, gpio.HIGH)
        gpio.output(self.BACK_D, gpio.LOW)
        self.PWM["I"].ChangeDutyCycle(100)
        self.PWM["D"].ChangeDutyCycle(100)
        