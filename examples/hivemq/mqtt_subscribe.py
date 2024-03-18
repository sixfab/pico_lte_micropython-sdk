"""
Example code for subscribing MQTT topics on HiveMQ
and reading data from them.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "hivemq": {
        "mqtts":{
            "url":"[YOUR_URL]",
            "port": [PORT_NUMBER],
            "username": "[HIVEMQ_USERNAME]",
            "password": "[HIVEMQ_PASSWORD]",
            "sub_topics": [
                    ["[YOUR_MQTT_TOPIC_1]",
                    ["[YOUR_MQTT_TOPIC_2]",
                    ...
                ]
         }
    }
}
"""

import time
from pico_lte.core import PicoLTE
from pico_lte.common import debug
from pico_lte.utils.status import Status

picoLTE = PicoLTE()

debug.info("Subscribing to topics...")
result = picoLTE.hivemq.subscribe_topics()
debug.info(result)

if result.get("status") == Status.SUCCESS:
    debug.info("Reading messages from subscribed topics...")
    # Check is there any data in subscribed topics
    # in each 5 seconds for 5 times
    for _ in range(0, 5):
        result = picoLTE.hivemq.read_messages()
        debug.info(result.get("messages"))
        time.sleep(5)
