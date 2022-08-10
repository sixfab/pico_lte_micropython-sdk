"""
Module for including functions of location service of picocell module.
"""

from core.temp import config, debug

class GPS:
    """
    Class for inculding functions of location service of picocell module.
    """
    def __init__(self, atcom):
        """
        Initialization of the class.
        """
        self.atcom = atcom

    def turn_on(self, mode=1, accuracy=3, fix_count=0, fix_rate=1):
        """
        Turn on the GPS.

        Parameters
        ----------
        mode : int
            Mode of the GPS (default=1)
        accuracy : int
            The desired level of accuracy acceptable for fix computation. (default=3)
                1 --> Low Accuracy (1000 m)
                2 --> Medium Accuracy (500 m)
                3 --> High Accuracy (50 m)
        fix_count : int
            Number of positioning or continuous positioning attempts. (0-1000)(default=0)
            0 indicates continuous positioning. Other values indicate the number of positioning
            attempts. When the value reaches the specified number of attempts, the GNSS will
            be stopped.
        fix_rate : int
            The interval between the first- and second-time positioning. Unit: second. (default=1)

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QGPS={mode},{accuracy},{fix_count},{fix_rate}'
        return self.atcom.send_at_comm(command, "OK")

    def turn_off(self):
        """
        Turn off the GPS.

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = "AT+QGPSEND"
        return self.atcom.send_at_comm(command, "OK")

    def get_location(self):
        """
        Get the location of the device.

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.

        """
        command = "AT+QGPSLOC"
        return self.atcom.send_at_comm(command, "OK")
