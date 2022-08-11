import json
import time
from core.modem import Modem
from core.utils.debug import Debug
from core.utils.status import Status


# Provide your server details to send HTTP
# requests. For testing purposes, you may
# use "webhook.site".
# Example:
#     Host: https://webhook.site
#     Query: /6112efa6-4f8c-4bdb-8fa3-5787cc02f80a?query_param=DATA
SERVER_DETAILS = {
    'HOST': '[YOUR_SERVER_DOMAIN_ADDRESS]',
    'QUERY': '[YOUR_REQUEST_QUERY_ADDRESS]'
}

# This messages are arbitrary, you can change
# both attribute and data names.
DATA_TO_POST = {
    'messageType': 'picocell_status',
    'message': 'Picocell can connect to the server.'
}

DATA_TO_PUT = {
    'messageType': 'picocell_battery',
    'message': '90%'
}


# Initilaze the instances for the Picocell SDK.
modem = Modem()
debug = Debug()

# Send APN details.
modem.network.set_apn()

# Check the network registration.
result = modem.network.check_network_registration()
if result["status"] != Status.SUCCESS:
    debug.error("Could not connected to the cellular network.")
    

# Set the first HTTP context.
modem.http.set_context_id()

# Activate PDP.
modem.network.deactivate_pdp_context()
modem.network.activate_pdp_context()

# Set server URL.
debug.info("Set Server URL: ", modem.http.set_server_url(SERVER_DETAILS["HOST"]))

# Send a POST request.
data_post_json = json.dumps(DATA_TO_POST)
header =    "POST " + SERVER_DETAILS["QUERY"] + " HTTP/1.1\n" + \
            "Host: " + SERVER_DETAILS["HOST"][8:] + "\n" + \
            "Custom-Header-Name: Custom-Data\n" + \
            "Content-Type: application/json\n" + \
            "Content-Length: " + str(len(data_post_json) + 1) + "\n" + \
            "\n\n"

debug.info("Send POST Request: ", modem.http.post(data=header+data_post_json, header_mode=1))

# Wait for the modem to be ready.
time.sleep(5)

# Send a GET request.
header =    "GET " + SERVER_DETAILS["QUERY"] + " HTTP/1.1\n" + \
            "Host: " + SERVER_DETAILS["HOST"][8:] + "\n" + \
            "Content-Type: text/plain\n" + \
            "Content-Length: 0\n" + \
            "Custom-Header-Name: Custom-Data\n" + \
            "\n\n"

debug.info("Send GET Request: ", modem.http.get(data=header, header_mode=1))

# Wait for the modem to be ready.
time.sleep(5)

# Send a PUT request.
data_put_json = json.dumps(DATA_TO_PUT)
header =    "PUT " + SERVER_DETAILS["QUERY"] + " HTTP/1.1\n" + \
            "Host: " + SERVER_DETAILS["HOST"][8:] + "\n" + \
            "Custom-Header-Name: Custom-Data\n" + \
            "Content-Type: application/json\n" + \
            "Content-Length: " + str(len(data_put_json) + 1) + "\n" + \
            "\n\n"

debug.info("Send PUT Request: ", modem.http.put(data=header+data_put_json, header_mode=1))
