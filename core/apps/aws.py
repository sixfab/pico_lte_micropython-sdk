"""
Module for including functions of AWS IoT operations of picocell module.
"""

import time

from core.temp import config
from core.utils.manager import StateManager, Step
from core.utils.status import Status
from core.utils.helpers import get_parameter


class AWS:
    """
    Class for including functions of AWS IoT operations of picocell module.
    """

    cache = config["cache"]

    def __init__(self, base, auth, network, ssl, mqtt, http):
        """
        Constructor of the class.

        Parameters
        ----------
        cache : dict
            Cache of the class.
        """
        self.base = base
        self.auth = auth
        self.network = network
        self.ssl = ssl
        self.mqtt = mqtt
        self.http = http

    def publish_message(self, payload, host=None, port=None, topic=None):
        """
        Function for publishing a message to AWS IoT by using MQTT.

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
        dict
            Result that includes "status" and "response" keys
        """
        if host is None:
            host = get_parameter(["aws", "mqtts", "host"])

        if port is None:
            port = get_parameter(["aws", "mqtts", "port"], 8883)

        if topic is None:
            topic = get_parameter(["aws", "mqtts", "pub_topic"])

        # Check if client is connected to the broker
        step_check_mqtt_connected = Step(
            function=self.mqtt.is_connected_to_broker,
            name="check_connected",
            success="publish_message",
            fail="check_opened",
        )

        # Check if client connected to AWS IoT
        step_check_mqtt_opened = Step(
            function=self.mqtt.has_opened_connection,
            name="check_opened",
            success="connect_mqtt_broker",
            fail="deactivate_pdp_context",
        )

        # If client is not connected to the broker and have no open connection with AWS IoT
        # Deactivate PDP and begin first step of the state machine
        step_deactivate_pdp_context = Step(
            function=self.network.deactivate_pdp_context,
            name="deactivate_pdp_context",
            success="load_certificates",
            fail="failure",
        )

        step_load_certificates = Step(
            function=self.auth.load_certificates,
            name="load_certificates",
            success="register_network",
            fail="failure",
        )
        step_network_reg = Step(
            function=self.network.register_network,
            name="register_network",
            success="get_ready_pdp",
            fail="failure",
        )

        step_get_pdp_ready = Step(
            function=self.network.get_pdp_ready,
            name="get_ready_pdp",
            success="ssl_configuration",
            fail="failure",
        )

        step_ssl_configuration = Step(
            function=self.ssl.configure_for_x509_certification,
            name="ssl_configuration",
            success="set_mqtt_version",
            fail="failure",
            cachable=True,
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
            function_params={"host": host, "port": port},
        )

        step_connect_mqtt_broker = Step(
            function=self.mqtt.connect_broker,
            name="connect_mqtt_broker",
            success="publish_message",
            fail="failure",
        )

        step_publish_message = Step(
            function=self.mqtt.publish_message,
            name="publish_message",
            success="success",
            fail="failure",
            function_params={"payload": payload, "topic": topic},
            cachable=True,
        )

        # Add cache if it is not already existed
        function_name = "aws.publish_message"

        sm = StateManager(first_step=step_check_mqtt_connected, function_name=function_name)

        sm.add_step(step_check_mqtt_connected)
        sm.add_step(step_check_mqtt_opened)
        sm.add_step(step_deactivate_pdp_context)
        sm.add_step(step_load_certificates)
        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_ssl_configuration)
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

    def subscribe_topics(self, host=None, port=None, topics=None):
        """
        Function for subscribing to topics of AWS.

        Parameters
        ----------
        topics : list
            List of topics.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if topics is None:
            topics = get_parameter(["aws", "mqtts", "sub_topics"])

        if host is None:
            host = get_parameter(["aws", "mqtts", "host"])

        if port is None:
            port = get_parameter(["aws", "mqtts", "port"], 8883)

        # Check if client is connected to the broker
        step_check_mqtt_connected = Step(
            function=self.mqtt.is_connected_to_broker,
            name="check_connected",
            success="subscribe_topics",
            fail="check_opened",
            retry=2,
        )

        # Check if client connected to AWS IoT
        step_check_mqtt_opened = Step(
            function=self.mqtt.has_opened_connection,
            name="check_opened",
            success="connect_mqtt_broker",
            fail="deactivate_pdp_context",
            retry=2,
        )

        # If client is not connected to the broker and have no open connection with AWS IoT
        # Deactivate PDP and begin first step of the state machine
        step_deactivate_pdp_context = Step(
            function=self.network.deactivate_pdp_context,
            name="deactivate_pdp_context",
            success="load_certificates",
            fail="failure",
        )

        step_load_certificates = Step(
            function=self.auth.load_certificates,
            name="load_certificates",
            success="register_network",
            fail="failure",
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
            success="ssl_configuration",
            fail="failure",
        )

        step_ssl_configuration = Step(
            function=self.ssl.configure_for_x509_certification,
            name="ssl_configuration",
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
            function_params={"host": host, "port": port},
        )

        step_connect_mqtt_broker = Step(
            function=self.mqtt.connect_broker,
            name="connect_mqtt_broker",
            success="subscribe_topics",
            fail="failure",
        )

        step_subscribe_topics = Step(
            function=self.mqtt.subscribe_topics,
            name="subscribe_topics",
            success="success",
            fail="failure",
            function_params={"topics": topics},
            cachable=True,
        )

        # Add cache if it is not already existed
        function_name = "aws.subscribe_message"

        sm = StateManager(first_step=step_check_mqtt_connected, function_name=function_name)

        sm.add_step(step_check_mqtt_connected)
        sm.add_step(step_check_mqtt_opened)
        sm.add_step(step_deactivate_pdp_context)
        sm.add_step(step_load_certificates)
        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_ssl_configuration)
        sm.add_step(step_set_mqtt_version)
        sm.add_step(step_set_mqtt_ssl_mode)
        sm.add_step(step_open_mqtt_connection)
        sm.add_step(step_connect_mqtt_broker)
        sm.add_step(step_subscribe_topics)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def read_messages(self):
        """
        Read messages from subscribed topics.
        """
        return self.mqtt.read_messages()

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
        dict
            Result that includes "status" and "response" keys
        """
        if url is None:
            endpoint = get_parameter(["aws", "https", "endpoint"])
            topic = get_parameter(["aws", "https", "topic"])

            if endpoint and topic:
                url = f"https://{endpoint}:8443/topics/{topic}?qos=1"

        step_load_certificates = Step(
            function=self.auth.load_certificates,
            name="load_certificates",
            success="register_network",
            fail="failure",
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
            success="ssl_configuration",
            fail="failure",
        )

        step_ssl_configuration = Step(
            function=self.ssl.configure_for_x509_certification,
            name="ssl_configuration",
            success="http_ssl_configuration",
            fail="failure",
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
            success="post_request",
            fail="failure",
            function_params={"url": url},
        )

        step_post_request = Step(
            function=self.http.post,
            name="post_request",
            success="read_response",
            fail="failure",
            function_params={"data": payload},
            cachable=True,
            interval=2,
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
            function_params={"desired_response": '"message":"OK"'},
        )

        # Add cache if it is not already existed
        function_name = "aws.post_message"

        sm = StateManager(first_step=step_load_certificates, function_name=function_name)

        sm.add_step(step_load_certificates)
        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_ssl_configuration)
        sm.add_step(step_http_ssl_configuration)
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
