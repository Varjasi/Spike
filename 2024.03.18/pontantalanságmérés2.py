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
    print(f'A kezdeti szög: \n {hub.imu.heading()}')
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
            print(f'Végszög: \n {hub.imu.heading()}')
            break
        wait(10)

egyenesmozgás(800, 200, 200)