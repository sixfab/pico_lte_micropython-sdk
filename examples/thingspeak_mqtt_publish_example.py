"""
Example code for publishing data to ThingSpeak channel by using SDK funtions.
"""
import time

from core.modem import Modem
from core.temp import debug

modem = Modem()
debug.set_debug_level(0)

while True:
    payload = {
        "field1": 30,
        "field2": 40,
        "status": "PICOCELL_THINGSPEAK_EXAMPLE"
        }

    result = modem.thingspeak.publish_message(payload)

    debug.info(result)
    time.sleep(10)
    