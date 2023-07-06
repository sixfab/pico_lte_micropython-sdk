"""
Example code for publishing location data which are received from GPS to the
any test server. The data is sent to the server using HTTP POST method. webhook.site
test server is used for this example.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "https":{
        "server": "[YOUR_SERVER_URL]",
        "username": "[YOUR_USERNAME]",
        "password": "[YOUR_PASSWORD]"
    }
}
"""

import time

from pico_lte.core import PicoLTE
from pico_lte.common import debug
from pico_lte.utils.status import Status


fix = False
picoLTE = PicoLTE()

debug.info("GPS Example")
picoLTE.peripherals.adjust_neopixel(255, 0, 0)

while True:
    # First go to GNSS prior mode and turn on GPS.
    picoLTE.gps.set_priority(0)
    time.sleep(3)
    picoLTE.gps.turn_on()
    debug.info("Trying to fix GPS...")

    for _ in range(0, 45):
        result = picoLTE.gps.get_location()
        debug.info(result)

        if result["status"] == Status.SUCCESS:
            debug.debug("GPS Fixed. Getting location data...")

            loc = result.get("value")
            debug.info("Lat-Lon:", loc)
            loc_message = ",".join(word for word in loc)

            fix = True
            break
        time.sleep(2)  # 45*2 = 90 seconds timeout for GPS fix.

    if fix:
        # Go to WWAN prior mode and turn on GPS.
        picoLTE.gps.set_priority(1)
        picoLTE.gps.turn_off()

        debug.info("Sending message to the server...")
        picoLTE.network.register_network()
        picoLTE.http.set_context_id()
        picoLTE.network.get_pdp_ready()
        picoLTE.http.set_server_url()

        result = picoLTE.http.post(data=loc_message)
        debug.info(result)

        if result["status"] == Status.SUCCESS:
            debug.info("Message sent successfully.")
            fix = False

    time.sleep(30)  # 30 seconds between each request.
