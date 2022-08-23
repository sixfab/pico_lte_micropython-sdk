"""
Module for including network functions of picocell module.
"""
import time

from core.temp import config
from core.utils.helpers import get_desired_data
from core.utils.manager import StateManager, Step
from core.utils.status import Status

class Network:
    """
    Class for inculding functions of network operations of picocell module.
    """
    cache = config["cache"]

    def __init__(self, atcom, base):
        """
        Initialization of Network class.
        """
        self.atcom = atcom
        self.base = base

    def check_apn(self):
        """
        Function for checking modem APN is correct

        Returns
        -------
        (response, status, value) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
            value : str
                APN of modem
        """
        command = "AT+CGDCONT?"
        desired = "super"
        result = self.atcom.send_at_comm(command, desired)
        return result

    def get_apn(self):
        """
        Function for getting modem APN

        Returns
        -------
        (response, status, value) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
            value : str
                APN of modem
        """
        command = "AT+CGDCONT?"
        result = self.atcom.send_at_comm(command)
        return get_desired_data(result, prefix="+CGDCONT: 2,", data_index=1)

    def set_apn(self, cid=1, pdp_type="IPV4V6", apn="super"):
        """
        Function for setting modem APN

        Parameters
        ----------
        cid : int
            Context ID (default=1)
        pdp_type : str
            PDP type (default="IPV4V6")
                IPV4V6 --> IPv4v6
                IP --> IPv4
                IPV6 --> IPv6
        apn : str
            APN (default="super")

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+CGDCONT={cid},"{pdp_type}","{apn}"'
        return self.atcom.send_at_comm(command)

    def check_network_registration(self):
        """
        Function for checking network registeration status

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        desired_reponses = ["+CREG: 0,1", "+CREG: 0,5"]
        return self.atcom.retry_at_comm("AT+CREG?", desired_reponses, retry_count=20, interval=1)

    def get_operator_information(self):
        """
        Function for getting operator information

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = "AT+COPS?"
        result = self.atcom.send_at_comm(command)
        return get_desired_data(result, prefix="+COPS: ", data_index=2)

    def configure_tcp_ip_context(
        self, context_id=1, context_type=1, apn="super", username="", password="", auth=0
        ):
        """
        Function for configuring TCP/IP context

        Parameters
        ----------
        context_id : int
            TCP/IP context identifier (range 1:5) (default=1)
        context_type : int
            TCP/IP context type (default=1)
                1 --> IPv4
                2 --> IPv6
                3 --> IPv4v6
        apn : str
            APN (default="super")
        username : str
            Username (default="")
        password : str
            Password (default="")
        auth : int
            Authentication type (default=0)
                0 --> No authentication
                1 --> PAP
                2 --> CHAP

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QICSGP={context_id},{context_type},"{apn}","{username}","{password}",{auth}'
        return self.atcom.send_at_comm(command)


    def check_pdp_context_status(self, context_id=1):
        """
        Function for checking PDP context status

        Parameters
        ----------
        context_id : int
            PDP context identifier (range 1:5) (default=1)

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = "AT+CGACT?"
        return self.atcom.send_at_comm(command, f"+CGACT: {context_id},1")

    def activate_pdp_context(self, context_id=1):
        """
        Function for activating PDP context

        Parameters
        ----------
        context_id : int
            PDP context identifier (range 1:5) (default=1)

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QIACT={context_id}'
        return self.atcom.send_at_comm(command)

    def deactivate_pdp_context(self, context_id=1):
        """
        Function for deactivating PDP context

        Parameters
        ----------
        context_id : int
            PDP context identifier (range 1:5) (default=1)

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
        """
        command = f'AT+QIDEACT={context_id}'
        return self.atcom.send_at_comm(command)

    def register_network(self):
        """
        Function for registering network.

        Returns
        -------
        (status, modem_response) : tuple
            status : int
                Status of the command.
            modem_response : str
                Response of the modem.
        """

        step_network_precheck = Step(
            function=self.check_network_registration,
            name="check_network_registration",
            success="success",
            fail="check_atcom",
        )

        step_atcom = Step(
            function=self.base.check_communication,
            name="check_atcom",
            success="check_sim_ready",
            fail="failure"
        )

        step_sim_ready = Step(
            function=self.base.check_sim_ready,
            name="check_sim_ready",
            success="get_apn",
            fail="failure",
        )

        step_check_apn = Step(
            function=self.check_apn,
            name="check_apn",
            success="check_network_registration",
            fail="set_apn",
        )

        step_set_apn = Step(
            function=self.set_apn,
            name="set_apn",
            success="get_apn",
            fail="failure",
        )

        step_check_network = Step(
            function=self.check_network_registration,
            name="check_network_registration",
            success="success",
            fail="failure",
            interval=5,
            retry=60, # 60 times = 5 minute
        )

        # Add cache if it is not already existed
        function_name = "register_network"

        sm = StateManager(first_step = step_network_precheck, function_name=function_name)
        sm.add_step(step_network_precheck)
        sm.add_step(step_atcom)
        sm.add_step(step_sim_ready)
        sm.add_step(step_check_apn)
        sm.add_step(step_set_apn)
        sm.add_step(step_check_network)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])

    def get_pdp_ready(self):
        """
        Function for getting ready pdp context

        Returns
        -------
        (status, modem_response) : tuple
            status : int
                Status of the command.
            modem_response : str
                Response of the modem.
        """

        step_precheck_pdp = Step(
            function=self.check_pdp_context_status,
            name="check_pdp_context_status",
            success="success",
            fail="configure_pdp_context",
        )

        step_configure_pdp = Step(
            function=self.configure_tcp_ip_context,
            name="configure_pdp_context",
            success="deactivate_pdp_context",
            fail="failure",
        )

        step_deactivate_pdp = Step(
            function=self.deactivate_pdp_context,
            name="deactivate_pdp_context",
            success="activate_pdp_context",
            fail="activate_pdp_context",
        )

        step_activate_pdp = Step(
            function=self.activate_pdp_context,
            name="activate_pdp_context",
            success="success",
            fail="failure",
        )

        step_check_pdp = Step(
            function=self.check_pdp_context_status,
            name="check_pdp_context_status",
            success="success",
            fail="failure",
        )

        sm = StateManager(first_step = step_precheck_pdp)
        sm.add_step(step_precheck_pdp)
        sm.add_step(step_configure_pdp)
        sm.add_step(step_deactivate_pdp)
        sm.add_step(step_activate_pdp)
        sm.add_step(step_check_pdp)

        while True:
            result = sm.run()

            if result["status"] == Status.SUCCESS:
                return result
            elif result["status"] == Status.ERROR:
                return result
            time.sleep(result["interval"])
