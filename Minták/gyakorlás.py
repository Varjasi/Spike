import asyncio
import time
async def MethodTwo():
    print("MethodTwo")
    await asyncio.sleep(3)
    print("MethodTwo done")

async def MethodOne():
    print("MethodOne")
    await asyncio.sleep(8.5)
    print("MethodOne done")

async def Main():
    print("Main")
    await MethodOne() #Megvárja, hogy lefusson a függvény, majd utánna csinálja a következőt
    await MethodTwo()

if __name__ == "__main__":
    asyncio.run(Main())