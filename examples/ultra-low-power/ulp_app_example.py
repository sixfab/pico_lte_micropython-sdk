"""
Example code to find out ultra low power concept of the
picocell SDK and how to use it. This example imitates the
real jobs with a neopixel indicator function. Please change
the job() function with yours.

The SDK and the picocell hardware have same pre-configured
settings. Min control period is the most important preset in
this case. Min control period is 5 mins. This means, SDK checks
the wakeup reason every 5 mins. You can adjust the sleep period
with power of 5 mins.
"""

import time
from core.crux import Crux
from core.temp import debug

DELAY = 0.2

crux = Crux()

# ULP setup
modem.ulp.enable()  # enable ultra low power mode
modem.ulp.set_deep_sleep_period(5)  # set sleep period

# Do ULP check every reboot
modem.peripherals.adjust_neopixel(255, 0, 0)  # indicator led
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
    modem.ulp.deep_sleep()  # go to sleep
