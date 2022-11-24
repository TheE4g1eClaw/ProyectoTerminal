from pyPS4Controller.controller import Controller
import RPi.GPIO as gpio

class MyController(Controller):
    def __init__(self, BACK_D, BACK_I, FORW_D, FORW_I, PWM_D, PWM_I, **kwargs):
        Controller.__init__(self, **kwargs)
        self.BACKW_D = BACK_D
        self.BACKW_I = BACK_I
        self.FORW_D = FORW_D
        self.FORW_I = FORW_I
        self.PWM_D = PWM_D
        self.PWM_I = PWM_I
    
    def adelanteI(self):
        gpio.output(self.BACKW_I, gpio.LOW)
        gpio.output(self.FORW_I, gpio.HIGH)

    def adelanteD(self):
        gpio.output(self.BACKW_D, gpio.LOW)
        gpio.output(self.FORW_D, gpio.HIGH)

    def atrasI(self):
        gpio.output(self.FORW_I, gpio.LOW)
        gpio.output(self.BACKW_I, gpio.HIGH)

    def atrasD(self):
        gpio.output(self.FORW_D, gpio.LOW)
        gpio.output(self.BACKW_D, gpio.HIGH)
    
    def on_R2_press(self, value):
        #print((value / 655.34) + 50)
        self.PWM_D.ChangeDutyCycle((value / 655.34) + 50)

    def on_L2_press(self, value):
        #print((value / 655.34) + 50)
        self.PWM_I.ChangeDutyCycle((value / 655.34) + 50)

    def on_R2_release(self):
        self.PWM_D.ChangeDutyCycle(0)

    def on_L2_release(self):
        self.PWM_I.ChangeDutyCycle(0)

    def on_square_press(self):
        self.atrasD()
        self.atrasI()

    def on_square_release(self):
        self.adelanteD()
        self.adelanteI()