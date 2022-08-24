"""
Module for including authentication functions of picocell module.
"""

import os

from core.temp import debug
from core.utils.status import Status
from core.utils.helpers import read_file
from core.modules.file import File

class Auth:
    """
    Class for including authentication functions of picocell module.
    """

    def __init__(self, atcom):
        """
        Constructor for Auth class.
        """
        self.atcom = atcom
        self.file = File(atcom)

    def load_certificates(self):
        """
        Function for loading certificates from file
        """
        cacert = read_file("../cert/cacert.pem")
        client_cert = read_file("../cert/client.pem")
        client_key = read_file("../cert/user_key.pem")

        first_run = cacert and client_cert and client_key

        # If first run, upload the certificates to the modem
        if first_run:
            try:
                # delete old certificates if existed
                self.file.delete_file_from_modem("/security/cacert.pem")
                self.file.delete_file_from_modem("/security/client.pem")
                self.file.delete_file_from_modem("/security/user_key.pem")
                # Upload new certificates
                self.file.upload_file_to_modem("/security/cacert.pem", cacert)
                self.file.upload_file_to_modem("/security/client.pem", client_cert)
                self.file.upload_file_to_modem("/security/user_key.pem", client_key)
            except Exception as error:
                debug.error("Error occured while uploading certificates", error)
                return {"status" : Status.ERROR, "response" : str(error)}

            debug.info("Certificates uploaded secure storage. Deleting from file system...")
            try:
                os.remove("../cert/cacert.pem")
                os.remove("../cert/client.pem")
                os.remove("../cert/user_key.pem")
            except Exception as error:
                debug.error("Error occured while deleting certificates", error)
                return {"status" : Status.ERROR, "response" : str(error)}

            debug.info("Certificates deleted from file system.")

        # check certificates in modem
        result = self.file.get_file_list("ufs:/security/*")
        response = result.get("response", [])

        cacert_in_modem = False
        client_cert_in_modem = False
        client_key_in_modem = False

        if result["status"] == Status.SUCCESS:
            for line in response:
                if "cacert.pem" in line:
                    cacert_in_modem = True
                if "client.pem" in line:
                    client_cert_in_modem = True
                if "user_key.pem" in line:
                    client_key_in_modem = True

            if cacert_in_modem and client_cert_in_modem and client_key_in_modem:
                debug.info("Certificates found in modem.")
                return {"status" : Status.SUCCESS, "response" : "Certificates found in modem."}
            else:
                debug.error("Certificates couldn't find in modem!")
                return {
                    "status" : Status.ERROR,
                    "response" : "Certificates couldn't find in modem!"
                    }
        else:
            debug.error("Error occured while getting certificates from modem!")
            return {
                "status" : Status.ERROR,
                "response" : "Error occured while getting certificates from modem!"
                }
