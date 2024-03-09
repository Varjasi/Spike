import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait

def terepzöld():
    a = szín.hsv()
    return(bool(a.h>130 and a.h<140 and a.s>40 and a.s<50))

def terepkék():
    a = szín.hsv()
    return(bool(a.h>219 and a.h<241 and a.s>35 and a.s<52))


szín = ColorSensor(Port.D)
hub = PrimeHub()

#Vészcsengő
dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
hub.speaker.play_notes(dallam, tempo=400)

#Szö elfordulása

print(f'Kezdeti szög: {hub.imu.heading()} \n')

Bal_motor = Motor(Port.B)
Jobb_motor = Motor(Port.A)

    # Make both motors run at 500 degrees per second.
kezdőszög = Bal_motor.angle()
    #sebesség = int(input("Adj meg egy sebességet!"))

wheel_diameter = float(55.8) #mm
distance_to_degree = 360/3.1416/wheel_diameter
v=180


dist=50
Bal_motor.run_angle(-v, dist*distance_to_degree, then=Stop.NONE, wait=False)
Jobb_motor.run_angle(v, dist*distance_to_degree, then=Stop.NONE, wait=True)

# jobb kanyar
S_bal = 70*3 #mm
S_jobb = 20*3 #mm
Bal_motor.run_angle(-v, S_bal*distance_to_degree, then=Stop.NONE, wait=False)
Jobb_motor.run_angle(v*S_jobb/S_bal, S_jobb*distance_to_degree, then=Stop.NONE, wait=True)

dist=100
Bal_motor.run_angle(-v, dist*distance_to_degree, then=Stop.NONE, wait=False)
Jobb_motor.run_angle(v, dist*distance_to_degree, then=Stop.NONE, wait=True)
print(f'Középszög: {hub.imu.heading()} \n')
# bal kanyar
S_bal = 20*3 #mm
S_jobb = 70*3 #mm
Bal_motor.run_angle(-v*S_bal/S_jobb, S_bal*distance_to_degree, then=Stop.NONE, wait=False)
Jobb_motor.run_angle(v, S_jobb*distance_to_degree, then=Stop.NONE, wait=True)

dist=400
Bal_motor.run_angle(-v, dist*distance_to_degree, then=Stop.NONE, wait=False)
Jobb_motor.run_angle(v, dist*distance_to_degree, then=Stop.NONE, wait=False)

while True:
    if terepzöld():
        break
    elif terepkék():
        break

Jobb_motor.stop()
Bal_motor.stop()
szín.lights.off()
        


végszög = Bal_motor.angle()

print(f'Végszög: {hub.imu.heading()} \n')
hub.imu.reset_heading(0)
