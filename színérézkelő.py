from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.pupdevices import ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait

# Initialize the sensor.
sensor = ColorSensor(Port.F)
a_motor = Motor(Port.A)
b_motor = Motor(Port.B)
hub = PrimeHub()

'''
# This is a function that waits for a desired color.
def wait_for_color(desired_color):
    # While the color is not the desired color, we keep waiting.
    while sensor.color() != desired_color:
        a_motor.run(500)
        b_motor.run(500)
        if sensor.color == desired_color:
            print("Goodbye!")
            wait(100)
            # Shut the hub down.
            hub.system.shutdown()

desired_color = "red"
'''

while True:
    print(sensor.color)

