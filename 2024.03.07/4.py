import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait

szín = ColorSensor(Port.D)
hub = PrimeHub()

Bal_motor = Motor(Port.B)
Jobb_motor = Motor(Port.A)

    # Make both motors run at 500 degrees per second.
kezdőszög = Bal_motor.angle()
    #sebesség = int(input("Adj meg egy sebességet!"))

wheel_diameter = float(55.8) #mm
distance_to_degree = 360/3.1416/wheel_diameter
v=180

dist=50
Bal_motor.run_angle(-v, dist*distance_to_degree, then=Stop.HOLD, wait=False)
Jobb_motor.run_angle(v, dist*distance_to_degree, then=Stop.HOLD, wait=True)

# jobb kanyar
S_bal = 70 #mm
S_jobb = 20 #mm
Bal_motor.run_angle(-v, S_bal*distance_to_degree, then=Stop.HOLD, wait=False)
Jobb_motor.run_angle(v*S_jobb/S_bal, S_jobb*distance_to_degree, then=Stop.HOLD, wait=True)

dist=100
Bal_motor.run_angle(-v, dist*distance_to_degree, then=Stop.HOLD, wait=False)
Jobb_motor.run_angle(v, dist*distance_to_degree, then=Stop.HOLD, wait=True)

# bal kanyar
S_bal = 20 #mm
S_jobb = 70 #mm
Bal_motor.run_angle(-v*S_bal/S_jobb, S_bal*distance_to_degree, then=Stop.HOLD, wait=False)
Jobb_motor.run_angle(v, S_jobb*distance_to_degree, then=Stop.HOLD, wait=True)

dist=400
Bal_motor.run_angle(-v, dist*distance_to_degree, then=Stop.HOLD, wait=False)
Jobb_motor.run_angle(v, dist*distance_to_degree, then=Stop.HOLD, wait=False)

while True:
    a = szín.hsv()
    if a.h>340 and a.s>70:
        break

Jobb_motor.stop()
Bal_motor.stop()
szín.lights.off()
        


végszög = Bal_motor.angle()