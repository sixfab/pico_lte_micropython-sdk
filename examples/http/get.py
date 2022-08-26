"""
Example code for performing GET request to a server with using HTTP.
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

while True:
    debug.info("Sending a GET request.")

    result = modem.http.get()
    debug.info(result)

    # Read the response after 5 seconds.
    time.sleep(5)
    result = modem.http.read_response("200")
    debug.info(result)
    if result["status"] == Status.SUCCESS:
        debug.info("Get request succeeded.")

    # Wait 10 seconds in each iteration.
    time.sleep(10)
