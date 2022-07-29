"""
Example code for publising data to AWS IoT by using manager class
"""

import time
import json
from core.modem import Modem
from core.utils.atcom import ATCom

config = {}
modem = Modem(config)
atcom=ATCom()

HOST = "a2q4ztq1aigmmt-ats.iot.us-west-2.amazonaws.com"
TOPIC = "$aws/things/picocell_test/shadow/update"
PAYLOAD_JSON = {"state": {"reported": {"Status": "Test message from Picocell!"}}}
server_url = 'https://' + HOST + ':8443/topics/' + TOPIC + '?qos=1'
payload = json.dumps(PAYLOAD_JSON)

print(modem.aws.post_message(payload, server_url))
