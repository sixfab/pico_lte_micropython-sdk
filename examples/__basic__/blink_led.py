"""

Example code for blinking the USER LED.

"""

import machine
import utime

led = machine.Pin(22, machine.Pin.OUT)

while True:
    led.toggle()
    utime.sleep(1)