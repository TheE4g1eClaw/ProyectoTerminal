import RPi.GPIO as gpio
import signal

sensorI = 8
gpio.setmode(gpio.BOARD)

gpio.setup(sensorI, gpio.IN)

timer = False
contador = 0

def temporizador(signum, frame):
    global contador
    global timer
    print(contador)
    contador = 0
    timer = False

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
        

        
signal.signal(signal.SIGINT, salir)
signal.signal(signal.SIGALRM, temporizador)
gpio.add_event_detect(sensorI, gpio.RISING, callback=detect)
