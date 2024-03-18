from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop
from pybricks.tools import StopWatch

hub = PrimeHub()
idő = StopWatch()

#Vészcsengő
dallam = ["C4/4", "C4/4", "G4/4", "G4/4"]
hub.speaker.play_notes(dallam, tempo=400)

print(f'A kezdeti szög: \n {hub.imu.heading()}')

Jobb_motor = Motor(Port.A)
Bal_motor = Motor(Port.B)

Bal_motor.run_time(1000, 2500, then=Stop.BRAKE, wait=False)
Jobb_motor.run_time(-1000, 2500, then=Stop.BRAKE, wait=True)

print(f'Végszög: {hub.imu.heading()} \n')
hub.imu.reset_heading(0)