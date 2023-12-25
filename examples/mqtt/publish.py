"""
Example code for publishing data to an MQTT broker.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "mqtts":{
        "host":"[HOST_ADDRESS]",
        "port": [PORT_NUMBER],
        "pub_qos": [QoS],
        "client_id": "[CLIENT_ID]",
        "username":"[MQTT_USERNAME]",
        "password":"[MQTT_PASSWORD]"
    },
}

- [HOST_ADDRESS] should be an IP address or a domain name (without "mqtt://").
- [QoS] is the quality of service level for the message and can be 0, 1 or 2. Default value is 1.
- "client_id", "username" and "password" are optional. If your MQTT broker does not require authentication, you can skip these parameters.
"""

from pico_lte.utils.status import Status
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

picoLTE.network.register_network()
picoLTE.network.get_pdp_ready()
picoLTE.mqtt.open_connection()
picoLTE.mqtt.connect_broker()

debug.info("Publishing a message.")

# PAYLOAD and TOPIC have to be in string format.
PAYLOAD = "[PAYLOAD_MESSAGE]"
TOPIC = "[TOPIC_NAME]"

# Publish the message to the topic.
result = picoLTE.mqtt.publish_message(PAYLOAD, TOPIC)
debug.info("Result:", result)

if result["status"] == Status.SUCCESS:
    debug.info("Publish succeeded.")
