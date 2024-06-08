
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait, StopWatch
from pybricks.tools import multitask, run_task

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

async def clear(): # terminál ablak törlése
    print("\x1b[H\x1b[3J", end="")
    print("\x1b[H\x1b[2J", end="")

# Kanyarodás állandó sebességgel (giroszkóppal)
async def kanyar(szög, sebesség, sugár):
    if szög > 0:
        v_bal = sebesség * (sugár + tengelytáv / 2)/sugár
        v_jobb = sebesség * (sugár - tengelytáv / 2)/sugár
    else:
        v_bal = sebesség * (sugár - tengelytáv / 2)/sugár
        v_jobb = sebesség * (sugár + tengelytáv / 2)/sugár
    szög1 = hub.imu.heading()
    szög2 = szög1 + szög
    Bal_motor.run(-v_bal * distance_to_degree)
    Jobb_motor.run(v_jobb * distance_to_degree)
    while True:
        if szög > 0:
            if hub.imu.heading() > szög2:
                #print(szög1, szög2)
                break
        else:
            if hub.imu.heading() < szög2:
                break
 
async def PontOdáigMegy(hossz, maxsebesség, gyorsulás,végsebesség,irány=None):
    global n
    global n_max
    global distance_to_degree
    s1 = (Jobb_motor.angle()-Bal_motor.angle()) / 2 / distance_to_degree #Kiindulási út
    s2 = s1 + hossz #Úticél
    v1 = (Jobb_motor.speed()-Bal_motor.speed()) / 2 / distance_to_degree #Kiindulási sebesség
    dv = gyorsulás * 0.01 #10 ms-onként mennyit változtathatunk a sebességen
    v = v1
    if irány == None:
        alfa1 = hub.imu.heading() #Kiindulási szög, ezt az irányt próbáljuk megtartani
    else:
        alfa1 = irány

    while True:
        alfa = hub.imu.heading()
        v_modosítás = (alfa-alfa1)*SzögSzab
        '''
        ELÁGAZÁS FELADATA: - Gyorsulás korlátozása
        
        '''
        if maxsebesség > v1:
            if (v + dv) > maxsebesség:
                v = maxsebesség
            else:
                v += dv
        else:
            if (v - dv) < maxsebesség:
                v = maxsebesség
            else:
                v -= dv
        s = (Jobb_motor.angle()-Bal_motor.angle()) / 2 / distance_to_degree
        fékút = s2 - s # Hátralévő út
        if fékút < 1:
            break        
        v_fékút = 2*fékút*gyorsulás+végsebesség*végsebesség  #Amekkora sebességről tudnák lefékezni
        if v > v_fékút:
            v = v_fékút
        
        v_jobb = v+v_modosítás
        v_bal = v-v_modosítás
        Jobb_motor.run(v_jobb * distance_to_degree)
        Bal_motor.run(-v_bal * distance_to_degree)

        wait(5)
async def zene():
    hub.speaker.volume(10)
    #await hub.speaker.beep(440,1000)
    dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
    #for x in dallam
    await hub.speaker.play_notes(dallam, tempo=120)

'''
MEGHÍVÁSOK
'''
async def main():
    # Fusi helyfoglalás 4*100 kétdimenziós tömbnek a rekorder funkcióhoz
    #pritty pratty putty

    Bal_motor.reset_angle(0)
    Jobb_motor.reset_angle(0)
    #Bal_motor.run_time(-100, 1000)
    #Jobb_motor.run_time(100, 1000)

    await PontOdáigMegy(1000, -200, 300, 0)
    await kanyar(90, 400, 180)
    await multitask(PontOdáigMegy(1000, -200, 300, 0), zene())
    #PontOdáigMegy(400, 200, 300, 100, 180)
    #PontOdáigMegy(100, 200, 300, 100,360)

    #PontOdáigMegy(100, 50, 300, 0)  

    Jobb_motor.hold()
    Bal_motor.hold()

    #print(distance_to_degree)

run_task(main())
