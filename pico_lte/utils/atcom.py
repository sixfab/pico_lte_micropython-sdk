"""
Module for communicating with cellular modem over UART interface.
"""

import time
from machine import UART, Pin
from pico_lte.common import debug
from pico_lte.utils.status import Status


class ATCom:
    """Class for handling AT communication with modem"""

    def __init__(self, uart_number=0, tx_pin=Pin(0), rx_pin=Pin(1), baudrate=115200, timeout=10000):
        self.modem_com = UART(uart_number, tx=tx_pin, rx=rx_pin, baudrate=baudrate, timeout=timeout)

    def send_at_comm_once(self, command, line_end=True):
        """
                Function for sending AT commmand to modem

                Parameters
        ----------
        command: str
            AT command to send
        line_end: bool, default: True
            If True, send line end
        """
        if line_end:
            compose = f"{command}\r".encode()
        else:
            compose = command.encode()
            debug.focus(compose)

        try:
            self.modem_com.write(compose)
        except:
            debug.error("Error occured while AT command writing to modem")

    def get_response(self, desired_responses=None, fault_responses=None, timeout=5):
        """
                Function for getting modem response

        Parameters
        ----------
        desired_response: str, default: None
            Desired response from modem
        timeout: int
            Timeout for getting response

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        response = ""
        processed = []

        if desired_responses:
            if isinstance(desired_responses, str):  # if desired response is string
                desired_responses = [desired_responses]  # make it list
        if fault_responses:
            if isinstance(fault_responses, str):  # if desired response is string
                fault_responses = [fault_responses]  # make it list

        timer = time.time()
        while True:
            time.sleep(0.1)  # wait for new chars

            if time.time() - timer < timeout:
                while self.modem_com.any():
                    try:
                        response += self.modem_com.read(self.modem_com.any()).decode("utf-8")
                        debug.debug("Response:", [response])
                    except:
                        pass
            else:
                return {"status": Status.TIMEOUT, "response": "timeout"}

            if response != "":
                responses = response.split("\r\n")
                processed.extend([x for x in responses if x != ""])
                debug.debug("Processed:", processed)
                response = ""

            head = 0
            for index, value in enumerate(processed):
                processed_part = processed[head : index + 1]

                if value == "OK":
                    if not desired_responses:  # if we don't look for specific responses
                        return {"status": Status.SUCCESS, "response": processed_part}
                    else:
                        if index - head < 1:  # we haven't got an informative response here
                            return {"status": Status.ERROR, "response": processed_part}

                        for focus_line in processed[head:index]:  # scan lines before 'OK'
                            if desired_responses:
                                if any(desired in focus_line for desired in desired_responses):
                                    debug.debug("Desired:", focus_line)
                                    return {"status": Status.SUCCESS, "response": processed_part}
                            if fault_responses:
                                if any(fault in focus_line for fault in fault_responses):
                                    debug.debug("Fault:", focus_line)
                                    return {"status": Status.ERROR, "response": processed_part}

                elif "+CME ERROR:" in value or value == "ERROR":  # error
                    return {"status": Status.ERROR, "response": processed_part}

    def get_urc_response(self, desired_responses=None, fault_responses=None, timeout=5):
        """
                Function for getting modem urc response

        Parameters
        ----------
        desired_response: str or list, default: None
            List of desired responses
        fault_response: str or list, default: None
            List of fault response from modem
        timeout: int
            timeout for getting response

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        response = ""
        processed = []

        if desired_responses:
            if isinstance(desired_responses, str):  # if desired response is string
                desired_responses = [desired_responses]  # make it list
        if fault_responses:
            if isinstance(fault_responses, str):  # if desired response is string
                fault_responses = [fault_responses]  # make it list

        if not desired_responses and not fault_responses:
            return {"status": Status.SUCCESS, "response": "No desired or fault responses"}

        timer = time.time()
        while True:
            time.sleep(0.1)  # wait for new chars

            if time.time() - timer < timeout:
                while self.modem_com.any():
                    try:
                        response += self.modem_com.read(self.modem_com.any()).decode("utf-8")
                    except:
                        pass
            else:
                return {"status": Status.TIMEOUT, "response": "timeout"}

            if response != "":
                responses = response.split("\r\n")
                processed.extend([x for x in responses if x != ""])
                debug.debug("Processed:", processed)
                response = ""

            head = 0
            for index, value in enumerate(processed):
                processed_part = processed[head : index + 1]

                if desired_responses:
                    for desired in desired_responses:
                        if desired in value:
                            return {"status": Status.SUCCESS, "response": processed_part}
                if fault_responses:
                    for fault in fault_responses:
                        if fault in value:
                            return {"status": Status.ERROR, "response": processed_part}

    def send_at_comm(self, command, desired=None, fault=None, timeout=5, line_end=True, urc=False):
        """
                Function for writing AT command to modem and getting modem response

        Parameters
        ----------
        command: str
            AT command to send
        desired: str or list, default: None
            List of desired responses
        fault: str or list, default: None
            List of fault responses
        timeout: int
            Timeout for getting response
        line_end: bool, default: True
            If True, send line end
        urc: bool, default: False
            If True, get urc response

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        self.send_at_comm_once(command, line_end=line_end)
        time.sleep(0.1)
        if urc:
            return self.get_urc_response(desired, fault, timeout)
        return self.get_response(desired, fault, timeout)
