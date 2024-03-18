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

hub = InventorHub()
motor = Motor(Port.A)
Idő = StopWatch()

hub.speaker.beep(440,100) # Indulás jelzése

v1 = 30 
v2 = 50
n = 0
n_max = 1000
# Fusi helyfoglalás 4*100 kétdimenziós tömbnek
a=[[0,0,0,0],[0,0,0,1]]
for i in range(2,n_max):
    a.append([0,0,0,i])

motor.reset_angle(0)
motor.dc(v1)
wait(1000)
Idő.reset()
#motor.dc(v2)

while (n<n_max):
    a[n] = [n,Idő.time(),motor.speed(),motor.angle()]
    if n==500:
        motor.dc(v2)
    wait(1)
    n += 1
motor.dc(0)
'''
#print("Indulok")
hub.speaker.beep(440,100)
Idő.reset()
Bal_motor.control.limits(acceleration=1000)
Bal_motor.control.pid(kd=1889)
felbontás = 2
Bal_motor.reset_angle(0)
alma[3]=13
for idx in range(1,felbontás+1):
    v=100*idx/felbontás
    Bal_motor.dc(v)
    for printidx in range(40):
        wait(25)
        print(v,Idő.time(),Bal_motor.speed(),Bal_motor.angle())
hub.speaker.beep(220,100)
#print("Vége")
'''
# Kétdimenziós tömb kiíratása a terminálra. Figyelem! Legfeljebb az utolsó 1008 sor fog megmaradni.
clear() # Terminál ablak törlése
for i in range(len(a)) :  
    for j in range(len(a[i])) :  
        print(a[i][j], end=" ") 
    print()
hub.speaker.beep(220,100)
wait(100)



