"""
Example code for publishing data to AWS IoT by using SDK funtions.
"""

import json
import time

from core.modem import Modem
from core.atcom import ATCom

config = {}

###########################
### AWS HTTP(s) example ###
###########################

modem = Modem(config)
atcom = ATCom()

HOST = "a2q4ztq1aigmmt-ats.iot.us-west-2.amazonaws.com"
TOPIC = "$aws/things/picocell_test/shadow/update"
PAYLOAD_JSON = {"state": {"reported": {"Status": "HTTPS TEST MESSAGE!"}}}
payload = json.dumps(PAYLOAD_JSON)
publish_url = 'https://' + HOST + ':8443/topics/' + TOPIC + '?qos=1'

# Check communication with modem
print("COM: ", modem.check_modem_communication())
print("Set APN: ", atcom.send_at_comm('AT+CGDCONT=1,"IP","super"',"OK"))
print("COPS: ", atcom.retry_at_comm("AT+COPS?","+COPS: 0,0", timeout=1, retry_count=10))
print(atcom.send_at_comm('AT+QICSGP=1,1,"super","","",1',"OK"))

# TCP/IP
print("TCPIP Context Configuration: ", modem.set_modem_http_context_id())
print("PDP Deactivation: ", modem.deactivate_pdp_context())
print("PDP Activatation: ", modem.activate_pdp_context())
print("PDP Test: ", atcom.send_at_comm("AT+CGACT?","OK"))

# Configurations
# SSL
print("Modem SSL CA: ", modem.set_modem_ssl_ca_cert())
print("Modem SSL Client Cert: ", modem.set_modem_ssl_client_cert())
print("Modem SSL Client Key: ", modem.set_modem_ssl_client_key())
print("Set Modem Security Level: ", modem.set_modem_ssl_sec_level())
print("Set modem SSL Version: ", modem.set_modem_ssl_version())
print("Set modem SSL Cipher: ", modem.set_modem_ssl_cipher_suite())
print("Set modem ignore local time: ", modem.set_modem_ssl_ignore_local_time())

# HTTP
print("Set HTTP SSL Context", modem.set_modem_http_ssl_context_id(2))
print("HTTP URL: ", modem.set_modem_http_server_url(url=publish_url))
print("HTTP POST: ", modem.http_post_request(data=payload))
time.sleep(2)
print("HTTP READ: ", modem.http_read_response())
