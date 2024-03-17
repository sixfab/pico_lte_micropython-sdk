"""
Module for including functions of ThingsBoard App for PicoLTE module.
"""
import time

from pico_lte.common import config
from pico_lte.utils.manager import StateManager, Step
from pico_lte.utils.status import Status
from pico_lte.utils.helpers import get_parameter


class ThingsBoard:
    """
    Class for including functions of ThingsBoard App operations for PicoLTE module.
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
        self,
        payload,
        host=None,
        port=None,
        topic=None,
        username=None,
        password=None,
        qos=None,
    ):
        """
        Function for publishing a message to ThingsBoard.

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
            host = get_parameter(["thingsboard", "host"])
        print(host)

        if port is None:
            port = get_parameter(["thingsboard", "port"])
        print(port)
        
        if topic is None:
            topic = get_parameter(["thingsboard", "pub_topic"])
        print(topic)

        if username is None:
            username = get_parameter(["thingsboard", "username"])
        print(username)

        if password is None:
            password = get_parameter(["thingsboard", "password"])
        print(password)
        
        if qos is None:
            qos = get_parameter(["thingsboard", "qos"])
        print(qos)

        # Create message from dictionary if needed.
        if isinstance(payload, dict):
            payload = ThingsBoard.create_message(payload)

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
        # ThingsBoard, begin the first step of the state machine.
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
                "password": password
            },
        )

        step_publish_message = Step(
            function=self.mqtt.publish_message,
            name="publish_message",
            success="success",
            fail="failure",
            function_params={"payload": payload, "topic": topic, "qos": qos},
            retry=3,
            interval=1,
        )

        # Add cache if it is not already existed
        function_name = "thingsboard.publish_message"

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
            

    def read_messages(self):
        """
        Read messages from subscribed topics.
        """
        return self.mqtt.read_messages()

    @staticmethod
    def create_message(payload_dict):
        """This function generates a payload message for publishing ThingsBoard messages.

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