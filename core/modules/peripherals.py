"""
Module for incuding periheral hardware functions of picocell module.
"""

from machine import Pin

class Periph:
    """
    Class for inculding periheral hardware functions of picocell module.
    """
    battery_voltage_pin = Pin(29, Pin.IN)
    battery_charge_status_pin = Pin(25, Pin.IN)

    def __init__(self):
        """
        Constructor for Periph class
        """
        print("Peripherals initialized")

    def get_battery_voltage(self):
        """
        Function for getting battery voltage

        Returns
        -------
        voltage : float
            Battery voltage
        """
        raw = self.battery_voltage_pin.value()
        calc = raw * (3.3 / 1024)
        return calc

    def get_charge_status(self):
        """
        Function for getting charge status

        Returns
        -------
        status : int
            Charge status
        """
        return self.battery_charge_status_pin.value()
