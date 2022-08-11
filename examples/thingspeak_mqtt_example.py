import time
from core.modem import Modem
from core.utils.debug import Debug
from core.utils.status import Status


# MQTT Server
HOST = "mqtt3.thingspeak.com"
PORT = 1883

# MQTT User Details
CHANNEL_ID = 0 # [YOUR CHANNEL ID]
USERNAME = "[YOUR USERNAME]"
CLIENT_ID = "[CLIENT ID]"
PASSWORD = "[YOUR PASSWORD]"

# Create the topic address for publishing and subscribing.
TOPIC_ADDR_PUBLISH = "channels/" + str(CHANNEL_ID) + "/publish"
SUBSCRIPTION_ADDR = "channels/" + str(CHANNEL_ID) + "/subscribe/fields/field2"

# Construct a modem and debug instance.
modem = Modem()
debug = Debug()

# Send APN details.
modem.network.set_apn()

# Check the network registration.
result = modem.network.check_network_registration()
if result["status"] != Status.SUCCESS:
    debug.error("Could not connected to the cellular network.")

# Cellular Network Configuration
debug.info("TCPIP Context Configuration: ", modem.network.configure_tcp_ip_context())
debug.info("PDP Deactivation: ", modem.network.deactivate_pdp_context())
debug.info("PDP Activatation: ", modem.network.activate_pdp_context())

# Enable and connect to the MQTT.
debug.info("Open MQTT Connection: ", modem.mqtt.open_connection(host=HOST, port=PORT))
debug.info("Connect MQTT Broker: ", modem.mqtt.connect_broker(client_id_string=CLIENT_ID, \
                                                                username=USERNAME, \
                                                                password=PASSWORD))

# Publish a message to the broker.
debug.info("Publish MQTT Message: ", modem.mqtt.publish_message(topic=TOPIC_ADDR_PUBLISH, \
                                                                payload="field1=15&field2=35&status=MQTT_PICOCELL_PUBLISH"))

# Subscribe to a topic/field.
topics = [(SUBSCRIPTION_ADDR, 0)]
debug.info("Subscribe to field1: ", modem.mqtt.subscribe_topics(topics))

# Save the waiting started time into a variable to check timeout.
TIMEOUT_SEC = 25

first_time = time.time()
while time.time() - first_time < TIMEOUT_SEC:
    # Check if there are any messages.
    message_list = modem.mqtt.read_messages()
    if len(message_list) != 0:
        # Print all the messages.
        for message in message_list["messages"]:
            debug.info(f'{message[2]} recieved from {message[1]}.')

# Unsubscribe from the topic.
debug.info("Unsubscribe to Field1: ", modem.mqtt.unsubscribe_topic(SUBSCRIPTION_ADDR))

# Close the MQTT connection.
debug.info("Close MQTT Connection: ", modem.mqtt.close_connection())
