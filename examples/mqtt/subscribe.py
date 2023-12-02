"""
Example code for subcribing to topic(s) of an MQTT broker.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "mqtts":{
        "host":"[HOST_ADDRESS]",
        "port": [PORT_NUMBER],
        "client_id": "[CLIENT_ID]",
        "username":"[MQTT_USERNAME]",
        "password":"[MQTT_PASSWORD]",
        "sub_topics": [
                ["[YOUR_MQTT_TOPIC_1]", [QoS]],
                ["[YOUR_MQTT_TOPIC_2]", [QoS]],
                ...
            ]
    },
}

- [HOST_ADDRESS] could be an IP address or a domain name (without "mqtt://").
- "client_id", "username" and "password" are optional. If your MQTT broker does not require authentication, you can skip these parameters.
- [QoS] is the quality of service level for the message and can be 0, 1 or 2.
"""

import time
from pico_lte.utils.status import Status
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

picoLTE.network.register_network()
picoLTE.network.get_pdp_ready()
picoLTE.mqtt.open_connection()
picoLTE.mqtt.connect_broker()

debug.info("Subscribing to topics...")
result = picoLTE.mqtt.subscribe_topics()
debug.info("Result:", result)

if result["status"] == Status.SUCCESS:
    # Check is there any data in subscribed topics in each 5 seconds for 5 times
    debug.info("Reading messages from subscribed topics...")
    for _ in range(0, 5):
        result = picoLTE.mqtt.read_messages()
        debug.info(result["messages"])
        time.sleep(5)
