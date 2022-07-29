"""
Example code for publishing data to AWS IoT by using SDK funtions.
"""

import json
import time

from core.modem import Modem
from core.utils.atcom import ATCom

###########################
### AWS HTTP(s) example ###
###########################

modem = Modem()
atcom = ATCom()

PAYLOAD_JSON = {"state": {"reported": {"Status": "Hello from Picocell --> HTTP"}}}
payload = json.dumps(PAYLOAD_JSON)

# Check communication with modem
print("COM: ", modem.base.check_communication())
print("Set APN: ", atcom.send_at_comm('AT+CGDCONT=1,"IP","super"',"OK"))
print("COPS: ", atcom.retry_at_comm("AT+COPS?","+COPS: 0,0", timeout=1, retry_count=10))
print(atcom.send_at_comm('AT+QICSGP=1,1,"super","","",1',"OK"))

# TCP/IP
print("TCPIP Context Configuration: ", modem.http.set_context_id())
print("PDP Deactivation: ", modem.network.deactivate_pdp_context())
print("PDP Activatation: ", modem.network.activate_pdp_context())
print("PDP Test: ", atcom.send_at_comm("AT+CGACT?","OK"))

# Configurations
# SSL
print("Modem SSL CA: ", modem.ssl.set_ca_cert())
print("Modem SSL Client Cert: ", modem.ssl.set_client_cert())
print("Modem SSL Client Key: ", modem.ssl.set_client_key())
print("Set Modem Security Level: ", modem.ssl.set_sec_level())
print("Set modem SSL Version: ", modem.ssl.set_version())
print("Set modem SSL Cipher: ", modem.ssl.set_cipher_suite())
print("Set modem ignore local time: ", modem.ssl.set_ignore_local_time())

# HTTP
print("Set HTTP SSL Context", modem.http.set_context_id(2))
print("HTTP URL: ", modem.http.set_server_url())
print("HTTP POST: ", modem.http.post(payload))
time.sleep(2)
print("HTTP READ: ", modem.http.read_response())
