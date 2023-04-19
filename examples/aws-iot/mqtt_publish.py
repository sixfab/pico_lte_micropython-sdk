"""
Example code for publising data to AWS IoT by using MQTT.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "aws":{
        "mqtts":{
            "host":"[YOUR_AWSIOT_ENDPOINT]",
            "port":"[YOUR_AWSIOT_MQTT_PORT]",
            "pub_topic":"[YOUR_MQTT_TOPIC]",
        }
    }
}
"""
import json
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

payload_json = {"state": {"reported": {"App": "AWS MQTT Example"}}}

debug.info("Publishing data to AWS IoT...")
payload = json.dumps(payload_json)
result = picoLTE.aws.publish_message(payload)
debug.info("Result", result)
