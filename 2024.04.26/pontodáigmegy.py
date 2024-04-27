import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait, StopWatch
from umath import sqrt
from usys import stdin
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

def clear(): # terminál ablak törlése
    print("\x1b[H\x1b[3J", end="")
    print("\x1b[H\x1b[2J", end="")

def PontOdáigMegy(hossz, végsebesség, gyorsulás):
    global n
    global n_max
    global distance_to_degree
    s1 = (Jobb_motor.angle()-Bal_motor.angle()) / 2 / distance_to_degree #Kiindulási út, ahol tart a motor
    print(s1)
    print(Jobb_motor.angle())
    print(Bal_motor.angle())
    s2 = s1 + hossz #Úticél
    v1 = (Jobb_motor.speed()-Bal_motor.speed()) / 2 / distance_to_degree #Kiindulási sebesség
    dv = gyorsulás * 0.01 #10 ms-onként mennyit változtathatunk a sebességen
    v = v1
    alfa1 = hub.imu.heading() #Kiindulási szög, ezt az irányt próbáljuk megtartani
    while True:
        alfa = hub.imu.heading()
        v_modosítás = (alfa-alfa1)*SzögSzab
        if végsebesség > v1:
            if (v + dv) > végsebesség:
                v = végsebesség
            else:
                v += dv
        else:
            if (v - dv) < végsebesség:
                v = végsebesség
            else:
                v -= dv
        s = (Jobb_motor.angle()-Bal_motor.angle()) / 2 / distance_to_degree
        fékút = s2 - s # Hátralévő út
        #print(s)
        #EZT NEM ÉRTEM
        if fékút < 1:
            break        
        v_fékút = sqrt(2*fékút*gyorsulás)
        if v > v_fékút:
            v = v_fékút
        
        v_bal = v+v_modosítás
        v_jobb = v-v_modosítás
        Jobb_motor.run(v_bal * distance_to_degree)
        Bal_motor.run(-v_jobb * distance_to_degree)
        wait(10)

cmd = stdin.readline().strip()
print(cmd)

PontOdáigMegy(100, -300, 300)  
Jobb_motor.hold()
Bal_motor.hold()

# Kétdimenziós tömb kiíratása a terminálra. Figyelem! Legfeljebb az utolsó 1008 sor fog megmaradni.
clear() # Terminál ablak törlése
