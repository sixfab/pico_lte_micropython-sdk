"""
Example code for publishing data to AWS IoT by using SDK functions.
"""

import json

from core.modem import Modem
from core.temp import debug
from core.utils.atcom import ATCom

###################
### AWS example ###
###################

modem = Modem()
atcom = ATCom()

PAYLOAD_JSON = {"state": {"reported": {"Status": "Hello from Picocell --> MQTT"}}}
payload = json.dumps(PAYLOAD_JSON)

# Check communication with modem
debug.info("COM: ", modem.base.check_communication())
debug.info("Set APN: ", atcom.send_at_comm('AT+CGDCONT=1,"IP","super"',"OK"))
debug.info("COPS: ", atcom.retry_at_comm("AT+COPS?","+COPS: 0,0", timeout=1, retry_count=10))

# TCP/IP
debug.info("TCPIP Context Configuration: ", modem.network.configure_tcp_ip_context())
debug.info("PDP Deactivation: ", modem.network.deactivate_pdp_context())
debug.info("PDP Activatation: ", modem.network.activate_pdp_context())
debug.info("PDP Test: ", atcom.send_at_comm("AT+CGACT?","OK"))

# Configurations
# SSL
debug.info("Modem SSL CA: ", modem.ssl.set_ca_cert())
debug.info("Modem SSL Client Cert: ", modem.ssl.set_client_cert())
debug.info("Modem SSL Client Key: ", modem.ssl.set_client_key())
debug.info("Set Modem Security Level: ", modem.ssl.set_sec_level())
debug.info("Set modem SSL Version: ", modem.ssl.set_version())
debug.info("Set modem SSL Cipher: ", modem.ssl.set_cipher_suite())
debug.info("Set modem ignore local time: ", modem.ssl.set_ignore_local_time())

# MQTT
debug.info("Modem MQTT version: ", modem.mqtt.set_version_config())
debug.info("Modem MQTT SSL Mode: ", modem.mqtt.set_ssl_mode_config())

debug.info("Open MQTT Connection: ", modem.mqtt.open_connection())
debug.info("Connect MQTT Broker: ", modem.mqtt.connect_broker())
debug.info("Publish MQTT Message: ", modem.mqtt.publish_message(payload))
debug.info("Close MQTT Connection: ", modem.mqtt.close_connection())
