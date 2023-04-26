"""
Module for including functions of Azure IoT operations of PicoLTE module.
"""

import time

from pico_lte.utils.manager import StateManager, Step
from pico_lte.common import Status
from pico_lte.utils.helpers import get_parameter


class Azure:
    """
    Class for including functions of Azure IoT operations of PicoLTE module.
    """

    APP_NAME = "azure"

    def __init__(self, base, auth, network, ssl, mqtt, http):
        """
        Constructor of the class.
        """
        self.base = base
        self.auth = auth
        self.network = network
        self.ssl = ssl
        self.mqtt = mqtt
        self.http = http

    def publish_message(
        self,
        payload,
        host=None,
        port=None,
        topic=None,
        client_id=None,
        username=None,
        device_id=None,
        hub_name=None,
    ):
        """
        Function for publishing a message to Azure IoT Hub by using MQTT.

        Parameters
        ----------
        payload : str, required
            Payload of the message.
        device_id : str, required
            Device ID of the Azure IoT Hub. If not provided,
            it will be read from the configuration file.
        hub_name : str, required
            Name of the Azure IoT Hub. If not provided,
            it will be read from the configuration file.
        host : str, optional
            Host of the MQTT broker.
        port : int, optional
            Port of the MQTT broker.
        topic : str, optional
            Topic of the message. If not provided,
            all reported fields will be updated.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if device_id is None:
            device_id = get_parameter([self.APP_NAME, "device_id"])

        if hub_name is None:
            hub_name = get_parameter([self.APP_NAME, "hub_name"])

        if host is None:
            host = get_parameter(
                [self.APP_NAME, "host"], f"{hub_name}.azure-devices.net"
            )

        if port is None:
            port = get_parameter([self.APP_NAME, "port"], 8883)

        if topic is None:
            topic = get_parameter(
                [self.APP_NAME, "pub_topic"],
                "$iothub/twin/PATCH/properties/reported/?$rid=1",
            )

        if client_id is None:
            client_id = get_parameter([self.APP_NAME, "client_id"], device_id)

        if username is None:
            username = get_parameter(
                [self.APP_NAME, "username"],
                f"{hub_name}.azure-devices.net/{device_id}/?api-version=2021-04-12",
            )

        # Check if client is connected to the broker
        step_check_mqtt_connected = Step(
            function=self.mqtt.is_connected_to_broker,
            name=self.APP_NAME + "_check_connected",
            success=self.APP_NAME + "_publish_message",
            fail=self.APP_NAME + "_check_opened",
        )

        # Check if client connected to AWS IoT
        step_check_mqtt_opened = Step(
            function=self.mqtt.has_opened_connection,
            name=self.APP_NAME + "_check_opened",
            success=self.APP_NAME + "_connect_mqtt_broker",
            fail=self.APP_NAME + "_deactivate_pdp_context",
        )

        # If client is not connected to the broker and have no open connection with AWS IoT
        # Deactivate PDP and begin first step of the state machine
        step_deactivate_pdp_context = Step(
            function=self.network.deactivate_pdp_context,
            name=self.APP_NAME + "_deactivate_pdp_context",
            success=self.APP_NAME + "_load_certificates",
            fail="failure",
        )

        step_load_certificates = Step(
            function=self.auth.load_certificates,
            name=self.APP_NAME + "_load_certificates",
            success=self.APP_NAME + "_register_network",
            fail="failure",
        )
        step_network_reg = Step(
            function=self.network.register_network,
            name=self.APP_NAME + "_register_network",
            success=self.APP_NAME + "_get_ready_pdp",
            fail="failure",
        )

        step_get_pdp_ready = Step(
            function=self.network.get_pdp_ready,
            name=self.APP_NAME + "_get_ready_pdp",
            success=self.APP_NAME + "_ssl_configuration",
            fail="failure",
        )

        step_ssl_configuration = Step(
            function=self.ssl.configure_for_x509_certification,
            name=self.APP_NAME + "_ssl_configuration",
            success=self.APP_NAME + "_set_mqtt_version",
            fail="failure",
            cachable=True,
        )

        step_set_mqtt_version = Step(
            function=self.mqtt.set_version_config,
            name=self.APP_NAME + "_set_mqtt_version",
            success=self.APP_NAME + "_set_mqtt_ssl_mode",
            fail="failure",
        )

        step_set_mqtt_ssl_mode = Step(
            function=self.mqtt.set_ssl_mode_config,
            name=self.APP_NAME + "_set_mqtt_ssl_mode",
            success=self.APP_NAME + "_open_mqtt_connection",
            fail="failure",
        )

        step_open_mqtt_connection = Step(
            function=self.mqtt.open_connection,
            name=self.APP_NAME + "_open_mqtt_connection",
            success=self.APP_NAME + "_connect_mqtt_broker",
            fail="failure",
            function_params={"host": host, "port": port},
        )

        step_connect_mqtt_broker = Step(
            function=self.mqtt.connect_broker,
            name=self.APP_NAME + "_connect_mqtt_broker",
            success=self.APP_NAME + "_publish_message",
            fail="failure",
            function_params={
                "username": username,
                "password": "unused",
                "client_id": client_id,
            },
        )

        step_publish_message = Step(
            function=self.mqtt.publish_message,
            name=self.APP_NAME + "_publish_message",
            success="success",
            fail="failure",
            function_params={"payload": payload, "topic": topic},
            cachable=True,
        )

        # Add cache if it is not already existed
        function_name = self.APP_NAME + "..publish_message"

        sm = StateManager(
            first_step=step_check_mqtt_connected, function_name=function_name
        )

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

    def subscribe_topics(
        self,
        host=None,
        port=None,
        topics=None,
        client_id=None,
        username=None,
        device_id=None,
        hub_name=None,
    ):
        """
        Function for subscribing to topics of Azure IoT Hub.

        Parameters
        ----------
        device_id : str, required
            Device ID of the device. If not provided,
            it will be taken from the config file.
        hub_name : str, required
            Hub name of the devie. If not provided,
            it will be taken from the config file.
        topics : list, required
            List of topics to subscribe. If not provided,
            it will be taken from the config file.
        host : str, optional
            Host of the broker.
        port : int, optional
            Port of the broker.
        client_id : str, optional
            Client ID of the device.
        username : str, optional
            Username of the device.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if device_id is None:
            device_id = get_parameter([self.APP_NAME, "device_id"])

        if hub_name is None:
            hub_name = get_parameter([self.APP_NAME, "hub_name"])

        if topics is None:
            topics = get_parameter([self.APP_NAME, "sub_topics"])

        if host is None:
            host = get_parameter(
                [self.APP_NAME, "host"], f"{hub_name}.azure-devices.net"
            )

        if port is None:
            port = get_parameter([self.APP_NAME, "port"], 8883)

        if client_id is None:
            client_id = get_parameter([self.APP_NAME, "client_id"], device_id)

        if username is None:
            username = get_parameter(
                [self.APP_NAME, "username"],
                f"{hub_name}.azure-devices.net/{device_id}/?api-version=2021-04-30-preview",
            )

        # Check if client is connected to the broker
        step_check_mqtt_connected = Step(
            function=self.mqtt.is_connected_to_broker,
            name=self.APP_NAME + "_check_connected",
            success=self.APP_NAME + "_subscribe_topics",
            fail=self.APP_NAME + "_check_opened",
            retry=2,
        )

        # Check if client connected to AWS IoT
        step_check_mqtt_opened = Step(
            function=self.mqtt.has_opened_connection,
            name=self.APP_NAME + "_check_opened",
            success=self.APP_NAME + "_connect_mqtt_broker",
            fail=self.APP_NAME + "_deactivate_pdp_context",
            retry=2,
        )

        # If client is not connected to the broker and have no open connection with AWS IoT
        # Deactivate PDP and begin first step of the state machine
        step_deactivate_pdp_context = Step(
            function=self.network.deactivate_pdp_context,
            name=self.APP_NAME + "_deactivate_pdp_context",
            success=self.APP_NAME + "_load_certificates",
            fail="failure",
        )

        step_load_certificates = Step(
            function=self.auth.load_certificates,
            name=self.APP_NAME + "_load_certificates",
            success=self.APP_NAME + "_register_network",
            fail="failure",
        )

        step_network_reg = Step(
            function=self.network.register_network,
            name=self.APP_NAME + "_register_network",
            success=self.APP_NAME + "_get_pdp_ready",
            fail="failure",
        )

        step_get_pdp_ready = Step(
            function=self.network.get_pdp_ready,
            name=self.APP_NAME + "_get_pdp_ready",
            success=self.APP_NAME + "_ssl_configuration",
            fail="failure",
        )

        step_ssl_configuration = Step(
            function=self.ssl.configure_for_x509_certification,
            name=self.APP_NAME + "_ssl_configuration",
            success=self.APP_NAME + "_set_mqtt_version",
            fail="failure",
        )

        step_set_mqtt_version = Step(
            function=self.mqtt.set_version_config,
            name=self.APP_NAME + "_set_mqtt_version",
            success=self.APP_NAME + "_set_mqtt_ssl_mode",
            fail="failure",
        )

        step_set_mqtt_ssl_mode = Step(
            function=self.mqtt.set_ssl_mode_config,
            name=self.APP_NAME + "_set_mqtt_ssl_mode",
            success=self.APP_NAME + "_open_mqtt_connection",
            fail="failure",
        )

        step_open_mqtt_connection = Step(
            function=self.mqtt.open_connection,
            name=self.APP_NAME + "_open_mqtt_connection",
            success=self.APP_NAME + "_connect_mqtt_broker",
            fail="failure",
            function_params={"host": host, "port": port},
        )

        step_connect_mqtt_broker = Step(
            function=self.mqtt.connect_broker,
            name=self.APP_NAME + "_connect_mqtt_broker",
            success=self.APP_NAME + "_subscribe_topics",
            fail="failure",
            function_params={
                "username": username,
                "password": "unused",
                "client_id": client_id,
            },
        )

        step_subscribe_topics = Step(
            function=self.mqtt.subscribe_topics,
            name=self.APP_NAME + "_subscribe_topics",
            success="success",
            fail="failure",
            function_params={"topics": topics},
            cachable=True,
        )

        # Add cache if it is not already existed
        function_name = self.APP_NAME + "..subscribe_message"

        sm = StateManager(
            first_step=step_check_mqtt_connected, function_name=function_name
        )

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

    def subscribe_to_device_commands(self, device_id=None):
        """Subscribe to the device commands from Azure IoT Hub

        Parameters
        ----------
        device_id : str, required
            Device ID, if not provided, it will
            be read from the configuration file.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if device_id is None:
            device_id = get_parameter([self.APP_NAME, "device_id"])

        return self.subscribe_topics(
            topics=[(f"devices/{device_id}/messages/devicebound/#", 1)]
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
