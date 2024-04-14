"""
Example code to get weather forecast with using Make Automation.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:
config.json
{
    "make_automation":{
        "url": "[INCOMING_WEBHOOK_URL]",
    }
}
"""

import json
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

payload_json = {"City": "Adana"}
payload = json.dumps(payload_json)

debug.info("Getting the forecast for tomorrow.")
result = picoLTE.make_automation.send_data(payload)
debug.info("Result: ", result)
