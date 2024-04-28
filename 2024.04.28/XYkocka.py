
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop, Axis
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait, StopWatch
from umath import sqrt, pi, cos, sin, atan2

idő = StopWatch()
kezdőidő = idő.time()
MaxCiklusIdő = 0
Jobb_motor = Motor(Port.A)
Bal_motor = Motor(Port.B)
daru = Motor(Port.F)
hub = PrimeHub()

szín = ColorSensor(Port.C)
markoló = Motor(Port.D)
class IndulásiPozíció:
  def __init__(self, X, Y, szög):
    self.X = X
    self.Y = Y
    self.szög = szög

class SzínFeltételek:
  def __init__(self, HueMax, HueMin, SaturationMax, SaturationMin, VolumeMax, VolumeMin):
    self.HueMax = HueMax
    self.HueMin = HueMin
    self.SaturationMax = SaturationMax
    self.SaturationMin = SaturationMin
    self.VolumeMax = VolumeMax
    self.VolumeMin = VolumeMin

KeresendőSzín = SzínFeltételek(None,None,None,None,None,None) #!!!
Xszín = None
Yszín = None

dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]

# Robotadatok
kerékátmérő = 55.72
tengelytáv = 128
fok_per_mm = 360/pi/kerékátmérő
s_hátfal = 58 # hátfal távolsága a tengelytől
szélesség = 143

# Pályaadatok. Az első négyet a helyszínen ellenőrizni kell !!!
Pályaszélesség = 2350 # Ezt a helyszínen meg kell mérni és változtatni kell!
Pályamagasság = 1136 # Ezt a helyszínen meg kell mérni és változtatni kell!
BalPalánk = 60 # a baloldali palánk távolsága a szemetes fehér téglalapjától
AlsóPalánk = 63 # az alsó palánk távolsága az induló fehér négyzettől

Xbal = 70-BalPalánk+s_hátfal 
Xjobb = Xbal+Pályaszélesség - 2*s_hátfal
Yalsó = 62-AlsóPalánk+s_hátfal 
Yfelső = Yalsó + Pályamagasság - 2*s_hátfal
IndulásiPozícióHidas = IndulásiPozíció(791,136+15,-90) # mia csudáért kell a +15?
IndulásiPozícióAkadályos = IndulásiPozíció(1498+139, 827+143/2+65, 180) 


# Beállítások
SzögSzab = 1000 #15*180/pi # mm/s/fok
AlapGyorsulás = 400
AlapSebesség = 300 # Úgy tűnik 400-nál már bizonytalan a jobb motor
SebességZaj = 100 # Ez alatt mondjuk azt, hogy kb. már áll a robot
ÚtZaj = 1 # Ha ennél kisebb utat tett meg a robot 100ms alatt, akkor már a palánknak ütközött
FaltolásEreje = 50 # Elég ahhoz, hogy menjen a robot, de kevés ahhoz, hogy megcsússzon a kerék

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

def PushData(v0,v1,v2,v3):
    global n
    global a
    global n_max
    if (n<n_max):
        a[n] = [v0,v1,v2,v3]
        n = n+1

def PrintLoggedData():
    global a
    global n
    # Kétdimenziós tömb kiíratása a terminálra. Figyelem! Legfeljebb az utolsó 1008 sor fog megmaradni.
    for i in range(n) :  
        for j in range(len(a[i])) :  
            print(a[i][j], end=" ") 
        print()

def DaruKalibráció():
    daru.dc(20)
    wait(500)
    daru.reset_angle(0)

def DaruBeállít(szög):
    daru.run_target(200,-szög,Stop.BRAKE,wait=True)
    
def DaruFelránt(szög):
    daru.run_target(1000,-szög,Stop.HOLD,wait=True)

def MarkolóNyit():
    markoló.run_until_stalled(1000,Stop.BRAKE,60)
    markoló.reset_angle(0)

