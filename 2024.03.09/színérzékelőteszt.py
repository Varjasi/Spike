from pybricks.parameters import Port
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait
from pybricks.hubs import PrimeHub

hub = PrimeHub()
szín = ColorSensor(Port.C)

#Vészcsengő
dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
hub.speaker.play_notes(dallam, tempo=400)

while True:
        
        # Read the color and reflection
    color = szín.hsv()
        #reflection = szín.reflection()

        # Print the measured color and reflection.
    print(color)
    wait(300)