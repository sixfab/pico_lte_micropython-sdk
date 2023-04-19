"""
Example code for publising data to AWS IoT using HTTP.

Example Configuration
---------------------
Create a config.json file in the root directory of the picocell device.
config.json file must include the following parameters for this example:

config.json
{
    "aws":{
        "https":{
            "endpoint":"[YOUR_AWS_IOT_ENDPOINT]"
            "topic":"[YOUR_DEVICE_TOPIC]"
        }
    }
}
"""
import json
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

payload_json = {"state": {"reported": {"App": "AWS HTTP Example"}}}

debug.info("Publishing data to AWS IoT...")
payload = json.dumps(payload_json)
result = picoLTE.aws.post_message(payload)
debug.info("Result", result)
