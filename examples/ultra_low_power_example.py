"""
Main code file.
"""

import time
from core.modem import Modem
from core.temp import debug

DELAY = 0.2

modem = Modem()

# ULP setup
modem.ulp.enable() # enable ultra low power mode
modem.ulp.set_deep_sleep_period(5) # set sleep period

# Do ULP check every reboot
modem.peripherals.adjust_neopixel(255, 0, 0) # indicator led
time.sleep(1)
modem.ulp.check()
time.sleep(1)


def job():
    """
    Example job function. Change it with yours. This one may be pushing
    data to cloud service or mailing some data to someone etc.
    """
    debug.info("Doing the job...")
    modem.peripherals.adjust_neopixel(255, 0, 0)
    time.sleep(DELAY)
    modem.peripherals.adjust_neopixel(0, 255, 0)
    time.sleep(DELAY)
    modem.peripherals.adjust_neopixel(0, 0, 255)
    time.sleep(DELAY)
    modem.peripherals.adjust_neopixel(255, 255, 255)
    time.sleep(DELAY)


while True:
    job()
    modem.ulp.deep_sleep() # go to sleep
