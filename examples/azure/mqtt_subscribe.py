"""
Example code for subscribing topics from Azure IoT Hub by using MQTT.

Example Configuration
---------------------
Create a config.json file in the root directory of the picocell device.
config.json file must include the following parameters for this example:

config.json
{
    "azure":{
        "hub_name": "[YOUR_AZURE_IOT_HUB_NAME]",
        "device_id": "[YOUR_DEVICE_ID]",
        "mqtts": {
            "host": "[YOUR_AZURE_ENDPOINT]",
            "port": 8883,
            "sub_topics": [
                ["[SUB_TOPIC/1]", [QOS]],
                ["[SUB_TOPIC/2]", [QOS]],
            ],
            "username": "[YOUR_HUB_NAME].azure-devices.net/[YOUR_DEVICE_ID]/?api-version=2021-04-12",
            "client_id": "[YOUR_DEVICE_ID]"
        }
    }
}

Note that "mqtts" attribute is optional. To connect your IoT Hub, "hub_name" and
"device_id" is the only ones needed.
"""
import time
from core.crux import Crux
from core.temp import debug
from core.utils.status import Status

crux = Crux()

debug.info("Subscribing to topics...")
result = crux.azure.subscribe_topics()
debug.info(result)

if result.get("status") == Status.SUCCESS:
    debug.info("Reading messages from subscribed topics...")
    # Check is there any data in subscribed topics
    # in each 5 seconds for 5 times
    for _ in range(0, 5):
        result = crux.azure.read_messages()
        debug.info(result.get("messages"))
        time.sleep(5)
