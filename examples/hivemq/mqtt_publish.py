"""
Example code for publising data to HiveMQ by using MQTT.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "hivemq": {
        "host":"[CLUSTER_URL]",
        "port": [PORT_NUMBER],
        "username": "[MQTT_USERNAME]",
        "password": "[MQTT_PASSWORD]"
    }
}
"""

from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

payload = "Hello HiveMQ! This is a test message."

debug.info("Publishing data to HiveMQ...")
result = picoLTE.hivemq.publish_message(payload, topic="topic")
debug.info("Result", result)
