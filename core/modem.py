from core.atcom import ATCom, Status
import time

class Modem:
    atcom = ATCom()

    CTRL_Z = '\x1A'

    ############################
    ### Main Modem functions ###
    ############################
    def check_modem_communication(self):
        """
        Function for checking modem communication
        """
        return self.atcom.send_at_comm("AT").get("status")

    def set_modem_echo_off(self):
        """
        Function for setting modem echo off
        """
        return self.atcom.send_at_comm("ATE0").get("status")

    def set_modem_echo_on(self):
        """
        Function for setting modem echo on
        """
        return self.atcom.send_at_comm("ATE1").get("status")

    ################################
    ### Authendication functions ###
    ################################
    def delete_modem_ca_cert(self):
        """
        Function for deleting modem CA certificate
        """
        return self.atcom.send_at_comm('AT+QFDEL="cacert.pem"').get("status")

    def delete_modem_client_cert(self):
        """
        Function for deleting modem client certificate
        """
        return self.atcom.send_at_comm('AT+QFDEL="client.pem"').get("status")

    def delete_modem_client_key(self):
        """
        Function for deleting modem client key
        """
        return self.atcom.send_at_comm('AT+QFDEL="client.key"').get("status")

    def upload_modem_ca_cert(self, ca_cert, timeout=5000):
        """
        Function for uploading modem CA certificate
        """
        len_cacert = len(ca_cert)
        command = f'AT+QFUPL="cacert.pem",{len_cacert},{timeout}'
        res = self.atcom.send_at_comm(command,"CONNECT").get("status")
    
        if res == Status.SUCCESS:
            self.atcom.send_at_comm_once(ca_cert) # send ca cert
            return self.atcom.send_at_comm(self.CTRL_Z).get("status") # send end char -> CTRL_Z
        else:
            return res

    def upload_modem_client_cert(self, client_cert, timeout=5000):
        """
        Function for uploading modem client certificate
        """
        len_clientcert = len(client_cert)
        command = f'AT+QFUPL="client.pem",{len_clientcert},{timeout}'
        res = self.atcom.send_at_comm(command,"CONNECT").get("status")
    
        if res == Status.SUCCESS:
            self.atcom.send_at_comm_once(client_cert) # send client cert
            return self.atcom.send_at_comm(self.CTRL_Z).get("status") # send end char -> CTRL_Z
        else:
            return res

    def upload_modem_client_key(self, client_key, timeout=5000):
        """
        Function for uploading modem client key
        """
        len_clientkey = len(client_key)
        command = f'AT+QFUPL="client.key",{len_clientkey},{timeout}'
        res = self.atcom.send_at_comm(command,"CONNECT").get("status")
    
        if res == Status.SUCCESS:
            self.atcom.send_at_comm_once(client_key) # send client key
            return self.atcom.send_at_comm(self.CTRL_Z).get("status") # send end char -> CTRL_Z
        else:
            return res
    
    ##################### 
    ### SSL functions ###
    #####################


    ######################
    ### MQTT Functions ###
    ######################