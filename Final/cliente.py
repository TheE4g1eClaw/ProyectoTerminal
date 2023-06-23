from carro import Carro
import socketio
from controles import ControlSIO
from sensores import Sensores
from camara import Camara

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
    "IR_1": 40,
    "IR_2": 35,
    "IR_3": 37,
    "IR_4": 40
    "IR_5": 38
    "IR_6": 36
}
servidor = "http://172.30.5.71:6660"
    
cliente = Carro(pines, 24)
sio = socketio.Client()
sio.connect(servidor)

print(" Se realizo la conexion ")
controles = ControlSIO(sio, cliente)
cliente.sensores.iniciar()
camara = Camara()

def handler(estado : dict):
    print(estado)
    sio.emit("estado", estado)
    
cliente.sensores.nHandler(handler)

@sio.on("disconnect")
def desconectar():
    camara.parar()
    controles.parar()
    cliente.sensores.parar()
    
@sio.on("/")
def conexion():
    camara.iniciar()
    cliente.sensores.iniciar()
    

try:
    while True:
        with camara.output.condition:
            camara.output.condition.wait()
            sio.emit('frame', camara.output.frame)
finally:
    camara.parar
    controles.parar()
    cliente.sensores.parar()
    controles.fin()