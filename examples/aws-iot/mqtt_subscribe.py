"""
Example code for subscribing MQTT topics on AWS IoT
and reading data from them
"""

import time
from core.modem import Modem
from core.temp import debug
from core.utils.status import Status

modem = Modem()

result = modem.aws.subscribe_topics()
debug.info(result)

if result.get("status") == Status.SUCCESS:
    # Check is there any data in subscribed topics
    # in each 5 seconds for 5 times
    for _ in range(0, 5):
        result = modem.aws.read_messages()
        debug.info(result.get("messages"))
        time.sleep(5)
