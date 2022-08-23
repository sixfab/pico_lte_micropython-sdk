"""
Module for including file functions of picocell module.
"""

from core.utils.status import Status

class File:
    """
    Class for inculding functions of file operations of picocell module.
    """
    CTRL_Z = '\x1A'

    def __init__(self, atcom):
        """
        Initialization of the class.
        """
        self.atcom = atcom

    def get_file_list(self, path="*"):
        """
        Function for getting file list

        Parameters
        ----------
        path : str
            Path to the directory (default="*")

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QFLST="{path}"'
        return self.atcom.send_at_comm(command)

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
        return self.atcom.send_at_comm(command)

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
        result = self.atcom.send_at_comm(command)

        if result["status"] == Status.WAITING_INPUT:
            self.atcom.send_at_comm_once(file) # send ca cert
            return self.atcom.send_at_comm(self.CTRL_Z) # send end char -> CTRL_Z
        return result
