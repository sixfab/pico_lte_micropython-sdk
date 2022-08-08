"""
Example code for publising data to any server with using HTTP methods.
"""

import json
import time

from core.modem import Modem
from core.status import Status

def handle_cellular_network_connection():
    """This function handles the connection to cellular network connection.
    """
    # Ask for return from the modem.
    modem.check_modem_communication()
    # Send APN details.
    modem.set_modem_apn(cid=1, apn="super")
    # Try to get a operator response for 10 times.
    for _index in range(0, 10):
        # Check if there is a connection to any operator.
        response = modem.get_operator_information()
        if response["status"] == Status.SUCCESS:
            return
        # Wait for 1 second.
        time.sleep(1)

def prepare_http_connection():
    """This function prepares HTTP connection for modem.
    """
    # Set the first HTTP context.
    modem.set_modem_http_context_id()
    # Activate PDP.
    modem.activate_pdp_context()

def prepare_http_with_query(host_url, query_string=""):
    """Sets the modem's HTTP server address.

    Args:
        host_url (str): Server address to send request.
        query_string (str, optional): Query payload for the server. Defaults to "".
    """
    # Add query to the server URL.
    url_to_post = host_url + "/?" + query_string
    # Set the HTTP url.
    modem.set_modem_http_server_url(url=url_to_post)

def send_post_request(server_url, data_dict, query_string=""):
    """POST request to the HTTP server with a payload and optional query.

    Args:
        server_url (str): Server address to send request.
        data_dict (dict): The data for the request as dictionary.
        query_string (str, optional): Query payload for the server. Defaults to "".
    """
    # Configure the HTTP address.
    prepare_http_with_query(server_url, query_string)
    # Convert to data to JSON.
    data_to_post = json.dumps(data_dict)
    # Send a post request to the URL.
    print("POST Request: ", modem.http_post_request(data=data_to_post))
    # Wait for six seconds before the next operation.
    time.sleep(6)

def send_get_request(server_url, query_string=""):
    """GET request to the HTTP server with optional query.

    Args:
        server_url (str): Server address to send request.
        query_string (str, optional): Query payload for the server. Defaults to "".
    """
    # Configure the HTTP address.
    prepare_http_with_query(server_url, query_string)
    # Send a GET request.
    print("GET Request: ", modem.http_get_request())
    # Wait for six seconds before the next operation.
    time.sleep(6)

def send_put_request(server_url, data_dict, query_string=""):
    """PUT request to the HTTP server with a payload and optional query.

    Args:
        server_url (str): Server address to send request.
        data_dict (dict): The data for the request as dictionary.
        query_string (str, optional): Query payload for the server. Defaults to "".
    """
    # Configure the HTTP address.
    prepare_http_with_query(server_url, query_string)
    # Convert to data to JSON.
    data_to_post = json.dumps(data_dict)
    # Send a PUT request.
    print("PUT Request: ", modem.http_put_request(data_to_post))
    # Wait for six seconds before the next operation.
    time.sleep(6)


if __name__ == "__main__":
    # Initilizate the modem.
    modem = Modem({})
    # Connect to a cellular network.
    handle_cellular_network_connection()
    # Prepare for the HTTP context.
    prepare_http_connection()
    # Select a HOST for testing purposes.
    HOST = "https://webhook.site/6112efa6-4f8c-4bdb-8fa3-5787cc02f80a"
    # Send a POST request to the server.
    send_post_request(HOST, {"ProjectTopic": "PicocellHTTPExample"}, "device=Pico&try=0")
    # Send a GET request to the server.
    send_get_request(HOST, "company=Sixfab&course=Picocell")
    # Send PUT request.
    send_put_request(HOST, {"Temperature(*C)": 28}, "sensor=Garden1")