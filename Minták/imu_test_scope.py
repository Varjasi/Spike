from pybricks.parameters import Port
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait, StopWatch
from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis

hub = PrimeHub()
szín = ColorSensor(Port.C)
idő = StopWatch()
gyors=hub.imu.acceleration(Axis.X)

def clear(): # terminál ablak törlése
    print("\x1b[H\x1b[3J", end="")
    print("\x1b[H\x1b[2J", end="")
    
# Fusi helyfoglalás 4*100 kétdimenziós tömbnek a rekorder funkcióhoz
n_max = 1000
rekord_minta = [1,2,3,4,5,6,7,8]
a=[rekord_minta,rekord_minta]
for i in range(2,n_max):
    a.append(rekord_minta)
n = 0

#Vészcsengő
dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
hub.speaker.volume(20)
hub.speaker.play_notes(dallam, tempo=400)

#idő.reset()
#hub.imu.reset_heading(0)
while (n<n_max):
    #b = szín.hsv()
    b = hub.imu.angular_velocity(Axis.Z)
    c = hub.imu.acceleration()
    d = hub.imu.heading()
    #a[n] = [b.h, b.s, b.v, szín.reflection(),c[0],c[1],c[2],d]
    a[n] = [n, idő.time(), b, 0,c[0],c[1],c[2],d]
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
