"""
Example code for publising data to AWS IoT by using manager class
"""
import time
import json
from core.modem import Modem
from core.temp import debug

modem = Modem()
debug.set_debug_level(0)

while True:
    PAYLOAD_JSON = {"state": {"reported": {"App": "AWS MQTT Example", "Timestamp": str(time.time())}}}
    payload = json.dumps(PAYLOAD_JSON)
    result = modem.aws.publish_message(payload)
    debug.info(result)
    time.sleep(10)
