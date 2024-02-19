from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

def indít():
    # Initialize motors on port A and B.
    track_motor = Motor(Port.A)
    gripper_motor = Motor(Port.B)

    # Make both motors run at 500 degrees per second.
    track_motor.run(-500)
    gripper_motor.run(500)

    # Wait for three seconds.
    wait(3000)
    def call():
        import subprocess
        subprocess.run("pybricksdev run ble motor Alapvető parancsok\definálása.py")
    call()


indít()