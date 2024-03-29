import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait
from pybricks.tools import StopWatch
from pybricks.parameters import Color


szín = ColorSensor(Port.C)
hub = PrimeHub()
idő = StopWatch()

def terepzöld():
    a = szín.hsv()
    return(bool(a.h>130 and a.h<140 and a.s>40 and a.s<50))

def terepkék():
    a = szín.hsv()
    return(bool(a.h>219 and a.h<241 and a.s>35 and a.s<52))

def sárga():
    a = szín.hsv()
    return(bool(a.h >= 40 and a.h <= 60 and a.s >= 50 and a.s <= 100 and a.v <= 13 and a.v>=10))

#Vészcsengő
dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
hub.speaker.play_notes(dallam, tempo=400)
def vonalkövetés():
    alapszög = hub.imu.heading()
    v = 200
    szögszab = 4
    Jobb_motor = Motor(Port.A)
    Bal_motor = Motor(Port.B)
    while not sárga():
        színek = [Color.RED, Color.BLUE]
        hub.light.animate(színek, 1000)  
        szög = hub.imu.heading() #CCW (Azaz: Óra járással ellentétes a pozitív irány)
        alma = szín.hsv()
        szögmódosítás = alma.v-13
        kívántszög = alapszög - szögmódosítás
        delta_v = (kívántszög - szög) * szögszab
        Bal_motor.run(v-delta_v)
        Jobb_motor.run(-v-delta_v)
        if idő.time() > 9000:
            kívántszög = 90
        elif idő.time() > 3000:
             kívántszög = 45

             
def call():
    import subprocess
    subprocess.run("pybricksdev run ble 2024.03.18/vonalkövetés + színérézkelés.py")
call()

vonalkövetés()

