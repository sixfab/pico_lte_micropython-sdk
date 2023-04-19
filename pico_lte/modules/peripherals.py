"""
Module for incuding periheral hardware functions of picocell module.
"""

from machine import Pin, I2C
from neopixel import NeoPixel


class Periph:
    """
    Class for inculding periheral hardware functions of picocell module.
    """
    user_button = Pin(21, Pin.IN)
    user_led = Pin(22, Pin.OUT)
    pico_led = Pin("LED", Pin.OUT)
    neopixel = Pin(15, Pin.OUT)

    qwiic = I2C(0, scl=Pin(17), sda=Pin(16), freq=400_000)

    def __init__(self):
        """
        Constructor for Periph class
        """

    def read_user_button(self):
        """
        Function for reading user button

        Returns
        -------
        status : int
            User button status
        """
        return self.user_button.value()

    def adjust_neopixel(self, red, green, blue):
        """
        Function for adjusting neopixel color and brightness

        Parameters
        ----------
        red : int
            Red color value (0-255)
        green : int
            Green color value (0-255)
        blue : int
            Blue color value (0-255)
        """
        neopixel = NeoPixel(self.neopixel, 8)
        neopixel[0] = (red, green, blue)
        neopixel.write()

    def qwiic_scan(self):
        """
        Function for scanning QWIIC devices
        """
        return self.qwiic.scan()
