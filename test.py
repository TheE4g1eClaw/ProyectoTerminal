import wiringpi
import RPi.GPIO as GPIO
from time import sleep

wiringpi.wiringPiSetupGpio()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
wiringpi.pinMode(20, 1)
GPIO.setup(20, GPIO.OUT)
pwm = GPIO.PWM(20, 100)
pwm.start(50)


while (True):
    x=0
    #wiringpi.digitalWrite(21, 1)
    #sleep(1)
    #wiringpi.digitalWrite(21, 0)
    #sleep(1)
    #wiringpi.analogWrite(18 , 255)
