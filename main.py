import json

from machine import UART, Pin
from core.modem import Modem
from core.auth import Auth
from core.atcom import ATCom

config = {}

###################
### AWS example ###
###################

modem = Modem()
auth = Auth(config)
atcom = ATCom()

auth.load_certificas()

host = "a2q4ztq1aigmmt-ats.iot.us-west-2.amazonaws.com"
port = 8883
topic = "$aws/things/picocell_test/shadow/update"
payload_json = {"state": {"reported": {"Status": "Hello Dude!"}}}
payload = json.dumps(payload_json)

# Check communication with modem
modem.publish_message_to_aws(host, port, topic, payload)