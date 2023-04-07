"""
Module for including functions of HTTP related operations of WiFi module.
"""

import urequests
import gc
from json import loads
from core.utils.enums import Status
from core.utils.helpers import get_parameter
from core.temp import debug


class HTTP:
    """
    Class for including functions of MQTT related operations of WiFi module.
    """

    def post(self, host=None, payload=None, headers=None, json=None):
        """
        Function for sending a POST request to a server/host using WiFi.

        Parameters
        ----------
        host: str
            Host address of the server,
            default is retrieved from config.json.
        payload: str
            Payload to send.
            default is retrieved from config.json.
        """
        if host is None:
            host = get_parameter(["http", "host"])
        if headers is None:
            headers = ""
        if json is None:
            json = ""
        if not host or not payload:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        response_content = None
        try:
            response = urequests.post(host, data=payload, headers=headers)

            debug.debug(f"HTTP POST Response: {response.json()}")
            try:
                response_content = response.json()
            except ValueError:
                debug.error("HTTP POST message is not in correct format.")
                response_content = response.text

            response.close()
            gc.collect()
            debug.debug("Response object closed. Garbage collector is called.")
            return {"status": Status.SUCCESS, "response": response_content}

        except Exception as error:
            debug.error(f"HTTP POST error: {error}")
            return {"status": Status.ERROR, "response": error}

    def get(self, host=None, payload=None, headers=None, json=None):
        """
        Function for sending a GET request to a server/host using WiFi.

        Parameters
        ----------
        host: str
            Host address of the server,
            default is retrieved from config.json.
        payload: str
            Payload to send.
            default is retrieved from config.json.
        """
        if host is None:
            host = get_parameter(["http", "host"])
        if headers is None:
            headers = ""
        if json is None:
            json = ""
        if not host:
            return {"status": Status.ERROR, "response": "Missing arguments!"}

        response_content = None
        try:
            response = urequests.get(host, data=payload, headers=headers, json=json)
            debug.debug(f"HTTP GET Response: {response.json()}")
            try:
                response_content = response.json()
            except ValueError:
                debug.error("HTTP GET message is not in correct format.")
                response_content = response.text

            response.close()
            gc.collect()
            debug.debug("Response object closed. Garbage collector is called.")
            return {"status": Status.SUCCESS, "response": response_content}

        except Exception as error:
            debug.error(f"HTTP GET error: {error}")
            return {"status": Status.ERROR, "response": error}
