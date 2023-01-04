"""
Example Configuration
---------------------
Create a config.json file in the root directory of the picocell device.
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
from core.crux import Crux
from core.temp import debug

crux = Crux()

payload_json = {"temp": "25"}
payload = json.dumps(payload_json)

debug.info("Sending data to Scriptr.io script...")
result = crux.scriptr.send_data(payload)
debug.info("Result:", result)
