from micropython import mem_info
from pybricks.tools import wait
import pybricks.hubs

hub = pybricks.hubs()


# Print memory usage.
while True:
    mem_info(
    wait(1000)