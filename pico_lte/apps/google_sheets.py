"""
Module for including functions of Google Sheets for Picocell module.
"""
import time
import json

from pico_lte.common import config
from pico_lte.utils.manager import StateManager, Step
from pico_lte.utils.status import Status
from pico_lte.utils.helpers import get_parameter


class GoogleSheets:
    """
    Class for including functions of Google Sheets operations for Picocell module.
    """

    cache = config["cache"]

    def __init__(self, base, network, http):
        self.base = base
        self.network = network
        self.http = http

    def create_sheet(self, create_url=None, create_body=None):
        if create_body is None:
            create_body = get_parameter(["google_sheets", "create_url"])

        if not create_body:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        if create_url is None:
            create_url = get_parameter(["google_sheets", "create_url"])

        if not create_url:
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
            function_params={"url": create_url},
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
            function_params={"data": create_body},
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

        function_name = "google_sheets.create_sheet"

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

    def get_data(self, sheet=None, data_range=None):
        if sheet is None:
            sheet = get_parameter(["google_sheets", "sheet"])

        if not sheet:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        if data_range is None:
            data_range = get_parameter(["google_sheets", "data_range"])

        host = get_parameter(["google_sheets", "host"])
        token = get_parameter(["google_sheets", "token"])
        spreadsheetId = get_parameter(["google_sheets", "spreadsheetId"])
        majorDimension = get_parameter(["google_sheets", "majorDimension"])
        valueRenderOption = get_parameter(["google_sheets", "valueRenderOption"])
        api_key = get_parameter(["google_sheets", "api_key"])

        if data_range == None:
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{sheet}?majorDimension={majorDimension}&valueRenderOption={valueRenderOption}&key={api_key}"
        else:
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{sheet}!{data_range}?majorDimension={majorDimension}&valueRenderOption={valueRenderOption}&key={api_key}"

        HEADER = "\n".join(
            [
                f"GET {url} HTTP/1.1",
                f"Host: {host}",
                f"Authorization: {token}",
                "\n\n",
            ]
        )

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
        )

        step_set_server_url = Step(
            function=self.http.set_server_url,
            name="set_server_url",
            success="set_content_type",
            fail="failure",
            function_params={"url": url},
            interval=2,
        )
        step_set_content_type = Step(
            function=self.http.set_content_type,
            name="set_content_type",
            success="get_request",
            fail="failure",
            function_params={"content_type": 4},
        )

        step_get_request = Step(
            function=self.http.get,
            name="get_request",
            success="read_response",
            fail="failure",
            cachable=True,
            interval=5,
            function_params={"header_mode": 1, "data": HEADER},
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
        )

        function_name = "google_sheets.get_data"

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_pdp_ready)
        sm.add_step(step_http_ssl_configuration)
        sm.add_step(step_set_server_url)
        sm.add_step(step_set_content_type)
        sm.add_step(step_get_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                return json.loads(result["response"][0])["values"]
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])
