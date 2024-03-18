from pybricks.hubs import PrimeHub
hub = PrimeHub()
index = 0
while index < 255:   
    print(hub.ble.signal_strength(index))
    index += 1

#print(f'Jelerősség:\n{hub.ble.signal_strength(0)}')