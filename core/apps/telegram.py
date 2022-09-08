"""
Module for including functions of Telegram bot for Picocell module.
"""
import time

from core.temp import config
from core.utils.manager import StateManager, Step
from core.utils.status import Status
from core.utils.helpers import get_parameter


class Telegram:
    """
    Telegram App module for Picocell lets you to create
    connections to your Telegram bot easily.
    """
    cache = config["cache"]

    def __init__(self, base, network, http):
        """Constructor of the class.

        Parameters
        ----------
        base : Base
            Picocell Base class
        network : Network
            Picocell Network class
        http : HTTP
            Picocell HTTP class
        """
        self.base = base
        self.network = network
        self.http = http

    def send_message(self, payload, host=None, bot_token=None, chat_id=None):
        """This function sends a message to the bot.

        Parameters
        ----------
        payload : str
            Payload of the message.
        host : str
            Telegram's server endpoint address.
        bot_token : str
            Bot's private token.
        chat_id : str
            Chat ID of where the bot lives.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if host is None:
            host = get_parameter(["telegram", "server"], "api.telegram.org/bot")

        if bot_token is None:
            bot_token = get_parameter(["telegram", "token"])

        if chat_id is None:
            chat_id = get_parameter(["telegram", "chat_id"])

        publish_url = f'https://{host}{bot_token}/' +\
                    f'sendMessage?chat_id={chat_id}&text={payload}'

        step_network_reg = Step(
            function=self.network.register_network,
            name="register_network",
            success="pdp_ready",
            fail="failure",
        )

        step_pdp_ready = Step(
            function=self.network.get_pdp_ready,
            name="pdp_ready",
            success="http_ssl_configuration",
            fail="failure",
        )

        step_http_ssl_configuration = Step(
            function=self.http.set_ssl_context_id,
            name="http_ssl_configuration",
            success="set_server_url",
            fail="failure",
            function_params={"id": 2},
        )

        step_set_server_url = Step(
            function=self.http.set_server_url,
            name="set_server_url",
            success="get_request",
            fail="failure",
            function_params={"url": publish_url},
            interval=2
        )

        step_get_request = Step(
            function=self.http.get,
            name="get_request",
            success="read_response",
            fail="failure",
            cachable=True,
            interval=5
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={'desired_response': '"ok":true'}
        )

        # Add cache if it is not already existed
        function_name = "telegram.send_message"

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
