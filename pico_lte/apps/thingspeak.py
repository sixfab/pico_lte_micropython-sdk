"""
Module for including functions of ThingSpeak for PicoLTE module.
"""
import time

from pico_lte.common import config
from pico_lte.utils.manager import StateManager, Step
from pico_lte.utils.status import Status
from pico_lte.utils.helpers import get_parameter


class ThingSpeak:
    """
    Class for including functions of ThingSpeak operations for PicoLTE module.
    """

    APP_NAME = "thingspeak"

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
        self,
        payload,
        channel_id=None,
        field_no=None,
        host=None,
        port=None,
        client_id=None,
        username=None,
        password=None,
    ):
        """
        Function for publishing a message to ThingSpeak.

        Parameters
        ----------
        payload : str
            Message to be published.
        channel_id : str
            Channel ID of ThingSpeak.
        field_no : str
            The field number to be updated.
        host : str
            Host name of the broker. Default is mqtt3.thingspeak.com.
        port : int
            Port number of the broker. Default is 1883.
        client_id : str
            Client ID of the client. If not provided, then the username is used.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        # Get the parameters from the config file if they are not provided.
        if field_no is None:
            field_no = get_parameter([self.APP_NAME, "field_no"])
        if channel_id is None:
            channel_id = get_parameter([self.APP_NAME, "channel_id"])
        if username is None:
            username = get_parameter([self.APP_NAME, "username"])
        if password is None:
            password = get_parameter([self.APP_NAME, "password"])

        if host is None:
            host = get_parameter([self.APP_NAME, "host"], "mqtt3.thingspeak.com")
        if port is None:
            port = get_parameter([self.APP_NAME, "port"], 1883)
        # If the client ID is not provided, then use the username.
        if client_id is None:
            client_id = get_parameter([self.APP_NAME, "client_id"], username)

        # Create the topic name.
        topic = self.__get_topic_name(channel_id, field_no, method="publish")

        # Create message from dictionary if needed.
        if isinstance(payload, dict):
            payload = self.create_message(payload)

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
            interval=1,
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
            retry=3,
            interval=1,
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

    def subscribe_topics(
        self, host=None, port=None, topics=None, client_id=None, username=None, password=None
    ):
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
            host = get_parameter([self.APP_NAME, "mqtts", "host"], "mqtt3.thingspeak.com")

        if port is None:
            port = get_parameter([self.APP_NAME, "mqtts", "port"], 1883)

        if client_id is None:
            client_id = get_parameter([self.APP_NAME, "mqtts", "client_id"])

        if username is None:
            username = get_parameter([self.APP_NAME, "mqtts", "username"])

        if password is None:
            password = get_parameter([self.APP_NAME, "mqtts", "password"])

        if topics is None:
            topics = get_parameter(
                [self.APP_NAME, "mqtts", "sub_topics"],
                ("channels/" + str(self.channel_id) + "/subscribe/fields/+", 0),
            )

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
            interval=1,
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
            retry=3,
            interval=1,
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
            payload_dict["status"] = "MQTT_PicoLTE_PUBLISH"

        for key, value in payload_dict.items():
            payload_string += f"{key}={value}&"

        return payload_string[:-1]

    @staticmethod
    def __get_topic_name(channel_id, field_no, method="publish"):
        """
        A function to create the topic name for the ThingSpeak MQTT.

        Parameters
        ----------
        channel_id : str
            The channel ID of the ThingSpeak channel.
        field_no : str
            The field number of the ThingSpeak channel.
            If all the fields are to be used, then use "+".

        Returns
        -------
        str
            The topic name for the ThingSpeak MQTT.
        """
        if method == "publish":
            if field_no == "+":
                return f"channels/{channel_id}/publish/fields/+"
            return f"channels/{channel_id}/publish/fields/field{field_no}"
        elif method == "subscribe":
            if field_no == "+":
                return f"channels/{channel_id}/subscribe/fields/+"
            return f"channels/{channel_id}/subscribe/fields/field{field_no}"
        else:
            raise ValueError("Invalid method name.")
