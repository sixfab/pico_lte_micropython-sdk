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

HOST = "[CHANGE WITH YOUR AWS IOT ENDPOINT]"
TOPIC = "[CHANGE WITH YOUR AWS IOT TOPIC]"
PAYLOAD_JSON = {"state": {"reported": {"Status": "Test message from Picocell!"}}}
server_url = 'https://' + HOST + ':8443/topics/' + TOPIC + '?qos=1'
payload = json.dumps(PAYLOAD_JSON)

print(modem.publish_message_to_aws_https(payload, server_url))
