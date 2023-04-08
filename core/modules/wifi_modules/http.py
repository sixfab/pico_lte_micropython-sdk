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

    def post(
        self, host=None, payload=None, headers=None, json=None, desired_response=None
    ):
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
        if not host:
            return {
                "status": Status.ERROR,
                "response": "Missing arguments! No host address is given.",
            }
        # Do not send empty payload,
        # it will cause an error.
        # Make it None instead.

        response_content = None
        try:
            response = urequests.post(host, data=payload, headers=headers, json=json)
            try:
                response_content = response.json()
            except ValueError:
                debug.debug("HTTP POST message is not in JSON format.")
                response_content = response.text
            response.close()
            gc.collect()
            debug.debug("Response object closed. Garbage collector is called.")

            if desired_response is not None and desired_response not in str(
                response_content
            ):
                return {"status": Status.ERROR, "response": response_content}
            return {"status": Status.SUCCESS, "response": response_content}

        except Exception as error:
            if isinstance(error, OSError):
                if error.errno == -2:
                    debug.error(
                        "OSError -2 occured. It needs to deinitialize the WLAN interface."
                    )
                elif error.errno == 12:
                    debug.error("Out of memory. Calling garbage collector.")
                    gc.collect()
                    debug.info(f"Garbage collector freed. Free Memory: {gc.mem_free()}")
            else:
                debug.error(f"HTTP POST: {error}")
                return {"status": Status.ERROR, "response": error}

    def get(
        self, host=None, payload=None, headers=None, json=None, desired_response=None
    ):
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
        if payload is None:
            payload = ""
        if not host:
            return {
                "status": Status.ERROR,
                "response": "Missing arguments! No host address is given.",
            }

        response_content = None
        try:
            response = urequests.get(host, data=payload, headers=headers, json=json)
            try:
                response_content = response.json()
            except ValueError:
                debug.debug("HTTP GET message is not in JSON format.")
                response_content = response.text

            response.close()
            gc.collect()
            debug.debug("Response object closed. Garbage collector is called.")

            if desired_response is not None and desired_response not in str(
                response_content
            ):
                return {"status": Status.ERROR, "response": response_content}
            return {"status": Status.SUCCESS, "response": response_content}

        except Exception as error:
            if isinstance(error, OSError):
                if error.errno == -2:
                    debug.error(
                        "OSError -2 occured. It needs to deinitialize the WLAN interface."
                    )
                elif error.errno == 12:
                    debug.error("Out of memory. Calling garbage collector.")
                    gc.collect()
                    debug.info(f"Garbage collector freed. Free Memory: {gc.mem_free()}")
            else:
                debug.error(f"HTTP GET: {error}")
                return {"status": Status.ERROR, "response": error}
