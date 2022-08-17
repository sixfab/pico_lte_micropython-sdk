"""
Example code for publishing and receiving data to Google IoT Cloud via MQTT.
"""

import time
from core.modem import Modem
from core.utils.debug import Debug
from core.utils.status import Status


# Complete this informations to connect to your Google Cloud services.
GCloudAccount = {
    'region': '[REGION_IN_GCLOUD]',
    'project_id': '[PROJECT_ID_IN_GCLOUD]',
    'registry_id': '[REGISTRY_ID_OF_DEVICE]',
    'device_id': '[DEVICE_ID]',
    'jwt': '[JSON_WEB_TOKEN]'
}

# Put a message here to send it to the topic.
DATA_TO_PUBLISH = "This message is an example from Picocell SDK that is send with MQTT."


if __name__ == "__main__":
    # This server details does not need to be changed.
    GCloudServer = {
        'HOST': 'mqtt.googleapis.com',
        'PORT': 8883,
        'CLIENT_ID': 'projects/' + GCloudAccount['project_id'] +\
                        '/locations/' + GCloudAccount['region'] +\
                        '/registries/' + GCloudAccount['registry_id'] +\
                        '/devices/' + GCloudAccount['device_id'],
        'TELEMETRY_TOPIC': '/devices/' + GCloudAccount['device_id'] + '/events',
        'COMMANDS_TOPIC': '/devices/' + GCloudAccount['device_id'] + '/commands/#'
    }

    # Initilize both Modem and Debug.
    debug = Debug()
    modem = Modem()

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

    # Activate MQTT SSL.
    debug.info("Modem MQTT version: ", modem.mqtt.set_version_config())
    debug.info("Activate SSL/TCP for MQTT: ", modem.mqtt.set_ssl_mode_config())

    # Open MQTT for the Google Cloud MQTT server.
    debug.info("Open MQTT Connection: ", modem.mqtt.open_connection(host=GCloudServer['HOST'],
                                                                   port=GCloudServer['PORT']))

    # Connect with given client ID and JWT password.
    debug.info("Connect MQTT Broker: ", modem.mqtt.connect_broker(client_id_string=GCloudServer['CLIENT_ID'],
                                                                  username="unused",
                                                                  password=GCloudAccount['jwt']))

    # Publish a message.
    debug.info("Publish MQTT Message: ", modem.mqtt.publish_message(topic=GCloudServer['TELEMETRY_TOPIC'],
                                                                    payload=DATA_TO_PUBLISH))

    # Subscribe to the commands topic.
    topics = [(GCloudServer['COMMANDS_TOPIC'], 1)]
    debug.info("Subscribe to Commands Topic: ", modem.mqtt.subscribe_topics(topics))

    # Save the waiting started time into a variable to check timeout.
    TIMEOUT_SEC = 25

    first_time = time.time()
    while time.time() - first_time < TIMEOUT_SEC:
        # Check if there are any messages.
        message_list = modem.mqtt.read_messages()
        if len(message_list) != 0:
            # Print all the messages.
            for message in message_list["messages"]:
                debug.info("Command Recieved: ", message[2])


    # Close the MQTT connection.
    debug.info("Close MQTT Connection: ", modem.mqtt.close_connection())
