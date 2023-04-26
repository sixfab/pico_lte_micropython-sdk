"""
Module for including functions of ssl operations of PicoLTE module.
"""

import time

from pico_lte.utils.manager import StateManager, Step
from pico_lte.common import Status


class SSL:
    """
    Class for including functions of ssl operations of PicoLTE module.
    """

    def __init__(self, atcom, auth):
        """
        Initialization of the class.
        """
        self.atcom = atcom
        self.auth = auth

    def set_ca_cert(self, ssl_context_id=2, file_path=None):
        """
        Function for setting modem CA certificate

        Parameters
        ----------
        ssl_context_id : int
            SSL context identifier

        file_path : str
            Path to the CA certificate file

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if file_path is None:
            file_path = "/security/" + self.auth.ROOT_CA_CERT_FILE
        command = f'AT+QSSLCFG="cacert",{ssl_context_id},"{file_path}"'
        return self.atcom.send_at_comm(command)

    def set_client_cert(self, ssl_context_id=2, file_path=None):
        """
        Function for setting modem client certificate

        Parameters
        ----------
        ssl_context_id : int
            SSL context identifier

        file_path : str
            Path to the client certificate file

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if file_path is None:
            file_path = "/security/" + self.auth.DEVICE_CERT_FILE
        command = f'AT+QSSLCFG="clientcert",{ssl_context_id},"{file_path}"'
        return self.atcom.send_at_comm(command)

    def set_client_key(self, ssl_context_id=2, file_path=None):
        """
        Function for setting modem client key

        Parameters
        ----------
        ssl_context_id : int
            SSL context identifier

        file_path : str
            Path to the client key file

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if file_path is None:
            file_path = "/security/" + self.auth.PRIVATE_FILE
        command = f'AT+QSSLCFG="clientkey",{ssl_context_id},"{file_path}"'
        return self.atcom.send_at_comm(command)

    def set_sec_level(self, ssl_context_id=2, sec_level=2):
        """
        Function for setting modem security level

        Parameters
        ----------
        ssl_context_id : int, default: 2
            SSL context identifier

        sec_level : int
            SSL Security level
            * 0 --> No authentication
            * 1 --> Perform server authentication
            * 2 --> Perform server and client authentication if requested by the remote server

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QSSLCFG="seclevel",{ssl_context_id},{sec_level}'
        return self.atcom.send_at_comm(command)

    def set_version(self, ssl_context_id=2, ssl_version=4):
        """
        Function for setting modem SSL version

        Parameters
        ----------
        ssl_context_id : int, default: 2
            SSL context identifier

        ssl_version : int
            SSL version (default=4)
            * 0 --> SSL3.0
            * 1 --> TLS1.0
            * 2 --> TLS1.1
            * 3 --> TLS1.2
            * 4 --> All

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QSSLCFG="sslversion",{ssl_context_id},{ssl_version}'
        return self.atcom.send_at_comm(command)

    def set_cipher_suite(self, ssl_context_id=2, cipher_suite="0xFFFF"):
        """
        Function for setting modem SSL cipher suite

        Parameters
        ----------
        ssl_context_id : int, default: 2
            SSL context identifier

        cipher_suite : str, default: "0xFFFF"
            SSL Cipher suite.
            * 0X0035 --> TLS_RSA_WITH_AES_256_CBC_SHA
            * 0X002F --> TLS_RSA_WITH_AES_128_CBC_SHA
            * 0X0005 --> TLS_RSA_WITH_RC4_128_SHA
            * 0X0004 --> TLS_RSA_WITH_RC4_128_MD5
            * 0X000A --> TLS_RSA_WITH_3DES_EDE_CBC_SHA
            * 0X003D --> TLS_RSA_WITH_AES_256_CBC_SHA256
            * 0XC002 --> TLS_ECDH_ECDSA_WITH_RC4_128_SHA
            * 0XC003 --> TLS_ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA
            * 0XC004 --> TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA
            * 0XC005 --> TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA
            * 0XC007 --> TLS_ECDHE_ECDSA_WITH_RC4_128_SHA
            * 0XC008 --> TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA
            * 0XC009 --> TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA
            * 0XC00A --> TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA
            * 0XC011 --> TLS_ECDHE_RSA_WITH_RC4_128_SHA
            * 0XC012 --> TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA
            * 0XC013 --> TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA
            * 0XC014 --> TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA
            * 0XC00C --> TLS_ECDH_RSA_WITH_RC4_128_SHA
            * 0XC00D --> TLS_ECDH_RSA_WITH_3DES_EDE_CBC_SHA
            * 0XC00E --> TLS_ECDH_RSA_WITH_AES_128_CBC_SHA
            * 0XC00F --> TLS_ECDH_RSA_WITH_AES_256_CBC_SHA
            * 0XC023 --> TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256
            * 0XC024 --> TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384
            * 0XC025 --> TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA256
            * 0XC026 --> TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384
            * 0XC027 --> TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256
            * 0XC028 --> TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
            * 0XC029 --> TLS_ECDH_RSA_WITH_AES_128_CBC_SHA256
            * 0XC02A --> TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384
            * 0XC02B --> TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256
            * 0XC02F --> TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
            * 0XC0A8 --> TLS_PSK_WITH_AES_128_CCM_8
            * 0X00AE --> TLS_PSK_WITH_AES_128_CBC_SHA256
            * 0XC0AE --> TLS_ECDHE_ECDSA_WITH_AES_128_CCM_8
            * 0XFFFF --> Support all cipher suites

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QSSLCFG="ciphersuite",{ssl_context_id},{cipher_suite}'
        return self.atcom.send_at_comm(command)

    def set_ignore_local_time(self, ssl_context_id=2, ignore_local_time=1):
        """
        Function for setting modem SSL ignore local time

        Parameters
        ----------
        ssl_context_id : int, default: 2
            SSL context identifier

        ignore_local_time : int, default: 1
            Ignore local time
            * 0 --> Do not ignore local time
            * 1 --> Ignore local time

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QSSLCFG="ignorelocaltime",{ssl_context_id},{ignore_local_time}'
        return self.atcom.send_at_comm(command)

    def configure_for_x509_certification(self):
        """
        Function for configuring the modem for X.509 certification.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """

        step_set_ca = Step(
            function=self.set_ca_cert,
            name="set_ca",
            success="set_client_cert",
            fail="failure",
        )

        step_set_client_cert = Step(
            function=self.set_client_cert,
            name="set_client_cert",
            success="set_client_key",
            fail="failure",
        )

        step_set_client_key = Step(
            function=self.set_client_key,
            name="set_client_key",
            success="set_sec_level",
            fail="failure",
        )

        step_set_sec_level = Step(
            function=self.set_sec_level,
            name="set_sec_level",
            success="set_ssl_ver",
            fail="failure",
        )

        step_set_ssl_ver = Step(
            function=self.set_version,
            name="set_ssl_ver",
            success="set_ssl_ciphers",
            fail="failure",
        )

        step_set_ssl_ciphers = Step(
            function=self.set_cipher_suite,
            name="set_ssl_ciphers",
            success="set_ignore_local_time",
            fail="failure",
        )

        step_set_ignore_local_time = Step(
            function=self.set_ignore_local_time,
            name="set_ignore_local_time",
            success="success",
            fail="failure",
        )

        sm = StateManager(first_step=step_set_ca)
        sm.add_step(step_set_ca)
        sm.add_step(step_set_client_cert)
        sm.add_step(step_set_client_key)
        sm.add_step(step_set_sec_level)
        sm.add_step(step_set_ssl_ver)
        sm.add_step(step_set_ssl_ciphers)
        sm.add_step(step_set_ignore_local_time)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])
