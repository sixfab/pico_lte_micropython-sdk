"""
Example code for publising data to GCloud IoT by using HTTP and GCloud app.
"""
import time
from core.modem import Modem
from core.temp import debug

modem = Modem()

while True:
    PAYLOAD = "Picocell Google Cloud IoT Example using HTTP"
    result = modem.gcloud.post_message(PAYLOAD)

    debug.info(result)
    time.sleep(10)
