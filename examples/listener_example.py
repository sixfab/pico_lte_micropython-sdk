"""
Example code for listener class
"""

import json
import time
from core.atcom import ATCom
from core.listener import Listener
from core.modem import Modem

config = {}
atcom = ATCom()
modem = Modem(config)

HOST = "a2q4ztq1aigmmt-ats.iot.us-west-2.amazonaws.com"
PORT = 8883
TOPIC = "$aws/things/picocell_test/shadow/update"
PAYLOAD_JSON = {"state": {"reported": {"Status": "Test message from Picocell!"}}}
payload = json.dumps(PAYLOAD_JSON)


def callback(message):
    """Example callback function"""
    print("Callback:", message)


listener = Listener(atcom)
listener.add_defined_response("+QMTRECV:", callback)
listener.add_defined_response("APP RDY", callback)
listener.add_defined_response("RDY")

atcom.send_at_comm("AT+CFUN=1,1", "OK")

while True:
    listener.run_once()
    time.sleep(0.1)
