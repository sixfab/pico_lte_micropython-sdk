"""
Example code for subcribing to topic(s) of an MQTT broker.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "thingsboard": {
        "host":"[HOST_ADDRESS]",
        "port": [PORT_NUMBER],
        "device":"[YOUR_MQTT_DEVICE]",
        "username": "[DEVICE_MQTT_USERNAME]",
        "password": "[DEVICE_MQTT_PASSWORD]",
        "topics": [
                ["[YOUR_MQTT_TOPIC_1]", [QoS]],
                ["[YOUR_MQTT_TOPIC_2]", [QoS]],
                ...
            ]
    },
}

- [HOST_ADDRESS] could be an IP address or a domain name (without "mqtt://").
- Username must be ACCESS_TOKEN.
- [QoS] is the quality of service level for the message and can be 0, 1 or 2.
"""

import time
from pico_lte.core import PicoLTE
from pico_lte.common import debug
from pico_lte.utils.status import Status

picoLTE = PicoLTE()
debug.set_level(0)

debug.info("Subscribing to topics...")
result = picoLTE.thingsboard.subscribe_topics()
debug.info("Result:", result)


debug.info("Reading messages from subscribed topics...")
for _ in range(0, 5):
    result = picoLTE.thingsboard.read_messages()
    debug.info(result.get("messages"))
    time.sleep(5)
