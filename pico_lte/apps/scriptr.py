"""
Module for including functions of scripter.io operations
"""

import time

from pico_lte.utils.manager import StateManager, Step
from pico_lte.common import Status
from pico_lte.utils.helpers import get_parameter


class Scriptr:
    """
    Class for including Scriptr.io functions.
    """

    APP_NAME = "scriptr"
    DEFAULT_API_ENDPOINT = "https://api.scriptrapps.io"

    def __init__(self, base, network, http):
        """Constructor of the class.

        Parameters
        ----------
        base : Base
            PicoLTE Base class
        network : Network
            PicoLTE Network class
        http : HTTP
            PicoLTE HTTP class
        """
        self.base = base
        self.network = network
        self.http = http

    def post_json(self, data, endpoint=None, device_token=None, host=None):
        """
        Function for posting a JSON to the Scriptr API endpoint.

        Parameters
        ----------
        data: str
            JSON for sending data to the script
        endpoint: str
            Scriptr API endpoint
        authorization: str
            Authorization token for the device.
        """

        if endpoint is None:
            endpoint = get_parameter([self.APP_NAME, "endpoint"])

        if device_token is None:
            device_token = get_parameter([self.APP_NAME, "device_token"])

        if host is None:
            host = get_parameter([self.APP_NAME, "host"], self.DEFAULT_API_ENDPOINT)

        if (
            not isinstance(endpoint, str)
            or not isinstance(device_token, str)
            or not isinstance(host, str)
        ):
            return {"status": Status.ERROR, "message": "Missing parameters."}

        # Remove leading and trailing slashes from endpoint and host.
        endpoint = "/" + endpoint if endpoint[0] != "/" else endpoint
        host = host[:-1] if host[-1] == "/" else host
        if host[:7] == "https:/":
            host_protocolless = host[8:]
        elif host[:7] == "http://":
            host_protocolless = host[7:]

        header = (
            "POST "
            + endpoint
            + " HTTP/1.1\n"
            + "Host: "
            + host_protocolless
            + "\n"
            + "Content-Type: application/json\n"
            + "Content-Length: "
            + str(len(data) + 1)
            + "\n"
            + "Authorization: Bearer "
            + device_token
            + "\n"
            + "\n\n"
        )

        step_network_reg = Step(
            function=self.network.register_network,
            name=self.APP_NAME + "_register_network",
            success=self.APP_NAME + "_get_pdp_ready",
            fail="failure",
        )

        step_get_pdp_ready = Step(
            function=self.network.get_pdp_ready,
            name=self.APP_NAME + "_get_pdp_ready",
            success=self.APP_NAME + "_set_server_url",
            fail="failure",
        )

        step_set_server_url = Step(
            function=self.http.set_server_url,
            name=self.APP_NAME + "_set_server_url",
            success=self.APP_NAME + "_post_request",
            fail="failure",
            function_params={"url": host},
        )

        step_post_request = Step(
            function=self.http.post,
            name=self.APP_NAME + "_post_request",
            success=self.APP_NAME + "_read_response",
            fail="failure",
            function_params={"data": header + data, "header_mode": "1"},
        )

        step_read_response = Step(
            function=self.http.read_response,
            name=self.APP_NAME + "_read_response",
            success="success",
            fail="failure",
            retry=3,
            interval=1,
            function_params={"desired_response": '"status": "success"'},
        )

        function_name = self.APP_NAME + ".post_json"
        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_set_server_url)
        sm.add_step(step_post_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()
            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])
