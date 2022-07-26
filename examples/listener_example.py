"""
Example code for listener class
"""

import json
import time
from core.utils.atcom import ATCom
from core.utils.listener import Listener
from core.modem import Modem

config = {}
atcom = ATCom()
modem = Modem(config)


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
