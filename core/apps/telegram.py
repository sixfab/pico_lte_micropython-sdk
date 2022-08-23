"""
Module for including functions of Telegram bot for Picocell module.
"""
import time
import json

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
        """_summary_

        Args:
            base (_type_): _description_
            network (_type_): _description_
            http (_type_): _description_
        """
        self.base = base
        self.network = network
        self.http = http

        self.host_url = get_parameter(["telegram", "server"], "api.telegram.org/bot")
        self.bot_token = get_parameter(["telegram", "token"])
        if self.bot_token is None:
            raise Exception("Bot token is mandatory to use Telegram app module.")

        self.bot_chat_id = get_parameter(["telegram", "chat_id"])
        if self.bot_chat_id is None:
            self.bot_chat_id = self.get_chat_id()

    def send_message(self, message):
        """ This function sends a message to the bot. """
        publish_url = f'https://{self.host_url}{self.bot_token}/' +\
                    f'sendMessage?chat_id={self.bot_chat_id}&text={message}'

        step_network_reg = Step(
            function=self.network.register_network,
            name="register_network",
            success="pdp_deactivate",
            fail="failure",
        )

        step_pdp_deactivate = Step(
            function=self.network.deactivate_pdp_context,
            name="pdp_deactivate",
            success="pdp_activate",
            fail="failure",
        )

        step_pdp_activate= Step(
            function=self.network.activate_pdp_context,
            name="pdp_activate",
            success="http_ssl_configuration",
            fail="failure"
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
        )

        step_get_request = Step(
            function=self.http.get,
            name="get_request",
            success="sleep_time",
            fail="failure",
            cachable=True,
            interval=2,
        )

        step_wait_time = Step(
            function=self.sleep_time_between_requests,
            name="sleep_time",
            success="read_response",
            fail="failure"
        )

        # TODO: http.read_response goes to timeout,
        # but the message is delived.
        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
        )

        # Add cache if it is not already existed
        function_name = "telegram.send_message"

        state_manager = StateManager(first_step=step_network_reg, function_name=function_name)

        state_manager.add_step(step_network_reg)
        state_manager.add_step(step_pdp_deactivate)
        state_manager.add_step(step_pdp_activate)
        state_manager.add_step(step_http_ssl_configuration)
        state_manager.add_step(step_set_server_url)
        state_manager.add_step(step_get_request)
        state_manager.add_step(step_wait_time)
        state_manager.add_step(step_read_response)

        while True:
            result = state_manager.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def get_chat_id(self):
        """ This function gets the chat ID from the bot automatically. """
        url_to_check_chat_id = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"

        step_network_reg = Step(
            function=self.network.register_network,
            name="register_network",
            success="pdp_deactivate",
            fail="failure",
        )

        step_pdp_deactivate = Step(
            function=self.network.deactivate_pdp_context,
            name="pdp_deactivate",
            success="pdp_activate",
            fail="failure",
        )

        step_pdp_activate= Step(
            function=self.network.activate_pdp_context,
            name="pdp_activate",
            success="http_ssl_configuration",
            fail="failure"
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
            function_params={"url": url_to_check_chat_id},
        )

        step_get_request = Step(
            function=self.http.get,
            name="get_request",
            success="sleep_time",
            fail="failure",
            cachable=True,
            interval=2,
        )

        step_wait_time = Step(
            function=self.sleep_time_between_requests,
            name="sleep_time",
            success="read_response",
            fail="failure"
        )

        # TODO: http.read_response goes to timeout,
        # but the message is delived.
        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
        )

        # Add cache if it is not already existed
        function_name = "telegram.check_chat_id"

        state_manager = StateManager(first_step=step_network_reg, function_name=function_name)

        state_manager.add_step(step_network_reg)
        state_manager.add_step(step_pdp_deactivate)
        state_manager.add_step(step_pdp_activate)
        state_manager.add_step(step_http_ssl_configuration)
        state_manager.add_step(step_set_server_url)
        state_manager.add_step(step_get_request)
        state_manager.add_step(step_wait_time)
        state_manager.add_step(step_read_response)

        while True:
            result = state_manager.run()

            if result["status"] == Status.SUCCESS:
                return self.parse_updates_response(result["response"])
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def parse_updates_response(self, response):
        """ This function parses the incoming response from getUpdates API. """
        starter_string_to_search = "CONNECT\r\n"
        starting_index = response.index(starter_string_to_search) + len(starter_string_to_search)
        print(starting_index)
        ender_string_to_search = "\r\nOK\r\n"
        ending_index = response.index(ender_string_to_search)
        print(ending_index)
        response_extracted = response[starting_index : ending_index]
        print(response_extracted)
        response_as_dict = json.loads(response_extracted)
        print(response_as_dict)

    @staticmethod
    def sleep_time_between_requests(secs=5):
        """ This function is an hat-function for state-manager usages. """
        time.sleep(secs)
        return {"status": 0, "response": "Waiting completed."}
