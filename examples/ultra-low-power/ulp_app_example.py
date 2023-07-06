"""
Example code to find out ultra low power concept of the
PicoLTE SDK and how to use it. This example imitates the
real jobs with a neopixel indicator function. Please change
the job() function with yours.

The SDK and the PicoLTE hardware have same pre-configured
settings. Min control period is the most important preset in
this case. Min control period is 5 mins. This means, SDK checks
the wakeup reason every 5 mins. You can adjust the sleep period
with power of 5 mins.
"""

import time
from pico_lte.core import PicoLTE
from pico_lte.common import debug

DELAY = 0.2

picoLTE = PicoLTE()

# ULP setup
picoLTE.ulp.enable()  # enable ultra low power mode
picoLTE.ulp.set_deep_sleep_period(5)  # set sleep period

# Do ULP check every reboot
picoLTE.peripherals.adjust_neopixel(255, 0, 0)  # indicator led
time.sleep(1)
picoLTE.ulp.check()
time.sleep(1)


def job():
    """
    Example job function. Change it with yours. This one may be pushing
    data to cloud service or mailing some data to someone etc.
    """
    debug.info("Doing the job...")
    picoLTE.peripherals.adjust_neopixel(255, 0, 0)
    time.sleep(DELAY)
    picoLTE.peripherals.adjust_neopixel(0, 255, 0)
    time.sleep(DELAY)
    picoLTE.peripherals.adjust_neopixel(0, 0, 255)
    time.sleep(DELAY)
    picoLTE.peripherals.adjust_neopixel(255, 255, 255)
    time.sleep(DELAY)


while True:
    job()
    picoLTE.ulp.deep_sleep()  # go to sleep
