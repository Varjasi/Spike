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

n = 0
n_max = 100
# Fusi helyfoglalás 4*100 kétdimenziós tömbnek
a=[[0,0,0,0],[0,0,0,1]]
for i in range(2,n_max):
    a.append([0,0,0,i])

motor.reset_angle(0)
#motor.dc(n_max)
wait(200)
Idő.reset()
motor.dc(20)
wait(100)
motor.run(50)
while (n<n_max):
    a[n] = [n,Idő.time(),motor.speed(),motor.angle()]
    n += 1
    wait(10)


# Kétdimenziós tömb kiíratása a terminálra. Figyelem! Legfeljebb az utolsó 1008 sor fog megmaradni.
clear() # Terminál ablak törlése
for i in range(len(a)) :  
    for j in range(len(a[i])) :  
        print(a[i][j], end=" ") 
    print()

hub.speaker.beep(220,100)
wait(100)



