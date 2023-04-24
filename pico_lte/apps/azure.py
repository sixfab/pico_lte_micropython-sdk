"""
Module for including functions of Azure IoT operations of PicoLTE module.
"""

import time

from pico_lte.common import config
from pico_lte.utils.manager import StateManager, Step
from pico_lte.common import Status
from pico_lte.utils.helpers import get_parameter


class Azure:
    """
    Class for including functions of Azure IoT operations of PicoLTE module.
    """

    cache = config["cache"]

    def __init__(self, base, auth, network, ssl, mqtt, http, device_id=None, hub_name=None):
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

        self.device_id = get_parameter(["azure", "device_id"]) if (device_id is None) else device_id
        self.hub_name = get_parameter(["azure", "hub_name"]) if (hub_name is None) else hub_name

    def publish_message(
        self, payload, host=None, port=None, topic=None, client_id=None, username=None
    ):
        """
        Function for publishing a message to Azure IoT Hub by using MQTT.

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
        host = (
            get_parameter(["azure", "mqtts", "host"], f"{self.hub_name}.azure-devices.net")
            if (host is None)
            else host
        )

        port = get_parameter(["azure", "mqtts", "port"], 8883) if (port is None) else port

        topic = (
            get_parameter(
                ["azure", "mqtts", "pub_topic"], "$iothub/twin/PATCH/properties/reported/?$rid=1"
            )
            if (topic is None)
            else topic
        )

        client_id = (
            get_parameter(["azure", "mqtts", "client_id"], self.device_id)
            if (client_id is None)
            else client_id
        )

        username = (
            get_parameter(
                ["azure", "mqtts", "username"],
                f"{self.hub_name}.azure-devices.net/{self.device_id}/?api-version=2021-04-12",
            )
            if (username is None)
            else username
        )

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
            function_params={
                "username": username,
                "password": "unused",
                "client_id": client_id,
            },
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
        function_name = "azure.publish_message"

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

    def subscribe_topics(self, host=None, port=None, topics=None, client_id=None, username=None):
        """
        Function for subscribing to topics of Azure IoT Hub.

        Parameters
        ----------
        topics : list
            List of topics.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        host = (
            get_parameter(["azure", "mqtts", "host"], f"{self.hub_name}.azure-devices.net")
            if (host is None)
            else host
        )

        port = get_parameter(["azure", "mqtts", "port"], 8883) if (port is None) else port

        topics = get_parameter(["azure", "mqtts", "sub_topics"]) if (topics is None) else topics

        client_id = (
            get_parameter(["azure", "mqtts", "client_id"], self.device_id)
            if (client_id is None)
            else client_id
        )

        username = (
            get_parameter(
                ["azure", "mqtts", "username"],
                f"{self.hub_name}.azure-devices.net/{self.device_id}/?api-version=2021-04-12",
            )
            if (username is None)
            else username
        )

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
            function_params={
                "username": username,
                "password": "unused",
                "client_id": client_id,
            },
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
        function_name = "azure.subscribe_message"

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

    def subscribe_to_device_commands(self):
        """Subscribe to the device commands from Azure IoT Hub

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        return self.subscribe_topics(
            topics=[(f"devices/{self.device_id}/messages/devicebound/#", 1)]
        )

    def retrieve_device_twin_status(self):
        """It sends a request to the MQTT server for retriving the "desired" and
        "reported" status of the device twin. You need to call read_messages() after
        this method.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        self.subscribe_topics(topics=["$iothub/twin/res/#", 1])
        return self.publish_message("", topic="$iothub/twin/GET/?$rid=1")
