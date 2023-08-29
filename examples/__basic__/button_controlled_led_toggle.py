"""

Example code for button controlled LED toggle.
When the USER button is pressed, the light turns on. When the button is not pressed, the light turns off.

"""

import machine
import utime

led = machine.Pin(22, machine.Pin.OUT)  # We set up the pin to control the light.
button = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)  # We set up the pin for the button.

while True:
    if button.value() == 0:  # If the button is pressed (value is 0):
        led.on()  # Turn on the light.
    else:  # If the button is not pressed (value is 1):
        led.off()  # Turn off the light.
    utime.sleep(0.1)  # Wait for a short moment before checking again.