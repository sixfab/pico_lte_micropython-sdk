"""
Example code for subscribing topics from Azure IoT Hub by using MQTT.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "azure":{
        "hub_name": "[YOUR_AZURE_IOT_HUB_NAME]",
        "device_id": "[YOUR_DEVICE_ID]",
        "mqtts": {
            "sub_topics": [
                ["[SUB_TOPIC/1]", [QOS]],
                ["[SUB_TOPIC/2]", [QOS]],
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
result = picoLTE.azure.subscribe_topics()
debug.info(result)

if result.get("status") == Status.SUCCESS:
    debug.info("Reading messages from subscribed topics...")
    # Check is there any data in subscribed topics
    # in each 5 seconds for 5 times
    for _ in range(0, 5):
        result = picoLTE.azure.read_messages()
        debug.info(result.get("messages"))
        time.sleep(5)
