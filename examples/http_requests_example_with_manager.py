"""
Example code for publising data to any server with using HTTP methods by using manager class.
"""

import json
import time

from core.modem import Modem
from core.status import Status
from core.manager import StateManager, Step

def step_for_setting_server_url(modem_object, next_function, url=None, query=""):
    """This function returns a step for setting server's URL with a query.

    Args:
        modem_object (Modem): The modem instance to call methods.
        next_function (string): Next step's name if the step got success.
        url (str, optional): URL for the host. Defaults to None.
        query (str, optional): Query for the server. Defaults to "".

    Returns:
        Step: The step instance for setting server URL in the modem.
    """

    url_with_query = url + "/?" + query
    # Set-up the steps for state manager.
    step_set_server_url = Step(
        function=modem_object.set_modem_http_server_url,
        name="set_server_url",
        success=next_function,
        fail="failure",
        function_params={"url": url_with_query},
        cachable=True
    )

    return step_set_server_url


def prepare_communication_for_http(modem_object):
    """A function to register the cellular network
    and activate the PDP.

    Args:
        modem_object (Modem): The modem instance to call methods.

    Returns:
        dict: A dictionary which has the results inside.
    """

    # Set-up the steps for state manager.
    step_network_reg = Step(
        function=modem_object.register_network,
        name="register_network",
        success="pdp_deactivate",
        fail="failure"
    )

    step_pdp_deactivate = Step(
        function=modem_object.deactivate_pdp_context,
        name="pdp_deactivate",
        success="pdp_activate",
        fail="failure"
    )

    step_pdp_activate = Step(
        function=modem_object.activate_pdp_context,
        name="pdp_activate",
        success="success",
        fail="failure",
        cachable=True
    )

    # Create a state for this function to put
    # modem's cache.
    function_name = "prepare_communication_for_http"

    # Create the state manager.
    state_manager = StateManager(first_step=step_network_reg,
                                cache=modem_object.cache,
                                function_name=function_name)

    # Add each step.
    state_manager.add_step(step_network_reg)
    state_manager.add_step(step_pdp_deactivate)
    state_manager.add_step(step_pdp_activate)

    # Run the loop to finish state manager.
    while True:
        result = state_manager.run()
        if result["status"] == Status.SUCCESS:
            return result
        elif result["status"] == Status.ERROR:
            return result
        time.sleep(result["interval"])


def post_message_to_http_server(modem_object, payload, url=None, query=""):
    """POST request to the HTTP server with a payload and optional query.

    Args:
        modem_object (Modem): The modem instance to call methods.
        payload (dict): The dictionary message which will be sent.
        url (str, optional): URL for the host. Defaults to None.
        query (str, optional): Query for the server. Defaults to "".

    Returns:
        dict: A dictionary which has the results inside.
    """

    # Set-up the steps for state manager.
    step_set_server_url = step_for_setting_server_url(
        modem_object, "post_request", url, query)

    step_post_request = Step(
        function=modem_object.http_post_request,
        name="post_request",
        success="success",
        fail="failure",
        function_params={"data": payload},
        cachable=True
    )

    # Create a state for this function to put
    # modem's cache.
    function_name = "post_message_to_http_server"

    # Create the state manager.
    state_manager = StateManager(first_step=step_set_server_url,
                                cache=modem_object.cache,
                                function_name=function_name)

    # Add each step.
    state_manager.add_step(step_set_server_url)
    state_manager.add_step(step_post_request)

    # Run the loop to finish state manager.
    while True:
        result = state_manager.run()
        if result["status"] == Status.SUCCESS:
            return result
        elif result["status"] == Status.ERROR:
            return result
        time.sleep(result["interval"])


def get_message_to_http_server(modem_object, url=None, query=""):
    """GET request to the HTTP server with optional query.

    Args:
        modem_object (Modem): The modem instance to call methods.
        url (str, optional): URL for the host. Defaults to None.
        query (str, optional): Query for the server. Defaults to "".

    Returns:
        dict: A dictionary which has the results inside.
    """

    # Set-up the steps for state manager.
    step_set_server_url = step_for_setting_server_url(
        modem_object, "get_request", url, query)

    step_get_request = Step(
        function=modem_object.http_get_request,
        name="get_request",
        success="success",
        fail="failure",
        cachable=True
    )

    # Create a state for this function to put
    # modem's cache.
    function_name = "get_message_to_http_server"

    # Create the state manager.
    state_manager = StateManager(first_step=step_set_server_url,
                                cache=modem_object.cache,
                                function_name=function_name)

    # Add each step.
    state_manager.add_step(step_set_server_url)
    state_manager.add_step(step_get_request)

    # Run the loop to finish state manager.
    while True:
        result = state_manager.run()
        if result["status"] == Status.SUCCESS:
            return result
        elif result["status"] == Status.ERROR:
            return result
        time.sleep(result["interval"])


def put_message_to_http_server(modem_object, payload, url=None, query=""):
    """PUT request to the HTTP server with a payload and optional query.

    Args:
        modem_object (Modem): The modem instance to call methods.
        payload (dict): The dictionary message which will be sent.
        url (str, optional): URL for the host. Defaults to None.
        query (str, optional): Query for the server. Defaults to "".

    Returns:
        dict: A dictionary which has the results inside.
    """

    # Set-up the steps for state manager.
    step_set_server_url = step_for_setting_server_url(
        modem_object, "put_request", url, query)

    step_put_request = Step(
        function=modem_object.http_put_request,
        name="put_request",
        success="success",
        fail="failure",
        function_params={"data": payload},
        cachable=True
    )

    # Create a state for this function to put
    # modem's cache.
    function_name = "put_message_to_http_server"

    # Create the state manager.
    state_manager = StateManager(first_step=step_set_server_url,
                                cache=modem_object.cache,
                                function_name=function_name)

    # Add each step.
    state_manager.add_step(step_set_server_url)
    state_manager.add_step(step_put_request)

    # Run the loop to finish state manager.
    while True:
        result = state_manager.run()
        if result["status"] == Status.SUCCESS:
            return result
        elif result["status"] == Status.ERROR:
            return result
        time.sleep(result["interval"])


if __name__ == "__main__":
    # Initilize the modem object.
    modem = Modem({})
    # Prepare communication for HTTP.
    prepare_communication_for_http(modem)
    # Server address to send requests.
    HOST = "https://webhook.site/6112efa6-4f8c-4bdb-8fa3-5787cc02f80a"
    # Prepare a payload to post into the server.
    payload_to_post = {"ProjectTopic": "PicocellHTTPExampleWithManager"}
    payload_to_post_as_json = json.dumps(payload_to_post)
    # Post it to the server with given query.
    post_message_to_http_server(
        modem, payload_to_post_as_json, HOST, "device=Pico&try=0")
    time.sleep(4)
    # Get a request from the server.
    get_message_to_http_server(modem, HOST, "company=Sixfab&course=Picocell")
    time.sleep(6)
    # Prepare a payload to put into the server.
    payload_to_put = {"Temperature(*C)": 28}
    payload_to_put_as_json = json.dumps(payload_to_put)
    # Send the request into the server.
    put_message_to_http_server(
        modem, payload_to_put_as_json, HOST, "sensor=Garden2")
    time.sleep(4)
