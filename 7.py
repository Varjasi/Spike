from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

def indít():
        # Initialize a motor on port A with the positive direction as counterclockwise.
    example_motor = Motor(Port.A)

    example_motor.run(500)

    # This is useful when your motor is mounted in reverse or upside down.
    # By changing the positive direction, your script will be easier to read,
    # because a positive value now makes your robot/mechanism go forward.

    # Wait for three seconds.
    wait(3000)
    def call():
        import subprocess
        #HA MÁSIK PYTHON-FILE-T SZERETNÉL FUTTATNI, MINDIG ÍRD ÁT AZ ÉRTÉKÉT
        subprocess.run("pybricksdev run ble 7.py")
    call()


indít()