"""
Module for including functions of AWS IoT operations of picocell module.
"""

import time

from core.temp import config
from core.utils.manager import StateManager, Step
from core.utils.status import Status

class AWS:
    """
    Class for including functions of AWS IoT operations of picocell module.
    """
    cache = config["cache"]

    def __init__(self, base, auth, network, ssl, mqtt, http):
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

    def publish_message(self, payload, host=None, port=None, topic=None):
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
        (status, modem_response) : tuple
            status : int
                Status of the command.
            modem_response : str
                Response of the modem.
        """

        step_load_certificates = Step(
            function=self.auth.load_certificates,
            name="load_certificates",
            success="register_network",
            fail="failure",
            cachable=True,
        )
        step_network_reg = Step(
            function=self.network.register_network,
            name="register_network",
            success="pdp_deactivate",
            fail="failure",
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
            success="ssl_configuration",
            fail="failure",
        )

        step_ssl_configuration = Step(
            function=self.ssl.configure_for_x509_certification,
            name="ssl_configuration",
            success="set_mqtt_version",
            fail="failure",
            cachable=True
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
            function_params={"host":host, "port":port},
            cachable=True,
        )

        step_connect_mqtt_broker = Step(
            function=self.mqtt.connect_broker,
            name="connect_mqtt_broker",
            success="publish_message",
            fail="failure",
            cachable=True,
        )

        step_publish_message = Step(
            function=self.mqtt.publish_message,
            name="publish_message",
            success="success",
            fail="failure",
            function_params={"payload":payload, "topic":topic},
            cachable=True,
        )

        # Add cache if it is not already existed
        function_name = "aws.publish_message"

        sm = StateManager(first_step=step_load_certificates, function_name=function_name)

        sm.add_step(step_load_certificates)
        sm.add_step(step_network_reg)
        sm.add_step(step_pdp_deactivate)
        sm.add_step(step_pdp_activate)
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

    def post_message(self, payload, url=None):
        """
        Function for publishing a message to AWS IoT by using HTTPS.

        Parameters
        ----------
        payload : str
            Payload of the message.
        url : str
            URL of the AWS device shadow

        Returns
        -------
        (status, modem_response) : tuple
            status : int
                Status of the command.
            modem_response : str
                Response of the modem.
        """
        step_load_certificates = Step(
            function=self.auth.load_certificates,
            name="load_certificates",
            success="register_network",
            fail="failure",
            cachable=True,
        )
        step_network_reg = Step(
            function=self.network.register_network,
            name="register_network",
            success="pdp_deactivate",
            fail="failure",
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
            success="ssl_configuration",
            fail="failure",
            cachable=True,
        )

        step_ssl_configuration = Step(
            function=self.ssl.configure_for_x509_certification,
            name="ssl_configuration",
            success="http_ssl_configuration",
            fail="failure",
            cachable=True,
        )

        step_http_ssl_configuration = Step(
            function=self.http.set_ssl_context_id,
            name="http_ssl_configuration",
            success="set_server_url",
            fail="failure",
            function_params={"id": 2},
            cachable=True,
        )

        step_set_server_url = Step(
            function=self.http.set_server_url,
            name="set_server_url",
            success="post_request",
            fail="failure",
            function_params={"url": url},
            cachable=True,
        )

        step_post_request = Step(
            function=self.http.post,
            name="post_request",
            success="read_response",
            fail="failure",
            function_params={"data": payload},
            cachable=True,
        )

        step_read_response = Step(
            function=self.http.read_response,
            name="read_response",
            success="success",
            fail="failure",
        )

        # Add cache if it is not already existed
        function_name = "aws.post_message"

        sm = StateManager(first_step=step_network_reg, function_name=function_name)

        sm.add_step(step_load_certificates)
        sm.add_step(step_network_reg)
        sm.add_step(step_pdp_deactivate)
        sm.add_step(step_pdp_activate)
        sm.add_step(step_ssl_configuration)
        sm.add_step(step_http_ssl_configuration)
        sm.add_step(step_set_server_url)
        sm.add_step(step_post_request)
        sm.add_step(step_read_response)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])
