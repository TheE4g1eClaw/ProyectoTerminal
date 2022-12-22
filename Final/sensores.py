from carro import Carro
from threading import Thread
import RPi.GPIO as gpio
from time import sleep, time
import json

class Sensores(Carro):
    def __init__(self, conexion, frecuencia):
        self.conexion = conexion
        self.__estado = {
            "velocidad": 0,
            "distancia": 0,
            "sensores": [0,0,0,0,0,0],
            "angulo": 0
        }
        self.__frecuencia = frecuencia
        self.__tick = 1 / self.__frecuencia
        self.__continue = True
        self.__contador = [0, 0]
        self.__timeUp = False
        self.__tiempoInicio = time()
        
        self.__capturaVelocidad = Thread(target=self.__temporizadorVelocidad, args=[1])
        self.__enviarPulso = Thread(target=self.__temporizadorDistancia, args=[0.02232, 10])
        self.__enviarEstado = Thread(target=self.__temporizadorInfo, args=[self.__tick])
    
    def iniciar(self):
        gpio.add_event_detect(self.IR_I, gpio.BOTH, callback=self.__detectIR)
        gpio.add_event_detect(self.IR_D, gpio.BOTH, callback=self.__detectIR)
        gpio.add_event_detect(self.ECHO, gpio.BOTH, callback=self.__detectEcho)
        self.__capturaVelocidad.start()
        self.__enviarPulso.start()
        self.__enviarEstado.start()
        
    def parar(self):
        self.__continue = False
        gpio.remove_event_detect(self.IR_I)
        gpio.remove_event_detect(self.IR_D)
        gpio.remove_event_detect(self.ECHO)
    
    def __detectIR(self, canal):
        #global contador
        if canal == self.IR_I:
            self.__contador[0] += 1
        else:
            self.__contador[1] += 1
        
    def __detectEcho(self, canal):
        #global timeUP, estado, tiempoInicio
        if not self.__timeUp:
            if gpio.input(canal) == gpio.LOW:
                tiempo = time() - self.__tiempoInicio 
                self.__estado["distancia"] = (tiempo * 340) / 0.02
            else:
                self.__tiempoInicio = time()
        else:
            self.__estado["distancia"] = "FR"
            
    def __temporizadorVelocidad(self, tiempo):
        #global contador, estado
        while self.__continue:
            contador = max(self.__contador)
            self.__estado["velocidad"] = contador / 17
            self.__contador = [0, 0]
            sleep(tiempo)

    def __temporizadorDistancia(self, tiempoMax, capturasXseg):
        #global estado, timeUp
        while self.__continue:
            self.__timeUp = False
            tiempoEspera = (1/capturasXseg) - tiempoMax
            gpio.output(self.TRIG, gpio.HIGH)
            sleep(0.0001)
            gpio.output(self.TRIG, gpio.LOW)
            sleep(tiempoMax)
            self.__timeUp = True
            sleep(tiempoEspera)
            
    def __temporizadorInfo(self, tiempo):
        #global estado
        while self.__continue:
                data = json.dumps(self.__estado)
                self.conexion.emit(data)
                sleep(tiempo)