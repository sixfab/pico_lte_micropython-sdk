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
        "username": "[DEVICE_MQTT_USERNAME]",
        "password": "[DEVICE_MQTT_PASSWORD]",
        "field_no": [FIELD_NO_INTEGER],
    }
}
"""
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

debug.info("Publishing data to ThingSpeak...")
result = picoLTE.thingspeak.publish_message(40)
debug.info("Result:", result)
