"""
Example code for subsscribing topics for GCloud IoT by using MQTT and GCloud app.
"""
import time
from core.modem import Modem
from core.temp import debug
from core.utils.status import Status

modem = Modem()

while True:
    result = modem.gcloud.subscribe_topics()

    if result.get("status") == Status.SUCCESS:
    # Check is there any data in subscribed topics
    # in each 5 seconds for 5 times
        for _ in range(0, 5):
            result = modem.aws.read_messages()
            debug.info(result.get("messages"))
            time.sleep(5)
