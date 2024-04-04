"""
Example code for publising data to HiveMQ by using MQTT.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "hivemq": {
        "mqtts":{
            "client_id": "[DEVICE_MQTT_CLIENT_ID]",
            "url":"[YOUR_URL]",
            "port": [PORT_NUMBER],
            "username": "[HIVEMQ_USERNAME]",
            "password": "[HIVEMQ_PASSWORD]",
            "pub_topic": "[YOUR_PUBLISH_TOPIC]"
         }
    }
}
"""

from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

payload = "Hello HiveMQ! This is a test message."

debug.info("Publishing data to HiveMQ...")
result = picoLTE.hivemq.publish_message(payload)
debug.info("Result", result)

