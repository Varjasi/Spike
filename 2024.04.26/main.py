import asyncio
import contextlib
import os
from usys import stdout

# must before tqdm import!
os.environ["TQDM_DISABLE"] = "1"

lista = []
bemenet = input("Adj meg 3 értéket")
index = 0
while index < 3:
     bemenet = input("Adj meg egy újabb értéket")
     lista.append(bemenet)
     index += 1

from pybricksdev.ble import find_device
from pybricksdev.connections.pybricks import PybricksHub


async def connect_to_hub():
    try:
        device = await find_device()
        hub = PybricksHub()
        await hub.connect(device)
        return hub
    except asyncio.TimeoutError:
        raise RuntimeError("Nem található eszköz")
    except OSError:
        raise RuntimeError("Kapcsold be a bluetooth-t!")


async def send_command(hub: PybricksHub, cmd: str):
    line = await asyncio.wait_for(hub.read_line(), timeout=5)

    if line != "OK":
        raise RuntimeError(f"Unexpected response: '{line}'")

    await hub.write_line(cmd)


async def stop_if_running(hub: PybricksHub):
    try:
        await hub.stop_user_program()
    except Exception:
        # ignore error, e.g. if hub is already disconnected
        pass


async def main():
    async with contextlib.AsyncExitStack() as stack:
        hub = await connect_to_hub()
        stack.push_async_callback(hub.disconnect)

        await hub.run("pontodáigmegy.py", print_output=True, wait=False)
        stack.push_async_callback(stop_if_running, hub)
        await send_command(hub, lista)
        await asyncio.sleep(3)
        await send_command(hub, lista)
        await asyncio.sleep(3)
        await send_command(hub, lista)


asyncio.run(main())


