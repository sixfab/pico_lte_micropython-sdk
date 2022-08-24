"""
Example code for performing PUT request to a server with using HTTP.
"""

import json
import time
from core.modem import Modem
from core.temp import debug

modem = Modem()

modem.network.set_apn()
modem.network.check_network_registration()
modem.http.set_context_id()
modem.network.activate_pdp_context()
modem.http.set_server_url()

while True:
    # Send a PUT request.
    payload_dict = {"message": "Picocell HTTP Put Example"}
    payload_json = json.dumps(payload_dict)
    result = modem.http.put(data=payload_json)
    debug.info(result)

    # Read the response after 5 seconds.
    time.sleep(5)
    result = modem.http.read_response()
    debug.info(result)

    # Wait 10 seconds in each iteration.
    time.sleep(10)
