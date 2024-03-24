"""
Example code for creating event in Google Calendar with using Make Automation.

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

payload_json = {"Name": "Meeting with someone.",
                "Start_Date": "27.03.2024 09:15",
                "Duration": "01:30"}
payload = json.dumps(payload_json)

debug.info("Setting event on Google Calendar.")
result = picoLTE.make_automation.send_data(payload)
debug.info("Result: ", result)

