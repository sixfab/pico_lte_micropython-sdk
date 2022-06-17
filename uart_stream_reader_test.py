import uasyncio as asyncio
from machine import UART, Pin

uart = UART(
            0,
            tx = Pin(0),
            rx = Pin(1),
            baudrate=115200,
            )

async def receiver():
    sreader = asyncio.StreamReader(uart)
    while True:
        res = await sreader.readline()
        print('Recieved', res)

loop = asyncio.get_event_loop()
#loop.create_task(sender())
loop.create_task(receiver())
loop.run_forever()

