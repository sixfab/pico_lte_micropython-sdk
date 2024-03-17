"""
Example code for publish topics for ThingsBoard and
recerving data from ThingsBoard channel by using MQTT.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

{
    "thingsboard": {
        "host":"[HOST_ADDRESS]",
        "port": [PORT_NUMBER],
        "pub_topic": "[YOUR_MQTT_TOPIC]",
        "username": "[DEVICE_MQTT_USERNAME]",
        "password": "[DEVICE_MQTT_PASSWORD]",
        "qos": "[QoS]",
    }
}
"""

from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

debug.info("Publishing a message.")


payload = {"device": "temp_sensor", "value_type": "celcius", "area": "indoor", "status": "Temperature value"}

debug.info("Publishing data to ThingsBoard...")
result = picoLTE.thingsboard.publish_message(payload)
debug.info("Result:", result)
