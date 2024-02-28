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

    def insert_one(
        self, payload, region=None, cloud_provider=None, app_id=None, api_key=None
    ):
        """
        Function for inserting new document in MongoDB Atlas.

        Parameters
        ----------
        payload: dict
            -
        region: str
            -
        cloud_provider: str
            -
        app_id: str
            -
        api_key: str
            -

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

        payload = json.dumps(payload)

        header = "\n".join(
            [
                f"POST /{query} HTTP/1.1",
                f"Host: {host}",
                "Content-Type: application/json",
                f"Content-Length: {len(payload)+1}",
                f"api-key: {api_key}",
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
            function_params={"content_type": 4},
        )

        step_post_request = Step(
            function=self.http.post,
            name="post_request",
            success="read_response",
            fail="failure",
            function_params={
                "header_mode": 1,
                "data": header + payload,
            },
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": "insertedId"},
        )

        # Add cache if it is not already existed
        function_name = "mongodb_atlas.insert_one"

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_set_server_url)
        sm.add_step(step_set_content_type)
        sm.add_step(step_post_request)
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
            -
        region: str
            -
        cloud_provider: str
            -
        app_id: str
            -
        api_key: str
            -

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
            query = f"app/{app_id}/endpoint/data/v1/action/findOne"
            url = f"https://{host}/{query}"
        else:
            debug.error("There are missing parameters for MongoDB Atlas.")

        payload = json.dumps(payload)

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
            function_params={"url": url},
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
            function_params={
                "header_mode": 1,
                "data": header + payload,
            },
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": "document"},
        )

        # Add cache if it is not already existed
        function_name = "mongodb_atlas.find_one"

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_set_server_url)
        sm.add_step(step_set_content_type)
        sm.add_step(step_post_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()
            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def get_clusters(self, username=None, password=None):
        """
        Function for list clusters in MongoDB Atlas.

        Parameters
        ----------
        username: str
            -
        password: str
            -

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        if not (username is None and password is None):
            username = get_parameter(["mongodb_atlas", "username"])
            password = get_parameter(["mongodb_atlas", "password"])
        else:
            debug.error("There are missing parameters for MongoDB Atlas.")

        host = "cloud.mongodb.com"
        query = "api/atlas/v2/clusters"
        url = f"https://{host}/{query}"

        header = "\n".join(
            [
                f"GET /{query} HTTP/1.1",
                f"Host: {host}",
                "Accept: application/vnd.atlas.2023-11-15+json",
                "Custom-Header-Name: Custom-Data",
                "Content-Type: application/json",
                "Content-Length: 0\n",
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
            success="set_server_url",
            fail="failure",
        )

        step_set_server_url = Step(
            function=self.http.set_server_url,
            name="set_server_url",
            success="set_auth",
            fail="failure",
            function_params={"url": url},
        )

        step_set_auth = Step(
            function=self.http.set_auth,
            name="set_auth",
            success="get_request",
            fail="failure",
            function_params={
                "username": f"{username}",
                "password": f"{password}",
            },
        )

        step_get_request = Step(
            function=self.http.get,
            name="get_request",
            success="read_response",
            fail="failure",
            function_params={
                "header_mode": 1,
                "data": header,
            },
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": "results"},
        )

        # Add cache if it is not already existed
        function_name = "mongodb_atlas.get_clusters"

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_set_server_url)
        sm.add_step(step_set_auth)
        sm.add_step(step_get_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()
            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])
