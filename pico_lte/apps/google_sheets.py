"""
Module for including functions of Google Sheets for for PicoLTE module.
"""
import time
import json

from pico_lte.common import config
from pico_lte.utils.manager import StateManager, Step
from pico_lte.utils.status import Status
from pico_lte.utils.helpers import get_parameter


class GoogleSheets:
    """
    Class for including functions of Google Sheets operations for PicoLTE module.
    """

    cache = config["cache"]
    access_token = ""

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

    def set_network(self):
        """
        Function includes network configurations for tcp/ip connection

        Returns
        -------
        dict
            Result dictionary that contains "status and ""response" keys.
        """

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
            success="success",
            fail="failure",
        )

        function_name = "set_network"

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_http_ssl_configuration)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def get_data(self, sheet=None, data_range=None):
        """
        Function for getting data from a Google Sheets document.

        Parameters
        ----------
        sheet: str
            Name of the target sheet
        data_range: str
            Data cell range of the sheet

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        if sheet is None:
            sheet = get_parameter(["google_sheets", "sheet"])

        if not sheet:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        api_key = get_parameter(["google_sheets", "api_key"])
        spreadsheet_id = get_parameter(["google_sheets", "spreadsheetId"])

        if data_range is None:
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet}?majorDimension=ROWS&prettyPrint=false&valueRenderOption=FORMATTED_VALUE&key={api_key}"
        else:
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet}!{data_range}?majorDimension=ROWS&prettyPrint=false&valueRenderOption=FORMATTED_VALUE&key={api_key}"

        def generate_header():
            header = "\n".join(
                [
                    f"GET {url} HTTP/1.1",
                    "Host: sheets.googleapis.com",
                    f"Authorization: Bearer {self.access_token}",
                    "\n\n",
                ]
            )

            return header

        header = generate_header()

        step_set_network = Step(
            function=self.set_network,
            name="set_network",
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

        step_request = Step(
            function=self.http.get,
            name="request",
            success="read_response",
            fail="failure",
            function_params={
                "header_mode": 1,
                "data": header,
                "fault_response": "403",
                "timeout": 15,
            },
            cachable=True,
            interval=2,
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": "range"},
            retry=2,
            interval=1,
        )

        function_name = "google_sheets.get_data"

        sm = StateManager(first_step=step_set_network, function_name=function_name)

        sm.add_step(step_set_network)
        sm.add_step(step_set_server_url)
        sm.add_step(step_set_content_type)
        sm.add_step(step_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                del result["interval"]
                return result

            elif result["status"] == Status.ERROR:
                try:
                    if "403" in result["response"][1]:
                        self.generate_access_token()
                        header = generate_header()
                        sm = StateManager(
                            first_step=step_set_network, function_name=function_name
                        )
                        sm.add_step(step_set_network)
                        sm.add_step(step_set_server_url)
                        sm.add_step(step_set_content_type)
                        sm.add_step(step_request)
                        sm.add_step(step_read_response)
                        step_request.update_function_params(data=header)
                        sm.update_step(step_request)
                    else:
                        del result["interval"]
                        return result
                except:
                    del result["interval"]
                    return result
            time.sleep(result["interval"])

    def add_row(self, sheet=None, data=None):
        """
        Function for adding a row data to a Google Sheets document

        Parameters
        ----------
        sheet: str
            Name of the target sheet
        data: list
            Data list to add

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        if sheet is None:
            sheet = get_parameter(["google_sheets", "sheet"])

        if not sheet:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        api_key = get_parameter(["google_sheets", "api_key"])
        spreadsheet_id = get_parameter(["google_sheets", "spreadsheetId"])

        url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet}:append?valueInputOption=RAW&prettyPrint=false&key={api_key}"

        payload = {"values": data}
        payload = json.dumps(payload)

        def generate_header():
            header = "\n".join(
                [
                    f"Post {url} HTTP/1.1",
                    "Host: sheets.googleapis.com",
                    f"Authorization: Bearer {self.access_token}",
                    f"Content-Length: {len(payload)+1}",
                    "\n\n",
                ]
            )

            return header

        header = generate_header()

        step_set_network = Step(
            function=self.set_network,
            name="set_network",
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

        step_request = Step(
            function=self.http.post,
            name="request",
            success="read_response",
            fail="failure",
            function_params={
                "header_mode": 1,
                "data": header + payload,
                "fault_response": "401",
                "timeout": 15,
            },
            cachable=True,
            interval=2,
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": "updatedRange"},
            retry=2,
            interval=1,
        )

        function_name = "google_sheets.add_row"

        sm = StateManager(first_step=step_set_network, function_name=function_name)

        sm.add_step(step_set_network)
        sm.add_step(step_set_server_url)
        sm.add_step(step_set_content_type)
        sm.add_step(step_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                del result["interval"]
                return result

            elif result["status"] == Status.ERROR:
                try:
                    if "401" in result["response"][1]:
                        self.generate_access_token()
                        header = generate_header()
                        sm = StateManager(
                            first_step=step_set_network, function_name=function_name
                        )
                        sm.add_step(step_set_network)
                        sm.add_step(step_set_server_url)
                        sm.add_step(step_set_content_type)
                        sm.add_step(step_request)
                        sm.add_step(step_read_response)
                        step_request.update_function_params(data=header + payload)
                        sm.update_step(step_request)
                    else:
                        del result["interval"]
                        return result
                except:
                    del result["interval"]
                    return result
            time.sleep(result["interval"])

    def add_data(self, sheet=None, data=None, data_range=None):
        """
        Function for adding data to a Google Sheets document

        Parameters
        ----------
        sheet: str
            Name of the target sheet
        data: list
            Data list to add
        data_range: str
            Data cell range to add data

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        if not data_range:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        if sheet is None:
            sheet = get_parameter(["google_sheets", "sheet"])

        if not sheet:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        api_key = get_parameter(["google_sheets", "api_key"])
        spreadsheet_id = get_parameter(["google_sheets", "spreadsheetId"])

        url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet}!{data_range}?valueInputOption=RAW&prettyPrint=false&key={api_key}"

        payload = {"values": data}
        payload = json.dumps(payload)

        def generate_header():
            header = "\n".join(
                [
                    f"PUT {url} HTTP/1.1",
                    "Host: sheets.googleapis.com",
                    f"Authorization: Bearer {self.access_token}",
                    f"Content-Length: {len(payload)+1}",
                    "\n\n",
                ]
            )

            return header

        header = generate_header()

        step_set_network = Step(
            function=self.set_network,
            name="set_network",
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

        step_request = Step(
            function=self.http.put,
            name="request",
            success="read_response",
            fail="failure",
            function_params={
                "header_mode": 1,
                "data": header + payload,
                "fault_response": "401",
                "timeout": 15,
            },
            cachable=True,
            interval=2,
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": "updatedRange"},
            retry=2,
            interval=1,
        )

        function_name = "google_sheets.add_data"

        sm = StateManager(first_step=step_set_network, function_name=function_name)

        sm.add_step(step_set_network)
        sm.add_step(step_set_server_url)
        sm.add_step(step_set_content_type)
        sm.add_step(step_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                del result["interval"]
                return result

            elif result["status"] == Status.ERROR:
                try:
                    if "401" in result["response"][1]:
                        self.generate_access_token()
                        header = generate_header()
                        sm = StateManager(
                            first_step=step_set_network, function_name=function_name
                        )
                        sm.add_step(step_set_network)
                        sm.add_step(step_set_server_url)
                        sm.add_step(step_set_content_type)
                        sm.add_step(step_request)
                        sm.add_step(step_read_response)
                        step_request.update_function_params(data=header + payload)
                        sm.update_step(step_request)
                    else:
                        del result["interval"]
                        return result

                except:
                    del result["interval"]
                    return result
            time.sleep(result["interval"])

    def create_sheet(self, sheets=None):
        """
        Function for creating new sheet(s) in Google Sheets

        Parameters
        ----------
        sheets: list
            Names of the target sheets

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        if sheets is None:
            sheets = [get_parameter(["google_sheets", "sheet"])]

        api_key = get_parameter(["google_sheets", "api_key"])

        url = f"https://sheets.googleapis.com/v4/spreadsheets?prettyPrint=false&key={api_key}"

        if sheets is None:
            payload = {}
        else:
            payload = {"sheets": []}
            for sheet in sheets:
                payload["sheets"].append({"properties": {"title": sheet}})

        payload = json.dumps(payload)

        def generate_header():
            header = "\n".join(
                [
                    f"Post {url} HTTP/1.1",
                    "Host: sheets.googleapis.com",
                    f"Authorization: Bearer {self.access_token}",
                    f"Content-Length: {len(payload)+1}",
                    "\n\n",
                ]
            )

            return header

        header = generate_header()

        step_set_network = Step(
            function=self.set_network,
            name="set_network",
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

        step_request = Step(
            function=self.http.post,
            name="request",
            success="read_response",
            fail="failure",
            function_params={
                "header_mode": 1,
                "data": header + payload,
                "fault_response": "401",
                "timeout": 15,
            },
            cachable=True,
            interval=2,
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": "spreadsheetId"},
            retry=2,
            interval=1,
        )

        function_name = "google_sheets.create_sheet"

        sm = StateManager(first_step=step_set_network, function_name=function_name)

        sm.add_step(step_set_network)
        sm.add_step(step_set_server_url)
        sm.add_step(step_set_content_type)
        sm.add_step(step_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                del result["interval"]
                return result

            elif result["status"] == Status.ERROR:
                try:
                    if "401" in result["response"][1]:
                        self.generate_access_token()
                        header = generate_header()
                        sm = StateManager(
                            first_step=step_set_network, function_name=function_name
                        )
                        sm.add_step(step_set_network)
                        sm.add_step(step_set_server_url)
                        sm.add_step(step_set_content_type)
                        sm.add_step(step_request)
                        sm.add_step(step_read_response)
                        step_request.update_function_params(data=header + payload)
                        sm.update_step(step_request)
                    else:
                        del result["interval"]
                        return result

                except:
                    del result["interval"]
                    return result
            time.sleep(result["interval"])

    def delete_data(self, sheet=None, data_range=None):
        """
        Function for deleting data from a Google Sheets document

        Parameters
        ----------
        sheet: str
            Name of the target sheet
        data_range: str
            Data cell range to delete

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        if sheet is None:
            sheet = get_parameter(["google_sheets", "sheet"])

        if not sheet:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        api_key = get_parameter(["google_sheets", "api_key"])
        spreadsheet_id = get_parameter(["google_sheets", "spreadsheetId"])

        if data_range is None:
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet}:clear?prettyPrint=false&key={api_key}"
        else:
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet}!{data_range}:clear?prettyPrint=false&key={api_key}"

        def generate_header():
            header = "\n".join(
                [
                    f"Post {url} HTTP/1.1",
                    "Host: sheets.googleapis.com",
                    f"Authorization: Bearer {self.access_token}",
                    "\n\n",
                ]
            )

            return header

        header = generate_header()

        step_set_network = Step(
            function=self.set_network,
            name="set_network",
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

        step_request = Step(
            function=self.http.post,
            name="request",
            success="read_response",
            fail="failure",
            function_params={
                "header_mode": 1,
                "data": header,
                "fault_response": "401",
                "timeout": 15,
            },
            cachable=True,
            interval=2,
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": "clearedRange"},
            retry=2,
            interval=1,
        )

        function_name = "google_sheets.delete_data"

        sm = StateManager(first_step=step_set_network, function_name=function_name)

        sm.add_step(step_set_network)
        sm.add_step(step_set_server_url)
        sm.add_step(step_set_content_type)
        sm.add_step(step_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                del result["interval"]
                return result

            elif result["status"] == Status.ERROR:
                try:
                    if "401" in result["response"][1]:
                        self.generate_access_token()
                        header = generate_header()
                        sm = StateManager(
                            first_step=step_set_network, function_name=function_name
                        )
                        sm.add_step(step_set_network)
                        sm.add_step(step_set_server_url)
                        sm.add_step(step_set_content_type)
                        sm.add_step(step_request)
                        sm.add_step(step_read_response)
                        step_request.update_function_params(data=header)
                        sm.update_step(step_request)
                    else:
                        del result["interval"]
                        return result

                except:
                    del result["interval"]
                    return result
            time.sleep(result["interval"])

    def generate_access_token(self):
        """
        Function for generating new access token for authorization to Google Sheets

        Returns
        -------
        dict
            Result dictionary that contains "status and ""response" keys.
        """

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

        step_set_network = Step(
            function=self.set_network,
            name="set_network",
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
            function_params={"header_mode": 1, "data": header, "timeout": 10},
            interval=1,
            cachable=True,
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

        sm = StateManager(first_step=step_set_network, function_name=function_name)

        sm.add_step(step_set_network)
        sm.add_step(step_set_server_url)
        sm.add_step(step_set_content_type)
        sm.add_step(step_post_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()
            if result["status"] == Status.SUCCESS:
                self.access_token = json.loads(result["response"][0] + '"}')[
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
