from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.tools import multitask, run_task
from umath import pi
'''
Tanulságok:
- ha gyorsan megy driftel, pontatlan lesz a kanyar
- ha a gyorsulást próbáljuk meg visszavenni, rosszul működik a szabályozója
'''
hub = InventorHub()
Jobb_motor = Motor(Port.A)
Bal_motor = Motor(Port.B)
kerékátmérő = 56
tengelytáv = 93
fok_út = 360/pi/kerékátmérő

def kanyar(sebesség,sugár,szög):
    v = sebesség * fok_út / sugár
    v_jobb = v*(sugár+tengelytáv/2)
    v_bal = v*(sugár-tengelytáv/2)
    szög_jobb = szög*(sugár+tengelytáv/2)/(kerékátmérő/2)
    szög_bal = szög*(sugár-tengelytáv/2)/(kerékátmérő/2)
    Jobb_motor.run_angle(-v_jobb,szög_jobb,Stop.HOLD,wait=False)
    Bal_motor.run_angle(v_bal,szög_bal,Stop.HOLD,wait=True)

print("Indulok")
hub.speaker.beep(440,100)
hub.imu.reset_heading(0)

Bal_motor.control.limits(acceleration=1000)
Jobb_motor.control.limits(acceleration=1000)
Bal_motor.control.pid(kd=5000)
kanyar(100,100,360)
Bal_motor.control.pid(kd=1889)
hub.speaker.beep(220,100)
print(hub.imu.heading())
print("Vége")
wait(100)


