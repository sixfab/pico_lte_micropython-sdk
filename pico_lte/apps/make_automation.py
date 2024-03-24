'''
Module for including functions of Make.com automations.
'''

import time

from pico_lte.common import config
from pico_lte.utils.manager import StateManager, Step
from pico_lte.utils.status import Status
from pico_lte.utils.helpers import get_parameter

class MakeAutomation:
    """
    Class for including MakeAutomation functions.
    """

    cache = config["cache"]

    def __init__(self, base, network, http, ssl):
        """Constructor of the class.

        Parameters
        ----------
        base : Base
            PicoLTE Base class
        network : Network
            PicoLTE Network class
        http : HTTP
            PicoLTE HTTP class
        ssl : SSL
            PicoLTE SSL class
        """
        self.base = base
        self.network = network
        self.http = http
        self.ssl = ssl

    def send_data(self, payload, host=None):
        """
        Function for sending data to Make.com.

        Parameters
        ----------
        message : str
            Json for sending data to the MakeAutomation
        host: str
            MakeAutomation webhook URL. 
            
        Returns
        -------
        dict
            Result dictionary that contains "status" and "message" keys.
        """
        if host is None:
            url = get_parameter(["make_automation", "url"])

        step_register_network = Step(
            name="register_network",
            function=self.network.register_network,
            success="prepare_pdp",
            fail="failure",
            retry=3,
        )

        step_prepare_pdp = Step(
            name="prepare_pdp",
            function=self.network.get_pdp_ready,
            success="set_sni",
            fail="failure",
        )

        step_set_sni = Step(
            name="set_sni",
            function=self.ssl.set_sni,
            success="set_server_url",
            fail="failure",
            function_params={"ssl_context_id": 1, "sni": 1}
        )

        step_set_server_url = Step(
            name="set_server_url",
            function=self.http.set_server_url,
            success="set_content_type",
            fail="failure",
            function_params={"url": url},
            interval=2,
        )

        step_set_content_type = Step(
            function=self.http.set_content_type,
            name="set_content_type",
            success="post_request",
            fail="failure",
            function_params={"content_type": 4},
        )

        step_post_request = Step(
            name="post_request",
            function=self.http.post,
            success="read_response",
            fail="failure",
            function_params={"data": payload},
            cachable=True,
            interval=3,
        )

        step_read_response = Step(
            name="read_response",
            function=self.http.read_response,
            success="success",
            fail="failure",
        )

        # Add cache if it is not already existed
        function_name = "make_automation.send_data"

        state_manager = StateManager(first_step=step_register_network, function_name=function_name)

        state_manager.add_step(step_register_network)
        state_manager.add_step(step_prepare_pdp)
        state_manager.add_step(step_set_sni)
        state_manager.add_step(step_set_server_url)
        state_manager.add_step(step_set_content_type)
        state_manager.add_step(step_post_request)
        state_manager.add_step(step_read_response)

        while True:
            result = state_manager.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])
