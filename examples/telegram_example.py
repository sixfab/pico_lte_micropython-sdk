"""
Example code for sending message to Telegram via Bot by using SDK functions.
"""

import json
import time

from core.modem import Modem
from core.atcom import ATCom

config = {}

############################
### Telegram API example ###
############################

modem = Modem(config)
atcom = ATCom()

# Write your text message here!
user_text = 'Your text message here!'

# Telegram Bot configurations 
bot_token = 'YOUT_BOT_TOKEN'
bot_chatID = 'YOUR_BOT_CHAT_ID'

HOST = "api.telegram.org/bot"
PAYLOAD_JSON = {""}
payload = json.dumps(PAYLOAD_JSON)

publish_url = 'https://' + HOST + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&text=' + user_text

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
print("Set HTTP SSL Context", modem.set_modem_http_ssl_context_id(2))
print("HTTP URL: ", modem.set_modem_http_server_url(url=publish_url))
time.sleep(6)
print("HTTP GET: ", modem.http_get_request())
time.sleep(6)
print("HTTP READ: ", modem.http_read_response())

