import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait
from pybricks.tools import StopWatch
hub = PrimeHub()
#Vészcsengő
dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
hub.speaker.play_notes(dallam, tempo=400)

#hub.display.text("hello", on=500, off=50)

#Szögek


marok = Motor(Port.F)

'''
marok.run_until_stalled(-100, Stop.BRAKE, duty_limit=100) #duty lmit = mennyi feszültséget adjon a motorra
wait(5000)
marok.reset_angle(0)
marok.run_angle(100, 150, Stop.BRAKE, duty_limit=100) #duty lmit = mennyi feszültséget adjon a motorra
print(marok.angle())


#marok.run_until_stalled(100, Stop.BRAKE, duty_limit=100) #duty lmit = mennyi feszültséget adjon a motorra
#wait(5000)
marok.run_until_stalled(-100, Stop.BRAKE, duty_limit=100) #duty lmit = mennyi feszültséget adjon a motorra
wait(5000)
'''
def markolóalapállapot():
    marok.run_until_stalled(-200, Stop.BRAKE, duty_limit=100) #duty lmit = mennyi feszültséget adjon a motorra
    marok.reset_angle(0)

def markolózár():
    marok.run_target(200, 150, Stop.BRAKE, wait=True)

markolóalapállapot()
wait(1000)
markolózár()
print(marok.angle())