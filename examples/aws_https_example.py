"""
Example code for publishing data to AWS IoT by using SDK funtions.
"""

import json
import time

from core.modem import Modem
from core.temp import debug
from core.utils.atcom import ATCom

###########################
### AWS HTTP(s) example ###
###########################

modem = Modem()
atcom = ATCom()

PAYLOAD_JSON = {"state": {"reported": {"Status": "Hello from Picocell --> HTTP"}}}
payload = json.dumps(PAYLOAD_JSON)

# Check communication with modem
debug.info("COM: ", modem.base.check_communication())
debug.info("Set APN: ", atcom.send_at_comm('AT+CGDCONT=1,"IP","super"',"OK"))
debug.info("COPS: ", atcom.retry_at_comm("AT+COPS?","+COPS: 0,0", timeout=1, retry_count=10))
debug.info(atcom.send_at_comm('AT+QICSGP=1,1,"super","","",1',"OK"))

# TCP/IP
debug.info("TCPIP Context Configuration: ", modem.http.set_context_id())
debug.info("PDP Deactivation: ", modem.network.deactivate_pdp_context())
debug.info("PDP Activatation: ", modem.network.activate_pdp_context())
debug.info("PDP Test: ", atcom.send_at_comm("AT+CGACT?","OK"))

# Configurations
# SSL
debug.info("Modem SSL CA: ", modem.ssl.set_ca_cert())
debug.info("Modem SSL Client Cert: ", modem.ssl.set_client_cert())
debug.info("Modem SSL Client Key: ", modem.ssl.set_client_key())
debug.info("Set Modem Security Level: ", modem.ssl.set_sec_level())
debug.info("Set modem SSL Version: ", modem.ssl.set_version())
debug.info("Set modem SSL Cipher: ", modem.ssl.set_cipher_suite())
debug.info("Set modem ignore local time: ", modem.ssl.set_ignore_local_time())

# HTTP
debug.info("Set HTTP SSL Context", modem.http.set_context_id(2))
debug.info("HTTP URL: ", modem.http.set_server_url())
debug.info("HTTP POST: ", modem.http.post(payload))
time.sleep(2)
debug.info("HTTP READ: ", modem.http.read_response())
