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

    def __init__(self, base, network, mqtt):
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
        self.network = network
        self.mqtt = mqtt

    def publish_message(
        self, payload, host=None, port=None, topic=None, username=None, password=None
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
            host = get_parameter(["hivemq", "mqtts", "url"])

        if port is None:
            port = get_parameter(["hivemq", "mqtts", "port"], 8883)

        if username is None:
            username = get_parameter(["hivemq", "mqtts", "username"])

        if password is None:
            password = get_parameter(["hivemq", "mqtts", "password"])

        if topic is None:
            topic = get_parameter(["hivemq", "mqtts", "pub_topic"])

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
            fail="register_network",
        )

        step_network_reg = Step(
            function=self.network.register_network,
            name="register_network",
            success="get_pdp_ready",
            fail="failure",
        )

        step_pdp_ready = Step(
            function=self.network.get_pdp_ready,
            name="get_pdp_ready",
            success="open_mqtt_connection",
            fail="failure",
        )

        step_open_mqtt_connection = Step(
            function=self.mqtt.open_connection,
            name="open_mqtt_connection",
            success="connect_mqtt_broker",
            fail="failure",
            function_params={"host": host, "port": port},
            interval=1,
        )

        step_connect_mqtt_broker = Step(
            function=self.mqtt.connect_broker,
            name="connect_mqtt_broker",
            success="publish_message",
            fail="failure",
            function_params={
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
            retry=3,
            interval=1,
        )

        # Add cache if it is not already existed
        function_name = "hivemq.publish_message"

        sm = StateManager(
            first_step=step_check_mqtt_connected, function_name=function_name
        )

        sm.add_step(step_check_mqtt_connected)
        sm.add_step(step_check_mqtt_opened)
        sm.add_step(step_network_reg)
        sm.add_step(step_pdp_ready)
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
        self, host=None, port=None, topics=None, username=None, password=None
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
            host = get_parameter(["hivemq", "mqtts", "url"])

        if port is None:
            port = get_parameter(["hivemq", "mqtts", "port"], 8883)

        if username is None:
            username = get_parameter(["thingspeak", "mqtts", "username"])

        if password is None:
            password = get_parameter(["thingspeak", "mqtts", "password"])

        if topics is None:
            topics = get_parameter(["hivemq", "mqtts", "sub_topics"])

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

        step_network_reg = Step(
            function=self.network.register_network,
            name="register_network",
            success="get_pdp_ready",
            fail="failure",
        )

        step_pdp_ready = Step(
            function=self.network.get_pdp_ready,
            name="get_pdp_ready",
            success="open_mqtt_connection",
            fail="failure",
        )

        step_open_mqtt_connection = Step(
            function=self.mqtt.open_connection,
            name="open_mqtt_connection",
            success="connect_mqtt_broker",
            fail="failure",
            function_params={"host": host, "port": port},
            interval=1,
        )

        step_connect_mqtt_broker = Step(
            function=self.mqtt.connect_broker,
            name="connect_mqtt_broker",
            success="subscribe_topics",
            fail="failure",
            function_params={
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
            retry=3,
            interval=1,
        )

        # Add cache if it is not already existed
        function_name = "hivemq.subscribe_message"

        sm = StateManager(
            first_step=step_check_mqtt_connected, function_name=function_name
        )

        sm.add_step(step_check_mqtt_connected)
        sm.add_step(step_check_mqtt_opened)
        sm.add_step(step_network_reg)
        sm.add_step(step_pdp_ready)
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
