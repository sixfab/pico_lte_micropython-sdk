import json
import time

from core.modem import Modem
from core.temp import debug, config
from core.utils.status import Status


####################
### GPS  example ###
####################
HOST = "https://webhook.site/76bc93f9-d703-4531-af50-076ae46c0f0a"

def handle_cellular_network_connection():
    """This function handles the connection to cellular network connection.
    """
    # Ask for return from the modem.
    modem.base.check_communication()
    # Send APN details.
    modem.network.set_apn(cid=1, apn="super")
    # Try to get a operator response for 100 times.
    for _ in range(0, 100):
        # Check if there is a connection to any operator.
        response = modem.network.get_operator_information()
        if response["status"] == Status.SUCCESS:
            return
        # Wait for 1 second.
        time.sleep(1)

def prepare_http_connection():
    """This function prepares HTTP connection for modem.
    """
    # Set the first HTTP context.
    modem.http.set_context_id()
    # Activate PDP.
    modem.network.activate_pdp_context()

def prepare_http_with_query(host_url, query_string=""):
    """Sets the modem's HTTP server address.

    Args:
        host_url (str): Server address to send request.
        query_string (str, optional): Query payload for the server. Defaults to "".
    """
    # Add query to the server URL.
    url_to_post = host_url + "/?" + query_string
    # Set the HTTP url.
    modem.http.set_server_url(url=url_to_post)

def send_post_request(server_url, data_dict, query_string=""):
    """POST request to the HTTP server with a payload and optional query.

    Args:
        server_url (str): Server address to send request.
        data_dict (dict): The data for the request as dictionary.
        query_string (str, optional): Query payload for the server. Defaults to "".
    """
    # Configure the HTTP address.
    prepare_http_with_query(server_url, query_string)
    # Convert to data to JSON.
    data_to_post = json.dumps(data_dict)
    # Send a post request to the URL.
    res = modem.http.post(data=data_to_post)
    print("POST Request: ", res)
    # Wait for six seconds before the next operation.
    return res

fix = False
location_sentence = None

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
            loc = loc[prefix_id:].replace('"\n\r',"").split(",")
            loc_dic = {}
            loc_dic["utc"] = loc[0]
            loc_dic["lat"] = loc[1]
            loc_dic["lon"] = loc[2]
            loc_dic["hdop"] = loc[3]
            loc_dic["alt"] = loc[4]
            loc_dic["fix"] = loc[5]
            loc_dic["cog"] = loc[6]
            loc_dic["spd"] = loc[7]
            loc_dic["date"] = loc[9]

            location_sentence = json.dumps(loc_dic)
            fix = True
            break
        time.sleep(2) # 45*2 = 90 seconds timeout for GPS fix.

    if fix:
        # Go to WWAN prior mode and turn on GPS.
        debug.info(modem.gps.set_priority(1))
        debug.info(modem.gps.turn_off())

        # Send the location data to the server.
        handle_cellular_network_connection()
        prepare_http_connection()
        result = send_post_request(HOST, location_sentence, "device=Pico&try=0")

        if result["status"] == Status.SUCCESS:
            fix = False

    time.sleep(30) # 30 seconds between each request.
