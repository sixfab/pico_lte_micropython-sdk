import json
from machine import UART, Pin
from core.modem import Modem
from core.auth import Auth
config = {}

modem = Modem()
auth = Auth(config)

auth.load_certificas()

host = "a2q4ztq1aigmmt-ats.iot.us-west-2.amazonaws.com"
port = 8883
topic = "$aws/things/picocell_test/shadow/update"
payload_json = {"state": {"reported": {"Status": "Test message from Picocell!"}}}
payload = json.dumps(payload_json)

print(modem.publish_message_to_aws(host=host, port=port, topic=topic, payload=payload))
