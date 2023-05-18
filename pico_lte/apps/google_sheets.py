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
    __oauth_token = ""

    def __init__(self, base, network, http):
        self.base = base
        self.network = network
        self.http = http

    def __set__state_manager(
        self,
        url="",
        header="",
        payload="",
        desired_response="",
        function_name="",
        request_type="",
    ):
        step_network_reg = Step(
            function=self.network.register_network,
            name="register_network",
            success="get_pdp_ready",
            fail="failure",
        )

        step_get_pdp_ready = Step(
            function=self.network.get_pdp_ready,
            name="get_pdp_ready",
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
        )

        step_set_content_type = Step(
            function=self.http.set_content_type,
            name="set_content_type",
            success="request",
            fail="failure",
            function_params={"content_type": 4},
        )

        if request_type == "post":
            request_function = self.http.post
        elif request_type == "get":
            request_function = self.http.get
        elif request_type == "put":
            request_function = self.http.put

        step_request = Step(
            function=request_function,
            name="request",
            success="read_response",
            fail="generate_access_token",
            function_params={
                "header_mode": 1,
                "data": header + payload,
                "fault_response": "401",
            },
            cachable=True,
            interval=2,
        )

        step_generate_access_token = Step(
            function=self.generate_access_token,
            name="generate_access_token",
            success="failure",
            fail="failure",
            interval=1,
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": desired_response},
            retry=2,
            interval=1,
        )

        function_name = "google_sheets.{function_name}"

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_set_content_type)
        sm.add_step(step_http_ssl_configuration)
        sm.add_step(step_set_server_url)
        sm.add_step(step_request)
        sm.add_step(step_generate_access_token)
        sm.add_step(step_read_response)

        return sm

    def get_data(self, sheet=None, data_range=None):
        if sheet is None:
            sheet = get_parameter(["google_sheets", "sheet"])

        if not sheet:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        oauth_token = self.__oauth_token
        spreadsheetId = get_parameter(["google_sheets", "spreadsheetId"])
        api_key = get_parameter(["google_sheets", "api_key"])

        if data_range == None:
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{sheet}?majorDimension=ROWS&valueRenderOption=FORMATTED_VALUE&key={api_key}"
        else:
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{sheet}!{data_range}?majorDimension=ROWS&valueRenderOption=FORMATTED_VALUE&key={api_key}"

        header = "\n".join(
            [
                f"GET {url} HTTP/1.1",
                "Host: sheets.googleapis.com",
                f"Authorization: Bearer {oauth_token}",
                "\n\n",
            ]
        )

        sm = self.__set__state_manager(
            url=url,
            header=header,
            desired_response="range",
            function_name="get_data",
            request_type="get",
        )

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                result = result["response"][0].split("\n")
                values = ""
                for value in result:
                    values += value
                values = json.loads(values + "]]}")["values"]
                return values

            elif result["status"] == Status.ERROR:
                return result

            time.sleep(result["interval"])

    def add_row(self, data=None, sheet=None):
        if sheet is None:
            sheet = get_parameter(["google_sheets", "sheet"])

        if not sheet:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        api_key = get_parameter(["google_sheets", "api_key"])
        oauth_token = self.__oauth_token
        spreadsheetId = get_parameter(["google_sheets", "spreadsheetId"])

        url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{sheet}!A1:append?valueInputOption=RAW&key={api_key}"

        payload = {"values": data}
        payload = json.dumps(payload)

        header = "\n".join(
            [
                f"Post {url} HTTP/1.1",
                "Host: sheets.googleapis.com",
                f"Authorization: Bearer {oauth_token}",
                f"Content-Length: {len(payload)+1}",
                "\n\n",
            ]
        )

        sm = self.__set__state_manager(
            url=url,
            header=header,
            payload=payload,
            desired_response="updatedRange",
            function_name="add_row",
            request_type="post",
        )

        while True:
            result = sm.run()
            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def add_data(self, data=None, data_range=None, sheet=None):
        if not data_range:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        if sheet is None:
            sheet = get_parameter(["google_sheets", "sheet"])

        if not sheet:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        api_key = get_parameter(["google_sheets", "api_key"])
        oauth_token = self.__oauth_token
        spreadsheetId = get_parameter(["google_sheets", "spreadsheetId"])

        url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{sheet}!{data_range}?valueInputOption=RAW&key={api_key}"

        payload = {"values": data}
        payload = json.dumps(payload)

        header = "\n".join(
            [
                f"PUT {url} HTTP/1.1",
                "Host: sheets.googleapis.com",
                f"Authorization: Bearer {oauth_token}",
                f"Content-Length: {len(payload)+1}",
                "\n\n",
            ]
        )

        sm = self.__set__state_manager(
            url=url,
            header=header,
            payload=payload,
            desired_response="updatedRange",
            function_name="add_data",
            request_type="put",
        )

        while True:
            result = sm.run()
            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def create_sheet(self, sheets=None):
        if sheets is None:
            sheets = [get_parameter(["google_sheets", "sheet"])]

        api_key = get_parameter(["google_sheets", "api_key"])
        oauth_token = self.__oauth_token

        url = f"https://sheets.googleapis.com/v4/spreadsheets?key={api_key}"

        if sheets is None:
            payload = {}
        else:
            payload = {"sheets": []}
            for sheet in sheets:
                payload["sheets"].append({"properties": {"title": sheet}})

        payload = json.dumps(payload)

        header = "\n".join(
            [
                f"Post {url} HTTP/1.1",
                "Host: sheets.googleapis.com",
                f"Authorization: Bearer {oauth_token}",
                f"Content-Length: {len(payload)+1}",
                "\n\n",
            ]
        )

        sm = self.__set__state_manager(
            url=url,
            header=header,
            payload=payload,
            desired_response="create_sheet",
            function_name="create_sheet",
            request_type="post",
        )

        while True:
            result = sm.run()
            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def delete_data(self, sheet=None, data_range=None):
        if sheet is None:
            sheet = get_parameter(["google_sheets", "sheet"])

        if not sheet:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        api_key = get_parameter(["google_sheets", "api_key"])
        oauth_token = self.__oauth_token
        spreadsheetId = get_parameter(["google_sheets", "spreadsheetId"])

        if data_range == None:
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{sheet}:clear?key={api_key}"
        else:
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{sheet}!{data_range}:clear?key={api_key}"

        header = "\n".join(
            [
                f"Post {url} HTTP/1.1",
                "Host: sheets.googleapis.com",
                f"Authorization: Bearer {oauth_token}",
                "\n\n",
            ]
        )

        sm = self.__set__state_manager(
            url=url,
            header=header,
            desired_response="clearedRange",
            function_name="delete_data",
            request_type="post",
        )

        while True:
            result = sm.run()
            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def generate_access_token(self):
        client_secret = get_parameter(["google_sheets", "client_secret"])
        refresh_token = get_parameter(["google_sheets", "refresh_token"])
        client_id = get_parameter(["google_sheets", "client_id"])

        url = f"https://oauth2.googleapis.com/token?client_secret={client_secret}&grant_type=refresh_token&refresh_token={refresh_token}&client_id={client_id}"

        header = "\n".join(
            [
                f"POST {url} HTTP/1.1",
                "Host: oauth2.googleapis.com",
                "Content-Length: 0",
                "\n\n",
            ]
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
        )

        step_set_content_type = Step(
            function=self.http.set_content_type,
            name="set_content_type",
            success="post_request",
            fail="failure",
        )

        step_post_request = Step(
            function=self.http.post,
            name="post_request",
            success="read_response",
            fail="failure",
            function_params={"header_mode": 1, "data": header},
            interval=1,
            retry=2,
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": "access_token"},
            retry=2,
            interval=1,
        )

        function_name = "google_sheets.generate_access_token"

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_set_content_type)
        sm.add_step(step_http_ssl_configuration)
        sm.add_step(step_set_server_url)
        sm.add_step(step_post_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()
            if result["status"] == Status.SUCCESS:
                self.__oauth_token = json.loads(result["response"][0] + '"}')[
                    "access_token"
                ]
                return {
                    "status": Status.SUCCESS,
                    "response": "Access token is generated.",
                }
            elif result["status"] == Status.ERROR:
                return {
                    "status": Status.ERROR,
                    "response": "Access token could not be generated.",
                }
            time.sleep(result["interval"])
