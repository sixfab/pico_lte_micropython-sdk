"""
Module for including functions of Slack API operations
"""

import time
from json import dumps
from core.apps.app_base import AppBase
from core.temp import config, debug
from core.utils.manager import StateManager, Step
from core.utils.enums import Status, Connection
from core.utils.helpers import get_parameter


class Slack(AppBase):
    """
    Class for including Slack API functions.
    """

    cache = config["cache"]
    APP_NAME = "slack"

    def __post_message_on_both(self, message, host=None):
        """
        A function to post a message to the server using both connections.

        Parameters
        ----------
        message: str
            Message to send
        host: str
            Host address of the server,
            default is retrieved from config.json.
        """
        params = {
            "message": message,
            "host": host,
        }

        return super().__post_message_on_both(Slack.APP_NAME, params)

    def __post_message_on_cellular(self, message, host=None):
        """
        A function to post a message to the server using cellular connection.

        Parameters
        ----------
        message: str
            Message to send
        host: str
            Host address of the server,
            default is retrieved from config.json.
        """
        debug.debug("Slack: Posting message on cellular.")

        if host is None:
            host = get_parameter(["slack", "webhook_url"])
        if not host or not message:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        # Construct the message to send with HTTP POST request.
        message = dumps({"text": message})

        step_network_reg = Step(
            function=self.cellular.network.register_network,
            name=f"{self.APP_NAME}_register_network_c",
            success=f"{self.APP_NAME}_get_pdp_ready_c",
            fail="failure",
        )

        step_get_pdp_ready = Step(
            function=self.cellular.network.get_pdp_ready,
            name=f"{self.APP_NAME}_get_pdp_ready_c",
            success=f"{self.APP_NAME}_set_server_url_c",
            fail="failure",
        )

        step_set_server_url = Step(
            function=self.cellular.http.set_server_url,
            name=f"{self.APP_NAME}_set_server_url_c",
            success=f"{self.APP_NAME}_set_content_type_c",
            fail="failure",
            function_params={"url": host},
        )

        step_set_content_type = Step(
            function=self.cellular.http.set_content_type,
            name=f"{self.APP_NAME}_set_content_type_c",
            success=f"{self.APP_NAME}_post_request_c",
            fail="failure",
            function_params={"content_type": 4},
        )

        step_post_request = Step(
            function=self.cellular.http.post,
            name=f"{self.APP_NAME}_post_request_c",
            success=f"{self.APP_NAME}_read_response_c",
            fail="failure",
            function_params={"data": message},
            cachable=True,
            interval=2,
        )

        step_read_response = Step(
            function=self.cellular.http.read_response,
            name=f"{self.APP_NAME}_read_response_c",
            success="success",
            fail="failure",
            function_params={"desired_response": "ok"},
        )

        # Create a state manager to run the steps.
        state_manager = StateManager(
            function_name=f"{self.APP_NAME}.send_message_on_cellular",
            first_step=step_network_reg,
        )

        state_manager.add_step(step_network_reg)
        state_manager.add_step(step_get_pdp_ready)
        state_manager.add_step(step_set_content_type)
        state_manager.add_step(step_set_server_url)
        state_manager.add_step(step_post_request)
        state_manager.add_step(step_read_response)

        while True:
            result = state_manager.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def __post_message_on_wifi(self, message, host=None):
        """
        A function to post a message to the server using WiFi connection.

        Parameters
        ----------
        message: str
            Message to send
        host: str
            Host address of the server,
            default is retrieved from config.json.
        """
        debug.debug("Slack: Posting message on WiFi.")

        if host is None:
            host = get_parameter(["slack", "webhook_url"])
        if not host or not message:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        # Construct the message for HTTP POST request.
        message = {"text": message}

        step_get_wifi_ready = Step(
            name=f"{self.APP_NAME}_get_wifi_ready",
            function=self.wifi.get_ready,
            function_params={},
            success=f"{self.APP_NAME}_send_message",
            fail="failure",
        )

        step_send_message = Step(
            name=f"{self.APP_NAME}_send_message",
            function=self.wifi.http.post,
            function_params={
                "host": host,
                "json": message,
                "desired_response": "ok",
            },
            success="success",
            fail="failure",
        )

        state_manager = StateManager(
            function_name=f"{Slack.APP_NAME}_publish_message_on_cellular",
            first_step=step_get_wifi_ready,
        )
        state_manager.add_step(step_get_wifi_ready)
        state_manager.add_step(step_send_message)

        while True:
            result = state_manager.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])
