"""
Example code for publishing data to AWS IoT by using SDK funtions.
"""

import json

from core.modem import Modem
from core.atcom import ATCom

config = {}

###################
### AWS example ###
###################

modem = Modem(config)
atcom = ATCom()

HOST = "a2q4ztq1aigmmt-ats.iot.us-west-2.amazonaws.com"
PORT = 8883
TOPIC = "$aws/things/picocell_test/shadow/update"
PAYLOAD_JSON = {"state": {"reported": {"Status": "Hello from Picocell!"}}}
payload = json.dumps(PAYLOAD_JSON)

# Check communication with modem
print("COM: ", modem.check_modem_communication())
print("Set APN: ", atcom.send_at_comm('AT+CGDCONT=1,"IP","super"',"OK"))
print("COPS: ", atcom.retry_at_comm("AT+COPS?","+COPS: 0,0", timeout=1, retry_count=10))

# TCP/IP
print("TCPIP Context Configuration: ", modem.configure_tcp_ip_context())
print("PDP Deactivation: ", modem.deactivate_pdp_context())
print("PDP Activatation: ", modem.activate_pdp_context())
print("PDP Test: ", atcom.send_at_comm("AT+CGACT?","OK"))

# Configurations
# SSL
print("Modem SSL CA: ", modem.set_modem_ssl_ca_cert())
print("Modem SSL Client Cert: ", modem.set_modem_ssl_client_cert())
print("Modem SSL Client Key: ", modem.set_modem_ssl_client_key())
print("Set Modem Security Level: ", modem.set_modem_ssl_sec_level())
print("Set modem SSL Version: ", modem.set_modem_ssl_version())
print("Set modem SSL Cipher: ", modem.set_modem_ssl_cipher_suite())
print("Set modem ignore local time: ", modem.set_modem_ssl_ignore_local_time())

# MQTT
print("Modem MQTT version: ", modem.set_modem_mqtt_version_config())
print("Modem MQTT SSL Mode: ", modem.set_modem_mqtt_ssl_mode_config())

print("Open MQTT Connection: ", modem.open_mqtt_connection(host=HOST, port=PORT))
print("Connect MQTT Broker: ", modem.connect_mqtt_broker())
print("Publish MQTT Message: ", modem.publish_mqtt_message(topic=TOPIC, payload=payload))
print("Close MQTT Connection: ", modem.close_mqtt_connection())
