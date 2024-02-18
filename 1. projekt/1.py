from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

# Initialize motors on port A and B.
track_motor = Motor(Port.A)
gripper_motor = Motor(Port.B)

#1. forduljon jobbra (90°-ot)
track_motor.angle(90)
# Make both motors run at 500 degrees per second.
track_motor.run(150)
gripper_motor.run(150)

gripper_motor.angle(90)

track_motor.run(150)
gripper_motor.run(150)
# Wait for three seconds.
wait(3000)