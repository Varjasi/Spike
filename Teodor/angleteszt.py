import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait, StopWatch
from umath import sqrt

Jobb_motor = Motor(Port.B)
Bal_motor = Motor(Port.A)

hub = PrimeHub()
idő = StopWatch()
szín = ColorSensor(Port.C)
#Vészcsengő
dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
hub.speaker.play_notes(dallam, tempo=400)

kerékátmérő = 55.55
tengelytáv = 128
distance_to_degree = 360/3.1416/kerékátmérő
SzögSzab = 5 # mm/s/fok

s1 = Jobb_motor.angle()
Jobb_motor.run_angle(400, 100, then=Stop.HOLD, wait=False)
Bal_motor.run_angle(-400, 100, then=Stop.HOLD, wait=True)
s2 = Jobb_motor.angle()
print(s1)
print(s2)




