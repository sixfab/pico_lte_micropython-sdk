from core.atcom import ATCom, Status
import time

class Modem:
    atcom = ATCom()

    CTRL_Z = '\x1A'

    ############################
    ### Main Modem functions ###
    ############################
    def check_modem_communication(self):
        """
        Function for checking modem communication

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        return self.atcom.send_at_comm("AT")

    def set_modem_echo_off(self):
        """
        Function for setting modem echo off

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        return self.atcom.send_at_comm("ATE0")

    def set_modem_echo_on(self):
        """
        Function for setting modem echo on
        
        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        return self.atcom.send_at_comm("ATE1")

    #################################
    ### Network Service Functions ###
    #################################
    def check_network_registeration(self):
        """
        Function for checking network registeration status
        
        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        desired_reponses = ["+CREG: 0,1", "+CREG: 0,5"]
        return self.atcom.retry_at_comm("AT+CREG?", desired_reponses, retry_count=20, interval=1)

    def get_operator_information(self):
        """
        Function for getting operator information

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = "AT+COPS?"
        return self.atcom.send_at_comm(command,"OK")
        
    ####################################
    ### Modem Extended Configuration ###
    ####################################
    def config_modem_scan_mode(self, scan_mode=0):
        """
        Function for configuring modem network scan mode

        Parameters
        ----------
        scan_mode : int
            Scan mode (default=0)
                0 --> Automatic
                1 --> GSM Only
                3 --> LTE Only

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QCFG="nwscanmode",{scan_mode}'
        return self.atcom.send_at_comm(command,"OK")
    
    def config_modem_scan_sequence(self, scan_sequence="00"):
        """
        Function for configuring modem scan sequence

        Parameters
        ----------
        scan_sequence : str
            Scan sequence (default=00)
                00 --> Automatic (eMTC → NB-IoT → GSM)
                01 --> GSM
                02 --> eMTC
                03 --> NB-IoT

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QCFG="nwscanseq",{scan_sequence}'
        return self.atcom.send_at_comm(command,"OK")

    def config_modem_iot_operation_mode(self, iotopmode=2):
        """
        Function for configuring modem IoT operation mode

        Parameters
        ----------
        iotopmode : int
            Operation mode (default=2)
                0 --> eMTC
                1 --> NB-IoT
                2 --> eMTC and NB-IoT

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QCFG="iotopmode",{iotopmode}'
        return self.atcom.send_at_comm(command,"OK")

    ################################
    ### TCP/IP functions Related ###
    ################################
    def configure_tcp_ip_context(self, context_id=1, context_type=1, apn="super", username="", password="", auth=0):
        """
        Function for configuring TCP/IP context

        Parameters
        ----------
        context_id : int
            TCP/IP context identifier (range 1:5) (default=1)
        context_type : int
            TCP/IP context type (default=1)
                1 --> IPv4
                2 --> IPv6
                3 --> IPv4v6
        apn : str
            APN (default="super")
        username : str
            Username (default="")
        password : str
            Password (default="")
        auth : int
            Authentication type (default=0)
                0 --> No authentication
                1 --> PAP
                2 --> CHAP

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QICSGP={context_id},{context_type},"{apn}","{username}","{password}",{auth}'
        return self.atcom.send_at_comm(command,"OK")

    def activate_pdp_context(self, context_id=1):
        """
        Function for activating PDP context

        Parameters
        ----------
        context_id : int
            PDP context identifier (range 1:5) (default=1)

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QIACT={context_id}'
        return self.atcom.send_at_comm(command,"OK")
    
    def deactivate_pdp_context(self, context_id=1):
        """
        Function for deactivating PDP context

        Parameters
        ----------
        context_id : int
            PDP context identifier (range 1:5) (default=1)

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QIDEACT={context_id}'
        return self.atcom.send_at_comm(command,"OK")

    ##############################
    ### File Process functions ###
    ##############################
    def delete_file_from_modem(self, file_name):
        """
        Function for deleting file from modem UFS storage

        Parameters
        ----------
        file_path : str
            Path to the file

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QFDEL="{file_name}"'
        return self.atcom.send_at_comm(command, "OK")

    def upload_file_to_modem(self, filename, file, timeout=5000):
        """
        Function for uploading file to modem

        Parameters
        ----------
        file : str
            Path to the file
        timeout : int (default=5000)
            Timeout for the command
        
        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        len_file = len(file)
        command = f'AT+QFUPL="{filename}",{len_file},{timeout}'
        result = self.atcom.send_at_comm(command,"CONNECT")
    
        if result["status"] == Status.SUCCESS:
            self.atcom.send_at_comm_once(file) # send ca cert
            return self.atcom.send_at_comm(self.CTRL_Z) # send end char -> CTRL_Z
        return result

    ##################### 
    ### SSL functions ###
    #####################
    def set_modem_ssl_ca_cert(self, ssl_context_id=2, file_path="cacert.pem"):
        """
        Function for setting modem CA certificate

        Parameters
        ----------
        ssl_context_id : int
            SSL context identifier
        
        file_path : str (default="cacert.pem")
            Path to the CA certificate file

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QSSLCFG="cacert",{ssl_context_id},"{file_path}"'
        return self.atcom.send_at_comm(command,"OK")

    def set_modem_ssl_client_cert(self, ssl_context_id=2, file_path="client.pem"):
        """
        Function for setting modem client certificate

        Parameters
        ----------
        ssl_context_id : int
            SSL context identifier
        
        file_path : str (default="client.pem")
            Path to the client certificate file

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QSSLCFG="clientcert",{ssl_context_id},"{file_path}"'
        return self.atcom.send_at_comm(command,"OK")

    def set_modem_ssl_client_key(self, ssl_context_id=2, file_path="user_key.pem"):
        """
        Function for setting modem client key

        Parameters
        ----------
        ssl_context_id : int
            SSL context identifier
        
        file_path : str (default="user_key.pem")
            Path to the client key file

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QSSLCFG="clientkey",{ssl_context_id},"{file_path}"'
        return self.atcom.send_at_comm(command,"OK")
        
    def set_modem_ssl_sec_level(self, ssl_context_id=2, sec_level=2):
        """
        Function for setting modem security level

        Parameters
        ----------
        ssl_context_id : int
            SSL context identifier
        
        sec_level : int
            SSL Security level
                0 --> No authentication
                1 --> Perform server authentication
                2 --> Perform server and client authentication if requested by the remote server

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QSSLCFG="seclevel",{ssl_context_id},{sec_level}'
        return self.atcom.send_at_comm(command,"OK")

    def set_modem_ssl_version(self, ssl_context_id=2, ssl_version=4):
        """
        Function for setting modem SSL version
        
        Parameters
        ----------
        ssl_context_id : int
            SSL context identifier(default=2)

        ssl_version : int 
            SSL version (default=4)
                0 --> SSL3.0
                1 --> TLS1.0
                2 --> TLS1.1
                3 --> TLS1.2
                4 --> All
        
        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.       
        """
        command = f'AT+QSSLCFG="sslversion",{ssl_context_id},{ssl_version}'
        return self.atcom.send_at_comm(command,"OK")

    def set_modem_ssl_cipher_suite(self,ssl_context_id=2, cipher_suite="0xFFFF"):
        """
        Function for setting modem SSL cipher suite

        Parameters
        ----------
        ssl_context_id : int
            SSL context identifier (default=2)
        
        cipher_suite : str
            SSL Cipher suite. 
                0X0035 --> TLS_RSA_WITH_AES_256_CBC_SHA
                0X002F --> TLS_RSA_WITH_AES_128_CBC_SHA
                0X0005 --> TLS_RSA_WITH_RC4_128_SHA
                0X0004 --> TLS_RSA_WITH_RC4_128_MD5
                0X000A --> TLS_RSA_WITH_3DES_EDE_CBC_SHA
                0X003D --> TLS_RSA_WITH_AES_256_CBC_SHA256
                0XC002 --> TLS_ECDH_ECDSA_WITH_RC4_128_SHA
                0XC003 --> TLS_ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA
                0XC004 --> TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA
                0XC005 --> TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA
                0XC007 --> TLS_ECDHE_ECDSA_WITH_RC4_128_SHA
                0XC008 --> TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA
                0XC009 --> TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA
                0XC00A --> TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA
                0XC011 --> TLS_ECDHE_RSA_WITH_RC4_128_SHA
                0XC012 --> TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA
                0XC013 --> TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA
                0XC014 --> TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA
                0XC00C --> TLS_ECDH_RSA_WITH_RC4_128_SHA
                0XC00D --> TLS_ECDH_RSA_WITH_3DES_EDE_CBC_SHA
                0XC00E --> TLS_ECDH_RSA_WITH_AES_128_CBC_SHA
                0XC00F --> TLS_ECDH_RSA_WITH_AES_256_CBC_SHA
                0XC023 --> TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256
                0XC024 --> TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384
                0XC025 --> TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA256
                0XC026 --> TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384
                0XC027 --> TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256
                0XC028 --> TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
                0XC029 --> TLS_ECDH_RSA_WITH_AES_128_CBC_SHA256
                0XC02A --> TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384
                0XC02B --> TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256
                0XC02F --> TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
                0XC0A8 --> TLS_PSK_WITH_AES_128_CCM_8
                0X00AE --> TLS_PSK_WITH_AES_128_CBC_SHA256
                0XC0AE --> TLS_ECDHE_ECDSA_WITH_AES_128_CCM_8
                0XFFFF --> Support all cipher suites

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QSSLCFG="ciphersuite",{ssl_context_id},{cipher_suite}'
        return self.atcom.send_at_comm(command)

    def set_modem_ssl_ignore_local_time(self, ssl_context_id=2, ignore_local_time=1):
        """
        Function for setting modem SSL ignore local time

        Parameters
        ----------
        ssl_context_id : int
            SSL context identifier (default=2)
        
        ignore_local_time : int
            Ignore local time (default=1)
                0 --> Do not ignore local time
                1 --> Ignore local time

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QSSLCFG="ignorelocaltime",{ssl_context_id},{ignore_local_time}'
        return self.atcom.send_at_comm(command,"OK")
    

    ######################
    ### MQTT Functions ###
    ######################
    def set_modem_mqtt_version_config(self, cid=0, version=4):
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
        return self.atcom.send_at_comm(command,"OK")

    def set_modem_mqtt_pdpcid_config(self, cid=0, pdpcid=0):
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
        return self.atcom.send_at_comm(command,"OK")
    
    def set_modem_mqtt_ssl_mode_config(self, cid=0, ssl_mode=1, ssl_ctx_index=2):
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
        return self.atcom.send_at_comm(command,"OK")
    
    def set_modem_mqtt_keep_alive_time_config(self, cid=0, keep_alive_time=120):
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
        return self.atcom.send_at_comm(command,"OK")

    def set_modem_mqtt_clean_session_config(self, cid=0, clean_session=0):
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
        return self.atcom.send_at_comm(command,"OK")

    def set_modem_mqtt_timeout_config(self, cid=0, timeout=5, retry_count=3, timeout_notice=0):
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
        return self.atcom.send_at_comm(command,"OK")

    def set_modem_mqtt_will_config(self, cid=0, will_flag=0, will_qos=0, will_retain=0, will_topic="", will_message=""):
        """
        Function for setting modem MQTT will configuration

        Parameters
        ----------
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
        will_topic : str
            Will topic. Maximum length: 255 bytes. (default="")
        will_message : str
            Will message. Maximum length: 255 bytes. (default="")
                The Will message defines the content of the message published on the Will topic 
                if the client is unexpectedly disconnected. It can be a zero-length message. 

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QMTCFG="will",{cid},{will_flag},{will_qos},{will_retain},"{will_topic}","{will_message}"'
        return self.atcom.send_at_comm(command,"OK")

    def set_modem_mqtt_message_recieve_mode_config(self, cid=0, message_recieve_mode=0):
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
        return self.atcom.send_at_comm(command,"OK")

    def open_mqtt_connection(self, cid=0, host="", port=8883):
        """
        Function for opening MQTT connection for client

        Parameters
        ----------
        cid : int
            MQTT Client ID (range 0:5) (default=0)
        host : str
            Server address. It could be an IP address or a domain name.
        port : int
            Port number of the server (range 0:65535)(default=8883)

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
        command = f'AT+QMTOPEN={cid},"{host}",{port}'
        result = self.atcom.send_at_comm(command,"OK")

        desired_response = f"+QMTOPEN: {cid},0"

        if result["status"] == Status.SUCCESS:
            result = self.atcom.get_response(desired_response, timeout=60)
            return result
        return result

    def close_mqtt_connection(self, cid=0):
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
        result =  self.atcom.send_at_comm(command,"OK")

        if result["status"] == Status.SUCCESS:
            desired_response = f"+QMTCLOSE: {cid},0"
            result = self.atcom.get_response(desired_response, timeout=60)
            return result
        return result
    
    def connect_mqtt_broker(self, cid=0, client_id_string="picocell", username=None, password=None):
        """
        Function for connecting to MQTT broker. This function is used when a client requests a connection to the MQTT server.
        When a TCP/IP socket connection is established between a client and a server, a protocol level session must be created 
        using a CONNECT flow.

        Parameters
        ----------
        cid : int
            MQTT Client ID (range 0:5) (default=0)
        client_id_string : str
            Client ID string. Maximum length: 23 bytes. (default="picocell")
        username : str
            Username. Maximum length: 23 bytes. (default="")
        password : str
            Password. Maximum length: 23 bytes. (default="")

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
            command = f'AT+QMTCONN={cid},"{client_id_string}"'
        else:
            command = f'AT+QMTCONN={cid},"{client_id_string}","{username}","{password}"'
        
        result = self.atcom.send_at_comm(command,"OK")

        if result["status"] == Status.SUCCESS:
            desired_response = f"+QMTCONN: {cid},0,0"
            result = self.atcom.get_response(desired_response, timeout=60)
            return result
        return result

    def disconnect_mqtt_broker(self, cid=0):
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
        return self.atcom.send_at_comm(command,"OK")

    def subscribe_mqtt_topic(self, cid=0, message_id=1, topic="", qos=0):
        """
        Function for subscribing to MQTT topic. This function is used when a client requests a subscription to a topic.

        Parameters
        ----------
        cid : int
            MQTT Client ID (range 0:5) (default=0)
        message_id : int
            Message ID. (range 1:65535)(default=1)
        topic : str
            Topic. Maximum length: 255 bytes. (default="")
        qos : int
            QoS. (default=0)
                0 --> At most once
                1 --> At least once
                2 --> Exactly once

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
                        If <result> is 0, it is a vector of granted QoS levels
                        If <result> is 1, it is the number of times the packet has been retransmitted
                        If <result> is 2, it will not be presented

        """
        command = f'AT+QMTSUB={cid},{message_id},"{topic}",{qos}'
        result = self.atcom.send_at_comm(command,"OK")

        if result["status"] == Status.SUCCESS:
            desired_response = f"+QMTSUB: {cid},{message_id},0"
            result = self.atcom.get_response(desired_response, timeout=60)
            return result
        return result

    def unsubscribe_mqtt_topic(self, cid=0, message_id=1, topic=""):
        """
        Function for unsubscribing from MQTT topic. This function is used when a client requests an unsubscription from a topic.

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
        return self.atcom.send_at_comm(command,"OK")

    def publish_mqtt_message(self, cid=0, message_id=1, qos=1, retain=0, topic="", payload=""):
        """
        Function for publishing MQTT message. This function is used when a client requests a message to be published.
        This method uses data mode of the modem to send the message.

        Parameters
        ----------
        cid : int
            MQTT Client ID (range 0:5) (default=0)
        message_id : int
            Message ID. (range 1:65535)(default=1)
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
        topic : str
            Topic. Maximum length: 255 bytes. (default="")

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
                        0 --> Packet sent successfully and ACK received from the server (message that
                            is published when <qos>=0 does not require ACK)
                        1 --> Packet retransmission
                        2 --> Failed to send a packet
                    value : int
                        If <result> is 1, it means the number of times a packet has been retransmitted.
                        If <result> is 0 or 2, it will not be presente
        """
        command = f'AT+QMTPUB={cid},{message_id},{qos},{retain},"{topic}"'
        result = self.atcom.send_at_comm(command,">")

        if result["status"] == Status.SUCCESS:
            self.atcom.send_at_comm_once(payload,"OK") # Send message
            return self.atcom.send_at_comm(self.CTRL_Z,"OK") # Send end char --> CTRL+Z
        else:
            return result
