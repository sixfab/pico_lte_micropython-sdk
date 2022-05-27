from machine import UART, Pin
import time
from core.modem import Modem
from core.auth import Auth

config = {}

modem = Modem()
auth = Auth(config)
auth.load_certificas()

print(modem.check_modem_communication())

print("Delete CA: ", modem.delete_modem_ca_cert())
print("Delete Client Cert: ", modem.delete_modem_client_cert())
print("Delete Client Key: ", modem.delete_modem_client_key())

print(modem.upload_modem_ca_cert(config["auth"]["cacert"]))
print(modem.upload_modem_client_cert(config["auth"]["client_cert"]))
print(modem.upload_modem_client_key(config["auth"]["client_key"]))



# pin = Pin(25, Pin.OUT)
# pin.value(1)
# time.sleep(1)
# pin.value(0)



 