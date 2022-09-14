"""
Module for including functions of ThingSpeak for Picocell module.
"""
import time

from core.temp import config
from core.utils.manager import StateManager, Step
from core.utils.status import Status
from core.utils.helpers import get_parameter


class ThingSpeak:
    """
    Class for including functions of ThingSpeak operations for Picocell module.
    """
    cache = config["cache"]

    def __init__(self, base, network, mqtt, channel_id=None):
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
        self.channel_id = get_parameter(["thingspeak", "channel_id"]) \
            if (channel_id is None) else channel_id

    def publish_message(self, payload, host=None, port=None, topic=None,
                        client_id=None, username=None, password=None):
        """
        Function for publishing a message to ThingSpeak.

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
            host = get_parameter(["thingspeak", "mqtts", "host"], "mqtt3.thingspeak.com")

        if port is None:
            port = get_parameter(["thingspeak", "mqtts", "port"], 1883)

        if client_id is None:
            client_id = get_parameter(["thingspeak", "mqtts", "client_id"])

        if username is None:
            username = get_parameter(["thingspeak", "mqtts", "username"])

        if password is None:
            password = get_parameter(["thingspeak", "mqtts", "password"])

        if topic is None:
            topic = get_parameter(["thingspeak", "mqtts", "pub_topic"],  \
                "channels/" + str(self.channel_id) + "/publish")

        # Create message from dictionary if needed.
        if type(payload) == dict:
            payload = ThingSpeak.create_message(payload)

        # Check if client is connected to the broker
        step_check_mqtt_connected = Step(
            function=self.mqtt.is_connected_to_broker,
            name="check_connected",
            success="publish_message",
            fail="check_opened",
        )

        # Check if client connected to Google Cloud IoT
        step_check_mqtt_opened = Step(
            function=self.mqtt.has_opened_connection,
            name="check_opened",
            success="connect_mqtt_broker",
            fail="register_network",
        )

        # If client is not connected to the broker and have no open connection with
        # ThingSpeak, begin the first step of the state machine.
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
            interval=1
        )

        step_connect_mqtt_broker = Step(
            function=self.mqtt.connect_broker,
            name="connect_mqtt_broker",
            success="publish_message",
            fail="failure",
            function_params={"client_id_string": client_id,
                            "username": username,
                            "password": password}
        )

        step_publish_message = Step(
            function=self.mqtt.publish_message,
            name="publish_message",
            success="success",
            fail="failure",
            function_params={"payload": payload,
                            "topic": topic,
                            "qos": 1},
            retry=3,
            interval=1
        )

        # Add cache if it is not already existed
        function_name = "thingspeak.publish_message"

        sm = StateManager(first_step=step_check_mqtt_connected, function_name=function_name)

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

    def subscribe_topics(self, host=None, port=None, topics=None,
                        client_id=None, username=None, password=None):
        """
        Function for subscribing to topics of ThingSpeak.

        Parameters
        ----------
        topics : list
            List of topics.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if host is None:
            host = get_parameter(["thingspeak", "mqtts", "host"], "mqtt3.thingspeak.com")

        if port is None:
            port = get_parameter(["thingspeak", "mqtts", "port"], 1883)

        if client_id is None:
            client_id = get_parameter(["thingspeak", "mqtts", "client_id"])

        if username is None:
            username = get_parameter(["thingspeak", "mqtts", "username"])

        if password is None:
            password = get_parameter(["thingspeak", "mqtts", "password"])

        if topics is None:
            topics = get_parameter(["thingspeak", "mqtts", "sub_topics"],  \
                ("channels/" + str(self.channel_id) + "/subscribe/fields/+", 0))

        # Check if client is connected to the broker
        step_check_mqtt_connected = Step(
            function=self.mqtt.is_connected_to_broker,
            name="check_connected",
            success="subscribe_topics",
            fail="check_opened",
        )

        # Check if client connected to Google Cloud IoT
        step_check_mqtt_opened = Step(
            function=self.mqtt.has_opened_connection,
            name="check_opened",
            success="connect_mqtt_broker",
            fail="register_network",
        )

        # If client is not connected to the broker and have no open connection with
        # ThingSpeak, begin the first step of the state machine.
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
            interval=1
        )

        step_connect_mqtt_broker = Step(
            function=self.mqtt.connect_broker,
            name="connect_mqtt_broker",
            success="subscribe_topics",
            fail="failure",
            function_params={"client_id_string": client_id,
                            "username": username,
                            "password": password}
        )

        step_subscribe_topics = Step(
            function=self.mqtt.subscribe_topics,
            name="subscribe_topics",
            success="success",
            fail="failure",
            function_params={"topics": topics},
            retry=3,
            interval=1
        )

        # Add cache if it is not already existed
        function_name = "thingspeak.subscribe_topics"

        sm = StateManager(first_step=step_check_mqtt_connected, function_name=function_name)

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

    @staticmethod
    def create_message(payload_dict):
        """This function generates a payload message for publishing ThingSpeak messages.

        Parameters
        ----------
        payload_dict : dict
            A dictionary instance that has "field" keys,
            and values. It's also possible to assing a
            "status" key.

        Returns
        ----------
        payload_string : str
            Returns a string similar to URL queries to add
            as a payload to mqtt.publish_message function.
        """
        payload_string = ""

        if "status" not in payload_dict:
            payload_dict["status"] = "MQTT_PICOCELL_PUBLISH"

        for key, value in payload_dict.items():
            payload_string += f"{key}={value}&"

        return payload_string[:-1]
