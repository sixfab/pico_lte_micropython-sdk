"""
Example code for sending message to group chat in Telegram with using its Bot API.
"""

import time
from core.modem import Modem
from core.temp import debug

modem = Modem()

while True:
    result = modem.telegram.send_message("This_is_an_example!")
    debug.info(result)

    time.sleep(10)
