"""
Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:
config.json
{
    "scriptr":{
        "query": "[QUERY_OF_SCRIPT]",
        "authorization": "[YOUR_TOKEN]"
    }
}
"""
import json
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

payload_json = {"temp": "25"}
payload = json.dumps(payload_json)

debug.info("Sending data to Scriptr.io script...")
result = picoLTE.scriptr.send_data(payload)
debug.info("Result:", result)
