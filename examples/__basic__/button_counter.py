"""

Example code for basic counter using USER button.
Create a simple counter using a USER Button on the Pico LTE. 
When the button is pressed, the counter increases by one, and the updated value is printed in the terminal.

"""

import machine
import utime

button = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)
counter = 0

while True:
    if button.value() == 0:
        counter += 1
        print("Counter:", counter)
        while button.value() == 0:
            pass  # Wait for the button to be released
        utime.sleep(0.1)