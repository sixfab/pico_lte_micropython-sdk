"""
This module is consist of WiFi related operations for proof of concept integration.
"""

import time
import network

from core.temp import debug
from core.utils.helpers import get_parameter
from core.utils.manager import StateManager, Step
from core.utils.enums import WiFiStatus, Status


class WiFiModem:
    """This class is responsible for operation related to WiFi network."""

    SLEEP_BETWEEN_CONNECTION_ATTEMPTS = 10
    SLEEP_WHEN_IT_IS_CONNECTING = 5

    def __init__(self):
        """This method is responsible for initializing the WiFiConnection class."""
        # Prepare WLAN.
        self.wlan = network.WLAN(network.STA_IF)

        # Internal attributes.
        self.known_networks = None
        self.__max_try_per_network = 50

    def prepare_wlan(self):
        """This method is responsible for preparing WLAN."""
        self.wlan.active(True)
        debug.debug("WLAN is activated.")
        return {"status": Status.SUCCESS, "response": "WLAN is activated."}

    def connect(self, wifi_settings: dict = None):
        """This method is a coordinator for connecting known networks.

        Parameters
        ----------
        wifi_settings : dict, optional
            It must be a dict which has "ssid" attributes with "password" values,
            by default None
        """
        self.known_networks = (
            wifi_settings if wifi_settings else get_parameter(["known_wifi_networks"])
        )
        debug.debug(
            f"Known hosts are saved into WiFiConnection instance: {self.known_networks}"
        )

        networks_found = self.scan_networks()
        debug.debug("Nearby WiFi network scan is completed.")

        # Check if there is any known network.
        if not networks_found.get("value"):
            debug.debug("No WiFi networks found nearby.")
            return self.get_status()

        for each_network in networks_found.get("value"):
            if each_network["ssid"] in self.known_networks:

                try_count = 0
                # Try to connect more than one for a network.
                while try_count <= self.__max_try_per_network:
                    # @TODO: Check if it also connects to OPEN networks.
                    result = self.connect_to_network(
                        each_network["ssid"], self.known_networks[each_network["ssid"]]
                    )

                    # Return if status is successed.
                    if result.get("status") == Status.SUCCESS:
                        debug.debug("Connection established to WiFi network.")
                        return result
                    else:
                        try_count += 1

                    if result["value"] == WiFiStatus.CONNECTING:
                        debug.debug("Sleeping for {self.SLEEP_WHEN_IT_IS_CONNECTING} seconds.")
                        time.sleep(self.SLEEP_WHEN_IT_IS_CONNECTING)
                    else:
                        debug.debug(
                            f"Sleeping for {self.SLEEP_BETWEEN_CONNECTION_ATTEMPTS} seconds."
                        )
                        time.sleep(self.SLEEP_BETWEEN_CONNECTION_ATTEMPTS)

        # If there is no known network, return the status.
        debug.debug("No known networks nearby.")
        return self.get_status()

    def connect_to_network(self, ssid, password):
        """This method is responsible for connecting to the WiFi network."""
        # Check if the board is already connected to the network.
        if self.is_connected().get("value"):
            debug.debug("The board is already connected to the network.")
            return self.get_status()

        # Try to connect to the network.
        self.wlan.connect(ssid, password)
        debug.debug(f"Trying to connect to the AP: {ssid}")

        return self.get_status()

    def disconnect(self):
        """This method is responsible for disconnecting the WiFi network by purpose."""
        self.wlan.disconnect()
        debug.debug("WiFi network is disconnected.")

        self.wlan.deinit()
        debug.debug("WiFi network is closed.")

        return {"status": Status.SUCCESS, "response": "WiFi network is disconnected."}

    def get_local_ip_address(self):
        """Returns the local ip address of the client.

        Returns
        -------
        str
            Local IP address of the Crux device
        """
        return {"status": Status.SUCCESS, "value": self.wlan.ifconfig()[0]}

    def get_status(self):
        """Returns the status of the WiFi connection.

        Returns
        -------
        dict
            A descriptive message and enum value about the status of WiFi connection.
        """
        got_ip = self.wlan.status() == WiFiStatus.GOT_IP
        connected = self.is_connected()["status"] == Status.SUCCESS
        debug.debug(f"WLAN status is retrived: GOT_IP={got_ip} CONNECTED={connected}")

        # (status >= WiFiStatus.GOT_IP or status < WiFiStatus.IDLE)
        # @TODO: Check if it is correct. Since 3 is not described in
        # https://docs.micropython.org/en/latest/library/network.WLAN.html#network.WLAN.status
        status_to_return = Status.SUCCESS if (connected and got_ip) else Status.ERROR

        return {"status": status_to_return, "value": [connected, got_ip]}

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

        # Check if there is any network nearby.
        if len(networks_nearby) == 0:
            debug.error("No WiFi networks found nearby.")
            return {
                "status": Status.ERROR,
                "value": networks_nearby,
                "response": "No WiFi networks found nearby.",
            }

        # Sort the networks by signal quality.
        networks_nearby = sorted(networks_nearby, key=lambda x: x[3], reverse=True)

        # Convert the list of tuples to list of dicts.
        networks_as_dicts = []
        for network in networks_nearby:
            networks_as_dicts.append(
                {
                    "ssid": network[0].decode("utf-8"),
                    "bssid": network[1],
                    "channel": network[2],
                    "rssi": network[3],
                    "security": network[4],
                    "hidden": network[5],
                }
            )
        debug.debug([ssid["ssid"] for ssid in networks_as_dicts])
        return {"status": Status.SUCCESS, "value": networks_as_dicts}

    def is_connected(self):
        """Returns the status of connection."""
        connection = self.wlan.isconnected()
        return {
            "status": Status.SUCCESS if connection else Status.ERROR,
            "value": connection,
        }

    def get_ready(self, wifi_settings: dict = None):
        """
        This method runs a StateManager which handles
        connection to a known WiFi network.

        Returns
        -------
        dict
            Result of the WiFi connection handling.
        """
        step_check_if_connected = Step(
            function=self.is_connected,
            name="wifi_is_connected",
            success="success",
            fail="wifi_activate_wlan",
        )

        step_activate_wlan = Step(
            function=self.prepare_wlan,
            name="wifi_activate_wlan",
            success="wifi_connect",
            fail="failure",
        )

        step_deactivate_wlan = Step(
            function=self.disconnect,
            name="wifi_deactivate_wlan",
            success="wifi_activate_wlan",
            fail="failure",
        )

        step_connect_to_wifi = Step(
            function=self.connect,
            name="wifi_connect",
            function_params={"wifi_settings": wifi_settings},
            success="wifi_is_connected",
            fail="wifi_deactivate_wlan",
            retry=5,
            interval=1
        )

        sm = StateManager(
            first_step=step_check_if_connected, function_name="get_wifi_ready"
        )
        sm.add_step(step_check_if_connected)
        sm.add_step(step_activate_wlan)
        sm.add_step(step_deactivate_wlan)
        sm.add_step(step_connect_to_wifi)

        while True:
            result = sm.run()

            if result.get("status") == Status.SUCCESS:
                return result
            elif result.get("status") == Status.ERROR:
                return result
            time.sleep(result["interval"])
