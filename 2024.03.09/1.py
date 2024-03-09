import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait
from pybricks.parameters import Axis


szín = ColorSensor(Port.D)
hub = PrimeHub()

calibrated = hub.imu.ready()

dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
hub.speaker.play_notes(dallam, tempo=400)

küszöbérték = hub.imu.settings(1.5, 250)
print(küszöbérték)
index = 0
while index < 10:
        a = hub.imu.up()
        calibrated = hub.imu.ready()
        stationary = hub.imu.stationary()
        print(stationary)
        #print(a)
        küszöbérték = hub.imu.settings()
        print(küszöbérték)
        print(hub.imu.heading())
        print(PrimeHub.imu.acceleration())
        wait(500)
        index += 1

