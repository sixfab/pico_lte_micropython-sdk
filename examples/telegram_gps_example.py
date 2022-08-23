import json
import time

from core.modem import Modem
from core.temp import debug
from core.utils.status import Status
from core.utils.atcom import ATCom

modem = Modem()
atcom = ATCom()

# Telegram Bot configurations
BOT_TOKEN = '5469433192:AAH3L7t2RPrqHsY1r9rvXO_DU67Z5NdtMMw'
BOT_CHAT_ID = '-645292239'
HOST = "api.telegram.org/bot"
PERIOD = 30 # seconds

def send_message_to_telegram(message):
    publish_url = f'https://{HOST}{BOT_TOKEN}/sendMessage?chat_id={BOT_CHAT_ID}&text={message}'

    # Check communication with modem
    print("COM: ", modem.base.check_communication())
    print("Set APN: ", atcom.send_at_comm('AT+CGDCONT=1,"IP","super"',"OK"))
    print("COPS: ", atcom.retry_at_comm("AT+COPS?","+COPS: 0,0", timeout=1, retry_count=10))
    print(atcom.send_at_comm('AT+QICSGP=1,1,"super","","",1',"OK"))

    # TCP/IP
    print("TCPIP Context Configuration: ", modem.http.set_context_id())
    print("PDP Deactivation: ", modem.network.deactivate_pdp_context())
    print("PDP Activatation: ", modem.network.activate_pdp_context())
    print("PDP Test: ", atcom.send_at_comm("AT+CGACT?","OK"))

    # HTTP
    print("Set HTTP SSL Context", modem.http.set_ssl_context_id(2))
    print("HTTP URL: ", modem.http.set_server_url(url=publish_url))
    time.sleep(6)
    print("HTTP GET: ", modem.http.get())


##############################
### GPS - Telegram example ###
##############################

fix = False
loc_message = None

modem = Modem()
debug.set_debug_channel(0)
debug.set_debug_level(0)

debug.info("GPS Example")
modem.peripherals.adjust_neopixel(255,0,0)

while True:
    # First go to GNSS prior mode and turn on GPS.
    debug.info(modem.gps.set_priority(0))
    time.sleep(3)
    debug.info(modem.gps.turn_on())

    for _ in range(0, 45):
        result = modem.gps.get_location()
        debug.debug(result)
        if result["status"] == Status.SUCCESS:
            debug.debug("GPS Fixed. Getting location data...")
            loc = result["response"]
            prefix_id = loc.find("+QGPSLOC: ")
            len_prefix = len("+QGPSLOC: ")
            loc = loc[prefix_id + len_prefix:].replace('"\n\r',"").split(",")
            loc_message = f'{loc[1]},{loc[2]}'
            fix = True
            break
        time.sleep(2) # 45*2 = 90 seconds timeout for GPS fix.

    if fix:
        # Go to WWAN prior mode and turn on GPS.
        debug.info(modem.gps.set_priority(1))
        debug.info(modem.gps.turn_off())

        # Send the location data to the server.
        send_message_to_telegram(loc_message)

        if result["status"] == Status.SUCCESS:
            fix = False

    time.sleep(PERIOD) # [PERIOD] seconds between each request.
