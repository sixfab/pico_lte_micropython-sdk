"""
This module is consist of WiFi related operations for proof of concept integration.
"""

import time
import network

from core.temp import debug
from core.utils.helpers import get_parameter
from core.utils.enums import WiFiStatus


class WiFiConnection:
    """This class is responsible for operation related to WiFi network."""

    def __init__(self, wifi_settings: list = None):
        """This method is responsible for initializing the WiFiConnection class.

        Parameters
        ----------
        wifi_settings : list, optional
            It must be a list of dictionaries which
            has "ssid" and "password" attributes, by default None
        """
        self.known_networks: dict = (
            wifi_settings if wifi_settings else get_parameter("known_wifi_networks")
        )
        debug.debug("Known hosts are saved into WiFiConnection instance.")
        
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        debug.debug("WLAN stationary mode is activated.")

        # Internal attributes.
        self.__max_try = 50

    def connect(self):
        """This method is a coordinator for connecting known networks."""
        networks = self.scan_networks()
        debug.debug("Nearby WiFi network scan is completed.")

        for network in networks:
            if network["ssid"] in self.known_networks:

                # Try to connect more than one for a network.
                while try_count <= self.__max_try:
                    # @TODO: Check if it also connects to OPEN networks.
                    result = self.connect_to_network(
                        network["ssid"], self.known_networks[network["ssid"]]
                    )
                    if result.get("status") == WiFiStatus.GOT_IP:
                        debug.debug("Connection established to WiFi network.")
                        return result
                    else:
                        try_count += 1

        debug.debug("No known WiFi networks found nearby.")
        return self.get_status()

    def connect_to_network(self, ssid, password):
        """This method is responsible for connecting to the WiFi network."""
        self.wlan.active(True)
        debug.debug("WLAN activated on stationary mode.")

        # Check if the board is already connected to the network.
        if self.is_connected:
            debug.debug("The board is already connected to the network.")
            return

        # Try to connect to the network.
        self.wlan.connect(ssid, password)
        debug.debug(f"Trying to connect to the AP: {ssid}")

        # Wait for a handshake.
        try_count = 0
        debug.debug("Waiting for handshake.")
        while not self.is_connected:
            try_count += 1
            time.sleep(0.1)

            if try_count >= self.__max_try:
                debug.error("Couldn't established a handshake to AP.")
                try_count = 0

        return self.get_status()

    def disconnect(self):
        """This method is responsible for disconnecting the WiFi network by purpose."""
        self.wlan.disconnect()
        debug.debug("WiFi network is disconnected.")

        self.wlan.deinit()
        debug.debug("WiFi network is closed.")

    def get_local_ip_address(self):
        """Returns the local ip address of the client.

        Returns
        -------
        str
            Local IP address of the Crux device
        """
        return self.wlan.ifconfig()[0]

    def get_status(self):
        """Returns the status of the WiFi connection.

        Returns
        -------
        dict
            A descriptive message and enum value about the status of WiFi connection.
        """
        messages = {
            WiFiStatus.IDLE: "idle",
            WiFiStatus.CONNECTING: "Connecting to Wi-Fi network",
            WiFiStatus.WRONG_PASSWORD: "Wrong password",
            WiFiStatus.CONNECTION_FAILED: "Connection failed due to problems",
            WiFiStatus.GOT_IP: "Successfully got IP",
        }
        status = self.wlan.status()
        debug.debug(f"WLAN status is retrivied: {messages[status]}")

        return {"status": status, "response": messages[status]}

    def scan_networks(self):
        """Returns the nearby networks sorted as the one which
        has higher signal quality at first.

        Returns
        -------
        list
            A list of dicts which has ssid, bssid, channel,
            rssi, security, is_hidden attributes.
        """
        networks_nearby = self.wlan.scan()
        networks_nearby = sorted(networks_nearby, key=lambda x: x[3], reverse=True)

        networks_as_dicts = []
        for network in networks_nearby:
            networks_as_dicts.append(
                {
                    "ssid": network[0].decode("utf-8"),
                    "bssid": network[1],
                    "channel": network[2],
                    "rssi": network[3],
                    "security": network[4],
                    "is_hidden": network[5],
                }
            )
        return networks_as_dicts

    @property
    def is_connected(self):
        """Returns the status of connection."""
        return self.wlan.isconnected()
