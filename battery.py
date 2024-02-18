from pybricks.hubs import PrimeHub
from pybricks.tools import wait

# Initialize the hub.
hub = PrimeHub()

a = hub.battery.voltage

b = hub.battery.current

print(f'Az akkumlátor feszültsége: {a} \n Az akkumlátor áramerőssége: {b}')