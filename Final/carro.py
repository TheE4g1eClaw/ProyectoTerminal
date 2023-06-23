import RPi.GPIO as gpio
from sensores import Sensores

class Carro:
    def __init__(self, pines: dict, frecuencia: int = 1):
        # Pines para el sentido de las llantas
        self.FORW_I = pines["FORW_I"]
        self.BACK_I = pines["BACK_I"]
        self.FORW_D = pines["FORW_D"]
        self.BACK_D = pines["BACK_D"]
        
        # Pines para la velocidad de la llantas
        self.PWM_I = pines["PWM_I"]
        self.PWM_D = pines["PWM_D"]
        
        # Pin para el motor del sonar
        self.PWM_US = pines["PWM_US"]
        
        # Pines para el control de sensor ultrasonico
        self.TRIG = pines["TRIG"]
        self.ECHO = pines["ECHO"]
        
        #pines para medir la velocidad
        self.IR_I = pines["IR_I"]
        self.IR_D = pines["IR_D"]
        
        self.IR_1 = pines["IR_1"]
        """# sensores de linea
        self.IR_2 = pines[IR_2]
        self.IR_3 = pines[IR_3]
        self.IR_4 = pines[IR_4]
        """
        
        # PWM para motor del sensor ultrasonico
        #self.PWM_US = pines[PWM_US]
        
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.FORW_I, gpio.OUT)    
        gpio.setup(self.BACK_I, gpio.OUT)   
        gpio.setup(self.FORW_D, gpio.OUT) 
        gpio.setup(self.BACK_D, gpio.OUT)   
        gpio.setup(self.PWM_I, gpio.OUT)      
        gpio.setup(self.PWM_D, gpio.OUT)
        gpio.setup(self.PWM_US, gpio.OUT)
        gpio.setup(self.TRIG, gpio.OUT)
        gpio.setup(self.ECHO, gpio.IN)
        gpio.setup(self.IR_I, gpio.IN)
        gpio.setup(self.IR_D, gpio.IN)
        gpio.setup(self.IR_1, gpio.IN)

        self.PWM = {
            "I": gpio.PWM(self.PWM_I, 100),
            "D": gpio.PWM(self.PWM_D, 100),
            "US": gpio.PWM(self.PWM_US, 100)
        }
        for pwm in self.PWM:
            self.PWM[pwm].start(0)
            
        self.sensores = Sensores(frecuencia, pines, self.PWM["US"])
    
    def fin(self):
        gpio.cleanup()