"""
Example code for send message to slack channel by using
incoming webhooks feature of Slack API.
"""

from core.modem import Modem
from core.temp import debug

modem = Modem()

MESSAGE = "Hi there. It is test message from Picocell!"
result = modem.slack.send_message(MESSAGE)
debug.info(result)
