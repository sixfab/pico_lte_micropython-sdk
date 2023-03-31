"""
Module for incuding periheral hardware functions of picocell module.
"""

from machine import Pin, I2C
from neopixel import NeoPixel


class Periph:
    """
    Class for inculding periheral hardware functions of picocell module.
    """
    user_button_pin = Pin(27, Pin.IN)
    neopixel_pin = Pin(20, Pin.OUT)

    qwiic_sda_pin = Pin(21)
    qwiic_scl_pin = Pin(22)
    qwiic = I2C(1, scl=qwiic_scl_pin, sda=qwiic_sda_pin, freq=400_000)

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
        return self.user_button_pin.value()

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
        neopixel = NeoPixel(self.neopixel_pin, 8)
        neopixel[0] = (red, green, blue)
        neopixel.write()

    def qwiic_scan(self):
        """
        Function for scanning QWIIC devices
        """
        return self.qwiic.scan()
