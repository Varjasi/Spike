import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop, Axis
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait, StopWatch
from umath import sqrt
Jobb_motor = Motor(Port.B)
Bal_motor = Motor(Port.A)
daru = Motor(Port.F)
hub = PrimeHub()
idő = StopWatch()
szín = ColorSensor(Port.C)
markoló = Motor(Port.D)

dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]

kerékátmérő = 55.55
tengelytáv = 128
fok_per_mm = 360/3.1416/kerékátmérő
SzögSzab = 2 # mm/s/fok
adatgyűjtés = False

def clear(): # terminál ablak törlése
    print("\x1b[H\x1b[3J", end="")
    print("\x1b[H\x1b[2J", end="")

def InitDataLogger(hossz):
    global a
    global n_max
    global n
    n = 0
    n_max = hossz
    clear()
    # Fusi helyfoglalás 4*100 kétdimenziós tömbnek
    a=[[0,0,0,0],[0,0,0,1]]
    for i in range(2,n_max):
        a.append([0,0,0,i])

def PushData(v1,v2,v3):
    global n
    global a
    global n_max
    if (n<n_max):
        a[n] = [n,v1,v2,v3]
        n = n+1

def PrintLoggedData():
    global a
    global n
    # Kétdimenziós tömb kiíratása a terminálra. Figyelem! Legfeljebb az utolsó 1008 sor fog megmaradni.
    for i in range(n) :  
        for j in range(len(a[i])) :  
            print(a[i][j], end=" ") 
        print()

def MarkolóNyit():
    markoló.dc(60)
    wait(1000)
    markoló.reset_angle(0)

def MarkolóZár():
    markoló.control.limits(None,None,60)
    markoló.run(-300)
    for i in range(100):
        #PushData(markoló.angle(),markoló.load(),markoló.speed())
        wait(10)

def DaruKalibráció():
    daru.dc(30)
    wait(2000)
    daru.reset_angle(0)

def DaruLeenged():
    daru.dc(30)
    for i in range(200):
        if adatgyűjtés:
            PushData(daru.load(),daru.angle(),hub.imu.rotation(Axis.X))
        wait(10)
    daru.reset_angle(0)

def DaruEmel(szög):
    #motor.control.limits(None,100,100)
    #motor.run_time(-300,idő,Stop.HOLD,wait=True)
    daru.run_target(300,szög,Stop.HOLD,wait=True)

# Kanyarodás állandó sebességgel (giroszkóppal)
def kanyar(szög, sebesség, sugár):
    if sebesség > 0:
        if szög > 0:
            v_bal = sebesség * (sugár + tengelytáv / 2)/sugár
            v_jobb = sebesség * (sugár - tengelytáv / 2)/sugár
        else:
            v_bal = sebesség * (sugár - tengelytáv / 2)/sugár
            v_jobb = sebesség * (sugár + tengelytáv / 2)/sugár
    else:
        if szög > 0:
            v_bal = sebesség * (sugár - tengelytáv / 2)/sugár
            v_jobb = sebesség * (sugár + tengelytáv / 2)/sugár
        else:
            v_bal = sebesség * (sugár + tengelytáv / 2)/sugár
            v_jobb = sebesség * (sugár - tengelytáv / 2)/sugár
    szög1 = hub.imu.heading()
    szög2 = szög1 + szög
    Bal_motor.run(-v_bal * fok_per_mm)
    Jobb_motor.run(v_jobb * fok_per_mm)
    while True:
        if szög > 0:
            if hub.imu.heading() > szög2:
                #print(szög1, szög2)
                break
        else:
            if hub.imu.heading() < szög2:
                break
                

def PontOdáigMegy(hossz, maxsebesség, gyorsulás,végsebesség,irány=None):
    # Hátra menetben csak a hossz negatív, a többi paraméter abszolút értéket jelent
    global n
    global n_max
    global fok_per_mm
    s1 = (Jobb_motor.angle()-Bal_motor.angle()) / 2 / fok_per_mm #Kiindulási út
    s2 = s1 + hossz #Úticél
    v1 = (Jobb_motor.speed()-Bal_motor.speed()) / 2 / fok_per_mm #Kiindulási sebesség
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
        if hossz>0:
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
        else:
            if -maxsebesség < v1: # negatív irány, gyorsítani akarunk
                if (v - dv) < -maxsebesség:
                    v = -maxsebesség
                else:
                    v -= dv
            else: # negatív irány, lassítani akarunk
                if (v + dv) > -maxsebesség:
                    v = -maxsebesség
                else:
                    v += dv
        s = (Jobb_motor.angle()-Bal_motor.angle()) / 2 / fok_per_mm
        if hossz>0:
            fékút = s2 - s # Hátralévő út
            if fékút < 1:
                if végsebesség==0:
                    Jobb_motor.brake()
                    Bal_motor.brake()
                break        
            v_fékút = sqrt(2*fékút*gyorsulás+végsebesség*végsebesség ) #Amekkora sebességről tudnák lefékezni
            if v > v_fékút:
                v = v_fékút
        else:
            fékút = s - s2 # Hátralévő út, negatív iránynál is pozitív érték
            if fékút < 1:
                if végsebesség==0:
                    Jobb_motor.brake()
                    Bal_motor.brake()
                break        
            v_fékút = sqrt(2*fékút*gyorsulás+végsebesség*végsebesség ) #Amekkora sebességről tudnák lefékezni
            if v < -v_fékút:
                v = -v_fékút
        v_jobb = v+v_modosítás
        v_bal = v-v_modosítás
        Jobb_motor.run(v_jobb * fok_per_mm)
        Bal_motor.run(-v_bal * fok_per_mm)

        wait(5)
        if adatgyűjtés:
            hsv = szín.hsv()
            PushData(hsv.h, hsv.s, hsv.v)

# Itt kezdődnek a cselekmények
if adatgyűjtés:
    InitDataLogger(500)
hub.speaker.play_notes(dallam, tempo=400) #Vészcsengő

'''
Mehívások
'''
MarkolóNyit()
DaruKalibráció()
#DaruEmel(-130) # Kocka keskeny részének elkapásához
#MarkolóZár()
DaruEmel(-290) # Közel a legmagasabb pont

hub.imu.reset_heading(0)
PontOdáigMegy(215, 200, 300, 100,0)
kanyar(-90, 100, 100)
PontOdáigMegy(-140, 200, 300, 0,-90)
PontOdáigMegy(60, 200, 300, 0, -90)
DaruEmel(-130)
MarkolóZár()
DaruEmel(-290)
PontOdáigMegy(-15, 200, 300, 50,-90)
kanyar(25, -50, 40)
PontOdáigMegy(-50, 200, 300, 50,-65)
kanyar(65, -50, 80)
kanyar(90, -70, 130)
PontOdáigMegy(-200, 200, 300, 0,90)
PontOdáigMegy(52, 200, 300, 0, 90)
DaruEmel(-180)
MarkolóNyit()
DaruEmel(-290)
PontOdáigMegy(200, 200, 300, 0, 90)
'''
kanyar(40, 100, 150)
kanyar(-35, 100, 100)
PontOdáigMegy(-200, 200, 300, 0,-85)

hub.speaker.beep(2000, 100)  

Jobb_motor.hold()
Bal_motor.hold()
'''
if adatgyűjtés:
    PrintLoggedData()