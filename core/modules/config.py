"""
Module for including extended configuration function of picocell module.
"""

class Config:
    """
    Class for including extended configuration functions.
    """
    def __init__(self, atcom):
        """
        Constructor of the Config class.
        """
        self.atcom = atcom

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
