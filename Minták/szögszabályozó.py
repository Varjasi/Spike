from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = InventorHub()

idő = StopWatch()

#Vészcsengő
dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
hub.speaker.play_notes(dallam, tempo=400)



kívántszög = hub.imu.heading()
sebesség_szöveg=input("Semmit")
v=int(sebesség_szöveg)
szögszab = 2
Jobb_motor = Motor(Port.A)
Bal_motor = Motor(Port.B)
while True:    
    szög = hub.imu.heading() #CCW (Azaz: Óra járással ellentétes a pozitív irány)
    delta_v = (kívántszög - szög) * szögszab
    Bal_motor.run(v-delta_v)
    Jobb_motor.run(-v-delta_v) 
    if idő.time() > 12000:   
        break 
    elif idő.time() > 9000:
        kívántszög = 90
    elif idő.time() > 3000:
        kívántszög = 45
print("Vége")
wait(1000)

