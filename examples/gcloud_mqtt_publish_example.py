"""
Example code for publising data to GCloud IoT by using MQTT and GCloud app.
"""
import time
from core.modem import Modem
from core.temp import debug

modem = Modem()

while True:
    result = modem.gcloud.publish_message("Picocell Google Cloud IoT Example using MQTT")

    debug.info(result)
    time.sleep(10)
