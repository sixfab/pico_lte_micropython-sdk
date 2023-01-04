"""
Example code for performing GET request to a server with using HTTP.

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

import time
from core.utils.enums import Status
from core.crux import Crux
from core.temp import debug

crux = Crux()

crux.modem.network.register_network()
crux.modem.http.set_context_id()
crux.modem.network.get_pdp_ready()
crux.modem.http.set_server_url()


debug.info("Sending a GET request.")

result = crux.modem.http.get()
debug.info(result)

# Read the response after 5 seconds.
time.sleep(5)
result = crux.modem.http.read_response()
debug.info(result)
if result["status"] == Status.SUCCESS:
    debug.info("Get request succeeded.")
