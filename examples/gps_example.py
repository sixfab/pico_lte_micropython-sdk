"""
Example code for publishing GPS data to a web-server by using HTTP protocol.
"""
import json
import time

from core.modem import Modem
from core.temp import debug
from core.utils.status import Status

HOST = "[YOUR_WEB_SERVER_ADRESS]"
IS_GPS_FIXED = False
LOCATION_TO_POST = None

modem = Modem()
modem.network.set_apn()
modem.network.check_network_registration()
modem.http.set_context_id()
modem.network.activate_pdp_context()
modem.http.set_server_url(url=HOST)

while True:
    # Go to GNSS prior mode and turn on GPS.
    debug.info("Set the GNSS prior mode: ", modem.gps.set_priority(0))
    time.sleep(3)
    debug.info("Turn on GPS: ", modem.gps.turn_on())

    # Try to fix GPS for 90 seconds.
    for _ in range(0, 45):
        result = modem.gps.get_location()
        if result["status"] == Status.SUCCESS:
            debug.info("GPS has been fixed. Getting location data...")
            location = result["response"]
            prefix_id = location.find("+QGPSLOC: ")
            location = location[prefix_id+10:].replace('"\n\r',"").split(",")
            location_dictionary = {
                "utc": location[0],
                "lat": location[1],
                "lon": location[2],
                "hdop": location[3],
                "alt": location[4],
                "fix": location[5],
                "cog": location[6],
                "spd": location[7],
                "date": location[9]
            }

            # Create the data to post, and set IS_GPS_FIXED.
            LOCATION_TO_POST = json.dumps(location_dictionary)
            IS_GPS_FIXED = True
            break

        # 45*2 = 90 seconds timeout for GPS fix.
        time.sleep(2)

    if IS_GPS_FIXED:
        # Go to WWAN prior mode and turn on GPS.
        debug.info("Set the WWAN prior mode: ", modem.gps.set_priority(1))
        debug.info("Turn off GPS: ", modem.gps.turn_off())

        # Send the location data to the server.
        modem.http.post(data=LOCATION_TO_POST)
        if result["status"] == Status.SUCCESS:
            debug.info(f"The GPS data sent to {HOST}: {LOCATION_TO_POST}")
            IS_GNSS_FIXED = False

    # 30 seconds between sending GPS data.
    time.sleep(30)
