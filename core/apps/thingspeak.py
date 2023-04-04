"""
Module for including functions of ThingSpeak for Picocell module.
"""
import time

from core.apps.app_base import AppBase
from core.temp import config, debug
from core.utils.manager import StateManager, Step
from core.utils.enums import Status, Connection
from core.utils.helpers import get_parameter


class ThingSpeak(AppBase):
    """
    Class for including functions of ThingSpeak connection.
    """

    cache = config["cache"]
    APP_NAME = "thingspeak"

    def __publish_message_on_cellular(
        self,
        message,
        field_no=None,
        channel_id=None,
        host=None,
        port=None,
        client_id=None,
        username=None,
        password=None,
    ):
        """
        A function to send a message to ThingSpeak with MQTT using cellular connection.

        Parameters
        ----------
        message : str
            The message to be sent.
        field_no : int, optional
            The field number to send the message to.
        channel_id : int, optional
            The channel ID to send the message to.
        host : str, optional
            The host name of the MQTT broker.
        port : int, optional
            The port number of the MQTT broker.
        client_id : str, optional
            The client ID to connect to the MQTT broker.
        username : str, optional
            The username to connect to the MQTT broker.
        password : str, optional
            The password to connect to the MQTT broker.

        Returns
        -------
        dict
            A resulting dictionary which has "status" and "response" keys.
        """
        debug.debug("ThingSpeak: Publishing message on cellular.")

        # Get the parameters from the config file if they are not provided.
        if field_no is None:
            field_no = get_parameter([ThingSpeak.APP_NAME, "field_no"])
        if channel_id is None:
            channel_id = get_parameter([ThingSpeak.APP_NAME, "channel_id"])

        if host is None:
            host = get_parameter([ThingSpeak.APP_NAME, "host"], "mqtt3.thingspeak.com")
        if port is None:
            port = get_parameter([ThingSpeak.APP_NAME, "port"], 1883)
        if username is None:
            username = get_parameter([ThingSpeak.APP_NAME, "username"])
        if password is None:
            password = get_parameter([ThingSpeak.APP_NAME, "password"])
        # If the client ID is not provided, then use the username.
        if client_id is None:
            client_id = get_parameter([ThingSpeak.APP_NAME, "client_id"], username)

        # Create the topic name.
        topic = self.__get_topic_name(channel_id, field_no, method="publish")

        # Create message from dictionary if needed.
        if isinstance(message, dict):
            message = ThingSpeak.__create_message(message)

        # Create steps for the state manager.
        step_check_mqtt_connected = Step(
            name=f"{ThingSpeak.APP_NAME}_check_connected",
            function=self.cellular.mqtt.is_connected_to_broker,
            success=f"{ThingSpeak.APP_NAME}_publish_message",
            fail=f"{ThingSpeak.APP_NAME}_check_opened",
        )

        step_check_mqtt_opened = Step(
            name=f"{ThingSpeak.APP_NAME}_check_opened",
            function=self.cellular.mqtt.has_opened_connection,
            success=f"{ThingSpeak.APP_NAME}_connect_mqtt_broker",
            fail=f"{ThingSpeak.APP_NAME}_register_network",
        )

        step_network_reg = Step(
            name=f"{ThingSpeak.APP_NAME}_register_network",
            function=self.cellular.network.register_network,
            success=f"{ThingSpeak.APP_NAME}_get_pdp_ready",
            fail="failure",
        )

        step_pdp_ready = Step(
            name=f"{ThingSpeak.APP_NAME}_get_pdp_ready",
            function=self.cellular.network.get_pdp_ready,
            success=f"{ThingSpeak.APP_NAME}_open_mqtt_connection",
            fail="failure",
        )

        step_open_mqtt_connection = Step(
            name=f"{ThingSpeak.APP_NAME}_open_mqtt_connection",
            function=self.cellular.mqtt.open_connection,
            function_params={"host": host, "port": port},
            success=f"{ThingSpeak.APP_NAME}_connect_mqtt_broker",
            fail="failure",
            interval=1,
        )

        step_connect_mqtt_broker = Step(
            name=f"{ThingSpeak.APP_NAME}_connect_mqtt_broker",
            function=self.cellular.mqtt.connect_broker,
            function_params={
                "client_id_string": client_id,
                "username": username,
                "password": password,
            },
            success=f"{ThingSpeak.APP_NAME}_publish_message",
            fail="failure",
        )

        step_publish_message = Step(
            name=f"{ThingSpeak.APP_NAME}_publish_message",
            function=self.cellular.mqtt.publish_message,
            function_params={"payload": message, "topic": topic, "qos": 1},
            success="success",
            fail="failure",
            retry=3,
            interval=1,
        )

        state_manager = StateManager(
            function_name=f"{ThingSpeak.APP_NAME}_publish_message_on_cellular",
            first_step=step_check_mqtt_connected,
        )

        state_manager.add_step(step_check_mqtt_connected)
        state_manager.add_step(step_check_mqtt_opened)
        state_manager.add_step(step_network_reg)
        state_manager.add_step(step_pdp_ready)
        state_manager.add_step(step_open_mqtt_connection)
        state_manager.add_step(step_connect_mqtt_broker)
        state_manager.add_step(step_publish_message)

        while True:
            result = state_manager.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def __publish_message_on_wifi(
        self,
        message,
        field_no=None,
        channel_id=None,
        host=None,
        port=None,
        client_id=None,
        username=None,
        password=None,
    ):
        """
        A function to send a message to ThingSpeak with MQTT using WiFi connection.

        Parameters
        ----------
        message : str
            The message to be sent.
        field_no : int, optional
            The field number to send the message to.
        channel_id : int, optional
            The channel ID to send the message to.
        host : str, optional
            The host name of the MQTT broker.
        port : int, optional
            The port number of the MQTT broker.
        client_id : str, optional
            The client ID to connect to the MQTT broker.
        username : str, optional
            The username to connect to the MQTT broker.
        password : str, optional
            The password to connect to the MQTT broker.

        Returns
        -------
        dict
            A resulting dictionary which has "status" and "response" keys.
        """
        debug.debug("ThingSpeak: Publishing message on WiFi.")

        # Get the parameters from the config file if they are not provided.
        if field_no is None:
            field_no = get_parameter([ThingSpeak.APP_NAME, "field_no"])
        if channel_id is None:
            channel_id = get_parameter([ThingSpeak.APP_NAME, "channel_id"])

        if host is None:
            host = get_parameter([ThingSpeak.APP_NAME, "host"], "mqtt3.thingspeak.com")
        if port is None:
            port = get_parameter([ThingSpeak.APP_NAME, "port"], 1883)
        if username is None:
            username = get_parameter([ThingSpeak.APP_NAME, "username"])
        if password is None:
            password = get_parameter([ThingSpeak.APP_NAME, "password"])
        # If the client ID is not provided, then use the username.
        if client_id is None:
            client_id = get_parameter([ThingSpeak.APP_NAME, "client_id"], username)

        # Create the topic name.
        topic = self.__get_topic_name(channel_id, field_no, method="publish")

        # Create message from dictionary if needed.
        if isinstance(message, dict):
            message = ThingSpeak.__create_message(message)

        # Create steps for the state manager.
        step_get_wifi_ready = Step(
            name=f"{ThingSpeak.APP_NAME}_get_wifi_ready",
            function=self.wifi.get_ready,
            success=f"{ThingSpeak.APP_NAME}_check_mqtt_is_connected",
            fail="failure",
            retry=5,
            interval=3,
        )

        step_check_mqtt_is_connected = Step(
            name=f"{ThingSpeak.APP_NAME}_check_mqtt_is_connected",
            function=self.wifi.mqtt.is_connected,
            success=f"{ThingSpeak.APP_NAME}_close_and_reconnect_mqtt",
            fail=f"{ThingSpeak.APP_NAME}_connect_to_mqtt",
        )

        step_close_and_reconnect_mqtt = Step(
            name=f"{ThingSpeak.APP_NAME}_close_and_reconnect_mqtt",
            function=self.wifi.mqtt.close_connection,
            success=f"{ThingSpeak.APP_NAME}_connect_to_mqtt",
            fail="failure",
        )

        step_connect_to_mqtt = Step(
            name=f"{ThingSpeak.APP_NAME}_connect_to_mqtt",
            function=self.wifi.mqtt.open_connection,
            function_params={
                "host": host,
                "port": port,
                "client_id": client_id,
                "username": username,
                "password": password,
            },
            success=f"{ThingSpeak.APP_NAME}_publish_message",
            fail="failure",
        )

        step_publish_message = Step(
            name=f"{ThingSpeak.APP_NAME}_publish_message",
            function=self.wifi.mqtt.publish_message,
            function_params={"payload": message, "topic": topic, "qos": 1},
            success=f"{ThingSpeak.APP_NAME}_disconnect_from_mqtt",
            fail="failure",
        )

        step_disconnect_from_mqtt = Step(
            name=f"{ThingSpeak.APP_NAME}_disconnect_from_mqtt",
            function=self.wifi.mqtt.close_connection,
            success="success",
            fail="failure",
        )

        # Create the state manager.
        state_manager = StateManager(
            function_name=f"{ThingSpeak.APP_NAME}_publish_message_on_wifi",
            first_step=step_get_wifi_ready,
        )

        # Add the steps to the state manager.
        state_manager.add_step(step_get_wifi_ready)
        state_manager.add_step(step_check_mqtt_is_connected)
        state_manager.add_step(step_close_and_reconnect_mqtt)
        state_manager.add_step(step_connect_to_mqtt)
        state_manager.add_step(step_publish_message)
        state_manager.add_step(step_disconnect_from_mqtt)

        # Run the state manager.
        while True:
            result = state_manager.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def __publish_message_on_both(
        self,
        message,
        field_no=None,
        channel_id=None,
        host=None,
        port=None,
        client_id=None,
        username=None,
        password=None,
    ):
        """
        A function to send a message to ThingSpeak with MQTT.

        Parameters
        ----------
        message : str
            The message to be sent.
        field_no : int, optional
            The field number to send the message to.
        channel_id : int, optional
            The channel ID to send the message to.
        host : str, optional
            The host name of the MQTT broker.
        port : int, optional
            The port number of the MQTT broker.
        client_id : str, optional
            The client ID to connect to the MQTT broker.
        username : str, optional
            The username to connect to the MQTT broker.
        password : str, optional
            The password to connect to the MQTT broker.

        Returns
        -------
        dict
            A resulting dictionary which has "status" and "response" keys.
        """
        params = {
            "message": message,
            "field_no": field_no,
            "channel_id": channel_id,
            "host": host,
            "port": port,
            "client_id": client_id,
            "username": username,
            "password": password,
        }

        return super().__publish_message_on_both(ThingSpeak.APP_NAME, params)

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

    @staticmethod
    def __create_message(payload_dict):
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
