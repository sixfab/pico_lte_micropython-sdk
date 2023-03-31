"""
Module for ease to use of cellular modem. This module includes required functions
for working with cellular modem without need of AT command knowledge.
"""

from core.temp import config

from core.utils.helpers import read_json_file
from core.utils.atcom import ATCom
from core.modules.config import Config

from core.modules.cellular.base import Base
from core.modules.cellular.auth import Auth
from core.modules.cellular.file import File
from core.modules.cellular.http import HTTP
from core.modules.cellular.mqtt import MQTT
from core.modules.cellular.network import Network
from core.modules.cellular.ssl import SSL
from core.modules.cellular.gps import GPS


class Modem:
    """
    Modem class that contains all functions for working with cellular modem
    """

    def __init__(self):
        """
        Initialize modem class
        """
        config["params"] = read_json_file("config.json")

        self.atcom = ATCom()

        self.base = Base(self.atcom)
        self.auth = Auth(self.atcom)
        self.config = Config(self.atcom)
        self.file = File(self.atcom)
        self.network = Network(self.atcom, self.base)
        self.ssl = SSL(self.atcom)
        self.http = HTTP(self.atcom)
        self.mqtt = MQTT(self.atcom)
        self.gps = GPS(self.atcom)

        # Powering up the modem.
        if self.base.power_status() != 0:
           self.base.power_on()
        self.base.wait_until_status_on()
        self.base.wait_until_modem_ready_to_communicate()
        self.base.set_echo_off()
