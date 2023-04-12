"""This module contains the KeyCase class, which is used to store the keys of a
application service for both cellular and wifi connections.
"""

import os
from core.utils.enums import Status, Connection
from core.utils.helpers import get_parameter, read_file
from core.temp import debug


class KeyCase:
    """This class enables a worker to store or delete the keys of all applications."""

    def __init__(self, cellular, wifi):
        self.cellular = cellular
        self.wifi = wifi

    def load_certificates(
        self, app_name, certificate_fields, for_connection=Connection.WIFI, secure=False
    ):
        """Function for get certificate paths of an application.
        It works for both cellular and WiFi connections.

        Parameters
        ----------
        app_name : str
            Name of the application.
        certificate_fields : list
            List of the names of the fields.
        for_connection : Connection, optional
            Connection type, by default Connection.WIFI
        secure_storage : bool, optional
            If True, certificates will be loaded to secure storage, by default False

        Returns
        -------
        list
            List of the paths of the certificates.
        """
        certs = self.get_certificate_paths(app_name, certificate_fields)

        if for_connection == Connection.WIFI:
            # If the connection is WiFi, return the paths of the certificates
            # ordered by the certificate_fields list.
            return [certs[field]["path"] for field in certificate_fields]

        if for_connection == Connection.CELLULAR:
            # If the connection is cellular, load the certificates to secure storage.
            # Return the paths of the certificates in the secure storage.
            fs_locs = [certs[field]["path"] for field in certificate_fields]
            ss_locs = []
            for field in certificate_fields:
                ss_locs.append(f'{app_name}_{certs[field]["name"]}')
            return self.load_certificates_to_cellular_modem(fs_locs, ss_locs, secure)

    def delete_certificate(self, file_location):
        """Function for deleting certificates from file system.

        Parameters
        ----------
        file : str
            Path of the file.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        try:
            os.remove(file_location)
        except Exception as error:
            debug.error("Error occured while deleting certificates", error)
            return {"status": Status.ERROR, "response": str(error)}

    def get_certificate_paths(self, app_name, field_names):
        """Returns the paths of the certificates of an application.

        Parameters
        ----------
        app_name : str
            Name of the application.
        field_names : list
            List of the names of the fields.

        Returns
        -------
        dict
            Dictionary of the certificates.
        """
        certificate_data = {}
        for field_name in field_names:
            cert_loc = get_parameter([app_name, "certificates", field_name])
            if cert_loc is None:
                raise Exception("Certificate location is not defined!")

            if not isinstance(cert_loc, str):
                raise Exception("Certificate location is not a string!")

            # Parse the name of the file from the path.
            cert_name = cert_loc.split("/")[-1]
            certificate_data[field_name] = {"name": cert_name, "path": cert_loc}

        return certificate_data

    def check_certificates_on_cellular_modem(self, output_loc):
        """
        Function for checking certificates in secure storage.

        Parameters
        ----------
        output_loc : list
            List of certificates in secure storage.

        Returns
        -------
        list
            List of the paths of the certificates.
        """
        # Get all the files in the /security folder.
        result = self.cellular.file.get_file_list("ufs:/security/*")
        response = result.get("value")

        # Check if the response success.
        if result["status"] != Status.SUCCESS:
            debug.error("Error occured while getting certificates from secure storage!")
            return {
                "status": Status.ERROR,
                "response": "Error occured while getting certificates from secure storage!",
            }

        # Check if the certificates are in the secure storage.
        for file_check in output_loc:
            file_path = "/security/" + file_check
            if file_path not in response:
                debug.error("Certificate couldn't find in secure storage!")
                return None

        # Return the paths of the certificates in the secure storage.
        return ["/security/" + file_check for file_check in output_loc]

    def load_certificates_to_cellular_modem(self, input_list, output_loc, secure=False):
        """
        Function for loading certificates from file

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        if len(input_list) != len(output_loc):
            raise Exception("Input and output lists are not equal!")

        # Read the files and upload them to the secure storage.
        for index, file in enumerate(input_list):
            file_content = read_file(file)
            # Check if file exists.
            if file_content is None:
                raise Exception("File doesn't exist!")

            file_location = "/security/" + output_loc[index]
            try:
                # Delete old certificate if existed.
                self.cellular.file.delete_file_from_modem(file_location)
                # Upload the new certificate.
                self.cellular.file.upload_file_to_modem(file_location, file_content)
            except Exception as error:
                debug.error("Error occured while uploading certificates", error)
                raise Exception("Error occured while uploading certificates.")

            # Delete the files from the file system if secure_storage is True.
            if secure:
                self.delete_certificate(file)
                debug.debug("Certificate deleted from file system.")

        return self.check_certificates_on_cellular_modem(output_loc)
