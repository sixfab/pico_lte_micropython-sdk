"""
Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:
config.json
{
    "scriptr":{
        "endpoint": "[API_ENDPOINT_QUERY]",
        "device_token": "[DEVICE_TOKEN]"
    }
}
Example endpoint query for the "Hello" scriptr in Scriptr.io is "HelloDevice".
You can create the device token on the Device Directory page in Scriptr.io.
"""
import json
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()
payload = json.dumps({"temp": "25"})

debug.info("Sending data to Scriptr.io script...")
result = picoLTE.scriptr.post_json(payload)
debug.info("Result:", result)
