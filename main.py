import json

from machine import UART, Pin
from core.modem import Modem
from core.auth import Auth
from core.atcom import ATCom

config = {}

###################
### AWS example ###
###################

modem = Modem()
auth = Auth(config)
atcom = ATCom()
auth.load_certificas()

host = "a2q4ztq1aigmmt-ats.iot.us-west-2.amazonaws.com"
port = 8883
topic = "$aws/things/picocell_test/shadow/update"
payload_json = {"state": {"reported": {"Status": "Hello from Picocell!"}}}
payload = json.dumps(payload_json)

# Check communication with modem
print("COM: ", modem.check_modem_communication())
print("Set APN: ", atcom.send_at_comm('AT+CGDCONT=1,"IP","super"',"OK"))
print("Network Registration: ", modem.check_network_registeration())
print("Operator Information: ", modem.get_operator_information())
print("MQTT Rec. Messages: ", modem.check_any_mqtt_messages())
print("Read MQTT Rec. Messages: ", modem.read_mqtt_messages())