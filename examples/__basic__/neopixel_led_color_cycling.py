"""

Example code for color cycling on NeoPixel LED.

"""

import machine
import neopixel
import utime

NUM_LEDS = 8
pin = machine.Pin(15)
np = neopixel.NeoPixel(pin, NUM_LEDS)

def color_cycle(wait):
    for i in range(NUM_LEDS):
        np[i] = (255, 0, 0)  # Set LED color to red
    np.write()
    utime.sleep_ms(wait)  # Wait for a short duration
    
    for i in range(NUM_LEDS):
        np[i] = (0, 255, 0)  # Set LED color to green
    np.write()
    utime.sleep_ms(wait)  # Wait for a short duration
    
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 255)  # Set LED color to blue
    np.write()
    utime.sleep_ms(wait)  # Wait for a short duration

while True:
    color_cycle(100)  # Call the color cycle function with a delay of 100 milliseconds