"""

Example code for rainbow effect on NeoPixel LED.

"""


import machine
import neopixel
import utime

NUM_LEDS = 8
pin = machine.Pin(15)
np = neopixel.NeoPixel(pin, NUM_LEDS)

# Function for rainbow effect
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            np[i] = wheel(rc_index & 255)  # Set LED color using wheel function
        np.write()
        utime.sleep_ms(wait)

def wheel(pos):
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)  # Red to Green transition
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)  # Green to Blue transition
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)  # Blue to Red transition

while True:
    rainbow_cycle(20)  # Call the rainbow effect function with a delay of 20 milliseconds