def MarkolóZár():
    markoló.run_until_stalled(-1000,Stop.BRAKE,70)

def MarkolóBeállít(szög):
    markoló.run_target(1000,-szög,Stop.BRAKE,wait=True)
    
def IrányOlvasás(): # A matematikai szöget adja vissza radiánban
    return -pi/180*hub.imu.heading()

def ÚtOlvasás(): # Az indulástól megtett utat adja vissza mm-ben
    return (Jobb_motor.angle()-Bal_motor.angle()) / 2 / fok_per_mm

def SebességOlvasás(): # Az aktuális sebességet adja vissza mm/s-ben
    return (Jobb_motor.speed()-Bal_motor.speed()) / 2 / fok_per_mm

def Fordul(szög,maxsebesség=AlapSebesség,gyorsulás=AlapGyorsulás): # álló helyzetben fordulás
    # szög: az aktuális helyzethez képest ennyit fordul el, radiánban megadva
    s21 = szög*tengelytáv/2 # ennyi ívet tegyen meg egy-egy motor 
    s1 = (Jobb_motor.angle()+Bal_motor.angle()) / 2 / fok_per_mm #Kiindulási ívhossz
    s2 = s1 + s21 #Úticél
    dv = gyorsulás * 0.005 #5 ms-onként mennyit változtathatunk a sebességen
    v = 0
    #print(s1,s2)
    if szög<0: # jobbra fordul
        maxsebesség = -maxsebesség    
    while True:
        # Gyorsulás korlátozás
        if (v + dv) < maxsebesség:
            v += dv
        elif (v - dv) > maxsebesség:
            v -= dv
        else:
            v = maxsebesség

        # A hátralévő út és a hozzátartozó maximális fékezéssel megengedett sebesség számítása
        s = (Jobb_motor.angle()+Bal_motor.angle()) / 2 / fok_per_mm
        if szög>0:
            fékút = s2 - s # Hátralévő út
            v_fékút = sqrt(2*fékút*gyorsulás) #Amekkora sebességről tudnák lefékezni
            if v > v_fékút:
                v = v_fékút
        else:
            fékút = s - s2 # Hátralévő út, negatív iránynál is pozitív érték
            v_fékút = sqrt(2*fékút*gyorsulás) #Amekkora sebességről tudnák lefékezni
            if v < -v_fékút:
                v = -v_fékút
        Jobb_motor.run(v * fok_per_mm)
        Bal_motor.run(v * fok_per_mm)        # Kilépünk az eljárásból, ha már odaértünk
        if fékút < 1:
            Jobb_motor.brake()
            Bal_motor.brake()
            break        
        wait(5)

