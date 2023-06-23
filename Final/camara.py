from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

from libcamera import Transform

import socketio

import io

class __Salida(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class Camara():
    def __init__(self, framerate = 5.0, resolucion = (640, 480)):
        self.__picam2 = Picamera2()
        self.__picam2.configure(self.__picam2.create_video_configuration(main={"size": resolucion}, transform=Transform(vflip=True)))
        self.__picam2.set_controls({"FrameRate": framerate})
        self.output = __Salida()
        
    def iniciar(self):
        self.__picam2.start_recording(JpegEncoder(), FileOutput(self.output))
        
    def parar(self):
        self.__picam2.stop_recording()