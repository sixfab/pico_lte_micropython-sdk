import time
from machine import UART, Pin


class Status:
    SUCCESS = 0
    ERROR = 1
    TIMEOUT = 2


class Modem:
    def __init__(
        self,
        uart_number = 0,
        tx_pin = Pin(0),
        rx_pin = Pin(1),
        baudrate = 115200,
        timeout = 10000
        ):
        self.modem_com = UART(
            uart_number,
            tx = tx_pin,
            rx = rx_pin,
            baudrate=baudrate,
            timeout=timeout
            )

    def send_at_comm_once(self, command, line_end=True):
        """
		Function for sending AT commmand to modem
        
		params:
			command: str, message that sending to modem
        """
        if line_end:
            self.compose = f"{command}\r".encode()
        else:
            self.compose = command.encode()

        try:
            self.modem_com.write(self.compose)
        except:
            print("Error occured while AT command writing to modem")
        
    def get_response(self, desired_response="OK", timeout=5):
        """
		Function for getting modem response
        
        params:
			desired_response: str, desired response of modem
            timeout: int, timeout in seconds
		"""
        response = ""

        timer = time.time()
        while True:
            if timer - time.time() < timeout:
                while self.modem_com.any():
                    response += self.modem_com.read(self.modem_com.any()).decode('utf-8')
            else:
                print("Timeout")
                return {"status": Status.TIMEOUT, "response": "timeout"}

            if desired_response in response:
                return {"status": Status.SUCCESS, "response": response}
            elif "ERROR" in response:
                return {"status": Status.ERROR, "response": response}
            else:
                return response

    def send_at_comm(self, command, response="OK", timeout=5):
        """
		Function for writing AT command to modem and getting modem response
		"""
        self.send_at_comm_once(command)
        time.sleep(0.1)
        return self.get_response(response, timeout)

    



            
            