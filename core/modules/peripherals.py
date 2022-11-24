"""
Module for incuding periheral hardware functions of picocell module.
"""

from machine import Pin, I2C, ADC
from neopixel import NeoPixel

class Periph:
    """
    Class for inculding periheral hardware functions of picocell module.
    """
    battery_voltage_pin = Pin(29, Pin.IN)
    battery_charge_status_pin = Pin(25, Pin.IN)
    user_button_pin = Pin(2, Pin.IN)
    neopixel_pin = Pin(10, Pin.OUT)

    qwiic_sda_pin = Pin(6)
    qwiic_scl_pin = Pin(7)
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

    def get_battery_voltage(self):
        """
        Function for getting battery voltage

        Returns
        -------
        voltage : float
            Battery voltage
        """
        adc_module = ADC(self.battery_voltage_pin)
        raw_16_bit = adc_module.read_u16()
        value_in_volts = (raw_16_bit / 65535) * 3.3
        return value_in_volts

    def get_charge_status(self):
        """
        Function for getting charge status

        Returns
        -------
        status : int
            Charge status
        """
        return self.battery_charge_status_pin.value()

    def qwiic_scan(self):
        """
        Function for scanning QWIIC devices
        """
        return self.qwiic.scan()
