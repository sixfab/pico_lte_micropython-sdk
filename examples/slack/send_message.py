"""
Example code for send message to slack channel by using
incoming webhooks feature of Slack API.

Example Configuration
---------------------
Create a config.json file in the root directory of the picocell device.
config.json file must include the following parameters for this example:

config.json
{
    "slack":{
        "webhook_url": "[INCOMING_WEBHOOK_URL]"
    }
}
"""

from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

debug.info("Sending message to slack channel...")
result = picoLTE.slack.send_message("It is test message from Picocell!")
debug.info("Result:", result)
