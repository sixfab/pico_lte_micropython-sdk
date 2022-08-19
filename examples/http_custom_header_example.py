"""
Example code for performing HTTP request to a server with using custom headers.
"""

import json
import time
from core.modem import Modem
from core.temp import debug
from core.utils.helpers import get_parameter

debug.set_debug_level(0)

# Prepare HTTP connection.
modem = Modem()
modem.network.set_apn()
result = modem.network.check_network_registration()
modem.http.set_context_id()
modem.network.activate_pdp_context()
modem.http.set_server_url()

# Get URL from the config.json.
URL = get_parameter(["https", "server"])

while True:
    # The messages that will be sent.
    DATA_TO_POST = {'message': 'Picocell HTTP POST Example with Custom Header'}
    DATA_TO_PUT = {'message': 'Picocell HTTP PUT Example with Custom Header'}

    # Convert dicts to JSONs.
    PAYLOAD_JSON_POST = json.dumps(DATA_TO_POST)
    PAYLOAD_JSON_PUT = json.dumps(DATA_TO_PUT)

    # Send a POST request.
    HEADER = "POST HTTP/1.1\n" + \
        "Host: " + URL[8:] + "\n" + \
        "Custom-Header-Name: Custom-Data\n" + \
        "Content-Type: application/json\n" + \
        "Content-Length: " + str(len(PAYLOAD_JSON_POST) + 1) + "\n" + \
        "\n\n"
    debug.info("Send POST Request: ", modem.http.post(data=HEADER+PAYLOAD_JSON_POST, header_mode=1))

    # Read response.
    time.sleep(5)
    debug.info("Response: ", modem.http.read_response())

    # Send a GET request.
    HEADER = "GET / HTTP/1.1\n" + \
        "Host: " + URL[8:] + "\n" + \
        "Content-Type: text/plain\n" + \
        "Content-Length: 0\n" + \
        "Custom-Header-Name: Custom-Data\n" + \
        "\n\n"
    debug.info("Send GET Request: ", modem.http.get(data=HEADER, header_mode=1))

    # Read response.
    time.sleep(5)
    debug.info("Response: ", modem.http.read_response())

    # Send a PUT request.
    HEADER = "PUT / HTTP/1.1\n" + \
        "Host: " + URL[8:] + "\n" + \
        "Custom-Header-Name: Custom-Data\n" + \
        "Content-Type: application/json\n" + \
        "Content-Length: " + str(len(PAYLOAD_JSON_PUT) + 1) + "\n" + \
        "\n\n"
    debug.info("Send PUT Request: ", modem.http.put(data=HEADER+PAYLOAD_JSON_PUT, header_mode=1))

    # Read response.
    time.sleep(5)
    debug.info("Response: ", modem.http.read_response())

    # Wait for 10 seconds for the next iteration.
    time.sleep(10)
