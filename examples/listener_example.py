import json
import time
from core.atcom import ATCom
from core.listener import Listener
from machine import UART, Pin
from core.modem import Modem
from core.auth import Auth
config = {}

atcom = ATCom()
modem = Modem()
auth = Auth(config)

auth.load_certificas()

host = "a2q4ztq1aigmmt-ats.iot.us-west-2.amazonaws.com"
port = 8883
topic = "$aws/things/picocell_test/shadow/update"
payload_json = {"state": {"reported": {"Status": "Test message from Picocell!"}}}
payload = json.dumps(payload_json)

# print(modem.publish_message_to_aws(host=host, port=port, topic=topic, payload=payload))
def mqtt_callback(message):
    print("MQTT callback", message)

def callback(message):
    print("Callback:", message)
    
listener = Listener(atcom)
listener.add_defined_response("+QMTRECV:", mqtt_callback)
listener.add_defined_response("APP RDY", callback)
listener.add_defined_response("RDY", callback)

atcom.send_at_comm("AT+CFUN=1,1", "OK")

while True:
    listener.run_once()
    time.sleep(0.1)
