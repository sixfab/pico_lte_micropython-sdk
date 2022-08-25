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
        # AWS IoT, begin the first step of the state machine.
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
            function_params={"client_id_string": client_id, \
                "username": username, "password": password}
        )

        step_publish_message = Step(
            function=self.mqtt.publish_message,
            name="publish_message",
            success="success",
            fail="failure",
            function_params={"payload": "field1=15&field2=35&status=MQTT_PICOCELL_PUBLISH", "topic": "channels/1825431/publish", "qos": 0},
            retry=3,
            interval=1
        )

        # Add cache if it is not already existed
        function_name = "thingspeak.publish_message"

        sm = StateManager(first_step=step_check_mqtt_connected, function_name=function_name)

        sm.add_step(step_check_mqtt_connected)
        sm.add_step(step_check_mqtt_opened)
        sm.add_step(step_network_reg)
        sm.add_step(step_tcpip_context)
        sm.add_step(step_pdp_deactivate)
        sm.add_step(step_pdp_activate)
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