def Mozgás(hossz, maxsebesség=AlapSebesség, gyorsulás=AlapGyorsulás, végsebesség=AlapSebesség, KezdőIrány=None, CélIrány=None):
    # Hátra menetben csak a hossz negatív, a többi paraméter abszolút értéket jelent
    # Hossz: ennyit fog haladni, mm-ben
    # maxsebesség: menet közben erre gyorsul fel. Ha kanyarodni is akarunk, kisebb legyen az AlapSebességnél
    # gyorsulás: ha egy pályaszakaszon kipörögne a kerék, csökkenteni kell az AlapGyorsulásról
    # végsebesség: ha nem adjuk meg, az út végén még nagyon hasít. Ha az út végén meg kell, hogy álljon, végsebesség = 0 legyen
    # KezdőIrány, Célirány:
    #   ha egyiket sem adjuk meg, végig tartja az éppen aktuális érzékelt irányt
    #   ha csak a KezdőIrányt adjuk meg, végig egyenesen próbál menni, ebben az irányban, alapvetően így használjuk egyenes vonalakhoz
    #   ha csak a CélIrányt adjuk meg, az éppen aktuális érzékelt irányról erre próbál meg átállni
    #   ha minkét irányt megadjuk, hasonló a helyzet az előzőhöz, csak kevésbé zavar az irányérzékelés zaja
    global n
    global n_max
    global fok_per_mm
    global X, Y
    global MaxCiklusIdő
    CiklusKezdőIdő = idő.time()
    s1 = ÚtOlvasás() #Kiindulási út
    s_előző = s1
    s2 = s1 + hossz #Úticél
    v1 = SebességOlvasás() #Kiindulási sebesség
    dv = gyorsulás * 0.005 #5 ms-onként mennyit változtathatunk a sebességen
    v = v1
    if KezdőIrány == None:
        alfa1 = IrányOlvasás() #Kiindulási szög, ezt az irányt próbáljuk megtartani
    else:
        alfa1 = KezdőIrány
    if CélIrány != None: # Ha van szükség kanyarodásra, segédszámítást végzünk 
                         # az aktuális kívánt irány számításához. Azért ilyen bonyi
                         # mert nem akarjuk hirtelen változtatni a szöget
        alfa2 = CélIrány
        sa = maxsebesség*maxsebesség/2/gyorsulás # a maxsebesség-re gyorsítási út
        # Ez akkor lenne igaz, ha álló helyzetből indulnánk.
        s21 = abs(hossz)
        if sa > s21/2:
            sa = s21/2
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
        # GPS: X és Y számítása
        s = ÚtOlvasás()
        delta_s = s - s_előző
        #if hossz<0:
        #    delta_s = -delta_s
        alfa = IrányOlvasás() # radián és CCW, matekban pozitív
        X += delta_s * cos(alfa)
        Y += delta_s * sin(alfa)
        s_előző = s
        PozícióSzínnél()

        # A hátralévő út és a hozzátartozó maximális fékezéssel megengedett sebesség számítása
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
                wait(100)
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
        v_modosítás = (alfa_ref-alfa)*SzögSzab
        # Itt kellene v-t korlátozni!!!
        v_jobb = v+v_modosítás
        v_bal = v-v_modosítás
        Jobb_motor.run(v_jobb * fok_per_mm)
        Bal_motor.run(-v_bal * fok_per_mm)
        IdőPont = idő.time()
        CiklusIdő = IdőPont-CiklusKezdőIdő
        if CiklusIdő>MaxCiklusIdő:
            MaxCiklusIdő = CiklusIdő
        CiklusKezdőIdő = IdőPont
        wait(5)
        if adatgyűjtés:
            PushData(alfa_ref,alfa,X,Y)

# HueMax, HueMin, SaturationMax, SaturationMin, VolumeMax, VolumeMin
def KeressFehéret():
    global KeresendőSzín
    KeresendőSzín = SzínFeltételek(None,None,5,None,None,99) #!!!

def KeressFeketét():
    global KeresendőSzín
    KeresendőSzín = SzínFeltételek(None,None,None,None,60,None) #!!!

def PozícióSzínnél():
    global X, Y, Xszín, Yszín, szín
    Padlószín = szín.hsv()
    Elértük=True
    if KeresendőSzín.HueMax != None:
        if Padlószín.h > KeresendőSzín.HueMax:
            Elértük = False
    if KeresendőSzín.HueMin != None:
        if Padlószín.h < KeresendőSzín.HueMin:
            Elértük = False
    if KeresendőSzín.SaturationMax != None:
        if Padlószín.s > KeresendőSzín.SaturationMax:
            Elértük = False
    if KeresendőSzín.SaturationMin != None:
        if Padlószín.s < KeresendőSzín.SaturationMin:
            Elértük = False
    if KeresendőSzín.VolumeMax != None:
        if Padlószín.v > KeresendőSzín.VolumeMax:
            Elértük = False
    if KeresendőSzín.VolumeMin != None:
        if Padlószín.v < KeresendőSzín.VolumeMin:
            Elértük = False
    if Elértük:
        Xszín = X
        Yszín = Y


