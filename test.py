import RPi.GPIO as GPI

GPIO.setmode(GPIO.BCM)
wiringpi.pinMode(20, 1)
GPIO.setup(20, GPIO.OUT)
pwm = GPIO.PWM(20, 100)
pwm.start(50)
