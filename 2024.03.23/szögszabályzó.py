import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait
from pybricks.tools import StopWatch

hub = PrimeHub()
idő = StopWatch()

#Vészcsengő
dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
hub.speaker.play_notes(dallam, tempo=400)



#kívántszög = hub.imu.heading()
v = 100
szögszab = 4
Jobb_motor = Motor(Port.A)
Bal_motor = Motor(Port.B)
while True:    
    szög = hub.imu.heading() #CCW (Azaz: Óra járással ellentétes a pozitív irány)
    delta_v = szög * szögszab
    Bal_motor.run(v-delta_v)
    Jobb_motor.run(-v-delta_v) 
    if idő.time() > 9000:
        kívántszög = 90
    elif idő.time() > 3000:
        kívántszög = 45

              