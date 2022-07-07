"""
Main code file.
"""

import json
from core.auth import Auth
from core.modem import Modem

config = {}
auth = Auth(config)

auth.load_certificates()

HOST = "a2q4ztq1aigmmt-ats.iot.us-west-2.amazonaws.com"
PORT = 8883
TOPIC = "$aws/things/picocell_test/shadow/update"
PAYLOAD_JSON = {"state": {"reported": {"Status": "Test message from Picocell!"}}}
payload = json.dumps(PAYLOAD_JSON)


modem = Modem()

if __name__ == "__main__":
    print("Starting...")

