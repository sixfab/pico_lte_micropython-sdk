"""
Example code for sending latitude longitude data which are received from GPS
to the telegram channel. The data is sent to the telegram channel using HTTP
POST method.

Example Configuration
---------------------
Create a config.json file in the root directory of the picocell device.
config.json file must include the following parameters for this example:

config.json
{
    "telegram":{
        "token": "your_telegram_token"
        "chat_id": "your_telegram_chat_id"
    }
}
"""

import time

from core.modem import Modem
from core.temp import debug
from core.utils.status import Status

PERIOD = 30  # seconds
fix = False

modem = Modem()

debug.info("GPS Example")

while True:
    # First go to GNSS prior mode and turn on GPS.
    modem.gps.set_priority(0)
    time.sleep(3)
    modem.gps.turn_on()
    debug.info("Trying to fix GPS...")

    for _ in range(0, 45):
        result = modem.gps.get_location()
        debug.info(result)

        if result["status"] == Status.SUCCESS:
            debug.info("GPS Fixed. Getting location data...")

            loc = result.get("value")
            debug.info("Lat-Lon:", loc)
            loc_message = ",".join(word for word in loc)

            fix = True
            break
        time.sleep(2)  # 45*2 = 90 seconds timeout for GPS fix.

    if fix:
        # Go to WWAN prior mode and turn on GPS.
        modem.gps.set_priority(1)
        modem.gps.turn_off()

        debug.info("Sending message to telegram channel...")
        result = modem.telegram.send_message(loc_message)
        debug.info(result)

        if result["status"] == Status.SUCCESS:
            debug.info("Message sent successfully.")
            fix = False

    time.sleep(PERIOD)  # [PERIOD] seconds between each request.
