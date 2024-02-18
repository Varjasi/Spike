from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait
# Initialize motors on port A and B.
track_motor = Motor(Port.A)
gripper_motor = Motor(Port.B)

hub = PrimeHub()
# Make both motors run at 500 degrees per second.
track_motor.run(500)
gripper_motor.run(500)
gripper_motor.angle(500)
a = hub.battery.voltage

print(a)

# Wait for three seconds.
wait(3000)