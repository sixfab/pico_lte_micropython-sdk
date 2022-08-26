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
from core.utils.status import Status
from core.modem import Modem
from core.temp import debug

modem = Modem()

modem.network.register_network()
modem.http.set_context_id()
modem.network.get_pdp_ready()
modem.http.set_server_url()


debug.info("Sending a GET request.")

result = modem.http.get()
debug.info(result)

# Read the response after 5 seconds.
time.sleep(5)
result = modem.http.read_response()
debug.info(result)
if result["status"] == Status.SUCCESS:
    debug.info("Get request succeeded.")
