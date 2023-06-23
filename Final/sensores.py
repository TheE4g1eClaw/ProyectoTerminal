from threading import Thread
import RPi.GPIO as gpio
from time import sleep, time
import json

class Sensores():
    def __init__(self, frecuencia, pines:dict, pwm:gpio.PWM):
        self.__estado = {
            "velocidad": 0,
            "distancia": 0,
            "sensores": [0,0,0,0,0,0],
            "angulo": frecuencia - 1
        }
        self.__frecuencia = frecuencia
        self.__tick = 1 / self.__frecuencia
        self.__continue = True
        self.__contador = [0, 0]
        self.__timeUp = False
        self.__tiempoInicio = time()
        
        self.__capturaVelocidad = Thread(target=self.__temporizadorVelocidad, args=[1])
        self.__enviarPulso = Thread(target=self.__temporizadorDistancia, args=[0.02353, 10])
        self.__enviarInfo = Thread(target=self.__temporizadorInfo, args=[self.__tick])
        self.pines = pines
        self.pwm = pwm
        self.pwm.start(0)
    
    
    def iniciar(self):
        gpio.add_event_detect(self.pines["IR_I"], gpio.RISING, callback=self.__detectIR)
        gpio.add_event_detect(self.pines["IR_D"], gpio.RISING, callback=self.__detectIR)
        gpio.add_event_detect(self.pines["ECHO"], gpio.BOTH, callback=self.__detectEcho)
        gpio.add_event_detect(self.pines["IR_1"], gpio.BOTH, callback=self.__detectAvoid)
        self.__capturaVelocidad.start()
        self.__enviarPulso.start()
        self.__enviarInfo.start()
        self.pwm.ChangeDutyCycle(7.2)
        
    def nHandler(self, handler):
        self.__handler = handler
        
    def __handler(self, estado):
        pass
        
    def parar(self):
        self.__continue = False
        gpio.remove_event_detect(self.pines["IR_I"])
        gpio.remove_event_detect(self.pines["IR_D"])
        gpio.remove_event_detect(self.pines["ECHO"])
        self.pwm.ChangeDutyCycle(0)
    
    def __detectIR(self, canal):
        #global contador
        if canal == self.pines["IR_I"]:
            self.__contador[0] += 1
        else:
            self.__contador[1] += 1
        
    def __detectEcho(self, canal):
        #global timeUP, estado, tiempoInicio
        if not self.__timeUp:
            if gpio.input(canal) == gpio.LOW:
                tiempo = time() - self.__tiempoInicio 
                self.__estado["distancia"] = (tiempo * 340) / 0.02
                if self.__estado["distancia"] > 300:
                    self.__estado["distancia"] = -1
            else:
                self.__tiempoInicio = time()
        else:
            self.__estado["distancia"] = -1
            
    def __detectAvoid(self, canal):
        #global timeUP, estado, tiempoInicio
        self.__estado["sensores"][0] = gpio.input(canal)
            
    def __temporizadorVelocidad(self, tiempo):
        #global contador, estado
        while self.__continue:
            contador = max(self.__contador)
            self.__estado["velocidad"] = round(contador / 17, 2)
            self.__contador = [0, 0]
            sleep(tiempo)

    def __temporizadorDistancia(self, tiempoMax, capturasXseg):
        #global estado, timeUp
        while self.__continue:
            self.__timeUp = False
            tiempoEspera = (1/capturasXseg) - tiempoMax
            gpio.output(self.pines["TRIG"], gpio.HIGH)
            sleep(0.0001)
            gpio.output(self.pines["TRIG"], gpio.LOW)
            sleep(tiempoMax)
            self.__timeUp = True
            sleep(tiempoEspera)
            self.__handler(self.__estado)
            self.__estado["angulo"] = (self.__estado["angulo"] + 1) % self.__frecuencia
            
    def __temporizadorInfo(self, tiempo):
        #global estado
        while self.__continue:
            self.__handler(self.__estado)
            sleep(tiempo)
                
    def getEstado(self):
        return self.__estado