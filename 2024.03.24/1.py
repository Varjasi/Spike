import pybricks as file
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.parameters import Stop
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait

szín = ColorSensor(Port.D)
hub = PrimeHub()
#sebesseg = int(input("Adj meg egy sebességet"))
'''
def indít():
    wait(1000)
    #sebesseg = input("Add meg az sebességet!")
    #print(sebesseg)
    # Initialize motors on port A and B.
    #Jobb_motor = Motor(Port.A, )
    #Bal_motor = Motor(Port.B)

    #Bal_motor.run_time(3000, 3000, then=Stop.NONE, wait=False)
    # Wait for three seconds.
    
    b = 50, 50, 50
    c = 50, 0, 0
    szín.lights.on([100, 0, 0])
    wait(1000)
    szín.lights.on([0,100,0])
    wait(1000)
    szín.lights.on([0,0,100])
    wait(1000)
    szín.lights.on([100, 100, 100])
    wait(1000)
    #Nyomaték
    '''
'''
    T = Bal_motor.load()
    print(f'Nyomaték: \n {T}')
    wait(2000)
    '''
    '''
    '''
    '''
    Measuring color
    '''
    while True:
        
        # Read the color and reflection
        color = szín.hsv()
        #reflection = szín.reflection()

        # Print the measured color and reflection.
        print(color)

        # Move the sensor around and see how
        # well you can detect colors.

        # Wait so we can read the value.
        wait(1000)
        '''
        '''
def call():
    import subprocess
    subprocess.run("pybricksdev run ble 2024.03.07/1.py")
call()


indít()