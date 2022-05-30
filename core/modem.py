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
        """
        return self.atcom.send_at_comm("AT").get("status")

    def set_modem_echo_off(self):
        """
        Function for setting modem echo off
        """
        return self.atcom.send_at_comm("ATE0").get("status")

    def set_modem_echo_on(self):
        """
        Function for setting modem echo on
        """
        return self.atcom.send_at_comm("ATE1").get("status")

    ################################
    ### Authendication functions ###
    ################################
    def delete_modem_ca_cert(self):
        """
        Function for deleting modem CA certificate
        """
        return self.atcom.send_at_comm('AT+QFDEL="cacert.pem"').get("status")

    def delete_modem_client_cert(self):
        """
        Function for deleting modem client certificate
        """
        return self.atcom.send_at_comm('AT+QFDEL="client.pem"').get("status")

    def delete_modem_client_key(self):
        """
        Function for deleting modem client key
        """
        return self.atcom.send_at_comm('AT+QFDEL="client.key"').get("status")

    def upload_modem_ca_cert(self, ca_cert, timeout=5000):
        """
        Function for uploading modem CA certificate
        """
        len_cacert = len(ca_cert)
        command = f'AT+QFUPL="cacert.pem",{len_cacert},{timeout}'
        res = self.atcom.send_at_comm(command,"CONNECT").get("status")
    
        if res == Status.SUCCESS:
            self.atcom.send_at_comm_once(ca_cert) # send ca cert
            return self.atcom.send_at_comm(self.CTRL_Z).get("status") # send end char -> CTRL_Z
        else:
            return res

    def upload_modem_client_cert(self, client_cert, timeout=5000):
        """
        Function for uploading modem client certificate
        """
        len_clientcert = len(client_cert)
        command = f'AT+QFUPL="client.pem",{len_clientcert},{timeout}'
        res = self.atcom.send_at_comm(command,"CONNECT").get("status")
    
        if res == Status.SUCCESS:
            self.atcom.send_at_comm_once(client_cert) # send client cert
            return self.atcom.send_at_comm(self.CTRL_Z).get("status") # send end char -> CTRL_Z
        else:
            return res

    def upload_modem_client_key(self, client_key, timeout=5000):
        """
        Function for uploading modem client key
        """
        len_clientkey = len(client_key)
        command = f'AT+QFUPL="client.key",{len_clientkey},{timeout}'
        res = self.atcom.send_at_comm(command,"CONNECT").get("status")
    
        if res == Status.SUCCESS:
            self.atcom.send_at_comm_once(client_key) # send client key
            return self.atcom.send_at_comm(self.CTRL_Z).get("status") # send end char -> CTRL_Z
        else:
            return res
    
    ##################### 
    ### SSL functions ###
    #####################
    def set_modem_ssl_ca_cert(self):
        """
        Function for setting modem CA certificate
        """
        return self.atcom.send_at_comm('AT+QSSLCFG="cacert",2,"cacert.pem"',"OK").get("status")

    def set_modem_ssl_client_cert(self):
        """
        Function for setting modem client certificate
        """
        return self.atcom.send_at_comm('AT+QSSLCFG="clientcert",2,"client.pem"',"OK").get("status")

    def set_modem_ssl_client_key(self):
        """
        Function for setting modem client key
        """
        return self.atcom.send_at_comm('AT+QSSLCFG="clientkey",2,"user_key.pem"',"OK").get("status")

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
        status : int
            Status of the command.
        """
        command = f'AT+QSSLCFG="seclevel",{ssl_context_id},{sec_level}'
        return self.atcom.send_at_comm(command,"OK").get("status")

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
        status : int
            Status of the command.       
        """
        command = f'AT+QSSLCFG="sslversion",{ssl_context_id},{ssl_version}'
        return self.atcom.send_at_comm(command,"OK").get("status")

    def set_modem_ssl_cipher_suite(self,ssl_context_id=2, cipher_suite=0xFFFF):
        """
        Function for setting modem SSL cipher suite

        Parameters
        ----------
        ssl_context_id : int
            SSL context identifier (default=2)
        
        cipher_suite : int
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
        status : int
            Status of the command.
        """
        command = f'AT+QSSLCFG="ciphersuite",{ssl_context_id},{cipher_suite}'
        return self.atcom.send_at_comm(command).get("status")

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
        status : int
            Status of the command.
        """
        command = f'AT+QSSLCFG="ignorelocaltime",{ssl_context_id},{ignore_local_time}'
        return self.atcom.send_at_comm(command,"OK").get("status")
    


    ######################
    ### MQTT Functions ###
    ######################
    def set_modem_mqtt_version_config(self, version=4):
        """
        Function for setting modem MQTT version configuration

        Parameters
        ----------
        version : int
            MQTT version (default=4)
                4 --> MQTT 3.1.1
                3 --> MQTT 3.1

        Returns
        -------
        status : int
            Status of the command.
        """
        command = f'AT+QMTCFG="version",{version}'
        return self.atcom.send_at_comm(command,"OK").get("status")

    def set_modem_mqtt_pdpcid_config(self, pdpcid=0):
        """
        Function for setting modem MQTT PDP context identifier configuration

        Parameters
        ----------
        pdpcid : int
            PDP context identifier (range 0:5) (default=0)

        Returns
        -------
        status : int
            Status of the command.
        """
        command = f'AT+QMTCFG="pdpcid",{pdpcid}'
        return self.atcom.send_at_comm(command,"OK").get("status")
    
    def set_modem_mqtt_ssl_mode_config(self, ssl_mode=0):
        """
        Function for setting modem MQTT SSL mode configuration

        Parameters
        ----------
        ssl_mode : int
            SSL mode (default=0)
                0 --> Use normal TCP connection for MQTT
                1 --> Use SSL TCP secure connection for MQTT
        
        Returns
        -------
        status : int
            Status of the command.
        """
        command = f'AT+QMTCFG="SSL_enable",{ssl_mode}'
        return self.atcom.send_at_comm(command,"OK").get("status")
    
    def set_modem_mqtt_keep_alive_time_config(self, keep_alive_time=120):
        """
        Function for setting modem MQTT keep alive time configuration

        Parameters
        ----------
        keep_alive_time : int 
            Keep alive time (unit: seconds)(range 0:3600)(default=120)
                It defines the maximum interval between messages received from a client. If the
                server does not receive a message from the client within 1.5 times of the
                keep-alive time value, it disconnects the client as if the client sent a
                DISCONNECT message. If the keep-alive time is 0, this means that the server is
                not required to disconnect the client on the grounds of inactivity.

        Returns
        -------
        status : int
            Status of the command.
        """
        command = f'AT+QMTCFG="keepalive",{keep_alive_time}'
        return self.atcom.send_at_comm(command,"OK").get("status")

    def set_modem_mqtt_clean_session_config(self, clean_session=0):
        """
        Function for setting modem MQTT clean session configuration

        Parameters
        ----------
        clean_session : int
            Clean session (default=1)
                0 --> The server must store the subscriptions of the client after it disconnects.
                1 --> The server must discard any previously maintained information about the
                    client after it disconnects and treat the connection as “clean”

        Returns
        -------
        status : int
            Status of the command.
        """
        command = f'AT+QMTCFG="clean_session",{clean_session}'
        return self.atcom.send_at_comm(command,"OK").get("status")

    def set_modem_mqtt_timeout_config(self, timeout=5):
        """
        Function for setting modem MQTT timeout configuration

        Parameters
        ----------
        timeout : int
            Packet delivery timeout (unit: seconds)(range 1:60)(default=5)
                
        Returns
        -------
        status : int
            Status of the command.
        """
        command = f'AT+QMTCFG="timeout",{timeout}'
        return self.atcom.send_at_comm(command,"OK").get("status")

    def set_modem_mqtt_will_config(self, will_flag=0, will_qos=0, will_retain=0, will_topic="", will_message=""):
        """
        Function for setting modem MQTT will configuration

        Parameters
        ----------
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
        status : int
            Status of the command.
        """
        command = f'AT+QMTCFG="will",{will_flag},{will_qos},{will_retain},"{will_topic}","{will_message}"'
        return self.atcom.send_at_comm(command,"OK").get("status")

    def set_modem_mqtt_message_recieve_mode_config(self, message_recieve_mode=0):
        """
        Function for setting modem MQTT message recieve mode configuration

        Parameters
        ----------
        message_recieve_mode : int
            MQTT message recieve mode (default=0)
                0 --> MQTT message received from server will be contained in URC
                1 --> MQTT message received from server will not be contained in URC

        Returns
        -------
        status : int
            Status of the command.
        """
        command = f'AT+QMTCFG="message_recieve_mode",{message_recieve_mode}'
        return self.atcom.send_at_comm(command,"OK").get("status")

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
            modem_response : str
                Response of the modem.
                0 --> Success
                -1 --> Failed to open MQTT connection
        """
        command = f'AT+QMTOPEN={cid},"{host}",{port}'
        return self.atcom.send_at_comm(command,"OK")

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
        return self.atcom.send_at_comm(command,"OK")
    
    def connect_mqtt_broker(self, cid=0, client_id_string="picocell", username="", password=""):
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
        command = f'AT+QMTCONN={cid},"{client_id_string}","{username}","{password}"'
        return self.atcom.send_at_comm(command,"OK")

    