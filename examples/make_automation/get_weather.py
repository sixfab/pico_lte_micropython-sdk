"""
Example code to send weather forecast to Telegram using Make Automation.

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

debug.set_level(0)

picoLTE = PicoLTE()

payload_json = {"City": "Adana"}
payload = json.dumps(payload_json)

debug.info("The weather forecast for tomorrow is being sent to Telegram.")
result = picoLTE.make_automation.send_data(payload)
debug.info("Result: ", result)

