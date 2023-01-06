"""
This module contains the Crux class which represents the functionality
of a Sixfab Crux board.
"""

from core.modules.ulp import ULP
from core.modules.peripherals import Periph
from core.modules.modem import Modem
from core.modules.wifi import WiFiConnection

from core.temp import config
from core.utils.helpers import read_json_file

from core.apps.aws import AWS
from core.apps.slack import Slack
from core.apps.telegram import Telegram
from core.apps.thingspeak import ThingSpeak
from core.apps.azure import Azure
from core.apps.scriptr import Scriptr


class Crux:
    """This class represents the functionality of a Sixfab Crux board."""

    def __init__(self):
        # Import configuration file.
        config["params"] = read_json_file("config.json")

        self.ulp = ULP()
        self.peripherals = Periph()
        self.modem = Modem()
        # TODO: Will be implemented in the future.
        self.wifi = WiFiConnection()

        self.aws = AWS(self.modem, self.wifi)
        self.telegram = Telegram(self.modem, self.wifi)
        self.thingspeak = ThingSpeak(self.modem, self.wifi)
        self.slack = Slack(self.modem, self.wifi)
        self.azure = Azure(self.modem, self.wifi)
        self.scriptr = Scriptr(self.modem, self.wifi)
