import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop
from pybricks.tools import wait

def indít():
    # Initialize motors on port A and B.
    Jobb_motor = Motor(Port.A, )
    Bal_motor = Motor(Port.B)

    # Make both motors run at 500 degrees per second.
    Jobb_motor.run_angle(-360, 360, wait=False)
    Bal_motor.run_angle(200, 360, then=Stop.HOLD, wait=False)

    # Wait for three seconds.
    wait(1000)
    def call():
        import subprocess
        subprocess.run("pybricksdev run ble motor.py")
    call()


indít()