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
        cid : int
            Client ID (default=0)
        version : int
            MQTT version (default=4)
                4 --> MQTT 3.1.1
                3 --> MQTT 3.1

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QMTCFG="version",{cid},{version}'
        return self.atcom.send_at_comm(command)

    def set_pdpcid_config(self, cid=0, pdpcid=0):
        """
        Function for setting modem MQTT PDP context identifier configuration

        Parameters
        ----------
        cid : int
            Client ID (default=0)
        pdpcid : int
            PDP context identifier (range 0:5) (default=0)

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QMTCFG="pdpcid",{cid},{pdpcid}'
        return self.atcom.send_at_comm(command)

    def set_ssl_mode_config(self, cid=0, ssl_mode=1, ssl_ctx_index=2):
        """
        Function for setting modem MQTT SSL mode configuration

        Parameters
        ----------
        cid : int
            Context identifier (range 0:5) (default=0)
        ssl_mode : int
            SSL mode (default=0)
                0 --> Use normal TCP connection for MQTT
                1 --> Use SSL TCP secure connection for MQTT
        ssl_ctx_index : int
            SSL context index (default=2)

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QMTCFG="SSL",{cid},{ssl_mode},{ssl_ctx_index}'
        return self.atcom.send_at_comm(command)

    def set_keep_alive_time_config(self, cid=0, keep_alive_time=120):
        """
        Function for setting modem MQTT keep alive time configuration

        Parameters
        ----------
        cid : int
            Client ID (range 0:5) (default=0)
        keep_alive_time : int
            Keep alive time (unit: seconds)(range 0:3600)(default=120)
                It defines the maximum interval between messages received from a client. If the
                server does not receive a message from the client within 1.5 times of the
                keep-alive time value, it disconnects the client as if the client sent a
                DISCONNECT message. If the keep-alive time is 0, this means that the server is
                not required to disconnect the client on the grounds of inactivity.

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QMTCFG="keepalive",{cid},{keep_alive_time}'
        return self.atcom.send_at_comm(command)

    def set_clean_session_config(self, cid=0, clean_session=0):
        """
        Function for setting modem MQTT clean session configuration

        Parameters
        ----------
        cid : int
            Client ID (range 0:5) (default=0)
        clean_session : int
            Clean session (default=1)
                0 --> The server must store the subscriptions of the client after it disconnects.
                1 --> The server must discard any previously maintained information about the
                    client after it disconnects and treat the connection as “clean”

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QMTCFG="clean_session",{cid},{clean_session}'
        return self.atcom.send_at_comm(command)

    def set_timeout_config(self, cid=0, timeout=5, retry_count=3, timeout_notice=0):
        """
        Function for setting modem MQTT timeout configuration

        Parameters
        ----------
        cid : int
            Client ID (range 0:5) (default=0)
        timeout : int
            Packet delivery timeout (unit: seconds)(range 1:60)(default=5)
        retry_count : int
            Retry count (range 1:10)(default=3)
        timeout_notice : int
            Timeout notice (default=0)
                0 --> Do not report
                1 --> Report

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
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
        cid : int
            Client ID (range 0:5) (default=0)
        will_flag : int
            Will flag (default=0)
                0 --> Ignore the Will flag configuration
                1 --> Require the Will flag configuration
        will_qos : int
            Will QoS (default=0)
                0 --> At most once
                1 --> At least once
                2 --> Exactly once
        will_retain : int
            Will retain. Will Retain flag is only used for PUBLISH messages.(default=0)
                0 --> When a client sends a PUBLISH message to a server, the server will not
                    retain the message after it has been delivered to the current subscribers.
                1 --> When a client sends a PUBLISH message to a server, the server should
                    retain the message after it has been delivered to the current subscribers.

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QMTCFG="will",{cid},{will_flag},{will_qos},\
                        {will_retain},"{will_topic}","{will_message}"'
        return self.atcom.send_at_comm(command)

    def set_message_recieve_mode_config(self, cid=0, message_recieve_mode=0):
        """
        Function for setting modem MQTT message recieve mode configuration

        Parameters
        ----------
        cid : int
            Client ID (range 0:5) (default=0)
        message_recieve_mode : int
            MQTT message recieve mode (default=0)
                0 --> MQTT message received from server will be contained in URC
                1 --> MQTT message received from server will not be contained in URC

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QMTCFG="message_recieve_mode",{cid},{message_recieve_mode}'
        return self.atcom.send_at_comm(command)

    def open_connection(self, host=None, port=None, cid=0):
        """
        Function for opening MQTT connection for client

        Parameters
        ----------
        host : str
            Server address. It could be an IP address or a domain name.(default=None)
        port : int
            Port number of the server (range 0:65535)(default=None)
        cid : int
            MQTT Client ID (range 0:5) (default=0)

        Returns
        -------
        (status, modem_response) : tuple
            status : int
                Status of the command.
            modem_response : "client_idx, result" str
                Response of the modem.
                    client_idx : int
                        MQTT client index
                    result : int
                        -1 --> Failed to open a network
                        0 --> Network opened successfully
                        1 --> Wrong parameter
                        2 --> MQTT client identifier is occupied
                        3 --> Failed to activate PDP
                        4 --> Failed to parse domain name
                        5 --> Network connection error
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
        return {"status": Status.ERROR, "response": "Missing parameters"}

    def has_opened_connection(self, cid=0):
        """
        Function for checking if MQTT connection is opened for client

        Parameters
        ----------
        cid : int
            MQTT Client ID (range 0:5) (default=0)

        Returns
        -------
        (status, modem_response) : tuple
            status : int
                Status of the command.
            modem_response : "client_idx, result" str
                Response of the modem.
        """
        command = "AT+QMTOPEN?"
        desired = f"+QMTOPEN: {cid}"
        return self.atcom.send_at_comm(command, desired)

    def close_connection(self, cid=0):
        """
        Function for closing MQTT connection for client

        Parameters
        ----------
        cid : int
            MQTT Client ID (range 0:5) (default=0)

        Returns
        -------
        (status, modem_response) : tuple
            status : int
                Status of the command.
            modem_response : str
                Response of the modem.
                0 --> Network closed successfully
                -1 --> Failed to close the network

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
        client_id_string : str
            Client ID string. Maximum length: 23 bytes. (default="Picocell")
        username : str
            Username. Maximum length: 23 bytes. (default=None)
        password : str
            Password. Maximum length: 23 bytes. (default=None)
        cid : int
            MQTT Client ID (range 0:5) (default=0)

        Returns
        -------
        (status, modem_response) : tuple
            status : int
                Status of the command.
            modem_response : "client_idx, result, ret_code" str
                Response of the modem.
                    client_idx : int
                        Client ID (range 0:5)
                    result : int
                        Command execution result.
                            0 --> Packet sent successfully and ACK received from the server
                            1 --> Packet retransmission
                            2 --> Failed to send the packet
                    ret_code : int
                        Connection status return code
                            0 --> Connection Accepted
                            1 --> Connection Refused: Unacceptable Protocol Version
                            2 --> Connection Refused: Identifier Rejected
                            3 --> Connection Refused: Server Unavailable
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
        cid : int
            Client ID (range 0:5) (default=0)
        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
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
        cid : int
            MQTT Client ID (range 0:5) (default=0)

        Returns
        -------
        (status, modem_response) : tuple
            status : int
                Status of the command.
            modem_response : "client_idx, result" str
                Response of the modem.
                    client_idx : int
                        Client ID (range 0:5)
                    result : int
                        0 --> Disconnection successful
                        -1 --> Failed to disconnect from the MQTT server
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
            topic : str
                Maximum length: 255 bytes. (default=None)
            qos : int
                QoS. (default=0)
                    0 --> At most once
                    1 --> At least once
                    2 --> Exactly once
        cid : int
            MQTT Client ID (range 0:5) (default=0)
        message_id : int
            Message ID. (range 1:65535)(default=1)

        Returns
        -------
        (status, modem_response) : tuple
            status : int
                Status of the command.
            modem_response : "client_idx, message_id, result, value" str
                Response of the modem.
                    client_idx : int
                        Client ID (range 0:5)
                    message_id : int
                        Message ID.
                    result : int
                        Command execution result.
                        0 --> Packet sent successfully and ACK received from the server
                        1 --> Packet retransmission
                        2 --> Failed to send a packet
                    value : int
                        If <result> is 0, a vector of granted QoS levels
                        If <result> is 1, the number of times the packet has been retransmitted
                        If <result> is 2, it will not be presented

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
        cid : int
            MQTT Client ID (range 0:5) (default=0)
        message_id : int
            Message ID. (range 1:65535)(default=1)
        topic : str
            Topic. Maximum length: 255 bytes. (default="")

        Returns
        -------
        (status, modem_response) : tuple
            status : int
                Status of the command.
            modem_response : "client_idx, message_id, result" str
                Response of the modem.
                    client_idx : int
                        Client ID (range 0:5)
                    message_id : int
                        Message ID.
                    result : int
                        Command execution result.
                        0 --> Packet sent successfully and ACK received from the server
                        1 --> Packet retransmission
                        2 --> Failed to send a packet
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
        qos : int
            QoS. (default=0)
                0 --> At most once
                1 --> At least once
                2 --> Exactly once
        retain : int
            Retain. (default=0)
            Determines whether the server will retain the message after it has been delivered
            to the current subscribers.
                0 --> The server will not retain the message after it has been
                    delivered to the current subscriber
                1 --> The server will retain the message after it has been delivered
                    to the current subscribers
        message_id : int
            Message ID. (range 1:65535)(default=1)
        cid : int
            MQTT Client ID (range 0:5) (default=0)

        Returns
        -------
        (status, modem_response) : tuple
            status : int
                Status of the command.
            modem_response : "client_idx, message_id, result, value" str
                Response of the modem.
                    client_idx : int
                        Client ID (range 0:5)
                    message_id : int
                        Message ID.
                    result : int
                        Command execution result.
                        0 --> Packet sent successfully and ACK received from the server
                            (message that is published when <qos>=0 does not require ACK)
                        1 --> Packet retransmission
                        2 --> Failed to send a packet
                    value : int
                        If <result> is 1, number of times a packet has been retransmitted.
                        If <result> is 0 or 2, it will not be presented
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
        cid : int
            MQTT Client ID (range 0:5) (default=0)

        Returns
        -------
        (status, modem_response, messages) : tuple
            status : int
                Status of the command.
            modem_response : str
                Response of the modem.
            messages : list ["client_idx,topic,payload"]
                List of messages.
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
        """_Function for extracting meaningful messages as an array
        from the response of +QMTRECV.

        Args:
            whole_message (str): The response from the "+QMTRECV" command.
            prefix (str): The prefix string for each meaningful message.
            remove_nones (bool, optional): Delete None messages. Defaults to True.

        Returns:
            array: Array of messages arrays.
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
