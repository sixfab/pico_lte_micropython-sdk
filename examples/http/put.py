"""
Example code for performing PUT request to a server with using HTTP.

Example Configuration
---------------------
Create a config.json file in the root directory of the picocell device.
config.json file must include the following parameters for this example:

config.json
{
    "https":{
        "server":"[HTTP_SERVER]",
        "username":"[YOUR_HTTP_USERNAME]",
        "password":"[YOUR_HTTP_PASSWORD]"
    },
}
"""

import json
import time
from pico_lte.utils.status import Status
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

picoLTE.network.register_network()
picoLTE.http.set_context_id()
picoLTE.network.get_pdp_ready()
picoLTE.http.set_server_url()

debug.info("Sending a PUT request.")

payload_dict = {"message": "Picocell HTTP Put Example"}
payload_json = json.dumps(payload_dict)
result = picoLTE.http.put(data=payload_json)
debug.info(result)

# Read the response after 5 seconds.
time.sleep(5)
result = picoLTE.http.read_response()
if result["status"] == Status.SUCCESS:
    debug.info("Put request succeeded.")
debug.info(result)
