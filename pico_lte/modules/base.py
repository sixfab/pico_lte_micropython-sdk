"""
Module for including base functionalities of PicoLTE module.
For example; power control of modem, basic communication check etc.
"""

import time

from machine import Pin
from pico_lte.common import debug
from pico_lte.utils.status import Status
from pico_lte.utils.helpers import get_desired_data


class Base:
    """
    Class for inculding basic functions of PicoLTE module.
    """

    def __init__(self, atcom):
        """
        Constructor for Base class
        """
        self.atcom = atcom
        # self.module_power = Pin(26, Pin.OUT)
        self.powerkey_pin = Pin(17, Pin.OUT)
        self.status_pin = Pin(20, Pin.IN)

    def power_off(self):
        """
        Function for powering off celullar modem
        """
        self.powerkey_pin.value(1)
        time.sleep(1)
        self.powerkey_pin.value(0)

    def power_on(self):
        """
        Function for powering on celullar modem
        """
        self.powerkey_pin.value(1)
        time.sleep(0.5)
        self.powerkey_pin.value(0)

    def power_status(self):
        """
        Function for getting power status of modem

        Returns
        -------
        power_status : int
            Power status of modem (0=on, 1=off)
        """
        debug.debug("Power status:", self.status_pin.value())
        return self.status_pin.value()

    def wait_until_status_on(self, timeout=30):
        """
        Function for waiting until modem status is on

        Parameters
        ----------
        timeout : int, default: 30
            Timeout in seconds for waiting.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.power_status()
            if status == 0:
                return {"status": Status.SUCCESS, "response": "Success"}
            time.sleep(1)
        return {"status": Status.TIMEOUT, "response": "Timeout"}

    def check_communication(self):
        """
        Function for checking modem communication

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        return self.atcom.send_at_comm("AT")

    def wait_until_modem_ready_to_communicate(self, timeout=30):
        """
        Function for waiting until modem is ready to communicate

        Parameters
        ----------
        timeout : int, optional
            Timeout for waiting. The default is 30.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        result_timeout = {"status": Status.TIMEOUT, "response": "timeout"}

        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.check_communication()
            debug.debug("COM:", result)
            if result["status"] == Status.SUCCESS:
                return result
            time.sleep(1)

        return result_timeout

    def set_echo_off(self):
        """
        Function for setting modem echo off

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        return self.atcom.send_at_comm("ATE0")

    def set_echo_on(self):
        """
        Function for setting modem echo on

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        return self.atcom.send_at_comm("ATE1")

    def check_sim_ready(self):
        """
        Function for checking SIM ready status

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        desired_reponses = ["+CPIN: READY"]
        return self.atcom.send_at_comm("AT+CPIN?", desired_reponses)

    def enter_sim_pin_code(self, pin_code):
        """
        Function for entering SIM PIN code

        Parameters
        ----------
        pin_code : str
            SIM PIN code

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+CPIN="{pin_code}"'
        return self.atcom.send_at_comm(command)

    def get_sim_iccid(self):
        """
        Function for getting SIM ICCID

        Returns
        -------
        dict
            Result that includes "status", "response" and "value" keys
        """
        command = "AT+QCCID"
        result = self.atcom.send_at_comm(command)
        return get_desired_data(result, "+QCCID: ")

    ####################
    ### Modem Config ###
    ####################
    def config_network_scan_mode(self, scan_mode=0):
        """
        Function for configuring modem network scan mode

        Parameters
        ----------
        scan_mode : int
            Scan mode (default=0)
            * 0 --> Automatic
            * 1 --> GSM Only
            * 3 --> LTE Only

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QCFG="nwscanmode",{scan_mode}'
        return self.atcom.send_at_comm(command)

    def config_network_scan_sequence(self, scan_sequence="00"):
        """
        Function for configuring modem scan sequence

        Parameters
        ----------
        scan_sequence : str
            Scan sequence (default=00)
            * 00 --> Automatic (eMTC → NB-IoT → GSM)
            * 01 --> GSM
            * 02 --> eMTC
            * 03 --> NB-IoT

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QCFG="nwscanseq",{scan_sequence}'
        return self.atcom.send_at_comm(command)

    def config_network_iot_operation_mode(self, iotopmode=2):
        """
        Function for configuring modem IoT operation mode

        Parameters
        ----------
        iotopmode : int
            Operation mode (default=2)
            * 0 --> eMTC
            * 1 --> NB-IoT
            * 2 --> eMTC and NB-IoT

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        command = f'AT+QCFG="iotopmode",{iotopmode}'
        return self.atcom.send_at_comm(command)

    ####################
    ### CellularTech ###
    ####################
    def get_cell_information(self, cell_type):
        """
        Function for getting cell information

        Parameters
        ----------
        cell_type : str
            Cell type ("servingcell" or "neighbourcell")

        Returns
        -------
        dict
            Result that includes "status" and "response" keys.
        """
        if cell_type not in ["servingcell", "neighbourcell"]:
            return {"status": Status.ERROR, "response": "Invalid cell type"}

        command = f'AT+QENG="{cell_type}"'
        return self.atcom.send_at_comm(command)

    def get_all_cells(self, technology="eMTC", timeout=60):
        """
        Function for getting all cells

        Parameters
        ----------
        technology : str
            Technology (default="eMTC")
            * "GSM"
            * "eMTC"
            * "NBIoT"

        Returns
        -------
        dict
            Result that includes "status" and "response" keys.
        """
        if technology == "GSM":
            technology_no = 1
        elif technology == "eMTC":
            technology_no = 8
        elif technology == "NBIoT":
            technology_no = 9
        else:
            return {"status": Status.ERROR, "response": "Invalid technology"}

        # TODO: Get all the information from the URC, not the first one.
        command = f"AT+QCELLSCAN={technology_no},{timeout}"
        return self.atcom.send_at_comm(
            command, timeout=timeout, urc=True, desired='+QCELLSCAN: "{technology}",'
        )
