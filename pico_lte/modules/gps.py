"""
Module for including functions of location service of PicoLTE module.
"""

from pico_lte.utils.helpers import get_desired_data
from pico_lte.utils.status import Status


class GPS:
    """
    Class for inculding functions of location service of PicoLTE module.
    """

    def __init__(self, atcom):
        """
        Initialization of the class.
        """
        self.atcom = atcom

    def get_priority(self):
        """
        Get the priority of the GPS.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = 'AT+QGPSCFG="priority"'
        return self.atcom.send_at_comm(command)

    def set_priority(self, priority):
        """
        Set the priority of the GPS.

        Parameters
        ----------
        priority : int
            Priority of the GPS.
            * 0 --> GNSS prior mode
            * 1 --> WWAN prior mode

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QGPSCFG="priority",{priority}'
        return self.atcom.send_at_comm(command)

    def turn_on(self, mode=1, accuracy=3, fix_count=0, fix_rate=1):
        """
        Turn on the GPS.

        Parameters
        ----------
        mode : int, default: 1
            Mode of the GPS.
        accuracy : int, default: 3
            The desired level of accuracy acceptable for fix computation.
            * 1 --> Low Accuracy (1000 m)
            * 2 --> Medium Accuracy (500 m)
            * 3 --> High Accuracy (50 m)
        fix_count : int
            Number of positioning or continuous positioning attempts. (0-1000)(default=0)
            0 indicates continuous positioning. Other values indicate the number of positioning
            attempts. When the value reaches the specified number of attempts, the GNSS will
            be stopped.
        fix_rate : int, default: 1
            The interval between the first- and second-time positioning. Unit: second.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f"AT+QGPS={mode},{accuracy},{fix_count},{fix_rate}"
        return self.atcom.send_at_comm(command)

    def turn_off(self):
        """
        Turn off the GPS.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = "AT+QGPSEND"
        return self.atcom.send_at_comm(command)

    def get_location(self):
        """
        Get the location of the device.

        Returns
        -------
        dict
            Result that includes "status","response" and "value" keys
            * "status" --> Status.SUCCESS or Status.ERROR
            * "response" --> Response of the command
            * "value" --> [lat,lon] Location of the device
        """
        command = "AT+QGPSLOC?"
        desired = "+QGPSLOC: "
        result = self.atcom.send_at_comm(command, desired)

        if result["status"] == Status.SUCCESS:
            data = get_desired_data(result, desired, data_index=[1, 2])
            data["value"]["Lat-Lon"][0] = self.nmea_to_decimal(
                data["value"]["Lat-Lon"][0]
            )
            data["value"]["Lat-Lon"][1] = self.nmea_to_decimal(
                data["value"]["Lat-Lon"][1]
            )
            return data
        return result

    def nmea_to_decimal(self, nmea_data):
        """
        Convert NMEA data to decimal.

        Parameters
        ----------
        nmea_data : str
            NMEA data to be converted to decimal.

        Returns
        -------
        str
            Converted decimal data in string format.
        """
        value = float(nmea_data[0:-1])
        integer = int(value * 0.01)
        degree = integer + ((value - (integer * 100)) / 60)

        if nmea_data[-1] == "S" or nmea_data[-1] == "W":
            degree *= -1.0

        return str(degree)
