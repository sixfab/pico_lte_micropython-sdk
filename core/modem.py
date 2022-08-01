"""
Module for ease to use of cellular modem. This module includes required functions
for working with cellular modem without need of AT command knowledge.
"""

from core.temp import config

from core.utils.helpers import read_json_file
from core.utils.atcom import ATCom

from core.modules.ulp import ULP
from core.modules.base import Base
from core.modules.auth import Auth
from core.modules.config import Config
from core.modules.file import File
from core.modules.http import HTTP
from core.modules.mqtt import MQTT
from core.modules.network import Network
from core.modules.peripherals import Periph
from core.modules.ssl import SSL

from core.apps.aws import AWS


class Modem:
    """
    Modem class that contains all functions for working with cellular modem
    """

    def __init__(self):
        """
        Initialize modem class
        """
        self.ulp = ULP()
        self.peripherals = Periph()
        self.atcom = ATCom()

        self.base = Base(self.atcom)
        self.auth = Auth(self.atcom)
        self.config = Config(self.atcom)
        self.file = File(self.atcom)
        self.network = Network(self.atcom, self.base)
        self.ssl = SSL(self.atcom)
        self.http = HTTP(self.atcom)
        self.mqtt = MQTT(self.atcom)

        self.aws = AWS(self.base, self.network, self.ssl, self.mqtt, self.http)

        # power up modem
        if self.base.power_status() != 0:
            self.base.power_on_off()
        self.base.wait_until_status_on()
        self.base.wait_until_modem_ready_to_communicate()

        # check certificates in modem or upload them
        self.auth.load_certificates()
        config["params"] = read_json_file("config.json")
