"""
This module is consist of WiFi related operations for proof of concept integration.
"""

import time
import network

from core.modules.wifi_modules.mqtt import MQTT
from core.modules.wifi_modules.http import HTTP

from core.temp import debug
from core.utils.helpers import get_parameter
from core.utils.manager import StateManager, Step
from core.utils.enums import WiFiStatus, Status


class WiFiModem:
    """This class is responsible for operation related to WiFi network."""

    MAX_RECONNECTION_TRY = 2  # times
    MAX_WAIT_FOR_CONNECTION = 5  # seconds

    def __init__(self):
        """This method is responsible for initializing the WiFiConnection class."""
        # Prepare WLAN.
        self.wlan = network.WLAN(network.STA_IF)

        # Modules
        self.mqtt = MQTT()
        self.http = HTTP()

        # Internal attributes.
        self.known_networks = None

    def prepare_wlan(self):
        """This method is responsible for preparing WLAN."""
        self.wlan.active(True)
        debug.debug("WLAN is activated.")
        return {"status": Status.SUCCESS, "response": "WLAN is activated."}

    def connect_known(self, wifi_settings=None):
        """This method is a coordinator for connecting known networks.

        Parameters
        ----------
        wifi_settings : dict, optional
            It must be a dict which has "ssid" attributes with "password" values,
            by default None
        """
        # Check if any known network settings given as function parameter.
        if wifi_settings is None:
            wifi_settings = get_parameter(["known_wifi_networks"])

            if wifi_settings is None:
                return {"status": Status.ERROR, "response": "No WiFi settings found."}

        # Save the known networks.
        self.known_networks = wifi_settings
        debug.debug(
            f"Trying to connect known WiFi access points: {wifi_settings}"
        )

        # Scan the network.
        networks_found = self.scan_networks()
        if networks_found.get("status") != Status.SUCCESS:
            return {"status": Status.ERROR, "response": "No WiFi networks found."}
        debug.debug("Nearby WiFi network scan is completed.")

        # Check if there is any known network.
        if len(networks_found.get("response")) == 0:
            debug.debug("No WiFi networks found nearby.")
            return self.get_status()

        # Try to connect to the known networks.
        for each_network in networks_found.get("response"):
            if each_network["ssid"] in wifi_settings:

                start_time = time.time()
                while time.time() - start_time < self.MAX_WAIT_FOR_CONNECTION:
                    # @TODO: Check if it also connects to OPEN networks.
                    result = self.connect_to(
                        each_network["ssid"], wifi_settings[each_network["ssid"]]
                    )

                    # Return if status is successed.
                    if result.get("status") == Status.SUCCESS:
                        debug.info("Connection established to WiFi network.")
                        return result

                    elif result["response"] == WiFiStatus.CONNECTING:
                        debug.debug("Trying to get IP address from DHCP server.")

                    time.sleep(0.1)

        # If the connection is not established, return the status.
        debug.debug("Connection could not be established to WiFi network.")
        return self.get_status()

    def connect_to(self, ssid, password):
        """This method is responsible for connecting to the WiFi network."""
        # Check if the board is already connected to the network.
        if self.is_connected().get("response"):
            debug.debug("The board is already connected to the network.")
            return self.get_status()

        # Try to connect to the network.
        self.wlan.connect(ssid, password)

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
        return {"status": Status.SUCCESS, "response": self.wlan.ifconfig()[0]}

    def get_status(self):
        """Returns the status of the WiFi connection.

        Returns
        -------
        dict
            A descriptive message and enum response about the status of WiFi connection.
        """
        got_ip = self.wlan.status() == WiFiStatus.GOT_IP
        connected = self.is_connected()["status"] == Status.SUCCESS

        # (status >= WiFiStatus.GOT_IP or status < WiFiStatus.IDLE)
        # @TODO: Check if it is correct. Since 3 is not described in
        # https://docs.micropython.org/en/latest/library/network.WLAN.html#network.WLAN.status
        status_to_return = Status.SUCCESS if (connected and got_ip) else Status.ERROR

        return {"status": status_to_return, "response": [connected, got_ip]}

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
        if len(networks_nearby) == 0 or networks_nearby is None:
            debug.debug("No WiFi networks found nearby.")
            return {
                "status": Status.ERROR,
                "response": [],
            }

        # Sort the networks by signal quality.
        networks_nearby = sorted(networks_nearby, key=lambda x: x[3], reverse=True)

        # Convert the list of tuples to list of dicts.
        networks_as_dicts = []
        for ap_network in networks_nearby:
            networks_as_dicts.append(
                {
                    "ssid": ap_network[0].decode("utf-8"),
                    "bssid": ap_network[1],
                    "channel": ap_network[2],
                    "rssi": ap_network[3],
                    "security": ap_network[4],
                    "hidden": ap_network[5],
                }
            )
        debug.debug([ssid["ssid"] for ssid in networks_as_dicts])
        return {"status": Status.SUCCESS, "response": networks_as_dicts}

    def is_connected(self):
        """Returns the status of connection."""
        connection = self.wlan.isconnected()
        return {
            "status": Status.SUCCESS if connection else Status.ERROR,
            "response": connection,
        }

    def get_ready(self, wifi_settings=None):
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
            function=self.connect_known,
            name="wifi_connect",
            function_params={"wifi_settings": wifi_settings},
            success="wifi_is_connected",
            fail="wifi_connect",
        )

        sm = StateManager(
            first_step=step_check_if_connected, function_name="get_wifi_ready"
        )
        sm.add_step(step_check_if_connected)
        sm.add_step(step_activate_wlan)
        sm.add_step(step_deactivate_wlan)
        sm.add_step(step_connect_to_wifi)

        retry_count = 0
        while True:
            result = sm.run()

            if result.get("status") == Status.SUCCESS:
                return result
            elif result.get("status") == Status.ERROR:
                return result

            if sm.current.name == "wifi_connect":
                if retry_count > self.MAX_RECONNECTION_TRY:
                    return {"status": Status.ERROR, "response": "WiFi connection failed."}
                retry_count += 1

            time.sleep(result["interval"])
