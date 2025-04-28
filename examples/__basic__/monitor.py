"""
Full Device and Network Monitoring Script for PicoLTE
Intended for technical support troubleshooting and device status reporting.
"""
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
    try:
        numbered_debug(f"Device Info: {at_communicator.send_at_comm('ATI')}")
    except Exception as e:
        numbered_debug(f"Device Info: Device not connected.")
    
    try:
        numbered_debug(f"IMEI: {at_communicator.send_at_comm('AT+GSN')}")
    except Exception as e:
        numbered_debug(f"IMEI: No IMEI found or Device not connected.")
    
    try:
        numbered_debug(f"Firmware Version: {at_communicator.send_at_comm('AT+QGMR')}")
    except Exception as e:
        numbered_debug(f"Firmware Version: Unable to retrieve version.")
    
    try:
        numbered_debug(f"Manufacturer: {at_communicator.send_at_comm('AT+CGMI')}")
    except Exception as e:
        numbered_debug(f"Manufacturer: Unable to retrieve manufacturer.")
    
    try:
        numbered_debug(f"Model: {at_communicator.send_at_comm('AT+CGMM')}\n")
    except Exception as e:
        numbered_debug(f"Model: Unable to retrieve model.\n")


# --------------- SIM Related Functions ---------------
# --------------- SIM Related Functions ---------------
def check_sim_information():
    """Retrieve and log SIM card information."""
    debug.info("--- SIM Card Information ---")
    try:
        numbered_debug(f"SIM ICCID: {base_module.get_sim_iccid()}")
    except Exception as e:
        numbered_debug(f"SIM ICCID: Unable to retrieve ICCID.")
    
    try:
        numbered_debug(f"SIM Ready Status: {base_module.check_sim_ready()}\n")
    except Exception as e:
        numbered_debug(f"SIM Ready Status: Unable to retrieve SIM Status information.\n")


# --------------- Network Type Check ---------------
def check_network_type():
    """Retrieve and log network type information."""
    debug.info("--- Network Type Information ---")
    try:
        numbered_debug(f"Network Scan Mode: {at_communicator.send_at_comm('AT+QCFG=\"nwscanmode\"')}")
    except Exception as e:
        numbered_debug(f"Network Scan Mode: Unable to retrieve scan mode.")")
    
    try:
        numbered_debug(f"IoT Optimization Mode: {at_communicator.send_at_comm('AT+QCFG=\"iotopmode\"')}")
    except Exception as e:
        numbered_debug(f"IoT Optimization Mode: Unable to retrieve optimization mode.")
    
    try:
        numbered_debug(f"Current Network Technology: {network_module.get_access_technology()}\n")
    except Exception as e:
        numbered_debug(f"Current Network Technology: Unable to retrieve current network technology. \n")

# --------------- Signal Quality ---------------
def check_signal_quality():
    """Retrieve and log signal quality."""
    debug.info("--- Signal Quality ---")
    try:
        numbered_debug(f"Signal Quality (CSQ): {at_communicator.send_at_comm('AT+CSQ')}\n")
    except Exception as e:
        numbered_debug(f"Signal Quality (CSQ): Unable to retrieve signal quality.\n")


# --------------- Network Related Functions ---------------
def check_network_status():
    """Retrieve and log network status information."""
    debug.info("--- Network Status ---")
    try:
        numbered_debug(f"Operator Info and Access Technology: {at_communicator.send_at_comm('AT+COPS?')}")
    except Exception as e:
        numbered_debug(f"Operator Info: Unable to retrieve operator information.")
    
    try:
        numbered_debug(f"Network Registration (CEREG - LTE): {at_communicator.send_at_comm('AT+CEREG?')}")
    except Exception as e:
        numbered_debug(f"Network Registration (CEREG): Unable to retrieve network registration status.")
    
    try:
        numbered_debug(f"Serving Cell Info: {at_communicator.send_at_comm('AT+QNWINFO')}")
    except Exception as e:
        numbered_debug(f"Serving Cell Info: Unable to retrieve serving cell information.")
    
    try:
        numbered_debug(f"Extended Signal Quality (QCSQ): {at_communicator.send_at_comm('AT+QCSQ')}")
    except Exception as e:
        numbered_debug(f"Extended Signal Quality (QCSQ): Unable to retrieve extended signal quality.")
    
    try:
        numbered_debug(f"Signaling Connection Status (QCSCON): {at_communicator.send_at_comm('AT+QCSCON?')}\n")
    except Exception as e:
        numbered_debug(f"Signaling Connection Status (QCSCON): Unable to retrieve signaling connection status.\n")


# --------------- Packet Attach and APN Related Functions ---------------
def check_packet_service_status():
    """Retrieve and log packet service and APN information."""
    debug.info("--- Packet Service and APN Info ---")
    try:
        numbered_debug(f"PDP Context (APN): {at_communicator.send_at_comm('AT+CGDCONT?')}")
    except Exception as e:
        numbered_debug(f"PDP Context (APN): Unable to retrieve PDP context.")
    
    try:
        numbered_debug(f"IP Address Info: {at_communicator.send_at_comm('AT+CGPADDR')}")
    except Exception as e:
        numbered_debug(f"IP Address Info: Unable to retrieve IP address information.")
    
    try:
        numbered_debug(f"Packet Attach Status (CGATT): {at_communicator.send_at_comm('AT+CGATT?')}\n")
    except Exception as e:
        numbered_debug(f"Packet Attach Status (CGATT): Unable to retrieve pocket attact status.\n")


# --------------- Main Monitoring Function ---------------
def main():
    """Main function to perform full device and network status checks."""
    global SERIAL_COUNTER
    SERIAL_COUNTER = 1
    debug.info("========== PicoLTE Device and Network Status Check Start ==========\n")

    get_device_information()
    check_sim_information()
    check_network_type()
    check_signal_quality()
    check_network_status()
    check_packet_service_status()

    debug.info("========== PicoLTE Device and Network Status Check Complete ==========")

if __name__ == "__main__":
    main()
