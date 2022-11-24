
from time import sleep, time
import RPi.GPIO as gpio
import signal
from threading import Thread
import socket
import json

from control import MyController

#Pines (Deacuerdo a GPIO) #Pin fisico
def salir(signum, frame):
    gpio.cleanup()
    exit()
    
def detect(canal):
    global timer
    global contador
    if timer == False:
        signal.alarm(1)
        contador = 1
        timer = True
    else:
        contador = contador +1
        
def detectEcho(canal):
    global timeUP, estado, tiempoInicio
    if not timeUp:
        if gpio.input(canal) == gpio.HIGH:
            estado["distancia"] = tiempoInicio - time()
        else:
            tiempoInicio = time()
    
def temporizadorVelocidad(tiempo):
    global contador, estado
    while True:
        estado["velocidad"] = contador
        contador = 0
        sleep(tiempo)
        
def temporizadorDistancia(tiempoMax, capturasXseg):
    global estado, timeUp
    tiempoEspera = (1/capturasXseg) - tiempoMax
    gpio.output(ULTR_S_TRIG, gpio.HIGH)
    sleep(0.00001)
    gpio.output(ULTR_S_TRIG, gpio.LOW)
    sleep(tiempoMax)
    timeUp = True
    sleep(tiempoEspera)
    
def temporizadorInfo(tiempo, IP, PORT):
    global estado
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = json.dumps(estado)
                conn.sendall(data)
                sleep(tiempo)
        
 
signal.signal(signal.SIGINT, salir)

""" Declaración de pines """
# Motores
FORW_D = 11
BACKW_D =13
FORW_I = 10
BACKW_I = 8

PWM_D = 15
PWM_I = 12

# Ultrasonico
ULTR_S_TRIG = 16
ULTR_S_ECHO = 18

# Infrarojos de ruedas
sensorI = 3
sensorD = 5

# Declarión del diccionario de estado
estado = {
    "velocidad": 0,
    "distancia": 0,
    "sensores": [0,0,0,0,0,0],
    "angulo": 0
}

gpio.setmode(gpio.BOARD)
gpio.setup(FORW_I, gpio.OUT)    
gpio.setup(BACKW_I, gpio.OUT)   
gpio.setup(FORW_D, gpio.OUT) 
gpio.setup(BACKW_D, gpio.OUT)   
gpio.setup(PWM_I, gpio.OUT)      
gpio.setup(PWM_D, gpio.OUT)

gpio.setup(sensorI, gpio.IN)

PWM_I = gpio.PWM(PWM_I, 100)
PWM_D = gpio.PWM(PWM_D, 100)
PWM_D.start(0)
PWM_I.start(0)

timer = False
contador = 0
timeUp = False
tiempoInicio = time()

def main():
    controller = MyController(BACKW_D, BACKW_I, FORW_D, FORW_I, PWM_D, PWM_I, interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()

gpio.add_event_detect(sensorI, gpio.RISING, callback=detect)
gpio.add_event_detect(ULTR_S_ECHO, gpio.BOTH, callback=detect)

if __name__== "__main__":
    main()
    capturaVelocidad = Thread(target=temporizadorVelocidad, args=(1))
    enviarPulso = Thread(target=temporizadorDistancia, args=(0.1, 10))
    enviarEstado = Thread(target=temporizadorInfo, args=(1, "0.0.0.0", 65432))
    
    capturaVelocidad.start()
    enviarPulso.start()
    enviarEstado.start()