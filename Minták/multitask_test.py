from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.tools import multitask, run_task

hub = InventorHub()

idő = StopWatch()

#Vészcsengő
async def zene():
    hub.speaker.volume(10)
    #await hub.speaker.beep(440,1000)
    dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
    #for x in dallam
    await hub.speaker.play_notes(dallam, tempo=120)


async def mozgat():
    kívántszög = hub.imu.heading()
    #sebesség_szöveg=input("Semmit")
    #v=int(sebesség_szöveg)
    v=200
    szögszab = 2
    while True:    
        await wait(1)
        szög = hub.imu.heading() #CCW (Azaz: Óra járással ellentétes a pozitív irány)
        delta_v = (kívántszög - szög) * szögszab
        Bal_motor.run(v-delta_v)    
        Jobb_motor.run(-v-delta_v) 
        if idő.time() > 12000:   
            break 
        elif idő.time() > 9000:
            kívántszög = 90
        elif idő.time() > 3000:
            kívántszög = 45

# Drive forward, turn move gripper at the same time, and drive backward.
async def main():
    await multitask(mozgat(), zene())
    #await zene()
    #await mozgat()

Jobb_motor = Motor(Port.A)
Bal_motor = Motor(Port.B)    
hub.speaker.beep(440,100)
run_task(main())
print("Vége")
wait(1000)
hub.speaker.beep(220,100)
wait(1000)

