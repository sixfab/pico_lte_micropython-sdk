"""
Module for including functions of AWS IoT operations of picocell module.
"""

import time
import json
import ubinascii

from core.temp import config
from core.utils.manager import StateManager, Step
from core.utils.status import Status
from core.utils.helpers import get_parameter

class GCloud:
    """
    Class for including functions of Google Cloud IoT operations of Picocell module.
    """
    cache = config["cache"]

    def __init__(self, base, network, ssl, mqtt, http,
                region=None, project_id=None, registry_id=None, device_id=None, jwt=None):
        """
        Constructor of the class.

        Parameters
        ----------
        cache : dict
            Cache of the class.
        """
        self.base = base
        self.network = network
        self.ssl = ssl
        self.mqtt = mqtt
        self.http = http

        # Assign the account parameters from the config file.
        self.region = get_parameter(["gcloud", "region"]) \
            if (region is None) else region
        self.project_id = get_parameter(["gcloud", "project_id"]) \
            if (project_id is None) else project_id
        self.registry_id = get_parameter(["gcloud", "registry_id"]) \
            if (registry_id is None) else registry_id
        self.device_id = get_parameter(["gcloud", "device_id"]) \
            if (device_id is None) else device_id
        self.jwt = get_parameter(["gcloud", "jwt"]) \
            if (jwt is None) else jwt

        # Create HTTP Attributes.
        self.http_query= '/v1/projects/' + self.project_id + \
            '/locations/' + self.region + \
            '/registries/' + self.registry_id + \
            '/devices/' + self.device_id


    def publish_message(self, payload, host=None, port=None, topic=None, client_id=None):
        """
        Function for publishing a message to GCloud IoT by using MQTT.

        Parameters
        ----------
        payload : str
            Payload of the message.
        host : str
            Host of the MQTT broker.
        port : int
            Port of the MQTT broker.
        topic : str
            Topic of the message.

        Returns
        -------
        (status, modem_response) : tuple
            status : int
                Status of the command.
            modem_response : str
                Response of the modem.
        """
        if host is None:
            host = get_parameter(["gcloud", "mqtts", "host"], default="mqtt.googleapis.com")

        if port is None:
            port = get_parameter(["gcloud", "mqtts", "port"], default=8883)

        if topic is None:
            topic = get_parameter(["gcloud", "mqtts", "pub_topic"],  \
                default=f'/devices/{self.device_id}/events')

        if client_id is None:
            client_id = 'projects/' + self.project_id + '/locations/' + self.region +\
                        '/registries/' + self.registry_id + '/devices/' + self.device_id

        step_network_reg = Step(
            function=self.network.register_network,
            name="register_network",
            success="configure_tcp_ip_context",
            fail="failure",
        )

        step_tcpip_context = Step(
            function=self.network.configure_tcp_ip_context,
            name="configure_tcp_ip_context",
            success="pdp_deactivate",
            fail="failure"
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
            success="set_mqtt_version",
            fail="failure",
        )

        step_set_mqtt_version = Step(
            function=self.mqtt.set_version_config,
            name="set_mqtt_version",
            success="set_mqtt_ssl_mode",
            fail="failure",
        )

        step_set_mqtt_ssl_mode = Step(
            function=self.mqtt.set_ssl_mode_config,
            name="set_mqtt_ssl_mode",
            success="open_mqtt_connection",
            fail="failure",
        )

        step_open_mqtt_connection = Step(
            function=self.mqtt.open_connection,
            name="open_mqtt_connection",
            success="connect_mqtt_broker",
            fail="failure",
            function_params={"host":host, "port":port}
        )

        step_connect_mqtt_broker = Step(
            function=self.mqtt.connect_broker,
            name="connect_mqtt_broker",
            success="publish_message",
            fail="publish_message",
            function_params={"client_id_string":client_id, \
                "username":"unused", "password": self.jwt}
        )

        step_publish_message = Step(
            function=self.mqtt.publish_message,
            name="publish_message",
            success="success",
            fail="failure",
            function_params={"payload":payload, "topic":topic},
            cachable=True,
        )

        # Add cache if it is not already existed
        function_name = "gcloud.publish_message"

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_tcpip_context)
        sm.add_step(step_pdp_deactivate)
        sm.add_step(step_pdp_activate)
        sm.add_step(step_set_mqtt_version)
        sm.add_step(step_set_mqtt_ssl_mode)
        sm.add_step(step_open_mqtt_connection)
        sm.add_step(step_connect_mqtt_broker)
        sm.add_step(step_publish_message)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])


    def post_message(self, payload, url=None):
        """
        Function for publishing a message to AWS IoT by using HTTPS.

        Parameters
        ----------
        payload : str
            Payload of the message.
        url : str
            URL of the AWS device shadow

        Returns
        -------
        (status, modem_response) : tuple
            status : int
                Status of the command.
            modem_response : str
                Response of the modem.
        """
        if url is None:
            url = get_parameter(["gcloud","https","endpoint"],
                "https://cloudiotdevice.googleapis.com")


        gcloud_get_query = '/config?local_version=1'
        gcloud_post_query = ':publishEvent'

        # Create the payload json.
        data_in_base64 = ubinascii.b2a_base64(payload)
        data_post_dict = {'binary_data': data_in_base64[0:-1]}
        payload_to_post = json.dumps(data_post_dict)


        # Construct the header for the request to register the device.
        # It is needed before publishing a message.
        header_get = "GET " + self.http_query + gcloud_get_query + " HTTP/1.1\n" + \
                    "Host: " + url[8:] + "\n" + \
                    "Content-Type: text/plain\n" + \
                    "Content-Length: 0\n" + \
                    "Authorization: Bearer " + self.jwt + "\n" + \
                    "\n\n"
        # Construct the header for the request to publish the message.
        header_post = "POST " + self.http_query + gcloud_post_query + " HTTP/1.1\n" + \
                    "Host: " + url[8:] + "\n" + \
                    "Content-Type: application/json\n" + \
                    "Authorization: Bearer " + self.jwt + "\n" + \
                    "Content-Length: " + str(len(payload_to_post) + 1) + "\n" + \
                    "\n\n"

        # Create the states for the state machine.
        step_network_reg = Step(
            function=self.network.register_network,
            name="register_network",
            success="configure_tcp_ip_context",
            fail="failure",
        )

        step_tcpip_context = Step(
            function=self.network.configure_tcp_ip_context,
            name="configure_tcp_ip_context",
            success="pdp_deactivate",
            fail="failure"
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
            success="set_server_url",
            fail="failure"
        )

        step_set_server_url = Step(
            function=self.http.set_server_url,
            name="set_server_url",
            success="post_request",
            fail="failure",
            function_params={"url": url},
        )

        step_get_request = Step(
            function=self.http.get,
            name="get_request_to_register",
            success="post_request",
            fail="failure",
            function_params={"data": header_get, "header_mode": 1}
        )

        step_post_request = Step(
            function=self.http.post,
            name="post_request",
            success="read_response",
            fail="failure",
            function_params={"data": header_post+payload_to_post,
                            "header_mode": 1},
            cachable=True,
            interval=2,
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
        )

        # Add cache if it is not already existed
        function_name = "gcloud.post_message"

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_network_reg)
        sm.add_step(step_tcpip_context)
        sm.add_step(step_pdp_deactivate)
        sm.add_step(step_pdp_activate)
        sm.add_step(step_set_server_url)
        sm.add_step(step_get_request)
        sm.add_step(step_post_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])
