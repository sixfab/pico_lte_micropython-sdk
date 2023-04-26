"""
Module for ease to use of cellular PicoLTE. This module includes required functions
for working with cellular modem without need of AT command knowledge.
"""
from pico_lte.common import config

from pico_lte.utils.helpers import read_json_file
from pico_lte.utils.atcom import ATCom

from pico_lte.modules.base import Base
from pico_lte.modules.auth import Auth
from pico_lte.modules.file import File
from pico_lte.modules.http import HTTP
from pico_lte.modules.mqtt import MQTT
from pico_lte.modules.network import Network
from pico_lte.modules.peripherals import Periph
from pico_lte.modules.ssl import SSL
from pico_lte.modules.gps import GPS

from pico_lte.apps.aws import AWS
from pico_lte.apps.slack import Slack
from pico_lte.apps.telegram import Telegram
from pico_lte.apps.thingspeak import ThingSpeak
from pico_lte.apps.azure import Azure
from pico_lte.apps.scriptr import Scriptr


class PicoLTE:
    """
    PicoLTE modem class that contains all functions for working with cellular modem
    """

    def __init__(self):
        """
        Initialize modem class
        """
        config["params"] = read_json_file("config.json")

        self.peripherals = Periph()
        self.atcom = ATCom()

        self.base = Base(self.atcom)
        self.file = File(self.atcom)
        self.auth = Auth(self.atcom, self.file)
        self.network = Network(self.atcom, self.base)
        self.ssl = SSL(self.atcom)
        self.http = HTTP(self.atcom)
        self.mqtt = MQTT(self.atcom)
        self.gps = GPS(self.atcom)

        self.aws = AWS(self.base, self.auth, self.network, self.ssl, self.mqtt, self.http)
        self.telegram = Telegram(self.base, self.network, self.http)
        self.thingspeak = ThingSpeak(self.base, self.network, self.mqtt)
        self.slack = Slack(self.base, self.network, self.http)
        self.azure = Azure(self.base, self.auth, self.network, self.ssl, self.mqtt, self.http)
        self.scriptr = Scriptr(self.base, self.network, self.http)

        # Power up modem
        if self.base.power_status() != 0:
            self.base.power_on()
        self.base.wait_until_status_on()
        self.base.wait_until_modem_ready_to_communicate()
        self.base.set_echo_off()
