from machine import UART, Pin
import time
from core.modem import Modem
from core.auth import Auth

config = {}

modem = Modem()
auth = Auth(config)
auth.load_certificas()


modem.send_at_comm("AT","OK")

len_ca = len(config["auth"]["cacert"])
len_client_cert = len(config["auth"]["client_cert"])
len_client_key = len(config["auth"]["client_key"])

print(len_ca, len_client_cert, len_client_key) 

# pin = Pin(25, Pin.OUT)
# pin.value(1)
# time.sleep(1)
# pin.value(0)



 