from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.tools import multitask, run_task

hub = InventorHub()

Markoló_motor = Motor(Port.C)
print("Indulok")
hub.speaker.beep(440,100)
Markoló_motor.run_until_stalled(-180,then=Stop.COAST,duty_limit=50)
Markoló_motor.reset_angle(0)
Markoló_motor.run_angle(180,100) #,Stop=Stop.HOLD,wait=True)
hub.speaker.beep(220,100)
print("Vége")
wait(1000)


