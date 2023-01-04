"""
This module is consist of WiFi related operations for proof of concept integration.
"""

import time
import network

from core.temp import debug
from core.utils.helpers import get_parameter

class WiFiConnection():
    """This class is responsible for operation related to WiFi network."""
    def __init__(self, wifi_settings: list = None):
        """This method is responsible for initializing the WiFiConnection class.

        Parameters
        ----------
        wifi_settings : list, optional
            It must be a list of dictionaries which
            has "ssid" and "password" attributes, by default None
        """
        self.known_networks: list = wifi_settings if wifi_settings else get_parameter("wifi")
        self.wlan = network.WLAN(network.STA_IF)

        # Internal attributes.
        self.__max_try = 10

    def connect(self):
        """This method is responsible for connecting to the WiFi network."""
        self.wlan.active(True)
        debug.debug("WLAN activated on stationary mode.")

        # Check if the board is already connected to the network.
        if self.is_connected:
            debug.debug("The board is already connected to the network.")
            return

        # Try to connect to the network throught the known networks list.
        for wifi_settings in self.known_networks:
            self.wlan.connect(wifi_settings["ssid"], wifi_settings["password"])
            debug.debug("Trying to connect to the AP: ", self.settings["ssid"])

            # Wait for a handshake.
            try_count = 0
            debug.debug("Waiting for handshake.")
            while not self.is_connected:
                try_count += 1
                time.sleep(0.50)

                if try_count >= self.__max_try:
                    debug.error("Couldn't established a handshake to AP.")
                    try_count = 0
                    continue

        debug.debug("Connection established. The board is online.")
    
    def disconnect(self):
        self.wlan.disconnect()
        try:
            debug.debug("WiFi network is disconnected.")
        except KeyboardInterrupt:
            print("[DEBUG] WiFi network is disconnected.")

        self.wlan.active(False)
        try:
            debug.debug("WiFi network is closed.")
        except KeyboardInterrupt:
            print("[DEBUG] WiFi network is closed.")

    def get_local_ip_address(self):
        return self.wlan.ifconfig()[0]
    
    @property
    def is_connected(self):
        return self.wlan.isconnected()