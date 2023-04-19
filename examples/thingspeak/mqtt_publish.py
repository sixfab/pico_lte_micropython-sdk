"""
Example code for publishing data to ThingSpeak channel by using SDK funtions.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "thingspeak": {
        "channel_id": "[YOUR_CHANNEL_ID]",
        "mqtts": {
            "client_id": "[DEVICE_MQTT_CLIENT_ID]",
            "username": "[DEVICE_MQTT_USERNAME]",
            "password": "[DEVICE_MQTT_PASSWORD]",
            "pub_topic": "[YOUR_MQTT_TOPIC]"
        }
    }
}
"""
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

payload = {"field1": 30, "field2": 40, "status": "PicoLTE_THINGSPEAK_EXAMPLE"}

debug.info("Publishing data to ThingSpeak...")
result = picoLTE.thingspeak.publish_message(payload)
debug.info("Result:", result)
