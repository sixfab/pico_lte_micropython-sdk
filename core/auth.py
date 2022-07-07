"""
Module for managing authentication.
"""

import os

from core.status import Status
from core.modem import Modem


def read_file(file_path):
    """
    Function for reading file
    """
    try:
        with open(file_path, "r") as file:
            data = file.read()
    except:
        return None
    else:
        return data


class Auth:
    """
    Class for getting certificates of cloud services
    """
    def __init__(self, config: dict):
        self.config = config
        self.config["auth"] = {}
        self.modem = Modem()

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
                self.modem.delete_file_from_modem("/security/cacert.pem")
                self.modem.delete_file_from_modem("/security/client.pem")
                self.modem.delete_file_from_modem("/security/user_key.pem")
                # Upload new certificates
                self.modem.upload_file_to_modem("/security/cacert.pem", cacert)
                self.modem.upload_file_to_modem("/security/client.pem", client_cert)
                self.modem.upload_file_to_modem("/security/user_key.pem", client_key)
            except Exception as error:
                print("Error occured while uploading certificates", error)
                return Status.ERROR

            print("Certificates uploaded secure storage. Deleting from file system...")
            try:
                os.remove("../cert/cacert.pem")
                os.remove("../cert/client.pem")
                os.remove("../cert/user_key.pem")
            except Exception as error:
                print("Error occured while deleting certificates", error)
                return Status.ERROR

            print("Certificates deleted from file system.")

        # check certificates in modem
        result = self.modem.get_file_list("ufs:/security/*")

        if result["status"] == Status.SUCCESS:
            if "cacert.pem" in result["response"] and \
                    "client.pem" in result["response"] and \
                        "user_key.pem" in result["response"]:
                print("Certificates found in modem.")
                return Status.SUCCESS
            else:
                print("Certificates couldn't find in modem!")
                return Status.ERROR
        else:
            print("Error occured while getting certificates from modem!")
            return Status.ERROR
