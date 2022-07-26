"""
Example code for publising data to AWS IoT by using manager class
"""
import time
import json
from core.modem import Modem

config = {}
modem = Modem(config)

HOST = "[CHANGE WITH YOUR AWS IOT ENDPOINT]"
TOPIC = "[CHANGE WITH YOUR AWS IOT TOPIC]"
PORT = 8883
PAYLOAD_JSON = {"state": {"reported": {"Status": "Test message from Picocell!"}}}
payload = json.dumps(PAYLOAD_JSON)

while True:
    print(modem.publish_message_to_aws(host=HOST, port=PORT, topic=TOPIC, payload=payload))
    print()
    print("CACHE:", modem.cache.states)
    print("\n\n")
    time.sleep(10)
