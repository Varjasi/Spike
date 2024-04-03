from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.tools import multitask, run_task
from umath import pi

'''
Tanulságok:
- ha gyorsan megy driftel, pontatlan lesz a kanyar
- ha a gyorsulást próbáljuk meg visszavenni, rosszul működik a szabályozója
'''

'''
hub = InventorHub()
Jobb_motor = Motor(Port.A)
Bal_motor = Motor(Port.B)
Idő = StopWatch()
kerékátmérő = 56
tengelytáv = 93
fok_út = 360/pi/kerékátmérő
alma = [0,1,2,3,4,5,6,7,8,9,10]
alma[2] = 3
print(alma[2])
'''
def kanyar(sebesség,sugár,szög):
    v = sebesség * fok_út / sugár
    v_jobb = v*(sugár+tengelytáv/2)
    v_bal = v*(sugár-tengelytáv/2)
    szög_jobb = szög*(sugár+tengelytáv/2)/(kerékátmérő/2)
    szög_bal = szög*(sugár-tengelytáv/2)/(kerékátmérő/2)
    Jobb_motor.run_angle(-v_jobb,szög_jobb,Stop.HOLD,wait=False)
    Bal_motor.run_angle(v_bal,szög_bal,Stop.HOLD,wait=True)
def clear(): # terminál ablak törlése
    print("\x1b[H\x1b[3J", end="")
    print("\x1b[H\x1b[2J", end="")

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
    '''
    wait(100)
    print(f' Szög: {markoló.angle()},Terheles: {markoló.load()}')    
    wait(100)
    print(f' Szög: {markoló.angle()},Terheles: {markoló.load()}')
    '''
    wait(1000)
    #print(f' Szög: {markoló.angle()},Terheles: {markoló.load()}')

def DaruEmel(szög):
    #motor.control.limits(None,100,100)
    #motor.run_time(-300,idő,Stop.HOLD,wait=True)
    daru.run_angle(-300,szög,Stop.HOLD,wait=True)

def Haladás(hossz):
    if (hossz>0):
        BalMotor.run_angle( 300,hossz,wait=False)
        JobbMotor.run_angle(-300,hossz,wait=True)
    else:
        BalMotor.run_angle(-300,-hossz,wait=False)
        JobbMotor.run_angle(+300,-hossz,wait=True)


hub = InventorHub()
BalMotor = Motor(Port.A)
JobbMotor = Motor(Port.B)
daru = Motor(Port.F)
markoló = Motor(Port.D)
Idő = StopWatch()
adatgyűjt= False
hub.speaker.beep(440,100) # Indulás jelzése

Haladás(360)
Haladás(-140)
MarkolóNyit()
DaruLeenged()
DaruEmel(70)
MarkolóZár()
DaruEmel(160)
Haladás(-200)
MarkolóNyit()
'''
v1 = 30 
v2 = 80
n = 0
n_max = 1
# Fusi helyfoglalás 4*100 kétdimenziós tömbnek
a=[[0,0,0,0],[0,0,0,1]]
for i in range(2,n_max):
    a.append([0,0,0,i])

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


# Kétdimenziós tömb kiíratása a terminálra. Figyelem! Legfeljebb az utolsó 1008 sor fog megmaradni.
if (adatgyűjt):
    clear() # Terminál ablak törlése
    for i in range(len(a)) :  
        for j in range(len(a[i])) :  
            print(a[i][j], end=" ") 
        print()
hub.speaker.beep(220,100)
wait(100)



