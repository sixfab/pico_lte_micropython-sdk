"""
Module for including authentication functions of PicoLTE module.
"""

import os

from pico_lte.common import debug, Status
from pico_lte.utils.helpers import read_file
from pico_lte.modules.file import File


class Auth:
    """
    Class for including authentication functions of PicoLTE module.
    """

    PRIVATE_FILE = "private_key.pem"
    DEVICE_CERT_FILE = "device_cert.pem"
    ROOT_CA_CERT_FILE = "root_ca.pem"

    def __init__(self, atcom):
        """
        Constructor for Auth class.
        """
        self.atcom = atcom
        self.file = File(atcom)

    def load_certificates(self):
        """
        Function for loading certificates from file

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        root_ca_cert = read_file(f"../cert/{self.ROOT_CA_CERT_FILE}")
        device_certificate = read_file(f"../cert/{self.DEVICE_CERT_FILE}")
        private_key_file = read_file(f"../cert/{self.PRIVATE_FILE}")

        first_run = root_ca_cert and device_certificate and private_key_file

        # If first run, upload the certificates to the modem
        if first_run:
            try:
                # delete old certificates if existed
                self.file.delete_file_from_modem(f"/security/{self.PRIVATE_FILE}")
                self.file.delete_file_from_modem(f"/security/{self.DEVICE_CERT_FILE}")
                self.file.delete_file_from_modem(f"/security/{self.ROOT_CA_CERT_FILE}")

                # Upload new certificates
                self.file.upload_file_to_modem(
                    f"/security/{self.PRIVATE_FILE}", root_ca_cert
                )
                self.file.upload_file_to_modem(
                    f"/security/{self.DEVICE_CERT_FILE}", device_certificate
                )
                self.file.upload_file_to_modem(
                    f"/security/{self.ROOT_CA_CERT_FILE}", private_key_file
                )
            except Exception as error:
                debug.error("Error occured while uploading certificates", error)
                return {"status": Status.ERROR, "response": str(error)}

            debug.info(
                "Certificates uploaded secure storage. Deleting from file system..."
            )
            try:
                os.remove(f"../cert/{self.ROOT_CA_CERT_FILE}")
                os.remove(f"../cert/{self.DEVICE_CERT_FILE}")
                os.remove(f"../cert/{self.PRIVATE_FILE}")
            except Exception as error:
                debug.error("Error occured while deleting certificates", error)
                return {"status": Status.ERROR, "response": str(error)}

            debug.info("Certificates deleted from file system.")

        # check certificates in modem
        result = self.file.get_file_list("ufs:/security/*")
        response = result.get("response", [])

        cacert_in_modem = False
        client_cert_in_modem = False
        client_key_in_modem = False

        if result["status"] == Status.SUCCESS:
            for line in response:
                if self.ROOT_CA_CERT_FILE in line:
                    cacert_in_modem = True
                if self.DEVICE_CERT_FILE in line:
                    client_cert_in_modem = True
                if self.PRIVATE_FILE in line:
                    client_key_in_modem = True

            if cacert_in_modem and client_cert_in_modem and client_key_in_modem:
                debug.info("Certificates found in PicoLTE.")
                return {
                    "status": Status.SUCCESS,
                    "response": "Certificates found in PicoLTE.",
                }
            else:
                debug.error("Certificates couldn't find in modem!")
                return {
                    "status": Status.ERROR,
                    "response": "Certificates couldn't find in modem!",
                }
        else:
            debug.error("Error occured while getting certificates from modem!")
            return {
                "status": Status.ERROR,
                "response": "Error occured while getting certificates from modem!",
            }
