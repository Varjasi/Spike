import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop
from pybricks.hubs import PrimeHub
from micropython import *

from pybricks.tools import wait

hub = PrimeHub()
sebesseg = int(input("Adj meg egy sebességet"))
def indít():
    a = hub.battery.voltage()
    print(f'Az akkumlátor feszültsége: {a}')
    # Initialize motors on port A and B.
    #Jobb_motor = Motor(Port.A, )
    Bal_motor = Motor(Port.B)

    # Make both motors run at 500 degrees per second.
    kezdőszög = Bal_motor.angle()
    #sebesség = int(input("Adj meg egy sebességet!"))

    Bal_motor.run_angle(sebesseg, 360, then=Stop.NONE, wait=True)
    Bal_motor.run_angle(360, 360, then=Stop.HOLD, wait=True)
    végszög = Bal_motor.angle()
    print(f'A kezdőszög: {kezdőszög}, a végszög pedig: {végszög}')


    a = hub.battery.voltage()
    print(f'Az akkumlátor feszültsége: {a}')
    # Wait for three seconds.
    wait(1000)
    def call():
        import subprocess
        subprocess.run("pybricksdev run ble motor.py")
    call()


indít()