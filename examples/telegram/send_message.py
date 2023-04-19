"""
Example code for sending message to group chat in Telegram with using its Bot API.

Example Configuration
---------------------
Create a config.json file in the root directory of the picocell device.
config.json file must include the following parameters for this example:

config.json
{
    "telegram": {
        "token": "[YOUR_BOT_TOKEN_ID]",
        "chat_id": "[YOUR_GROUP_CHAT_ID]"
    }
}
"""

from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

debug.info("Sending message to Telegram channel...")
result = picoLTE.telegram.send_message("Picocell Telegram Example")
debug.info("Result:", result)
