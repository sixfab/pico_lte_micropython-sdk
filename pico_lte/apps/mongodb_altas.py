"""
Module for including functions of MongoDB Atlas for for PicoLTE module.
"""

import time
import json

from pico_lte.common import debug
from pico_lte.utils.manager import StateManager, Step
from pico_lte.utils.status import Status
from pico_lte.utils.helpers import get_parameter


class MongoDBAtlas:
    """
    Class for including functions of MongoDB Atlas operations for PicoLTE module.
    """

    def __init__(self, base, network, http):
        """
        Constructor of the class.

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
        Function includes network configurations for tcp/ip connection.

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
            success="success",
            fail="failure",
        )

        function_name = "set_network"

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def base_http_function(
        self,
        function_name,
        http_method,
        url,
        data,
        desired_response,
        username=None,
        password=None,
    ):
        """
        Base function for MongoDB Atlas HTTP requests.

        Parameters
        ----------
        function_name: str
            Name of the function.
        http_method: str
            HTTP method for the request.
        url: str
            URL for the request.
        data: str
            Data for the request.
        desired_response: str
            Desired response for the request.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
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
            success="set_server_url",
            fail="failure",
        )

        step_set_server_url = Step(
            function=self.http.set_server_url,
            name="set_server_url",
            success=(
                "http_request" if username is None or password is None else "set_auth"
            ),
            fail="failure",
            function_params={"url": url},
        )

        step_set_auth = Step(
            function=self.http.set_auth,
            name="set_auth",
            success="http_request",
            fail="failure",
            function_params={"username": username, "password": password},
        )

        if http_method == "GET":
            step_http_request = Step(
                function=self.http.get,
                name="http_request",
                success="read_response",
                fail="failure",
                function_params={
                    "header_mode": 1,
                    "data": data,
                },
            )
        elif http_method == "POST":
            step_http_request = Step(
                function=self.http.post,
                name="http_request",
                success="read_response",
                fail="failure",
                function_params={
                    "header_mode": 1,
                    "data": data,
                },
            )
        elif http_method == "PUT":
            step_http_request = Step(
                function=self.http.put,
                name="http_request",
                success="read_response",
                fail="failure",
                function_params={
                    "header_mode": 1,
                    "data": data,
                },
            )
        else:
            return {"status": Status.ERROR, "response": "Invalid HTTP method."}

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": desired_response},
        )

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_set_server_url)
        sm.add_step(step_set_auth)
        sm.add_step(step_http_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()
            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def find_one(
        self, payload, region=None, cloud_provider=None, app_id=None, api_key=None
    ):
        """
        Function for finding a document in MongoDB Atlas.

        Parameters
        ----------
        payload: dict
            Payload for the request.
        region: str
            Region of the MongoDB Atlas.
        cloud_provider: str
            Cloud provider of the MongoDB Atlas.
        app_id: str
            Application ID of the MongoDB Atlas.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        region = get_parameter(["mongodb_atlas", "region"])
        cloud_provider = get_parameter(["mongodb_atlas", "cloud_provider"])
        app_id = get_parameter(["mongodb_atlas", "app_id"])
        api_key = get_parameter(["mongodb_atlas", "api_key"])

        if not (
            region is None
            or cloud_provider is None
            or app_id is None
            or api_key is None
        ):
            host = f"{region}.{cloud_provider}.data.mongodb-api.com"
            query = f"app/{app_id}/endpoint/data/v1/action/findOne"
            url = f"https://{host}/{query}"
        else:
            debug.error("There are missing parameters for MongoDB Atlas.")

        header = "\n".join(
            [
                f"POST /{query} HTTP/1.1",
                f"Host: {host}",
                "Custom-Header-Name: Custom-Data",
                "Content-Type: application/json",
                f"Content-Length: {len(payload)+1}",
                f"apiKey: {api_key}",
                "\n\n",
            ]
        )

        data = header + json.dumps(payload)

        return self.base_http_function(
            "mongodb_atlas.find_one", "POST", url, data, "document"
        )

    def find_many(
        self, payload, region=None, cloud_provider=None, app_id=None, api_key=None
    ):
        """
        Function for finding multiple documents in MongoDB Atlas.

        Parameters
        ----------
        payload: dict
            Payload for the request.
        region: str
            Region of the MongoDB Atlas.
        cloud_provider: str
            Cloud provider of the MongoDB Atlas.
        app_id: str
            Application ID of the MongoDB Atlas.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        region = get_parameter(["mongodb_atlas", "region"])
        cloud_provider = get_parameter(["mongodb_atlas", "cloud_provider"])
        app_id = get_parameter(["mongodb_atlas", "app_id"])
        api_key = get_parameter(["mongodb_atlas", "api_key"])

        if not (
            region is None
            or cloud_provider is None
            or app_id is None
            or api_key is None
        ):
            host = f"{region}.{cloud_provider}.data.mongodb-api.com"
            query = f"app/{app_id}/endpoint/data/v1/action/findMany"
            url = f"https://{host}/{query}"
        else:
            debug.error("There are missing parameters for MongoDB Atlas.")

        header = "\n".join(
            [
                f"POST /{query} HTTP/1.1",
                f"Host: {host}",
                "Custom-Header-Name: Custom-Data",
                "Content-Type: application/json",
                f"Content-Length: {len(payload)+1}",
                f"apiKey: {api_key}",
                "\n\n",
            ]
        )

        data = header + json.dumps(payload)

        return self.base_http_function(
            "mongodb_atlas.find_many", "POST", url, data, "document"
        )

    def insert_one(
        self, payload, region=None, cloud_provider=None, app_id=None, api_key=None
    ):
        """
        Function for inserting a document in MongoDB Atlas.

        Parameters
        ----------
        payload: dict
            Payload for the request.
        region: str
            Region of the MongoDB Atlas.
        cloud_provider: str
            Cloud provider of the MongoDB Atlas.
        app_id: str
            Application ID of the MongoDB Atlas.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        region = get_parameter(["mongodb_atlas", "region"])
        cloud_provider = get_parameter(["mongodb_atlas", "cloud_provider"])
        app_id = get_parameter(["mongodb_atlas", "app_id"])
        api_key = get_parameter(["mongodb_atlas", "api_key"])

        if not (
            region is None
            and cloud_provider is None
            and app_id is None
            and api_key is None
        ):
            host = f"{region}.{cloud_provider}.data.mongodb-api.com"
            query = f"app/{app_id}/endpoint/data/v1/action/insertOne"
            url = f"https://{host}/{query}"
        else:
            debug.error("There are missing parameters for MongoDB Atlas.")

        header = "\n".join(
            [
                f"POST /{query} HTTP/1.1",
                f"Host: {host}",
                "Content-Type: application/json",
                f"Content-Length: {len(payload)+1}",
                f"apiKey: {api_key}",
                "\n\n",
            ]
        )

        data = header + json.dumps(payload)

        return self.base_http_function(
            "mongodb_atlas.insert_one", "POST", url, data, "insertedId"
        )

    def insert_many(
        self, payload, region=None, cloud_provider=None, app_id=None, api_key=None
    ):
        """
        Function for inserting multiple documents in MongoDB Atlas.

        Parameters
        ----------
        payload: dict
            Payload for the request.
        region: str
            Region of the MongoDB Atlas.
        cloud_provider: str
            Cloud provider of the MongoDB Atlas.
        app_id: str
            Application ID of the MongoDB Atlas.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        region = get_parameter(["mongodb_atlas", "region"])
        cloud_provider = get_parameter(["mongodb_atlas", "cloud_provider"])
        app_id = get_parameter(["mongodb_atlas", "app_id"])
        api_key = get_parameter(["mongodb_atlas", "api_key"])

        if not (
            region is None
            and cloud_provider is None
            and app_id is None
            and api_key is None
        ):
            host = f"{region}.{cloud_provider}.data.mongodb-api.com"
            query = f"app/{app_id}/endpoint/data/v1/action/insertMany"
            url = f"https://{host}/{query}"
        else:
            debug.error("There are missing parameters for MongoDB Atlas.")

        header = "\n".join(
            [
                f"POST /{query} HTTP/1.1",
                f"Host: {host}",
                "Content-Type: application/json",
                f"Content-Length: {len(payload)+1}",
                f"apiKey: {api_key}",
                "\n\n",
            ]
        )

        data = header + json.dumps(payload)

        return self.base_http_function(
            "mongodb_atlas.insert_many", "POST", url, data, "insertedIds"
        )

    def update_one(
        self, payload, region=None, cloud_provider=None, app_id=None, api_key=None
    ):
        """
        Function for update a document in MongoDB Atlas.

        Parameters
        ----------
        payload: dict
            Payload for the request.
        region: str
            Region of the MongoDB Atlas.
        cloud_provider: str
            Cloud provider of the MongoDB Atlas.
        app_id: str
            Application ID of the MongoDB Atlas.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        region = get_parameter(["mongodb_atlas", "region"])
        cloud_provider = get_parameter(["mongodb_atlas", "cloud_provider"])
        app_id = get_parameter(["mongodb_atlas", "app_id"])
        api_key = get_parameter(["mongodb_atlas", "api_key"])

        if not (
            region is None
            and cloud_provider is None
            and app_id is None
            and api_key is None
        ):
            host = f"{region}.{cloud_provider}.data.mongodb-api.com"
            query = f"app/{app_id}/endpoint/data/v1/action/updateOne"
            url = f"https://{host}/{query}"
        else:
            debug.error("There are missing parameters for MongoDB Atlas.")

        header = "\n".join(
            [
                f"POST /{query} HTTP/1.1",
                f"Host: {host}",
                "Content-Type: application/json",
                f"Content-Length: {len(payload)+1}",
                f"apiKey: {api_key}",
                "\n\n",
            ]
        )

        data = header + json.dumps(payload)

        return self.base_http_function(
            "mongodb_atlas.update_one", "POST", url, data, "matchedCount"
        )

    def update_many(
        self, payload, region=None, cloud_provider=None, app_id=None, api_key=None
    ):
        """
        Function for updating multiple documents in MongoDB Atlas.

        Parameters
        ----------
        payload: dict
            Payload for the request.
        region: str
            Region of the MongoDB Atlas.
        cloud_provider: str
            Cloud provider of the MongoDB Atlas.
        app_id: str
            Application ID of the MongoDB Atlas.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        region = get_parameter(["mongodb_atlas", "region"])
        cloud_provider = get_parameter(["mongodb_atlas", "cloud_provider"])
        app_id = get_parameter(["mongodb_atlas", "app_id"])
        api_key = get_parameter(["mongodb_atlas", "api_key"])

        if not (
            region is None
            and cloud_provider is None
            and app_id is None
            and api_key is None
        ):
            host = f"{region}.{cloud_provider}.data.mongodb-api.com"
            query = f"app/{app_id}/endpoint/data/v1/action/updateMany"
            url = f"https://{host}/{query}"
        else:
            debug.error("There are missing parameters for MongoDB Atlas.")

        header = "\n".join(
            [
                f"POST /{query} HTTP/1.1",
                f"Host: {host}",
                "Content-Type: application/json",
                f"Content-Length: {len(payload)+1}",
                f"apiKey: {api_key}",
                "\n\n",
            ]
        )

        data = header + json.dumps(payload)

        return self.base_http_function(
            "mongodb_atlas.update_many", "POST", url, data, "matchedCount"
        )

    def delete_one(
        self, payload, region=None, cloud_provider=None, app_id=None, api_key=None
    ):
        """
        Function for deleting a document in MongoDB Atlas.

        Parameters
        ----------
        payload: dict
            Payload for the request.
        region: str
            Region of the MongoDB Atlas.
        cloud_provider: str
            Cloud provider of the MongoDB Atlas.
        app_id: str
            Application ID of the MongoDB Atlas.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        region = get_parameter(["mongodb_atlas", "region"])
        cloud_provider = get_parameter(["mongodb_atlas", "cloud_provider"])
        app_id = get_parameter(["mongodb_atlas", "app_id"])
        api_key = get_parameter(["mongodb_atlas", "api_key"])

        if not (
            region is None
            and cloud_provider is None
            and app_id is None
            and api_key is None
        ):
            host = f"{region}.{cloud_provider}.data.mongodb-api.com"
            query = f"app/{app_id}/endpoint/data/v1/action/deleteOne"
            url = f"https://{host}/{query}"
        else:
            debug.error("There are missing parameters for MongoDB Atlas.")

        header = "\n".join(
            [
                f"POST /{query} HTTP/1.1",
                f"Host: {host}",
                "Content-Type: application/json",
                f"Content-Length: {len(payload)+1}",
                f"apiKey: {api_key}",
                "\n\n",
            ]
        )

        data = header + json.dumps(payload)

        return self.base_http_function(
            "mongodb_atlas.delete_one", "POST", url, data, "deletedCount"
        )

    def delete_many(
        self, payload, region=None, cloud_provider=None, app_id=None, api_key=None
    ):
        """
        Function for deleting multiple documents in MongoDB Atlas.

        Parameters
        ----------
        payload: dict
            Payload for the request.
        region: str
            Region of the MongoDB Atlas.
        cloud_provider: str
            Cloud provider of the MongoDB Atlas.
        app_id: str
            Application ID of the MongoDB Atlas.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        region = get_parameter(["mongodb_atlas", "region"])
        cloud_provider = get_parameter(["mongodb_atlas", "cloud_provider"])
        app_id = get_parameter(["mongodb_atlas", "app_id"])
        api_key = get_parameter(["mongodb_atlas", "api_key"])

        if not (
            region is None
            and cloud_provider is None
            and app_id is None
            and api_key is None
        ):
            host = f"{region}.{cloud_provider}.data.mongodb-api.com"
            query = f"app/{app_id}/endpoint/data/v1/action/deleteMany"
            url = f"https://{host}/{query}"
        else:
            debug.error("There are missing parameters for MongoDB Atlas.")

        header = "\n".join(
            [
                f"POST /{query} HTTP/1.1",
                f"Host: {host}",
                "Content-Type: application/json",
                f"Content-Length: {len(payload)+1}",
                f"apiKey: {api_key}",
                "\n\n",
            ]
        )

        data = header + json.dumps(payload)

        return self.base_http_function(
            "mongodb_atlas.delete_many", "POST", url, data, "deletedCount"
        )
