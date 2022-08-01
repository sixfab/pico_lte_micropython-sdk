"""
Example code for publising data to AWS IoT by using manager class
"""

import time
import json
from core.modem import Modem

modem = Modem()

while True:
    PAYLOAD_JSON = {"state": {"reported": {"App": "AWS HTTP Example", "Timestamp": str(time.time())}}}
    payload = json.dumps(PAYLOAD_JSON)
    result = modem.aws.post_message(payload)

    print(result)
    time.sleep(10)