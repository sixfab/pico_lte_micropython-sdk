"""
Module for including functions of AWS IoT operations of picocell module.
"""

import time

from core.apps.app_base import AppBase
from core.utils.manager import StateManager, Step
from core.utils.enums import Status
from core.utils.helpers import get_parameter
from core.temp import config


class AWS(AppBase):
    """
    Class for including functions of AWS IoT operations of picocell module.
    """

    APP_NAME = "aws"
    CERTS_NEEDED = ["root_ca", "device_cert", "private_key"]

    def __init__(self, cellular, wifi, keycase):
        """It is used to initialize the AWS class."""
        self.cellular = cellular
        self.wifi = wifi
        self.keycase = keycase

    def __publish_message_on_wifi(
        self,
        message,
        host=None,
        port=None,
        topic=None,
        client_id=None,
        username=None,
        secure=None,
    ):
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
            host = get_parameter([AWS.APP_NAME, "host"])
        if port is None:
            port = get_parameter([AWS.APP_NAME, "port"], 8883)
        if topic is None:
            topic = get_parameter([AWS.APP_NAME, "pub_topic"])
        if secure is None:
            secure = get_parameter([AWS.APP_NAME, "secure_storage"], False)
        if client_id is None:
            client_id = get_parameter([AWS.APP_NAME, "client_id"], "Sixfab-PicoLTE")

        # Load the certificates.
        cert_locs = self.keycase.load_certificates(
            AWS.APP_NAME, AWS.CERTS_NEEDED, for_connection="wifi"
        )
        if cert_locs is None:
            return {"status": Status.ERROR, "response": "Certificate loading failed."}

        # Create steps for the state manager.
        step_get_wifi_ready = Step(
            name=f"{AWS.APP_NAME}_get_wifi_ready",
            function=self.wifi.get_ready,
            success=f"{AWS.APP_NAME}_check_mqtt_is_connected",
            fail="failure",
        )

        step_check_mqtt_is_connected = Step(
            name=f"{AWS.APP_NAME}_check_mqtt_is_connected",
            function=self.wifi.mqtt.is_connected,
            function_params={"host": host, "port": port},
            success=f"{AWS.APP_NAME}_publish_message",
            fail=f"{AWS.APP_NAME}_reconnect_mqtt",
        )

        step_reconnect_mqtt = Step(
            name=f"{AWS.APP_NAME}_reconnect_mqtt",
            function=self.wifi.mqtt.reconnect,
            success=f"{AWS.APP_NAME}_check_mqtt_is_connected",
            fail=f"{AWS.APP_NAME}_close_and_reconnect_mqtt",
        )

        step_close_and_reconnect_mqtt = Step(
            name=f"{AWS.APP_NAME}_close_and_reconnect_mqtt",
            function=self.wifi.mqtt.close_connection,
            success=f"{AWS.APP_NAME}_connect_to_mqtt",
            fail=f"{AWS.APP_NAME}_connect_to_mqtt",
        )

        step_connect_to_mqtt = Step(
            name=f"{AWS.APP_NAME}_connect_to_mqtt",
            function=self.wifi.mqtt.open_connection,
            function_params={
                "host": host,
                "port": port,
                "client_id": client_id,
                "ssl_device_cert": "/" + cert_locs[1],
                "ssl_private_key": "/" + cert_locs[2],
            },
            success=f"{AWS.APP_NAME}_check_mqtt_is_connected",
            fail="failure",
        )

        step_publish_message = Step(
            name=f"{AWS.APP_NAME}_publish_message",
            function=self.wifi.mqtt.publish_message,
            function_params={"payload": message, "topic": topic, "qos": 1},
            success="success",
            fail="failure",
        )

        # Create the state manager.
        state_manager = StateManager(
            function_name=f"{AWS.APP_NAME}_publish_message_on_wifi",
            first_step=step_get_wifi_ready,
        )

        # Add the steps to the state manager.
        state_manager.add_step(step_get_wifi_ready)
        state_manager.add_step(step_check_mqtt_is_connected)
        state_manager.add_step(step_reconnect_mqtt)
        state_manager.add_step(step_close_and_reconnect_mqtt)
        state_manager.add_step(step_connect_to_mqtt)
        state_manager.add_step(step_publish_message)

        # Run the state manager.
        while True:
            result = state_manager.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def __publish_message_on_cellular(
        self,
        message,
        host=None,
        port=None,
        topic=None,
        client_id=None,
        username=None,
        secure=None,
    ):
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
            host = get_parameter([AWS.APP_NAME, "host"])
        if port is None:
            port = get_parameter([AWS.APP_NAME, "port"], 8883)
        if topic is None:
            topic = get_parameter([AWS.APP_NAME, "pub_topic"])
        if secure is None:
            secure = get_parameter([AWS.APP_NAME, "secure_storage"], False)

        # Load the certificates to the cellular modem.
        cert_locs = self.keycase.load_certificates(
            AWS.APP_NAME, AWS.CERTS_NEEDED, for_connection="cellular", secure=secure
        )
        if cert_locs is None:
            return {"status": Status.ERROR, "response": "Certificate loading failed."}

        # Check if client is connected to the broker
        step_check_mqtt_connected = Step(
            name=f"{AWS.APP_NAME}_check_connected",
            function=self.cellular.mqtt.is_connected_to_broker,
            success=f"{AWS.APP_NAME}_publish_message",
            fail=f"{AWS.APP_NAME}_check_opened",
        )

        # Check if client connected to AWS IoT
        step_check_mqtt_opened = Step(
            name=f"{AWS.APP_NAME}_check_opened",
            function=self.cellular.mqtt.has_opened_connection,
            success=f"{AWS.APP_NAME}_connect_mqtt_broker",
            fail=f"{AWS.APP_NAME}_deactivate_pdp_context",
        )

        # If client is not connected to the broker and have no open connection with AWS IoT
        # Deactivate PDP and begin first step of the state machine
        step_deactivate_pdp_context = Step(
            name=f"{AWS.APP_NAME}_deactivate_pdp_context",
            function=self.cellular.network.deactivate_pdp_context,
            success=f"{AWS.APP_NAME}_register_network",
            fail="failure",
        )

        step_network_reg = Step(
            name=f"{AWS.APP_NAME}_register_network",
            function=self.cellular.network.register_network,
            success=f"{AWS.APP_NAME}_get_ready_pdp",
            fail="failure",
        )

        step_get_pdp_ready = Step(
            name=f"{AWS.APP_NAME}_get_ready_pdp",
            function=self.cellular.network.get_pdp_ready,
            success=f"{AWS.APP_NAME}_ssl_configuration",
            fail="failure",
        )

        step_ssl_configuration = Step(
            name=f"{AWS.APP_NAME}_ssl_configuration",
            function=self.cellular.ssl.configure_for_x509_certification,
            function_params={
                "root_ca": cert_locs[0],
                "device_cert": cert_locs[1],
                "private_key": cert_locs[2],
            },
            success=f"{AWS.APP_NAME}_set_mqtt_version",
            fail="failure",
            cachable=True,
        )

        step_set_mqtt_version = Step(
            name=f"{AWS.APP_NAME}_set_mqtt_version",
            function=self.cellular.mqtt.set_version_config,
            success=f"{AWS.APP_NAME}_set_mqtt_ssl_mode",
            fail="failure",
        )

        step_set_mqtt_ssl_mode = Step(
            name=f"{AWS.APP_NAME}_set_mqtt_ssl_mode",
            function=self.cellular.mqtt.set_ssl_mode_config,
            success=f"{AWS.APP_NAME}_open_mqtt_connection",
            fail="failure",
        )

        step_open_mqtt_connection = Step(
            name=f"{AWS.APP_NAME}_open_mqtt_connection",
            function=self.cellular.mqtt.open_connection,
            function_params={"host": host, "port": port},
            success=f"{AWS.APP_NAME}_connect_mqtt_broker",
            fail="failure",
        )

        step_connect_mqtt_broker = Step(
            name=f"{AWS.APP_NAME}_connect_mqtt_broker",
            function=self.cellular.mqtt.connect_broker,
            success=f"{AWS.APP_NAME}_publish_message",
            fail="failure",
        )

        step_publish_message = Step(
            name=f"{AWS.APP_NAME}_publish_message",
            function=self.cellular.mqtt.publish_message,
            function_params={"payload": message, "topic": topic},
            success="success",
            fail="failure",
            cachable=True,
        )

        state_manager = StateManager(
            function_name=f"{AWS.APP_NAME}_publish_message",
            first_step=step_check_mqtt_connected,
        )

        state_manager.add_step(step_check_mqtt_connected)
        state_manager.add_step(step_check_mqtt_opened)
        state_manager.add_step(step_deactivate_pdp_context)
        state_manager.add_step(step_network_reg)
        state_manager.add_step(step_get_pdp_ready)
        state_manager.add_step(step_ssl_configuration)
        state_manager.add_step(step_set_mqtt_version)
        state_manager.add_step(step_set_mqtt_ssl_mode)
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
