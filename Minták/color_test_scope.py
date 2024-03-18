from pybricks.parameters import Port
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait, StopWatch
from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis

hub = PrimeHub()
szín = ColorSensor(Port.D)
idő = StopWatch()

def clear(): # terminál ablak törlése
    print("\x1b[H\x1b[3J", end="")
    print("\x1b[H\x1b[2J", end="")
    
# Fusi helyfoglalás 4*100 kétdimenziós tömbnek a rekorder funkcióhoz
n_max = 1000
a=[[0,0,0,0],[0,0,0,1]]
for i in range(2,n_max):
    a.append([0,0,0,i])
n = 0

#Vészcsengő
dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
hub.speaker.volume(20)
hub.speaker.play_notes(dallam, tempo=400)
gyors=hub.imu.acceleration(Axis.X)
idx=0
szaml=0
idő.reset()

while (n<n_max):
    b = szín.hsv()
    a[n] = [b.h, b.s, b.v, szín.reflection()]
    wait(1)
    n += 1

# Kétdimenziós tömb kiíratása a terminálra. Figyelem! Legfeljebb az utolsó 1008 sor fog megmaradni.
clear() # Terminál ablak törlése
for i in range(len(a)) :  
    for j in range(len(a[i])) :  
        print(a[i][j], end=" ") 
    print()

# Jelezzük a hangszórón a tevékenység végét
hub.speaker.beep(220,100)
wait(100)
