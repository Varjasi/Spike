from pybricks.parameters import Port
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait, StopWatch
from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis

hub = PrimeHub()
szín = ColorSensor(Port.D)
Stopper = StopWatch()
#Vészcsengő
dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
hub.speaker.volume(20)
hub.speaker.play_notes(dallam, tempo=400)
gyors=hub.imu.acceleration(Axis.X)
idx=0
szaml=0
Stopper.reset()
while True:
    #gyors += (hub.imu.acceleration(Axis.X)-gyors)*0.01
    print(szín.hsv())
    wait(200)
print(Stopper.time())
print("Vége")
wait(500)
