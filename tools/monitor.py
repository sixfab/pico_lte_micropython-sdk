"""
Full Device and Network Monitoring Script for PicoLTE
Intended for technical support troubleshooting and device status reporting.
"""
import sys
import os

# Add the project root (one level up) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from pico_lte.core import PicoLTE
from pico_lte.common import debug
from pico_lte.modules.base import Base
from pico_lte.modules.network import Network
from pico_lte.utils.atcom import ATCom


# Initialize PicoLTE core and modules
pico_lte_device = PicoLTE()
at_communicator = ATCom()
base_module = Base(at_communicator)
network_module = Network(at_communicator, base_module)

# Serial counter
SERIAL_COUNTER = 1

def numbered_debug(message):
    """Outputs a debug message with a serial number."""
    global SERIAL_COUNTER
    if message:
        debug.info(f"{SERIAL_COUNTER}. {message}")
        SERIAL_COUNTER += 1

# --------------- Device Related Functions ---------------
def get_device_information():
    """Retrieve and log device information."""
    debug.info("--- Device Information ---")
    numbered_debug(f"Device Info: {at_communicator.send_at_comm('ATI')}")
    numbered_debug(f"IMEI: {at_communicator.send_at_comm('AT+GSN')}")
    numbered_debug(f"Firmware Version: {at_communicator.send_at_comm('AT+QGMR')}")
    numbered_debug(f"Manufacturer: {at_communicator.send_at_comm('AT+CGMI')}")
    numbered_debug(f"Model: {at_communicator.send_at_comm('AT+CGMM')}\n")

# --------------- SIM Related Functions ---------------
def check_sim_information():
    """Retrieve and log SIM card information."""
    debug.info("--- SIM Card Information ---")
    numbered_debug(f"SIM ICCID: {base_module.get_sim_iccid()}")
    numbered_debug(f"SIM Ready Status: {base_module.check_sim_ready()}\n")

# --------------- CAT-M1 and Connection Type Check ---------------
def check_cat_m1_and_network_type():
    """Retrieve and log CAT-M1 and network type information."""
    debug.info("--- CAT-M1 and Network Type ---")
    numbered_debug(
        f"CAT-M1 Scan Mode: {at_communicator.send_at_comm('AT+QCFG=\"nwscanmode\"')}"
    )
    numbered_debug(
        f"IoT Optimization Mode: {at_communicator.send_at_comm('AT+QCFG=\"iotopmode\"')}"
    )
    numbered_debug(
        f"Current Network Technology: {network_module.get_access_technology()}\n"
    )

# --------------- Signal Quality First ---------------
def check_signal_quality_first():
    """Retrieve and log initial signal quality."""
    debug.info("--- Signal Quality ---")
    numbered_debug(f"Signal Quality (CSQ): {at_communicator.send_at_comm('AT+CSQ')}\n")

# --------------- Network Related Functions ---------------
def check_network_status():
    """Retrieve and log network status information."""
    debug.info("--- Network Status ---")
    cops_info = at_communicator.send_at_comm('AT+COPS?')
    numbered_debug(f"Operator Info and Access Technology: {cops_info}")
    numbered_debug(
        f"Network Registration (CEREG - LTE): {at_communicator.send_at_comm('AT+CEREG?')}"
    )
    numbered_debug(f"Serving Cell Info: {at_communicator.send_at_comm('AT+QNWINFO')}")
    numbered_debug(f"Extended Signal Quality (QCSQ): {at_communicator.send_at_comm('AT+QCSQ')}")
    numbered_debug(
        f"Signaling Connection Status (QCSCON): {at_communicator.send_at_comm('AT+QCSCON?')}\n"
    )

# --------------- Packet Attach and APN Related Functions ---------------
def check_packet_service_status():
    """Retrieve and log packet service and APN information."""
    debug.info("--- Packet Service and APN Info ---")
    numbered_debug(f"PDP Context (APN): {at_communicator.send_at_comm('AT+CGDCONT?')}")
    numbered_debug(f"IP Address Info: {at_communicator.send_at_comm('AT+CGPADDR')}")
    numbered_debug(f"Packet Attach Status (CGATT): {at_communicator.send_at_comm('AT+CGATT?')}\n")

# --------------- Main Monitoring Function ---------------
def main():
    """Main function to perform full device and network status checks."""
    global SERIAL_COUNTER
    SERIAL_COUNTER = 1
    debug.info("========== PicoLTE Device and Network Status Check Start ==========\n")

    get_device_information()
    check_sim_information()
    check_cat_m1_and_network_type()
    check_signal_quality_first()
    check_network_status()
    check_packet_service_status()
    debug.info("========== PicoLTE Device and Network Status Check Complete ==========")

if __name__ == "__main__":
    main()
