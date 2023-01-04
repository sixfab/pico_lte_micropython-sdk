"""
Example code for subscribing topics for Thingspeak and
recerving data from Thingspeak channel by using MQTT.

Example Configuration
---------------------
Create a config.json file in the root directory of the picocell device.
config.json file must include the following parameters for this example:

config.json
{
    "thingspeak": {
        "channel_id": "[YOUR_CHANNEL_ID]",
        "mqtts": {
            "client_id": "[DEVICE_MQTT_CLIENT_ID]",
            "username": "[DEVICE_MQTT_USERNAME]",
            "password": "[DEVICE_MQTT_PASSWORD]",
            "sub_topics": [
                ["[YOUR_MQTT_TOPIC]", [QOS]]
            ]
        }
    }
}
"""
import time
from core.crux import Crux
from core.temp import debug
from core.utils.enums import Status

crux = Crux()

debug.info("Subscribing to topics...")
result = crux.thingspeak.subscribe_topics()
debug.info("Result:", result)


if result.get("status") == Status.SUCCESS:
    # Check is there any data in subscribed topics
    # in each 5 seconds for 5 times
    debug.info("Reading messages from subscribed topics...")
    for _ in range(0, 5):
        result = crux.thingspeak.read_messages()
        debug.info(result.get("messages"))
        time.sleep(5)
