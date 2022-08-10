"""
Example code for sending message to a Slack channel by using SDK funtions.
"""
import json
import time

from core.modem import Modem
from core.atcom import ATCom

config = {}

###########################
## Slack HTTP(s) example ##
###########################

modem = Modem(config)
atcom = ATCom()

SERVICE_URL = "https://hooks.slack.com/services/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 "
CUSTOM_HEADER = 'Content-type: application/json\n'
DATA = {
  "text": "Test Message"
}

payload = json.dumps(DATA)

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

# HTTP
print("HTTP URL: ", modem.set_modem_http_server_url(url=SERVICE_URL))
atcom.send_at_comm('AT+QHTTPCFG="requestheader",1')
#print("HTTP Header:", modem.set_modem_http_content_type(content_type=4))
print("HTTP POST: ", modem.http_post_request(data = CUSTOM_HEADER + payload))

time.sleep(5)
print("HTTP READ: ", modem.http_read_response())