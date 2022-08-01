"""
Main code file.
"""

import time
import json
from core.modem import Modem
from core.temp import config, debug


HOST = "a2q4ztq1aigmmt-ats.iot.us-west-2.amazonaws.com"
PORT = 8883
TOPIC = "$aws/things/picocell_test/shadow/update"
PAYLOAD_JSON = {"state": {"reported": {"Status": "Test message from Picocell!"}}}
payload = json.dumps(PAYLOAD_JSON)

DELAY = 0.2

modem = Modem()
modem.ulp.enable()
modem.ulp.set_deep_sleep_period(2)

modem.peripherals.adjust_neopixel(255, 0, 0)
time.sleep(1)
modem.ulp.check()
time.sleep(1)

def main():
    debug.print("Starting...")
    debug.print(config)

    while True:
        modem.peripherals.adjust_neopixel(255, 0, 0)
        time.sleep(DELAY)
        modem.peripherals.adjust_neopixel(0, 255, 0)
        time.sleep(DELAY)
        modem.peripherals.adjust_neopixel(0, 0, 255)
        time.sleep(DELAY)
        modem.peripherals.adjust_neopixel(255, 255, 255)
        time.sleep(DELAY)
        modem.ulp.deep_sleep()


if __name__ == "__main__":
    main()
    pass
