"""
Module for including functions of Telegram bot for PicoLTE module.
"""
import time

from pico_lte.utils.manager import StateManager, Step
from pico_lte.common import Status
from pico_lte.utils.helpers import get_parameter


class Telegram:
    """
    Telegram App module for PicoLTE lets you to create
    connections to your Telegram bot easily.
    """

    APP_NAME = "telegram"

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

    def send_message(self, payload, host=None, bot_token=None, chat_id=None):
        """This function sends a message to the bot.

        Parameters
        ----------
        payload : str, required
            Payload of the message.
        host : str, optional
            Telegram's server endpoint address.
        bot_token : str, required
            Bot's private token. It will be read
            from the config file if not provided.
        chat_id : str, required
            Chat ID of where the bot lives. It will be read
            from the config file if not provided.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if host is None:
            host = get_parameter([self.APP_NAME, "server"], "api.telegram.org/bot")

        if bot_token is None:
            bot_token = get_parameter([self.APP_NAME, "token"])

        if chat_id is None:
            chat_id = get_parameter([self.APP_NAME, "chat_id"])

        publish_url = (
            f"https://{host}{bot_token}/" + f"sendMessage?chat_id={chat_id}&text={payload}"
        )

        step_network_reg = Step(
            function=self.network.register_network,
            name=self.APP_NAME + "_register_network",
            success=self.APP_NAME + "_pdp_ready",
            fail="failure",
        )

        step_pdp_ready = Step(
            function=self.network.get_pdp_ready,
            name=self.APP_NAME + "_pdp_ready",
            success=self.APP_NAME + "_http_ssl_configuration",
            fail="failure",
        )

        step_http_ssl_configuration = Step(
            function=self.http.set_ssl_context_id,
            name=self.APP_NAME + "_http_ssl_configuration",
            success=self.APP_NAME + "_set_server_url",
            fail="failure",
            function_params={"cid": 2},
        )

        step_set_server_url = Step(
            function=self.http.set_server_url,
            name=self.APP_NAME + "_set_server_url",
            success=self.APP_NAME + "_get_request",
            fail="failure",
            function_params={"url": publish_url},
            interval=2,
        )

        step_get_request = Step(
            function=self.http.get,
            name=self.APP_NAME + "_get_request",
            success=self.APP_NAME + "_read_response",
            fail="failure",
            cachable=True,
            interval=5,
        )

        step_read_response = Step(
            function=self.http.read_response,
            name=self.APP_NAME + "_read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": '"ok":true'},
            interval=3,
            retry=5,
        )

        # Add cache if it is not already existed
        function_name = self.APP_NAME + ".send_message"

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_pdp_ready)
        sm.add_step(step_http_ssl_configuration)
        sm.add_step(step_set_server_url)
        sm.add_step(step_get_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])
