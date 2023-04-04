"""
Module for including functions of MQTT related operations of WiFi module.
"""
from umqtt.robust import MQTTClient
from core.utils.enums import Status
from core.utils.helpers import get_parameter
from core.temp import debug


class MQTT:
    """
    Class for including functions of MQTT related operations of WiFi module.
    """

    def __init__(self):
        self.mqtt_client = None

        # MQTT connection details
        self.host = ""
        self.port = 8883
        self.username = ""
        self.password = ""
        self.client_id = ""
        self.keepalive = 60
        self.clean_session = True
        self.subscribed_topics = []

        # Interal variables
        self._mqtt_buffer = []

    def set_will_config(self, will_topic, will_message, will_qos=0, will_retain=0):
        """
        Set will configuration for MQTT client for WiFi.

        Parameters
        ----------
        will_topic : str
            Will topic.
        will_message : str
            Will message.
        will_qos : int, default: 0
            Will QoS.
        will_retain : int, default: 0
            Will retain.

        Returns
        -------
        dict
            Result that includes "status" and "message" keys
        """
        if self.mqtt_client is None:
            return {
                "status": Status.ERROR,
                "message": "MQTT client not initialized yet.",
            }

        self.mqtt_client.set_last_will(will_topic, will_message, will_retain, will_qos)
        return {
            "status": Status.SUCCESS,
            "message": "Will configuration set successfully.",
        }

    def open_connection(
        self,
        host=None,
        port=None,
        client_id=None,
        username=None,
        password=None,
        ssl=False,
        ssl_params=None,
    ):
        """
        Open connection to MQTT server with WiFi.

        Parameters
        ----------
        host : str
            Host name or IP address of the MQTT server.
        port : int
            Port number of the MQTT server.
        client_id : str, default: None
            Client ID. If not provided, it will be generated automatically.
        username : str, default: None
            Username for authentication.
        password : str, default: None
            Password for authentication.
        ssl : bool, default: False
            Enable SSL.
        ssl_params : dict, default: None
            SSL parameters.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        # Check if MQTT client is already initialized.
        if self.mqtt_client is not None:
            return {
                "status": Status.ERROR,
                "response": "MQTT client already initialized.",
            }

        # Get MQTT connection parameters.
        if host is None:
            host = get_parameter(["mqtts", "host"])
        if port is None:
            port = get_parameter(["mqtts", "port"], 8883)  # default port is 8883
        if username is None and password is None:
            username = get_parameter(["mqtts", "username"])
            password = get_parameter(["mqtts", "password"])
        if client_id is None:
            client_id = get_parameter(["mqtts", "client_id"], "Picocell")

        # Initialize MQTT client.
        self.mqtt_client = MQTTClient(
            client_id=client_id,
            server=host,
            port=port,
            user=username,
            password=password,
            ssl=ssl,
            ssl_params=ssl_params,
        )

        # Connect to MQTT server.
        result = self.mqtt_client.connect()
        if result != 0:
            self.mqtt_client = None
            return {
                "status": Status.ERROR,
                "response": f"MQTT connection failed. ({result})",
            }
        debug.debug("MQTT connection opened successfully.")

        # Save the connection parameters into internal variables.
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client_id = client_id
        return {
            "status": Status.SUCCESS,
            "response": "MQTT connection opened successfully.",
        }

    def close_connection(self):
        """
        Close connection to MQTT server with WiFi.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if self.mqtt_client is None:
            return {
                "status": Status.ERROR,
                "response": "MQTT client not initialized yet.",
            }

        self.mqtt_client.disconnect()
        self.mqtt_client = None
        debug.debug("MQTT connection closed successfully.")
        return {
            "status": Status.SUCCESS,
            "response": "MQTT connection closed successfully.",
        }

    def publish_message(self, payload, topic=None, qos=1, retain=0):
        """Publish messages into MQTT topics given with WiFi.

        Parameters
        ----------
        payload : str
            Payload.
        topic : str
            Topic. Maximum length: 255 bytes.
        qos : int, default: 1
            QoS.
            * 0 --> At most once
            * 1 --> At least once
            * 2 --> Exactly once
        retain : int, default: 0
            Retain.
            Determines whether the server will retain the message after it has been delivered
            to the current subscribers.
            * 0 --> The server will not retain the message after it has been
                delivered to the current subscriber
            * 1 --> The server will retain the message after it has been delivered
                to the current subscribers

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        # Check if MQTT client is initialized.
        if self.mqtt_client is None:
            return {
                "status": Status.ERROR,
                "response": "MQTT client not initialized yet.",
            }

        # Get MQTT topic.
        if topic is None:
            topic = get_parameter(["mqtts", "topic"])

        # Publish message.
        self.mqtt_client.publish(topic, payload, qos, retain)
        debug.debug(f"Message ({payload}) published to topic '{topic}'.")
        return {
            "status": Status.SUCCESS,
            "response": "Message published successfully.",
        }

    def subscribe_topics(self, topics=None, qos=1):
        """Function for subscribing MQTT topic with WiFi.

        Parameters
        ----------
        topics : list of tupple [(topic1, qos1),(topic2, qos2),...]
            topic : str, default: None
                Maximum length: 255 bytes.
            qos : int, default: 0
                QoS.
                * 0 --> At most once
                * 1 --> At least once
                * 2 --> Exactly once
        cid : int, default: 0
            MQTT Client ID (range 0:5)
        message_id : int, default: 1
            Message ID. (range 1:65535)

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        # Check if MQTT client is initialized.
        if self.mqtt_client is None:
            return {
                "status": Status.ERROR,
                "response": "MQTT client not initialized yet.",
            }

        # Get MQTT topics.
        if topics is None:
            topics = get_parameter(["mqtts", "sub_topics"])

        # Set callback function for MQTT message recieve.
        self.mqtt_client.set_callback(self.__calback_on_message_recieve)
        debug.debug("Callback function for MQTT message recieve is set.")

        # Subscribe to topics and add them to subscribed_topics list.
        try:
            for topic, qos in topics:
                self.mqtt_client.subscribe(topic, qos)
                self.subscribed_topics.append(topic)
                debug.debug(f"Subscribed to topic '{topic}'.")
        except OSError as error:
            return {
                "status": Status.ERROR,
                "response": f"Error while subscribing topic(s). ({error})",
            }

        return {
            "status": Status.SUCCESS,
            "response": "Topic subscribed successfully.",
        }

    def read_messages(self):
        """
        Read MQTT messages from buffer for WiFi.

        Returns
        -------
        dict
            Result that includes "status", "response" and "messages" keys
        """
        # Check if MQTT client is initialized.
        if self.mqtt_client is None:
            return {
                "status": Status.ERROR,
                "response": "MQTT client not initialized yet.",
            }

        # Receive messages in non-blocking way.
        self.mqtt_client.check_msg()

        # Copy messages from the buffer and clear the old buffer.
        messages = self._mqtt_buffer.copy()
        self._mqtt_buffer.clear()
        return {
            "status": Status.SUCCESS,
            "response": "Messages read successfully.",
            "messages": messages,
        }

    def is_connected(self, host=None, port=None):
        """
        Check if MQTT client is connected with WiFi.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        # Check if MQTT client is initialized.
        if self.mqtt_client is None:
            return {
                "status": Status.ERROR,
                "response": "MQTT client not initialized yet.",
            }

        # Get MQTT host and port.
        if host is None:
            host = get_parameter(["mqtts", "host"])
        if port is None:
            port = get_parameter(["mqtts", "port"])

        # Check if MQTT client is connected.
        if host != self.host or port != self.port:
            return {
                "status": Status.ERROR,
                "response": f"MQTT client is connected to {self.host}:{self.port}.",
            }

        # If already connected to given host and port, debug it.
        debug.debug(
            f"MQTT client is connected to {self.host}:{self.port}."
        )

        # Ping MQTT server to check if connected.
        try:
            self.mqtt_client.ping()
            debug.debug("MQTT client is pinged, socket is still open.")
        except OSError:
            return {
                "status": Status.ERROR,
                "response": "MQTT client is not connected.",
            }

        # Return success since MQTT client is connected and socket is open.
        return {
            "status": Status.SUCCESS,
            "response": "MQTT client is connected.",
        }

    def __calback_on_message_recieve(self, topic, message):
        """
        Add MQTT message to buffer.

        Parameters
        ----------
        topic : str
            Topic that where the message recieved.
        message : str
            Message that is recieved from MQTT.

        Returns
        -------
        None
        """
        self._mqtt_buffer.append({"topic": topic, "message": message})
        debug.debug(
            f"Message ({message}) recieved from topic '{topic}' added to the buffer."
        )
