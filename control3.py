from pyPS4Controller.controller import Controller
from time import sleep
import RPi.GPIO as gpio
import signal

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
    
def temporizador(signum, frame):
    global contador
    global timer
    print(contador)
    contador = 0
    timer = False
 
signal.signal(signal.SIGINT, salir)

FORW_D = 11
BACKW_D =13
FORW_I = 10
BACKW_I = 8

PWM_D = 15
PWM_I = 12

#sensores
sensorI = 3

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

def adelanteI():
    gpio.output(BACKW_I, gpio.LOW)
    gpio.output(FORW_I, gpio.HIGH)

def adelanteD():
    gpio.output(BACKW_D, gpio.LOW)
    gpio.output(FORW_D, gpio.HIGH)

def atrasI():
    gpio.output(FORW_I, gpio.LOW)
    gpio.output(BACKW_I, gpio.HIGH)

def atrasD():
    gpio.output(FORW_D, gpio.LOW)
    gpio.output(BACKW_D, gpio.HIGH)

class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    
    def on_R2_press(self, value):
        #print((value / 655.34) + 50)
        PWM_D.ChangeDutyCycle((value / 655.34) + 50)

    def on_L2_press(self, value):
        #print((value / 655.34) + 50)
        PWM_I.ChangeDutyCycle((value / 655.34) + 50)

    def on_R2_release(self):
        PWM_D.ChangeDutyCycle(0)

    def on_L2_release(self):
        PWM_I.ChangeDutyCycle(0)

    def on_square_press(self):
        atrasD()
        atrasI()

    def on_square_release(self):
        adelanteD()
        adelanteI()

def main():
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()

signal.signal(signal.SIGALRM, temporizador)
gpio.add_event_detect(sensorI, gpio.RISING, callback=detect)

if __name__== "__main__":
    main()