def MenjFalnak():
    global X, Y
    Jobb_motor.dc(-FaltolásEreje)
    Bal_motor.dc(FaltolásEreje)
    wait(500)
    # a matematikai irányt beolvassuk és pozitív 45 feletti tartományba toljuk
    alfa = IrányOlvasás() #radián
    '''
    A ciklusok arra szolgálnak, hogy körön kelül maradjunk.
    '''
    while alfa>2*pi:
        alfa -= 2*pi
    while alfa<0:
        alfa += 2*pi 
    # alfa most már 0 és 2*pi között van
    # feltételezzük, hogy legalább +- 45 fok alatti hibával merőleges a kérdéses palánkhoz
    # ebből tudjuk eldönteni, hogy melyik falnak tolattunk neki
    if (alfa<pi/4) | (alfa>pi*7/4): # bal oldali palánknak ütköztünk
        hub.imu.reset_heading(0)
        X = Xbal
    elif alfa<pi*3/4: # alsó palánk (135°)
        hub.imu.reset_heading(-90)
        Y = Yalsó
    elif alfa<pi*5/4: # jobb palánk
        hub.imu.reset_heading(-180)
        X = Xjobb
    else: # akkor csak a felső palánk lehet
        hub.imu.reset_heading(90)
        Y = Yfelső
    Jobb_motor.brake()
    Bal_motor.brake()
    wait(200) # hogy biztosan megálljunk

def MenjPonthoz(X2, Y2, Utazósebesség=AlapSebesség ,Végsebesség=0, Előre=True):
    global X,Y
    s = sqrt((X2-X)*(X2-X)+(Y2-Y)*(Y2-Y)) # a derékszögű háromszög átlója
    alfa2 = atan2(Y2-Y,X2-X) # az alapon lévő szög, radiánban
    if Előre==False:
        alfa2 = alfa2 + pi # ha farolunk, 180-fokot fordulunk és rükverz
        s = -s
    alfa1 = IrányOlvasás() #Kiindulási
    # attól függően fordulunk jobbra vagy balra, hogy hol érjük el hamarabb az irányt
    while (alfa2-alfa1)>pi:
        alfa2 -= 2*pi
    while (alfa2-alfa1)<-pi:
        alfa2 += 2*pi

    v1 = SebességOlvasás() #Kiindulási sebesség
    if abs(v1)<SebességZaj: # Közelítőleg áll, tehát most kell befordulni az irányba
        Fordul(alfa2-alfa1)
    #hub.speaker.beep(2000, 100)  
    #print(v1,alfa1,alfa2)
    Mozgás(s,maxsebesség=Utazósebesség,végsebesség=Végsebesség,KezdőIrány=alfa2)

def KezdetiHelyzetBeállítása():
    global X, Y, Hidas
    színérték=szín.hsv(True)
    Hidas = színérték.s>40
    if Hidas:     # Ha hídhoz közelebbi kiinduláson vagyunk akkor sárga felületen vagyunk
        X = IndulásiPozícióHidas.X 
        Y = IndulásiPozícióHidas.Y 
        hub.imu.reset_heading(IndulásiPozícióHidas.szög)
    else:
        X = IndulásiPozícióAkadályos.X 
        Y = IndulásiPozícióAkadályos.Y 
        hub.imu.reset_heading(IndulásiPozícióAkadályos.szög)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Itt kezdődnek a cselekmények
adatgyűjtés = False
if adatgyűjtés:
    InitDataLogger(500)
clear() # arra az esetre, ha futásközben kiíratnánk dolgokat, Ne legyen benne az éles progiban !!!
hub.speaker.play_notes(dallam, tempo=400) #Vészcsengő

'''
Meghívások
'''

# Kezdeti állapot beállítása
X=300
Y=170
hub.imu.reset_heading(170)

# Pozciót kalibráljuk, alsó palánknak ütközve
MenjPonthoz(500,210,Előre=False)
MenjPonthoz(500,98,Végsebesség=200,Előre=False)
MenjFalnak() # Y-t beállítottuk

