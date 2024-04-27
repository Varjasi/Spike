from pybricks.pupdevices import Motor
from pybricks.parameters import Port

# Standard MicroPython modules
from usys import stdin

motor = Motor(Port.A)

while True:
    # let PC know we are ready for a command
    print("OK")

    # wait for command from PC
    cmd = stdin.readline().strip()

    # Decide what to do based on the command.
    if cmd == "50":
        motor.dc(50)
    elif cmd == "rev":
        motor.dc(-50)
    elif cmd == "bye":
        break