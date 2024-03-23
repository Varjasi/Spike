import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait, StopWatch
Bal_motor = Motor(Port.B)
Jobb_motor = Motor(Port.A)

hub = PrimeHub()
idő = StopWatch()
#Vészcsengő
dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
hub.speaker.play_notes(dallam, tempo=400)

kerékátmérő = 56
tengelytáv = 128
distance_to_degree = 360/3.1416/kerékátmérő
SzögSzab = 2 # mm/s/fok

def clear(): # terminál ablak törlése
    print("\x1b[H\x1b[3J", end="")
    print("\x1b[H\x1b[2J", end="")

def IránytartóEgyenesMozgás(hossz, végsebesség, gyorsulás):
    global n
    global n_max
    global distance_to_degree
    s1 = (Bal_motor.angle()-Jobb_motor.angle()) / 2 / distance_to_degree
    s2 = s1 + hossz
    v1 = (Bal_motor.speed()-Jobb_motor.speed()) / 2 / distance_to_degree
    dv = gyorsulás * 0.01
    v = v1
    alfa1 = hub.imu.heading()
    while True:
        v_modosítás = (hub.imu.heading()-alfa1)*SzögSzab
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
        v_bal = v+v_modosítás
        v_jobb = v-v_modosítás
        Bal_motor.run(v_bal * distance_to_degree)
        Jobb_motor.run(-v_jobb * distance_to_degree)
        s = (Bal_motor.angle()-Jobb_motor.angle()) / 2 / distance_to_degree
        if s > s2:
            break
        wait(10)
        if (n<n_max):
            a[n] = [n, idő.time(), v_bal, v_jobb,v_modosítás,s,s1,s2]
        n += 1

# Fusi helyfoglalás 4*100 kétdimenziós tömbnek a rekorder funkcióhoz
n_max = 1000
rekord_minta = [1,2,3,4,5,6,7,8]
a=[rekord_minta,rekord_minta]
for i in range(2,n_max):
    a.append(rekord_minta)
n = 0

IránytartóEgyenesMozgás(100, 100, 300)  

# Kétdimenziós tömb kiíratása a terminálra. Figyelem! Legfeljebb az utolsó 1008 sor fog megmaradni.
clear() # Terminál ablak törlése
for i in range(n) :  
    for j in range(len(a[i])) :  
        adatok = (a[i][j])        
        with open('./adatok/kimenet.txt', 'w', encoding='utf-8') as celfajl:

            # lista elemeit írja a fájlba
            print(*object ,adatok, end='; ', file=celfajl)
    
   
    print() # új sor

print(distance_to_degree)
