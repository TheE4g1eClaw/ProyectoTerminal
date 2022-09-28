from time import sleep
import RPi.GPIO as gpio
import signal

#Pines (Deacuerdo a GPIO) #Pin fisico
FORW_I = 3
BACKW_I = 5
FORW_D = 8
BACKW_D = 10

PWM_I = 7 #26
PWM_D = 12 #22

def salir(signum, frame):
    gpio.cleanup()
 
signal.signal(signal.SIGINT, salir)

def main():
    setup()
    adelante()
    for i in range(200):
        setVelocidad(i/2)
        sleep(0.5)

def setup():
    gpio.setmode(gpio.BOARD)    #Se configuran los pines deacuerdo a la distribucion fisica
    gpio.setup(FORW_I, gpio.OUT)       # Set pin 12 a 1 ( OUTPUT ) #Latch
    gpio.setup(BACKW_I, gpio.OUT)       # Set pin 16 a 1 ( OUTPUT ) #Data
    gpio.setup(FORW_D, gpio.OUT)       # Set pin 18 a 1 ( OUTPUT ) #Enable
    gpio.setup(BACKW_D, gpio.OUT)       # Set pin 22 a 1 ( OUTPUT ) #PWM M3
    gpio.setup(PWM_I, gpio.OUT)       # Set pin 24 a 1 ( OUTPUT )  #Clock
    gpio.setup(PWM_D, gpio.OUT)       # Set pin 26 a 1 ( OUTPUT )  #PWM M2
    PWM_I = gpio.PWM(PWM_I, 100)
    PWM_D = gpio.PWM(PWM_D, 100)

def adelante():
    gpio.output(BACKW_I, gpio.LOW)
    gpio.output(BACKW_D, gpio.LOW)
    gpio.output(FORW_I, gpio.HIGH)
    gpio.output(FORW_D, gpio.HIGH)
    
def atras():
    gpio.output(FORW_I, gpio.LOW)
    gpio.output(FORW_D, gpio.LOW)
    gpio.output(BACKW_I, gpio.HIGH)
    gpio.output(BACKW_D, gpio.HIGH)

def parar():
    gpio.output(FORW_I, gpio.LOW)
    gpio.output(FORW_D, gpio.LOW)
    gpio.output(BACKW_I, gpio.LOW)
    gpio.output(BACKW_D, gpio.LOW)

def setVelocidad(dc : int):
    PWM_I.ChangeDutyCycle(dc)
    PWM_D.ChangeDutyCycle(dc)

if __name__== "__main__":
    main()
