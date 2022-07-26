from machine import Pin

class Periph:
    battery_voltage_pin = Pin(29, Pin.IN)
    battery_charge_status_pin = Pin(25, Pin.IN)
    def __init__(self):
        print("Peripherals initialized")

    def get_battery_voltage(self):
        raw = self.battery_voltage_pin.value()
        calc = raw * (3.3 / 1024)
        return calc

    def get_charge_status(self):
        return self.battery_charge_status_pin.value()