# Kezdeti állapot beállításának folytatása, a rendes progiban nem kell!!!
daru.dc(40)
wait(200)
daru.dc(20)
wait(2000)
daru.reset_angle(0)
DaruFelránt(280)

# közelítünk a piros kockához
MenjPonthoz(500, 58+25)  # eljöttünk a faltal egy kicsit
KeressFehéret()
MenjPonthoz(997, 76, Utazósebesség=100) # beállunk a kocka magasságába
print(Xszín,Yszín)

'''
KeressFeketét()
#print(KeresendőSzín.VolumeMax,KeresendőSzín.VolumeMin)
MenjPonthoz(1081,772+3) # nagy sárga közepe fölé 20cm-rel
print(Xszín,Yszín)
daru.reset_angle(0)
DaruFelránt(78)
MenjPonthoz(780+40,972) # szürke szemetes fölé megyünk
print(Xszín,Yszín)

# felkapjuk a szürke szemetest
DaruBeállít(65)
MarkolóZár()
DaruBeállít(280)

# Megyünk a szemétlerakóba, de útba ejtjük a sárga szemetet
MenjPonthoz(921,687+20+20) #Sárga szemét közelébe
MenjPonthoz(310, 170+20+20) #Végállomásra
DaruBeállít(100)
MarkolóNyit()
DaruFelránt(300)

# Pozciót kalibráljuk, alsó, majd a bal palánknak ütközve
MenjPonthoz(504,310,Előre=False)
MenjPonthoz(504,98,Végsebesség=200,Előre=False)
MenjFalnak() # Y-t beállítottuk
YaPöcköléshez=240
MenjPonthoz(504,YaPöcköléshez,Előre=True)
MenjPonthoz(98,YaPöcköléshez,Végsebesség=200,Előre=False)
MenjFalnak()

# a vízvezeték mellé állunk és a pöcökkel aláfordulunk, majd felrántjuk
MenjPonthoz(183,YaPöcköléshez)
DaruBeállít(73)
Fordul(pi/2+0.25) # itt akasztja be a pöcköt a rúd alá
MenjPonthoz(183,YaPöcköléshez+20) # kicsit még közelebb megy
DaruFelránt(280)

# innen kezdődik a jobb szemét progi
MenjPonthoz(1081,781) # nagy sárga négyzet fölött, a szürke szemét magasságában
MenjPonthoz(2026-208,781)
DaruBeállít(65)
MarkolóZár() # megfogtuk a szemetet
DaruBeállít(280)

# újra kalibráljuk Y a felső palánkhoz ütközve
MenjPonthoz(X, 1040, Előre=False, Végsebesség=200)
MenjFalnak()
YaPöcköléshez=811
MenjPonthoz(X,YaPöcköléshez)
# újra kalibráljuk X-t a jobb palánkhoz ütközve
MenjPonthoz(2260,YaPöcköléshez, Előre=False, Végsebesség=200)
MenjFalnak()

# jobb vízvezeték felpöckölési procedúra
MenjPonthoz(2090,YaPöcköléshez)
DaruBeállít(73)
Fordul(pi/2+0.2) # itt akasztja be a pöcköt a rúd alá
MenjPonthoz(2090,YaPöcköléshez-20) # kicsit még közelebb megy
DaruFelránt(280)

# Megyünk a szemétlerakóba, de útba ejtjük a sárga szemetet
MenjPonthoz(1901 ,630) # jobb sárga szemét közelébe
MenjPonthoz(310, 170) #Végállomásra
DaruBeállít(100) # kissé leenged

MarkolóNyit()
DaruFelránt(300)
'''
hub.speaker.beep(2000, 100)  

Jobb_motor.brake()
Bal_motor.brake()
print(f'Kezdőidő: {kezdőidő}, Végidő: {idő.time()}, Ciklus futási ideje: {MaxCiklusIdő}')
if adatgyűjtés:
    clear()
    PrintLoggedData()
