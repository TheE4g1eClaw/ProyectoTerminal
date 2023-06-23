from carro import Carro
import socketio
import RPi.GPIO as gpio

class ControlSIO():
    def __init__(self, conexion: socketio.Client, cliente:Carro):
        self.conexion = conexion
        self.FORW_I = cliente.FORW_I
        self.BACK_I = cliente.BACK_I
        self.FORW_D = cliente.FORW_D
        self.BACK_D = cliente.BACK_D
        self.PWM = {
            "I": cliente.PWM["I"],
            "D": cliente.PWM["D"]
        }
        
        @self.conexion.on("control")
        def instruccion(data):
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
        gpio.output(self.FORW_I, gpio.LOW)
        gpio.output(self.BACK_I, gpio.LOW)
        gpio.output(self.FORW_D, gpio.HIGH)
        gpio.output(self.BACK_D, gpio.LOW)
        self.PWM["I"].ChangeDutyCycle(0)
        self.PWM["D"].ChangeDutyCycle(100)
    
    def __derecha(self):
        gpio.output(self.FORW_I, gpio.HIGH)
        gpio.output(self.BACK_I, gpio.LOW)
        gpio.output(self.FORW_D, gpio.LOW)
        gpio.output(self.BACK_D, gpio.LOW)
        self.PWM["I"].ChangeDutyCycle(100)
        self.PWM["D"].ChangeDutyCycle(0)
        