from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.tools import multitask, run_task
from umath import pi
#from datalogger import InitDataLogger, PushData, PrintLoggedData

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
'''
Tanulságok:
- ha gyorsan megy driftel, pontatlan lesz a kanyar
- ha a gyorsulást próbáljuk meg visszavenni, rosszul működik a szabályozója
'''


hub = InventorHub()
Jobb_motor = Motor(Port.B)
Bal_motor = Motor(Port.A)
Idő = StopWatch()
kerékátmérő = 56
tengelytáv = 93
fok_út = 360/pi/kerékátmérő
alma = [0,1,2,3,4,5,6,7,8,9,10]
alma[2] = 3
#print(alma[2])

def kanyar(sebesség,sugár,szög):
    v = sebesség * fok_út / sugár
    v_jobb = v*(sugár+tengelytáv/2)
    v_bal = v*(sugár-tengelytáv/2)
    szög_jobb = szög*(sugár+tengelytáv/2)/(kerékátmérő/2)
    szög_bal = szög*(sugár-tengelytáv/2)/(kerékátmérő/2)
    Jobb_motor.run_angle(-v_jobb,szög_jobb,Stop.HOLD,wait=False)
    Bal_motor.run_angle(v_bal,szög_bal,Stop.HOLD,wait=True)


def MarkolóNyit():
    markoló.dc(50)
    wait(1000)
    markoló.reset_angle(0)

def DaruLeenged():
    daru.dc(30)
    wait(2000)
    daru.reset_angle(0)

def MarkolóZár():
    markoló.control.limits(None,None,60)
    markoló.run(-300)
    for i in range(n_max):
        PushData(markoló.angle(),markoló.load(),markoló.speed())
        wait(10)
    '''
    wait(100)
    print(f' Szög: {markoló.angle()},Terheles: {markoló.load()}')    
    wait(100)
    print(f' Szög: {markoló.angle()},Terheles: {markoló.load()}')
    '''
    #wait(1000)
    #print(f' Szög: {markoló.angle()},Terheles: {markoló.load()}')

def DaruEmel(szög):
    #motor.control.limits(None,100,100)
    #motor.run_time(-300,idő,Stop.HOLD,wait=True)
    daru.run_angle(-300,szög,Stop.HOLD,wait=True)

def Haladás(hossz):
    if (hossz>0):
        Bal_motor.run_angle( 300,hossz,wait=False)
        Jobb_motor.run_angle(-300,hossz,wait=True)
    else:
        Bal_motor.run_angle(-300,-hossz,wait=False)
        Jobb_motor.run_angle(+300,-hossz,wait=True)

InitDataLogger(100)

hub = InventorHub()
daru = Motor(Port.F)
markoló = Motor(Port.D)
Idő = StopWatch()
adatgyűjt= False
hub.speaker.beep(440,100) # Indulás jelzése

Haladás(360)
Haladás(-140)
MarkolóNyit()
DaruLeenged()
DaruEmel(55)
MarkolóZár()
DaruEmel(160)
Haladás(-200)
MarkolóNyit()

PrintLoggedData()
'''
v1 = 30 
v2 = 80
n = 0
n_max = 1


motor.dc(-60)
wait(2000)
motor.reset_angle(0)
Idő.reset()
motor.control.limits(None,100,100)
motor.run_time(-300,200,Stop.HOLD,wait=True)
wait(10)
while (n<n_max):
    a[n] = [n,Idő.time(),motor.speed(),motor.angle()]
    if n==50:
        motor.dc(v2)
    wait(1)
    n += 1
'''



hub.speaker.beep(220,100)
wait(100)



