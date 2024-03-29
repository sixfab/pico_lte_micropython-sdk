"""
Module for including functions of MongoDB Atlas for for PicoLTE module.
"""

import time

from pico_lte.common import debug
from pico_lte.utils.manager import StateManager, Step
from pico_lte.utils.status import Status
from pico_lte.utils.helpers import get_parameter


class MongoDBAtlas:
    """
    Class for including functions of MongoDB Atlas operations for PicoLTE module.
    """

    def __init__(self, base, network, http, ssl):
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
        ssl : SSL
            PicoLTE SSL class
        """
        self.base = base
        self.network = network
        self.http = http
        self.ssl = ssl

    def base_http_function(
        self,
        function_name,
        base_url,
        endpoint,
        api_key,
        payload,
        desired_response,
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

        base_url = get_parameter(["mongodb_atlas", "base_url"])
        api_key = get_parameter(["mongodb_atlas", "api_key"])

        url = base_url + endpoint

        if (url is not None) and (api_key is not None):
            temp_url = url.replace("https://", "")
            index = temp_url.find("/") if temp_url.find("/") != -1 else len(temp_url)
            host = temp_url[:index]
            query = temp_url[index:]
        else:
            debug.error("There are missing parameters for MongoDB Atlas.")

        header = "\n".join(
            [
                f"POST {query} HTTP/1.1",
                f"Host: {host}",
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
            success="http_ssl_configuration",
            fail="failure",
        )

        step_http_ssl_configuration = Step(
            function=self.http.set_ssl_context_id,
            name="http_ssl_configuration",
            success="set_sni",
            fail="failure",
            function_params={"cid": 1},
        )

        step_set_sni = Step(
            function=self.ssl.set_sni,
            name="set_sni",
            success="set_server_url",
            fail="failure",
            function_params={"ssl_context_id": 1, "sni": 1},
        )

        step_set_server_url = Step(
            function=self.http.set_server_url,
            name="set_server_url",
            success="post_request",
            fail="failure",
            function_params={"url": url},
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
            function_params={"desired_response": desired_response},
        )

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_http_ssl_configuration)
        sm.add_step(step_set_sni)
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

    def find_one(self, payload, base_url=None, api_key=None):
        """
        Function for finding a document in MongoDB Atlas.

        Parameters
        ----------
        payload: str
            JSON payload for sending to the MongoDB Atlas.
        base_url: str
            Base URL of the MongoDB Atlas Data API.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        return self.base_http_function(
            function_name="mongodb_atlas.find_one",
            base_url=base_url,
            endpoint="/action/findOne",
            api_key=api_key,
            payload=payload,
            desired_response="document",
        )

    def find_many(self, payload, base_url=None, api_key=None):
        """
        Function for finding multiple documents in MongoDB Atlas.

        Parameters
        ----------
        payload: str
            JSON payload for sending to the MongoDB Atlas.
        base_url: str
            Base URL of the MongoDB Atlas Data API.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        return self.base_http_function(
            function_name="mongodb_atlas.find_many",
            base_url=base_url,
            endpoint="/action/find",
            api_key=api_key,
            payload=payload,
            desired_response="documents",
        )

    def insert_one(self, payload, base_url=None, api_key=None):
        """
        Function for inserting a document in MongoDB Atlas.

        Parameters
        ----------
        payload: str
            JSON payload for sending to the MongoDB Atlas.
        base_url: str
            Base URL of the MongoDB Atlas Data API.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        return self.base_http_function(
            function_name="mongodb_atlas.insert_one",
            base_url=base_url,
            endpoint="/action/insertOne",
            api_key=api_key,
            payload=payload,
            desired_response="insertedId",
        )

    def insert_many(self, payload, base_url=None, api_key=None):
        """
        Function for inserting multiple documents in MongoDB Atlas.

        Parameters
        ----------
        payload: str
            JSON payload for sending to the MongoDB Atlas.
        base_url: str
            Base URL of the MongoDB Atlas Data API.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        return self.base_http_function(
            function_name="mongodb_atlas.insert_many",
            base_url=base_url,
            endpoint="/action/insertMany",
            api_key=api_key,
            payload=payload,
            desired_response="insertedIds",
        )

    def update_one(self, payload, base_url=None, api_key=None):
        """
        Function for updating a document in MongoDB Atlas.

        Parameters
        ----------
        payload: str
            JSON payload for sending to the MongoDB Atlas.
        base_url: str
            Base URL of the MongoDB Atlas Data API.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        return self.base_http_function(
            function_name="mongodb_atlas.update_one",
            base_url=base_url,
            endpoint="/action/updateOne",
            api_key=api_key,
            payload=payload,
            desired_response="matchedCount",
        )

    def update_many(self, payload, base_url=None, api_key=None):
        """
        Function for updating multiple documents in MongoDB Atlas.

        Parameters
        ----------
        payload: str
            JSON payload for sending to the MongoDB Atlas.
        base_url: str
            Base URL of the MongoDB Atlas Data API.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        return self.base_http_function(
            function_name="mongodb_atlas.update_many",
            base_url=base_url,
            endpoint="/action/updateMany",
            api_key=api_key,
            payload=payload,
            desired_response="matchedCount",
        )

    def delete_one(self, payload, base_url=None, api_key=None):
        """
        Function for deleting a document in MongoDB Atlas.

        Parameters
        ----------
        payload: str
            JSON payload for sending to the MongoDB Atlas.
        base_url: str
            Base URL of the MongoDB Atlas Data API.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        return self.base_http_function(
            function_name="mongodb_atlas.delete_one",
            base_url=base_url,
            endpoint="/action/deleteOne",
            api_key=api_key,
            payload=payload,
            desired_response="deletedCount",
        )

    def delete_many(self, payload, base_url=None, api_key=None):
        """
        Function for deleting multiple documents in MongoDB Atlas.

        Parameters
        ----------
        payload: str
            JSON payload for sending to the MongoDB Atlas.
        base_url: str
            Base URL of the MongoDB Atlas Data API.
        api_key: str
            API key of the MongoDB Atlas.

        Returns
        -------
        dict
            Result dictionary that contains "status" and "response" keys.
        """

        return self.base_http_function(
            function_name="mongodb_atlas.delete_many",
            base_url=base_url,
            endpoint="/action/deleteMany",
            api_key=api_key,
            payload=payload,
            desired_response="deletedCount",
        )
