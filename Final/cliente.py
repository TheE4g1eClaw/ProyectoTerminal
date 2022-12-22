from carro import Carro
import socketio
from controles import ControlSIO
from sensores import Sensores

import io
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

from libcamera import Transform

import socketio

pines = {
    "FORW_D": 11,
    "BACK_D": 13,
    "FORW_I": 10,
    "BACK_I": 8,
    "PWM_D": 15,
    "PWM_I": 12,
    "PWM_US": 16,
    "TRIG": 18,
    "ECHO": 22,
    "IR_I": 29,
    "IR_D": 31,
    #"IR_1": 33,
    #"IR_2": 35,
    #"IR_3": 37,
    #"IR_4": 40
}
servidor = "http://localhost:5000"
    
cliente = Carro(pines)
cliente.fin()
sio = socketio.Client()
sio.connect(servidor)

print("Llego hasta aqui")
controles = ControlSIO(cliente, sio)
sensores =  Sensores(cliente, sio)

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()
            

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}, transform=Transform(vflip=True)))
picam2.set_controls({"FrameRate": 5.0})
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

@sio.on("disconnect")
def desconectar():
    picam2.stop_recording()
    controles.parar()
    sensores.parar()
    
@sio.on("/")
def desconectar():
    picam2.start_recording()
    sensores.iniciar()
    

try:
    while True:
        with output.condition:
            output.condition.wait()
            sio.emit('frame', output.frame)
finally:
    picam2.stop_recording()
    controles.parar()
    sensores.parar()
    controles.fin()