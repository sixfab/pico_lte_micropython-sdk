"""
Example code for publising data to AWS IoT by using manager class
"""

import time
import json
from core.modem import Modem
from core.atcom import ATCom

config = {}
modem = Modem(config)
atcom=ATCom()

HOST = "a2q4ztq1aigmmt-ats.iot.us-west-2.amazonaws.com"
PORT = 8883
TOPIC = "$aws/things/picocell_test/shadow/update"
PAYLOAD_JSON = {"state": {"reported": {"Status": "Test message from Picocell!"}}}
payload = json.dumps(PAYLOAD_JSON)

print(modem.set_modem_http_context_id(1))
time.sleep(1)
print(atcom.send_at_comm('AT+QHTTPCFG="contextid"',"OK"))
