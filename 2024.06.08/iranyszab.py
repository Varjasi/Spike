from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Axis
from pybricks.tools import wait, StopWatch

kerékátmérő = 87.8
tengelyhossz = 142

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

hub = InventorHub()
Idő = StopWatch()

Jobb_motor = Motor(Port.F)
Bal_motor = Motor(Port.A)

adatgyűjtés = False
if adatgyűjtés:
    InitDataLogger(400)

dc=0
Bal_motor.dc(dc)
Jobb_motor.dc(-dc)
Bal_motor.reset_angle(0)
Jobb_motor.reset_angle(0)
hub.imu.reset_heading(0)

v=0
dv=100/(300/5) # 5ms-onként 300ms alatt 100-ra
maxsebesség=99
kp=5
kd=5
ki=0.05
alfa_ref=0
x_last=0
int=0
idx=0
while (idx<500):
    idx+=1
    # Gyorsulás korlátozása
    if (v + dv) < maxsebesség:
        v += dv
    else:
        v = maxsebesség
    alfa = hub.imu.heading()
    x = alfa_ref-alfa # hibajel képzése
    xd = x + (x-x_last)*kd
    x_last=x
    int += ki*xd
    y = kp*(xd+int) # y a PID szabályozó kimenete
    if y>0:
        v_bal=v
        v_jobb=v-y
    else:
        v_bal=v+y # ez valójában csökkent
        v_jobb=v
    Bal_motor.dc(-v_bal)
    Jobb_motor.dc(v_jobb)    
    wait(5)
    if adatgyűjtés:
        a[n] = [Idő.time(),-Bal_motor.angle(),Jobb_motor.angle(),v,alfa,-v_bal,v_jobb,y]
        n += 1

Bal_motor.stop()
Jobb_motor.stop()
if adatgyűjtés:
    clear()
    PrintLoggedData()
