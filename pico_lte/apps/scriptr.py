"""
Module for including functions of scripter.io operations
"""

import time

from pico_lte.common import config
from pico_lte.utils.manager import StateManager, Step
from pico_lte.utils.status import Status
from pico_lte.utils.helpers import get_parameter


class Scriptr:
    """
    Class for including Scriptr.io functions.
    """

    cache = config["cache"]

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

    def send_data(self, data, query=None, authorization=None):
        """
        Function for sending data to script.

        Parameters
        ----------
        data: str
            Json for sending data to the script
        query: str
            Query of script
        authorization: str
            Authorization token
        """

        if query is None:
            query = get_parameter(["scriptr", "query"])

        if authorization is None:
            authorization = get_parameter(["scriptr", "authorization"])

        header = (
            "POST "
            + query
            + " HTTP/1.1\n"
            + "Host: "
            + "api.scriptrapps.io"
            + "\n"
            + "Content-Type: application/json\n"
            + "Content-Length: "
            + str(len(data) + 1)
            + "\n"
            + "Authorization: Bearer "
            + authorization
            + "\n"
            + "\n\n"
        )

        step_network_reg = Step(
            function=self.network.register_network,
            name="register_network",
            success="get_pdp_ready",
            fail="failure",
        )

        step_get_pdp_ready = Step(
            function=self.network.get_pdp_ready,
            name="get_pdp_ready",
            success="set_server_url",
            fail="failure",
        )

        step_set_server_url = Step(
            function=self.http.set_server_url,
            name="set_server_url",
            success="post_request",
            fail="failure",
            function_params={"url": "https://api.scriptrapps.io"},
        )

        step_post_request = Step(
            function=self.http.post,
            name="post_request",
            success="read_response",
            fail="failure",
            function_params={"data": header + data, "header_mode": "1"},
            cachable=True,
            interval=1,
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": '"status": "success"'},
            retry=3,
            interval=1,
        )

        function_name = "scriptr_io.send_data"
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
