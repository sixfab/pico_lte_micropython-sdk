"""
Example code for publising data to AWS IoT by using manager class
"""
import time
import json
from core.modem import Modem
from core.auth import Auth

config = {}

modem = Modem()
auth = Auth(config)

auth.load_certificates()

HOST = "a2q4ztq1aigmmt-ats.iot.us-west-2.amazonaws.com"
PORT = 8883
TOPIC = "$aws/things/picocell_test/shadow/update"
PAYLOAD_JSON = {"state": {"reported": {"Status": "Test message from Picocell!"}}}
payload = json.dumps(PAYLOAD_JSON)

while True:
    print(modem.publish_message_to_aws(host=HOST, port=PORT, topic=TOPIC, payload=payload))
    print()
    print("CACHE:", modem.cache.states)
    print("\n\n")
    time.sleep(10)
