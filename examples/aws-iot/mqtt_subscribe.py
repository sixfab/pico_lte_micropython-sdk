"""
Example code for subscribing MQTT topics on AWS IoT
and reading data from them.

Example Configuration
---------------------
Create a config.json file in the root directory of the picocell device.
config.json file must include the following parameters for this example:

config.json
{
    "aws":{
        "mqtts":{
            "host":"[YOUR_AWSIOT_ENDPOINT]",
            "port":"[YOUR_AWSIOT_MQTT_PORT]",
            "sub_topics":[
                "[YOUR_MQTT_TOPIC/1]",
                "[YOUR_MQTT_TOPIC/2]"
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
result = crux.aws.subscribe_topics()
debug.info(result)

if result.get("status") == Status.SUCCESS:
    debug.info("Reading messages from subscribed topics...")
    # Check is there any data in subscribed topics
    # in each 5 seconds for 5 times
    for _ in range(0, 5):
        result = crux.aws.read_messages()
        debug.info(result.get("messages"))
        time.sleep(5)
