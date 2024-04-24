"""
Module for including functions of HiveMQ operations of PicoLTE module.
"""

import time

from pico_lte.common import config
from pico_lte.utils.manager import StateManager, Step
from pico_lte.utils.status import Status
from pico_lte.utils.helpers import get_parameter


class HiveMQ:
    """
    Class for including functions of HiveMQ operations of PicoLTE module.
    """

    cache = config["cache"]

    def __init__(self, base, auth, network, ssl, mqtt):
        """Constructor of the class.

        Parameters
        ----------
        base : Base
            Modem Base instance
        network : Network
            Modem Network instance
        mqtt : MQTT
            Modem MQTT instance
        """
        self.base = base
        self.auth = auth
        self.network = network
        self.ssl = ssl
        self.mqtt = mqtt

    def publish_message(
        self,
        payload,
        host=None,
        port=None,
        topic=None,
        client_id=None,
        username=None,
        password=None,
    ):
        """
        Function for publishing a message to HiveMQ by using MQTT.

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
        username : str
            Username for authenticating with the MQTT broker.
        password : str
            Password for authenticating with the MQTT broker.


        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if host is None:
            host = get_parameter(["hivemq", "host"])

        if port is None:
            port = get_parameter(["hivemq", "port"], 8883)

        if username is None:
            username = get_parameter(["hivemq", "username"])

        if client_id is None:
            client_id = get_parameter(["hivemq", "client_id"])

        if password is None:
            password = get_parameter(["hivemq", "password"])

        if topic is None:
            topic = get_parameter(["hivemq", "pub_topic"])

        # Check if client is connected to the broker
        step_check_mqtt_connected = Step(
            function=self.mqtt.is_connected_to_broker,
            name="check_connected",
            success="publish_message",
            fail="check_opened",
        )

        # Check if client connected to HiveMQ
        step_check_mqtt_opened = Step(
            function=self.mqtt.has_opened_connection,
            name="check_opened",
            success="connect_mqtt_broker",
            fail="deactivate_pdp_context",
        )

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
            success="set_sni",
            fail="failure",
        )

        step_set_sni = Step(
            function=self.ssl.set_sni,
            name="set_sni",
            success="set_mqtt_version",
            fail="failure",
            function_params={"ssl_context_id": 2, "sni": 1},
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
                "client_id_string": client_id,
                "username": username,
                "password": password,
            },
        )

        step_publish_message = Step(
            function=self.mqtt.publish_message,
            name="publish_message",
            success="success",
            fail="failure",
            function_params={"payload": payload, "topic": topic, "qos": 1},
            retry=2,
            interval=1,
            cachable=True,
        )

        # Add cache if it is not already existed
        function_name = "hivemq.publish_message"

        sm = StateManager(first_step=step_check_mqtt_connected, function_name=function_name)

        sm.add_step(step_check_mqtt_connected)
        sm.add_step(step_check_mqtt_opened)
        sm.add_step(step_deactivate_pdp_context)
        sm.add_step(step_load_certificates)
        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_ssl_configuration)
        sm.add_step(step_set_sni)
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
        password=None,
    ):
        """
        Function for subscribing to topics of HiveMQ.

        Parameters
        ----------
        host : str
            Host of the MQTT broker.
        port : int
            Port of the MQTT broker.
        topics : list
            List of topics.
        username : str
            Username for authenticating with the MQTT broker.
        password : str
            Password for authenticating with the MQTT broker.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if host is None:
            host = get_parameter(["hivemq", "host"])

        if port is None:
            port = get_parameter(["hivemq", "port"], 8883)

        if client_id is None:
            client_id = get_parameter(["hivemq", "client_id"])

        if username is None:
            username = get_parameter(["hivemq", "username"])

        if password is None:
            password = get_parameter(["hivemq", "password"])

        if topics is None:
            topics = get_parameter(["hivemq", "sub_topics"])

        # Check if client is connected to the broker
        step_check_mqtt_connected = Step(
            function=self.mqtt.is_connected_to_broker,
            name="check_connected",
            success="subscribe_topics",
            fail="check_opened",
        )

        # Check if client connected to HiveMQ IoT
        step_check_mqtt_opened = Step(
            function=self.mqtt.has_opened_connection,
            name="check_opened",
            success="connect_mqtt_broker",
            fail="deactivate_pdp_context",
        )

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
            success="set_sni",
            fail="failure",
        )

        step_set_sni = Step(
            function=self.ssl.set_sni,
            name="set_sni",
            success="set_mqtt_version",
            fail="failure",
            function_params={"ssl_context_id": 2, "sni": 1},
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
                "client_id_string": client_id,
                "username": username,
                "password": password,
            },
        )

        step_subscribe_topics = Step(
            function=self.mqtt.subscribe_topics,
            name="subscribe_topics",
            success="success",
            fail="failure",
            function_params={"topics": topics},
            retry=2,
            interval=1,
            cachable=True,
        )

        # Add cache if it is not already existed
        function_name = "hivemq.subscribe_message"

        sm = StateManager(first_step=step_check_mqtt_connected, function_name=function_name)

        sm.add_step(step_check_mqtt_connected)
        sm.add_step(step_check_mqtt_opened)
        sm.add_step(step_deactivate_pdp_context)
        sm.add_step(step_load_certificates)
        sm.add_step(step_network_reg)
        sm.add_step(step_get_pdp_ready)
        sm.add_step(step_ssl_configuration)
        sm.add_step(step_set_sni)
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
