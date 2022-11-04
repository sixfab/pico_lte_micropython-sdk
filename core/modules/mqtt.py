"""
Module for including functions of MQTT related operations of picocell module.
"""

from core.utils.status import Status
from core.utils.helpers import get_parameter


class MQTT:
    """
    Class for including functions of MQTT related operations of picocell module.
    """
    CTRL_Z = '\x1A'

    def __init__(self, atcom):
        """
        Initialization of the class.
        """
        self.atcom = atcom

    def set_version_config(self, cid=0, version=4):
        """
        Function for setting modem MQTT version configuration

        Parameters
        ----------
        cid : int, default: 0
            Client ID (range 0:5).
        version : int, default: 4
            MQTT version.
            * 4 --> MQTT 3.1.1
            * 3 --> MQTT 3.1

        Returns
        -------
        dict
            Result that includes "status" and "response" keys.
        """
        command = f'AT+QMTCFG="version",{cid},{version}'
        return self.atcom.send_at_comm(command)

    def set_pdpcid_config(self, cid=0, pdpcid=0):
        """
        Function for setting modem MQTT PDP context identifier configuration

        Parameters
        ----------
        cid : int, default: 0
            Client ID
        pdpcid : int, default: 0
            PDP context identifier (range 0:5)

        Returns
        -------
        dict
            Result that includes "status" and "response" keys.
        """
        command = f'AT+QMTCFG="pdpcid",{cid},{pdpcid}'
        return self.atcom.send_at_comm(command)

    def set_ssl_mode_config(self, cid=0, ssl_mode=1, ssl_ctx_index=2):
        """
        Function for setting modem MQTT SSL mode configuration

        Parameters
        ----------
        cid : int, default: 0
            Context identifier (range 0:5)
        ssl_mode : int, default: 1
            SSL mode
            * 0 --> Use normal TCP connection for MQTT
            * 1 --> Use SSL TCP secure connection for MQTT
        ssl_ctx_index : int, default: 2
            SSL context index

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QMTCFG="SSL",{cid},{ssl_mode},{ssl_ctx_index}'
        return self.atcom.send_at_comm(command)

    def set_keep_alive_time_config(self, cid=0, keep_alive_time=120):
        """
        Function for setting modem MQTT keep alive time configuration

        Parameters
        ----------
        cid : int, default: 0
            Client ID (range 0:5)
        keep_alive_time : int, default: 120
            Keep alive time (unit: seconds)(range 0:3600)
                It defines the maximum interval between messages received from a client. If the
                server does not receive a message from the client within 1.5 times of the
                keep-alive time value, it disconnects the client as if the client sent a
                DISCONNECT message. If the keep-alive time is 0, this means that the server is
                not required to disconnect the client on the grounds of inactivity.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QMTCFG="keepalive",{cid},{keep_alive_time}'
        return self.atcom.send_at_comm(command)

    def set_clean_session_config(self, cid=0, clean_session=0):
        """
        Function for setting modem MQTT clean session configuration

        Parameters
        ----------
        cid : int, default: 0
            Client ID (range 0:5)
        clean_session : int, default: 0
            Clean session
            * 0 --> The server must store the subscriptions of the client after it disconnects.
            * 1 --> The server must discard any previously maintained information about the
                    client after it disconnects and treat the connection as “clean”

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QMTCFG="clean_session",{cid},{clean_session}'
        return self.atcom.send_at_comm(command)

    def set_timeout_config(self, cid=0, timeout=5, retry_count=3, timeout_notice=0):
        """
        Function for setting modem MQTT timeout configuration

        Parameters
        ----------
        cid : int, default: 0
            Client ID (range 0:5)
        timeout : int, default: 5
            Packet delivery timeout in seconds(range 1:60)
        retry_count : int, default: 3
            Retry count (range 1:10)
        timeout_notice : int, default: 0
            Timeout notice
            * 0 --> Do not report
            * 1 --> Report

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QMTCFG="timeout",{cid},{timeout},{retry_count},{timeout_notice}'
        return self.atcom.send_at_comm(command)

    def set_will_config(
        self, will_topic, will_message, cid=0, will_flag=0, will_qos=0, will_retain=0
        ):
        """
        Function for setting modem MQTT will configuration

        Parameters
        ----------
        will_topic : str
            Will topic. Maximum length: 255 bytes.
        will_message : str
            Will message. Maximum length: 255 bytes.
                The Will message defines the content of the message published on the Will topic
                if the client is unexpectedly disconnected. It can be a zero-length message.
        cid : int, default: 0
            Client ID (range 0:5)
        will_flag : int, default: 0
            Will flag
            * 0 --> Ignore the Will flag configuration
            * 1 --> Require the Will flag configuration
        will_qos : int, default: 0
            Will QoS
            * 0 --> At most once
            * 1 --> At least once
            * 2 --> Exactly once
        will_retain : int, default: 0
            Will retain. Will Retain flag is only used for PUBLISH messages.
            * 0 --> When a client sends a PUBLISH message to a server, the server will not
                retain the message after it has been delivered to the current subscribers.
            * 1 --> When a client sends a PUBLISH message to a server, the server should
                retain the message after it has been delivered to the current subscribers.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QMTCFG="will",{cid},{will_flag},{will_qos},\
{will_retain},"{will_topic}","{will_message}"'
        return self.atcom.send_at_comm(command)

    def set_message_recieve_mode_config(self, cid=0, message_recieve_mode=0):
        """
        Function for setting modem MQTT message recieve mode configuration

        Parameters
        ----------
        cid : int, default: 0
            Client ID (range 0:5)
        message_recieve_mode : int, default: 0
            MQTT message recieve mode
            * 0 --> MQTT message received from server will be contained in URC
            * 1 --> MQTT message received from server will not be contained in URC

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QMTCFG="message_recieve_mode",{cid},{message_recieve_mode}'
        return self.atcom.send_at_comm(command)

    def open_connection(self, host=None, port=None, cid=0):
        """
        Function for opening MQTT connection for client

        Parameters
        ----------
        host : str, default: None
            Server address. It could be an IP address or a domain name.
        port : int, default: None
            Port number of the server (range 0:65535)
        cid : int, default: 0
            MQTT Client ID (range 0:5)

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if host is None:
            host = get_parameter(["mqtts","host"])

        if port is None:
            port = get_parameter(["mqtts","port"], 8883) # default port is 8883

        if host and port:
            command = f'AT+QMTOPEN={cid},"{host}",{port}'
            result = self.atcom.send_at_comm(command)

            desired_response = f"+QMTOPEN: {cid},0"
            fault_responses = [
                f"+QMTOPEN: {cid},1",
                f"+QMTOPEN: {cid},2",
                f"+QMTOPEN: {cid},3",
                f"+QMTOPEN: {cid},4",
                f"+QMTOPEN: {cid},5",
                ]

            if result["status"] == Status.SUCCESS:
                result = self.atcom.get_urc_response(desired_response, fault_responses, timeout=60)
            return result
        return {"status": Status.ERROR, "response": "Missing parameters : host"}

    def has_opened_connection(self, cid=0):
        """
        Function for checking if MQTT connection is opened for client

        Parameters
        ----------
        cid : int, default: 0
            MQTT Client ID (range 0:5)

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = "AT+QMTOPEN?"
        desired = f"+QMTOPEN: {cid}"
        return self.atcom.send_at_comm(command, desired)

    def close_connection(self, cid=0):
        """
        Function for closing MQTT connection for client

        Parameters
        ----------
        cid : int, default: 0
            MQTT Client ID (range 0:5)

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QMTCLOSE={cid}'
        result =  self.atcom.send_at_comm(command)

        if result["status"] == Status.SUCCESS:
            desired_response = f"+QMTCLOSE: {cid},0"
            result = self.atcom.get_urc_response(desired_response, timeout=60)
        return result

    def connect_broker(self, client_id_string="Picocell", username=None, password=None, cid=0):
        """
        Function for connecting to MQTT broker. This function is used when a client requests a
        connection to the MQTT server. When a TCP/IP socket connection is established between
        a client and a server, a protocol level session must be created using a CONNECT flow.

        Parameters
        ----------
        client_id_string : str, default: "Picocell"
            Client ID string. Maximum length: 23 bytes.
        username : str, default: None
            Username. Maximum length: 23 bytes.
        password : str, default: None
            Password. Maximum length: 23 bytes.
        cid : int, default: 0
            MQTT Client ID (range 0:5)

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if username is None and password is None:
            username = get_parameter(["mqtts","username"])
            password = get_parameter(["mqtts","password"])

        if username and password:
            command = f'AT+QMTCONN={cid},"{client_id_string}","{username}","{password}"'
        else:
            command = f'AT+QMTCONN={cid},"{client_id_string}"'

        result = self.atcom.send_at_comm(command)

        if result["status"] == Status.SUCCESS:
            desired_response = f"+QMTCONN: {cid},0,0"
            result = self.atcom.get_urc_response(desired_response, timeout=60)
        return result

    def is_connected_to_broker(self, cid=0):
        """
        Function for checking modem MQTT connection status

        Parameters
        ----------
        cid : int, default: 0
            Client ID (range 0:5)
        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = "AT+QMTCONN?"
        desired = f"+QMTCONN: {cid},3"
        return self.atcom.send_at_comm(command, desired)

    def disconnect_broker(self, cid=0):
        """
        Function for disconnecting from MQTT broker. This function is used when a client
        requests a disconnection from the MQTT server.

        Parameters
        ----------
        cid : int, default: 0
            MQTT Client ID (range 0:5)

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QMTDISC={cid}'
        return self.atcom.send_at_comm(command)

    def subscribe_topics(self, topics=None, cid=0, message_id=1):
        """
        Function for subscribing to MQTT topic. This function is used when a client requests
        a subscription to a topic.

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
        if topics is None:
            topics = get_parameter(["mqtts","sub_topics"])

        if topics:
            prefix = f'AT+QMTSUB={cid},{message_id},'
            command = prefix + ",".join(f'"{topic}",{qos}' for topic, qos in topics)
            result = self.atcom.send_at_comm(command)

            if result["status"] == Status.SUCCESS:
                desired_response = f"+QMTSUB: {cid},{message_id},0"
                result = self.atcom.get_urc_response(desired_response, timeout=60)
            return result
        return {"response": "Missing parameter : topic", "status": Status.ERROR}

    def unsubscribe_topic(self, topic, cid=0, message_id=1):
        """
        Function for unsubscribing from MQTT topic. This function is used
        when a client requests an unsubscription from a topic.

        Parameters
        ----------
        cid : int, default: 0
            MQTT Client ID (range 0:5)
        message_id : int, default: 1
            Message ID. (range 1:65535)
        topic : str
            Topic. Maximum length: 255 bytes.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QMTUNS={cid},{message_id},"{topic}"'
        return self.atcom.send_at_comm(command)

    def publish_message(self, payload, topic=None, qos=1, retain=0, message_id=1, cid=0):
        """
        Function for publishing MQTT message. This function is used when a client requests
        a message to be published. This method uses data mode of the modem to send the message.

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
        message_id : int, default: 1
            Message ID. (range 1:65535)
        cid : int, default: 0
            MQTT Client ID (range 0:5)

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if topic is None:
            topic = get_parameter(["mqtts","pub_topic"])

        if payload and topic:
            command = f'AT+QMTPUB={cid},{message_id},{qos},{retain},"{topic}"'
            result = self.atcom.send_at_comm(command, ">", urc=True)

            if result["status"] == Status.SUCCESS:
                self.atcom.send_at_comm_once(payload, line_end=False) # Send message
                result = self.atcom.send_at_comm(self.CTRL_Z) # Send end char --> CTRL+Z
            return result
        return {"response": "Missing parameter", "status": Status.ERROR}

    def read_messages(self, cid=0):
        """
        Function for receiving MQTT messages.

        Parameters
        ----------
        cid : int, default: 0
            MQTT Client ID (range 0:5)

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        messages = []
        result = self.atcom.send_at_comm("AT+QMTRECV?","+QMTRECV:")

        if result["status"] == Status.SUCCESS:
            prefix = f"+QMTRECV: {cid},"
            messages = self.extract_messages(result["response"], prefix)

        result["messages"] = messages
        return result

    @staticmethod
    def extract_messages(whole_message, prefix):
        """
        Function for extracting meaningful messages as an array
        from the response of +QMTRECV.

        Parameters
        ----------
        whole_message : str
            The response from the "+QMTRECV" command.
        prefix : str
            The prefix string for each meaningful message.

        Returns:
            array: List of messages.
        """
        messages = []

        for message in whole_message:
            start_pos = message.find(prefix)

            if start_pos != -1:
                if "0,0,0,0,0,0" in message[start_pos:]:
                    pass
                else:
                    messages.append(message[start_pos+len(prefix):])

        return messages
