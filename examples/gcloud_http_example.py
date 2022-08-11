"""
Example code for publishing data to Google IoT Cloud via HTTP.
"""

import json
import time
import ubinascii
from core.modem import Modem
from core.utils.debug import Debug
from core.utils.status import Status


# Complete this informations to connect to your Google Cloud services.
GCloudAccount = {
    'project_id': '[PROJECT_ID_IN_GCLOUD]',
    'region': '[REGION_IN_GCLOUD]',
    'registry_id': '[REGISTRY_ID_OF_DEVICE]',
    'device_id': '[DEVICE_ID]',
    'jwt': '[JSON_WEB_TOKEN]'
}

# Put a message here to send it to the topic.
DATA_TO_POST = "This message is an example from Picocell SDK."


if __name__ == "__main__":
    # This server details does not need to be changed.
    GCloudServer = {
        'HOST': 'https://cloudiotdevice.googleapis.com',
        'QUERY': '/v1/projects/' + GCloudAccount['project_id'] + \
                 '/locations/' + GCloudAccount['region'] + \
                 '/registries/' + GCloudAccount['registry_id'] + \
                 '/devices/' + GCloudAccount['device_id'],
        'QUERY_EXTRA_GET': '/config?local_version=1',
        'QUERY_EXTRA_POST': ':publishEvent'
    }

    # Initialize the instances for the Picocell SDK.
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
    debug.info("Set server URL: ", modem.http.set_server_url(GCloudServer['HOST']))

    # Construct the header for the request to register the device.
    # It is needed before publishing a message.
    HEADER = "GET " + GCloudServer['QUERY'] + GCloudServer['QUERY_EXTRA_GET'] + " HTTP/1.1\n" + \
                "Host: " + GCloudServer['HOST'][8:] + "\n" + \
                "Content-Type: text/plain\n" + \
                "Content-Length: 0\n" + \
                "Authorization: Bearer " + GCloudAccount['jwt'] + "\n" + \
                "\n\n"

    # Send the GET request with given header.
    debug.info("Send registration request: ", modem.http.get(data=HEADER, header_mode=1))

    # Wait for the modem to be ready.
    time.sleep(3)

    # Convert the message from ASCII to base64, and put it to
    # a JSON with 'binary_data' field.
    data_in_base64 = ubinascii.b2a_base64(DATA_TO_POST)
    data_post_dict = {'binary_data': data_in_base64[0:-1]}
    data_post_json = json.dumps(data_post_dict)

    # Construct the header for the request to publish the message.
    HEADER = "POST " + GCloudServer['QUERY'] + GCloudServer['QUERY_EXTRA_POST'] + " HTTP/1.1\n" + \
                "Host: " + GCloudServer['HOST'][8:] + "\n" + \
                "Content-Type: application/json\n" + \
                "Authorization: Bearer " + GCloudAccount['jwt'] + "\n" + \
                "Content-Length: " + str(len(data_post_json) + 1) + "\n" + \
                "\n\n"

    # Send the POST request with given header.
    debug.info("Send the data: ", modem.http.post(data=HEADER+data_post_json, header_mode=1))
