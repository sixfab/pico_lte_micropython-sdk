"""
Module for including functions of Slack API operations
"""

import time
import json

from pico_lte.common import config
from pico_lte.utils.manager import StateManager, Step
from pico_lte.utils.status import Status
from pico_lte.utils.helpers import get_parameter


class Slack:
    """
    Class for including Slack API functions.
    """

    cache = config["cache"]

    def __init__(self, base, network, http):
        """
        Initialize Slack class.
        """
        self.base = base
        self.network = network
        self.http = http

    def send_message(self, message, webhook_url=None):
        """
        Function for sending message to Slack channel by using
        incoming webhook feature of Slack.

        Parameters
        ----------
        message: str
            Message to send
        webhook_url: str
            Webhook URL of the Slack application

        Returns
        -------
        dict
            Result dictionary that contains "status" and "message" keys.
        """

        payload_json = {"text": message}
        payload = json.dumps(payload_json)

        if webhook_url is None:
            webhook_url = get_parameter(["slack", "webhook_url"])

        if not webhook_url:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

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
            success="set_content_type",
            fail="failure",
            function_params={"url": webhook_url},
        )

        step_set_content_type = Step(
            function=self.http.set_content_type,
            name="set_content_type",
            success="post_request",
            fail="failure",
            function_params={"content_type": 4},
        )

        step_post_request = Step(
            function=self.http.post,
            name="post_request",
            success="read_response",
            fail="failure",
            function_params={"data": payload},
            cachable=True,
            interval=2,
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": "ok"},
        )

        # Add cache if it is not already existed
        function_name = "slack.send_message"

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_set_content_type)
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
