from pybricks.tools import *
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

def indít():
    # Initialize motors on port A and B.
    track_motor = Motor(Port.A)
    B_motor = Motor(Port.B)
    #B_motor = Motor(Port.B)
    track_motor.control.target_tolerances(500, 1000)
    print("Demo of run_time")
    track_motor.run(500)
    B_motor.run(-500)
    wait(1500)
    

        # Make both motors run at 500 degrees per second.
        # Run at 500 deg/s for 90 degrees.
    '''
    print("Demo of run_angle")
    track_motor.run_angle(500, 90)
    B_motor.run_angle(500, 90)
    wait(1500)

    # Run at 500 deg/s back to the 0 angle
    print("Demo of run_target to 0")
    track_motor.run_target(500, 0)
    B_motor.run_target(500, 0)
    wait(1500)

    # Wait for three seconds.
    wait(3000)
    '''
    def call():
        import subprocess
        subprocess.run("pybricksdev run ble motor.py")
    call()


indít()