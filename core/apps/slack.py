"""
Module for including functions of Slack API operations
"""

import time
import json
import urequests

from core.temp import config
from core.utils.manager import StateManager, Step
from core.utils.enums import Status, Connection
from core.utils.helpers import get_parameter


class Slack:
    """
    Class for including Slack API functions.
    """

    cache = config["cache"]

    def __init__(self, modem, wifi):
        """
        Initialize Slack class.
        """
        self.modem = modem
        self.wifi = wifi

    def send_message(self, message, webhook_url=None, via=Connection.BOTH):
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

        if via == Connection.CELLULAR:
            return self.__send_message_on_cellular(payload, webhook_url)
        elif via == Connection.WIFI:
            return self.__send_message_on_wifi(payload, webhook_url)
        else:
            return self.__send_message_on_both(payload, webhook_url)


    def __send_message_on_both(self, payload, webhook_url):
        """
        Function for sending message to Slack channel by using
        incoming webhook feature of Slack. It tries to send it
        via WiFi at first, and if WiFi connection fails, tries to
        send it via cellular network.

        Parameters
        ----------
        payload: json
            Message to send with "text" attribute
        webhook_url: str
            Webhook URL of the Slack application

        Returns
        -------
        dict
            A dictionary that contains "status" and "message" keys.
        """

        params = {
            "payload": payload,
            "webhook_url": webhook_url
        }

        step_try_wifi = Step(
            function=self.__send_message_on_wifi,
            function_params=params,
            name="send_message_on_wifi",
            success="success",
            fail="send_message_on_cellular",
        )

        step_try_cellular = Step(
            function=self.__send_message_on_cellular,
            function_params=params,
            name="send_message_on_cellular",
            success="success",
            fail="failure",
        )

        # Add cache if it is not already existed
        function_name = "slack.send_message_on_both"

        sm = StateManager(first_step=step_try_wifi, function_name=function_name)

        sm.add_step(step_try_wifi)
        sm.add_step(step_try_cellular)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])


    def __send_message_on_wifi(self, payload, webhook_url, timeout=60):
        """Function for sending message to Slack channel by using
        incoming webhook feature of Slack. It uses WLAN/WiFi connectivity.

        Parameters
        ----------
        payload : json
            Message to send with "text" attribute
        webhook_url : str
            Webhook URL of the Slack application

        Returns
        -------
        dict
            A dictionary that contains "status" and "message" keys.
        """
        step_get_wifi_ready = Step(
            function=self.wifi.get_ready,
            name="get_wifi_ready",
            success="send_message",
            fail="failure",
            retry=3,
        )

        step_send_message = Step(
            function=self.__wifi_send_message,
            function_params={"payload": payload, "webhook_url": webhook_url},
            name="send_message",
            success="success",
            fail="get_wifi_ready",
            interval=5,
        )

        # Add cache if it is not already existed
        function_name = "slack.send_message_on_wifi"
        sm = StateManager(first_step=step_get_wifi_ready, function_name=function_name)
        sm.add_step(step_get_wifi_ready)
        sm.add_step(step_send_message)

        start_time = time.time()
        while time.time() - start_time < timeout:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

        return {"status": Status.TIMEOUT, "response": "Timeout reached."}

    def __send_message_on_cellular(self, payload, webhook_url):
        """
        Function for sending message to Slack channel by using
        incoming webhook feature of Slack. It uses cellular connectivity.

        Parameters
        ----------
        payload: json
            Message to send with "text" attribute
        webhook_url: str
            Webhook URL of the Slack application

        Returns
        -------
        dict
            A dictionary that contains "status" and "message" keys.
        """

        step_network_reg = Step(
            function=self.modem.network.register_network,
            name="register_network",
            success="get_pdp_ready",
            fail="failure",
        )

        step_get_pdp_ready = Step(
            function=self.modem.network.get_pdp_ready,
            name="get_pdp_ready",
            success="set_server_url",
            fail="failure",
        )

        step_set_server_url = Step(
            function=self.modem.http.set_server_url,
            name="set_server_url",
            success="set_content_type",
            fail="failure",
            function_params={"url": webhook_url},
        )

        step_set_content_type = Step(
            function=self.modem.http.set_content_type,
            name="set_content_type",
            success="post_request",
            fail="failure",
            function_params={"content_type": 4},
        )

        step_post_request = Step(
            function=self.modem.http.post,
            name="post_request",
            success="read_response",
            fail="failure",
            function_params={"data": payload},
            cachable=True,
            interval=2,
        )

        step_read_response = Step(
            function=self.modem.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": "ok"},
        )

        # Add cache if it is not already existed
        function_name = "slack.send_message_on_cellular"

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

    @staticmethod
    def __wifi_send_message(payload, webhook_url):
        """Something will come here"""
        try:
            response = urequests.post(webhook_url, data=payload)
            print(response)
            response.close()  # Mandatory to garbage collect this response.
            return {"status": Status.SUCCESS, "response": response}
        except OSError as err:
            return {"status": Status.ERROR, "response": err}

