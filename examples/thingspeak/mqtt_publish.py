"""
Example code for publishing data to ThingSpeak channel by using SDK funtions.

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
            "pub_topic": "[YOUR_MQTT_TOPIC]"
        }
    }
}
"""
from core.modules.modem import Modem
from core.temp import debug

modem = Modem()

payload = {"field1": 30, "field2": 40, "status": "PICOCELL_THINGSPEAK_EXAMPLE"}

debug.info("Publishing data to ThingSpeak...")
result = modem.thingspeak.publish_message(payload)
debug.info("Result:", result)
