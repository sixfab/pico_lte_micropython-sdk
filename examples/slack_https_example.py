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

SERVER_DETAILS = {
    'HOST': 'https://hooks.slack.com',
    'QUERY': '/services/T03TQ6CSL1F/B03TMH5TZ51/s82yfH54cnxYo7sS3LQ4Dl57'
}

DATA = {
  'text': 'Message from PicoCell!'
}

data_post_json = json.dumps(DATA)

header =    "POST " + SERVER_DETAILS["QUERY"] + " HTTP/1.1\n" + \
            "Host: " + SERVER_DETAILS["HOST"][8:] + "\n" + \
            "Custom-Header-Name: Custom-Data\n" + \
            "Content-Type: application/json\n" + \
            "Content-Length: " + str(len(data_post_json) + 1) + "\n" + \
            "\n\n"

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
print("HTTP URL: ", modem.set_modem_http_server_url(url = SERVER_DETAILS["HOST"]))
atcom.send_at_comm('AT+QHTTPCFG="requestheader",1')
print("HTTP POST: ", modem.http_post_request(data = header + data_post_json))

time.sleep(5)
print("HTTP READ: ", modem.http_read_response())