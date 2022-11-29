# Test sonar con ultrasonico
import RPi.GPIO as gpio
from time import sleep, time

#Pines (Deacuerdo a GPIO) #Pin fisico

TRIG = 23
ECHO = 24

PWM = 18

INFRAROJO = 17

gpio.setmode(gpio.BCM)
gpio.setup(TRIG, gpio.OUT)
gpio.setup(ECHO, gpio.IN)
gpio.setup(PWM, gpio.OUT)
gpio.setup(INFRAROJO, gpio.IN)

def conteo(canal):
    global contador
    contador = contador + 1
    
def detectEcho(canal):
    global timeUP, tiempoInicio, distancias, pos
    if not timeUp:
        if gpio.input(canal) == gpio.HIGH:
            distancias[pos] = tiempoInicio - time()	
        else:
            tiempoInicio = time()
            



#variables gobales
contador = 0
velocidad = 0 #en rpm
nDientes = 17
timeUp = False
nCapturas = 10
distancias = [0 for x in range(nCapturas)]
tiempoInicio = time()
tiempoMax = 0.0002
pos = 0

if __name__ == "__main__":
    # configuramos el pwm a 1 rpm
    # con variacion de busqueda binaria
    pwm = gpio.PWM(PWM, 1000)
    pwm.start(0)
    pwmListo = False
    rangos = [0, 50 ,100]
    gpio.add_event_detect(TRIG, gpio.RISING, callback=conteo)
    while not pwmListo:
        pwm.ChangeDutyCycle(rangos[1])
        sleep(0.5)
        contador = 0
        sleep(1)
        velocidad = contador / nDientes
        if velocidad == 1:
            pwmListo = True
        elif velocidad > 1:
            rangos[2] = rangos[1]
            rangos[1] = (rangos[1] + rangos[0]) / 2
        else:
            rangos[0] = rangos[1]
            rangos[1] = (rangos[1] + rangos[2]) / 2
    print("PWM listo con trabajo de ", rangos[1])
    tiempoEspera = (1/nCapturas) - tiempoMax
    while True:
        gpio.output(TRIG, gpio.HIGH)
        sleep(0.00001)
        gpio.output(ECHO, gpio.LOW)
        sleep(tiempoMax)
        timeUp = True
        sleep(tiempoEspera)
        pos = pos + 1 % nCapturas
        if pos == 0:
          print("Las distancias son: ", distancias)
