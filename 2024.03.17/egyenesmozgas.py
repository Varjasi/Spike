import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait
Bal_motor = Motor(Port.B)
Jobb_motor = Motor(Port.A)

hub = PrimeHub()
#Vészcsengő
dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
hub.speaker.play_notes(dallam, tempo=400)

kerékátmérő = 56
tengelytáv = 128
distance_to_degree = 360/3.1416/kerékátmérő



def egyenesmozgás(hossz, végsebesség, gyorsulás):
    s1 = (Bal_motor.angle()-Jobb_motor.angle()) / 2 / distance_to_degree
    s2 = s1 + hossz
    v1 = (Bal_motor.speed()-Jobb_motor.speed()) / 2 / distance_to_degree
    dv = gyorsulás * 0.01
    v = v1
    while True:
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

        Bal_motor.run(v * distance_to_degree)
        Jobb_motor.run(-v * distance_to_degree)
        s = (Bal_motor.angle()-Jobb_motor.angle()) / 2 / distance_to_degree
        if s > s2:
            break
        wait(10)

# Kanyarodás állandó sebességgel (giroszkóppal)
def kanyar(szög, sebesség, sugár):
    if szög > 0:
        v_bal = sebesség * (sugár - tengelytáv / 2)/sugár
        v_jobb = sebesség * (sugár + tengelytáv / 2)/sugár
    else:
        v_bal = sebesség * (sugár + tengelytáv / 2)/sugár
        v_jobb = sebesség * (sugár - tengelytáv / 2)/sugár
    szög1 = hub.imu.heading()
    szög2 = szög1 + szög
    Bal_motor.run(v_bal * distance_to_degree)
    Jobb_motor.run(-v_jobb * distance_to_degree)
    while True:
        if szög > 0:
            if hub.imu.heading() > szög2:
                print(szög1, szög2)
                break
        else:
            if hub.imu.heading() < szög2:
                break
'''
egyenesmozgás(400, 200, 1000)
egyenesmozgás(100, 100, 1000)

kanyar(270, 100, 150)
kanyar(-90, 100, 150)
'''
egyenesmozgás(100, 100, 1000)
