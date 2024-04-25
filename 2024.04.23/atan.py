import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop, Axis
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait, StopWatch
from pybricks.hubs import PrimeHub
from umath import sqrt
from umath import atan2, sin, cos, pi

Jobb_motor = Motor(Port.B)
Bal_motor = Motor(Port.A)
daru = Motor(Port.F)
hub = PrimeHub()
idő = StopWatch()
szín = ColorSensor(Port.C)
markoló = Motor(Port.D)


dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
alfa = atan2
kerékátmérő = 55.55
tengelytáv = 128
fok_per_mm = 360/3.1416/kerékátmérő
SzögSzab = 15 # mm/s/fok
adatgyűjtés = False
AlapGyorsulás = 300
AlapSebesség = 200

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
    daru.reset_angle(0)

def DaruBeállít(szög):
    #motor.control.limits(None,100,100)
    #motor.run_time(-300,idő,Stop.HOLD,wait=True)
    daru.run_target(1000,-szög,Stop.HOLD,wait=True)

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
                

def MenjPonthoz(X2, Y2, Utazósebesség = AlapSebesség, Végsebesség = 0, Előre=True):
    global X, Y
    s = sqrt((X2-X)*(X2-X)+(Y2-Y)*(Y2-Y))
    alfa=atan2(Y2-Y,X2-X)
    Mozgás(s,maxsebesség=Utazósebesség, végsebesség=Végsebesség, Célirány=alfa)


def Mozgás(hossz, maxsebesség=AlapSebesség, gyorsulás=AlapGyorsulás, végsebesség=AlapSebesség, KezdőIrány=None, CélIrány=None):
    # Hátra menetben csak a hossz negatív, a többi paraméter abszolút értéket jelent
    global n
    global n_max
    global fok_per_mm
    global X, Y

    s1 = (Jobb_motor.angle()-Bal_motor.angle()) / 2 / fok_per_mm #Kiindulási út
    s_előző = s1
    s2 = s1 + hossz #Úticél
    v1 = (Jobb_motor.speed()-Bal_motor.speed()) / 2 / fok_per_mm #Kiindulási sebesség
    dv = gyorsulás * 0.005 #5 ms-onként mennyit változtathatunk a sebességen
    v = v1
    if KezdőIrány == None:
        alfa1 = hub.imu.heading() #Kiindulási szög, ezt az irányt próbáljuk megtartani
    else:
        alfa1 = KezdőIrány
    if CélIrány != None: # Ha van szükség kanyarodásra
        alfa2 = CélIrány
        sa = maxsebesség*maxsebesség/2/gyorsulás # a maxsebesség-re gyorsítási út
        s21 = abs(hossz)
        alfa21 = abs(alfa2-alfa1)
        alfam = alfa21/(s21-sa)
        #print(s21,alfa21,alfam)
    if hossz<0: # Hátra megy
        maxsebesség = -maxsebesség
    while True:
        # ELÁGAZÁS FELADATA: - Gyorsulás korlátozása
        if (v + dv) < maxsebesség:
            v += dv
        elif (v - dv) > maxsebesség:
            v -= dv
        else:
            v = maxsebesség
        # X,Y koordináták számítása, GPS
        s= (Jobb_motor.angle()-Bal_motor.angle()) / 2 / fok_per_mm
        delta_s = s - s_előző
        alfa10 = -pi/180*hub.imu.heading()
        X = X + delta_s*cos(alfa10)
        Y = Y + delta_s*sin(alfa10)
        s_előző = s
        if hossz>0:
            fékút = s2 - s # Hátralévő út
            v_fékút = sqrt(2*fékút*gyorsulás+végsebesség*végsebesség ) #Amekkora sebességről tudnák lefékezni
            if v > v_fékút:
                v = v_fékút
        else:
            fékút = s - s2 # Hátralévő út, negatív iránynál is pozitív érték
            v_fékút = sqrt(2*fékút*gyorsulás+végsebesség*végsebesség ) #Amekkora sebességről tudnák lefékezni
            if v < -v_fékút:
                v = -v_fékút
        # Kilépünk az eljárásból, ha már odaértünk
        if fékút < 1:
            if végsebesség==0:
                Jobb_motor.brake()
                Bal_motor.brake()
            break        
        # Irány alapjelének előállítása
        if CélIrány == None: # Ha nincs szükség kanyarodásra
            alfa_ref = alfa1
        else:
            s = s21 - fékút # az eddig megtett út = (a teljes út) - (a hátralévő)
            if s<sa: # Kezdeti szakasz
                alfa_ref = alfam/sa*s*s/2
            elif fékút<sa:
                alfa_ref = alfa21-alfam/sa*fékút*fékút/2
            else:
                alfa_ref = alfam*(s-sa/2)
            if alfa2>alfa1:
                alfa_ref = alfa1+alfa_ref
            else:
                alfa_ref = alfa1-alfa_ref
        alfa = hub.imu.heading()
        v_modosítás = (alfa-alfa_ref)*SzögSzab
        # Itt kellene v-t korlátozni!!!
        v_jobb = v+v_modosítás
        v_bal = v-v_modosítás
        Jobb_motor.run(v_jobb * fok_per_mm)
        Bal_motor.run(-v_bal * fok_per_mm)
        wait(5)
        if adatgyűjtés:
            hsv = szín.hsv()
            PushData(X, Y)
            #PushData(s, alfa_ref, alfa)
            #PushData(s, v_jobb, v_bal)

# Itt kezdődnek a cselekmények
if adatgyűjtés:
    InitDataLogger(500)
hub.speaker.play_notes(dallam, tempo=400) #Vészcsengő

'''
Meghívások

színérték=szín.hsv(True)
hidas=(színérték.s<20) # Ha hídhoz közelebbi kiinduláson vagyunk akkor fekete-fehér betűn vagyunk
#DaruKalibráció()
#DaruBeállít(290) # Közel a legmagasabb pont
hub.imu.reset_heading(0)
Jobb_motor.control.limits(None,None,100)
Bal_motor.control.limits(None,None,100)
if hidas:
    
    Mozgás(-200,CélIrány=20)
    Mozgás(-200,CélIrány=0)
    Mozgás(-110,KezdőIrány=0)
    Mozgás(-200,CélIrány=-45)
    Mozgás(-160,végsebesség=0,CélIrány=-45) # nekiment
    Mozgás(100,CélIrány=-70)
    Mozgás(100,CélIrány=-45)
    Mozgás(80,végsebesség=0,CélIrány=-45)
    MarkolóNyit()
    DaruKalibráció()
    DaruBeállít(85)
    Mozgás(-160, végsebesség=0, CélIrány=-40)
    DaruBeállít(55)
    #MarkolóNyit()
    MarkolóZár()
    DaruBeállít(290)
    Mozgás(390, végsebesség=0, CélIrány=-127)
    Mozgás(-1000, végsebesség=0, CélIrány=-135)
    DaruBeállít(55) 
    MarkolóNyit()
    DaruBeállít(290)

else:
    #hub.speaker.beep(500, 1000)
    #DaruBeállít(200)
    DaruKalibráció()
    wait(2000)
    DaruBeállít(290)

#Mozgás(-100,100,200,0,CélIrány=0)
'''
X=0
Y=0
Mozgás(200)
print(X,Y)
hub.speaker.beep(2000, 100)  

Jobb_motor.hold()
Bal_motor.hold()

if adatgyűjtés:
    PrintLoggedData()