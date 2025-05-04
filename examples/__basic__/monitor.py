"""
Full Device and Network Monitoring Script for PicoLTE and PicoLTE 2
This script is designed for technical support teams to perform detailed, read-only monitoring of the device and network status.

Each section includes clear comments explaining:
- What the code checks
- Why the check is important
- What the output can tell you when diagnosing issues

Version: 2.0.0
Date: 2025-05-05
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

# Serial counter for numbering debug outputs
SERIAL_COUNTER = 1

def numbered_debug(message):
    """Outputs a debug message with a serial number so logs are easier to follow."""
    global SERIAL_COUNTER
    if message:
        debug.info(f"{SERIAL_COUNTER}. {message}")
        SERIAL_COUNTER += 1

# --------------- Device Information Check ---------------
# This section confirms that the device hardware is alive and communicating.
# It retrieves basic identifiers like IMEI, firmware version, manufacturer, and model.
# Failures here may point to a hardware issue, bad connection, or module failure.
def get_device_information():
    debug.info("--- Device Information ---")
    try:
        numbered_debug(f"Device General Info: {at_communicator.send_at_comm('ATI')}")
    except Exception:
        numbered_debug(f"Device Info: Device not connected or not responding.")
    
    try:
        numbered_debug(f"IMEI (Unique Module ID): {at_communicator.send_at_comm('AT+GSN')}")
    except Exception:
        numbered_debug(f"IMEI: Unable to retrieve — possible hardware or SIM problem.")
    
    try:
        numbered_debug(f"Firmware Version: {at_communicator.send_at_comm('AT+QGMR')}")
    except Exception:
        numbered_debug(f"Firmware Version: Unable to retrieve firmware details.")
    
    try:
        numbered_debug(f"Manufacturer Name: {at_communicator.send_at_comm('AT+CGMI')}")
    except Exception:
        numbered_debug(f"Manufacturer: Unable to retrieve manufacturer name.")
    
    try:
        numbered_debug(f"Model Name: {at_communicator.send_at_comm('AT+CGMM')}\n")
    except Exception:
        numbered_debug(f"Model: Unable to retrieve model name.\n")

# --------------- SIM Card Status Check ---------------
# This section checks if the SIM card is inserted, readable, and ready.
# It retrieves the ICCID (SIM serial number) and SIM readiness status.
# If this fails, there may be SIM insertion problems, SIM card damage, or slot issues.
def check_sim_information():
    debug.info("--- SIM Card Information ---")
    try:
        numbered_debug(f"SIM ICCID (Card Serial Number): {base_module.get_sim_iccid()}")
    except Exception:
        numbered_debug(f"SIM ICCID: Could not retrieve — check SIM insertion or health.")
    
    try:
        numbered_debug(f"SIM Ready Status: {base_module.check_sim_ready()}\n")
    except Exception:
        numbered_debug(f"SIM Ready Status: Unable to check — possible SIM or module fault.\n")

# --------------- Network Configuration Check ---------------
# This section retrieves network scan mode (Cat-M1, eGPRS, NB-IoT),
# IoT optimization mode, and current access technology.
# These details are important to confirm the device is configured to use the intended network types.
def check_network_type():
    debug.info("--- Network Type Information ---")
    try:
        numbered_debug(f"Network Scan Mode: {at_communicator.send_at_comm('AT+QCFG=\"nwscanmode\"')}")
    except Exception:
        numbered_debug(f"Network Scan Mode: Unable to retrieve — check module settings.")
    
    try:
        numbered_debug(f"IoT Optimization Mode: {at_communicator.send_at_comm('AT+QCFG=\"iotopmode\"')}")
    except Exception:
        numbered_debug(f"IoT Optimization Mode: Unable to retrieve optimization configuration.")
    
    try:
        numbered_debug(f"Current Network Technology: {network_module.get_access_technology()}\n")
    except Exception:
        numbered_debug(f"Current Network Technology: Unable to detect — possible signal or config issue.\n")

# --------------- Signal Quality Check ---------------
# This section checks basic signal strength reported by the module.
# Weak signals may show as high numbers like 99,99 (unavailable).
# Useful for diagnosing antenna or location-related problems.
def check_signal_quality():
    debug.info("--- Signal Quality ---")
    try:
        numbered_debug(f"Signal Quality (CSQ - RSSI/BER): {at_communicator.send_at_comm('AT+CSQ')}\n")
    except Exception:
        numbered_debug(f"Signal Quality: Cannot retrieve — check antenna connection or network coverage.\n")

# --------------- Network Status Check ---------------
# This section retrieves operator info, LTE registration status, serving cell info,
# extended signal quality, and signaling connection status.
# It helps verify if the device is properly connected and communicating with the mobile network.
def check_network_status():
    debug.info("--- Network Status ---")
    try:
        numbered_debug(f"Operator Info + Access Tech: {at_communicator.send_at_comm('AT+COPS?')}")
    except Exception:
        numbered_debug(f"Operator Info: Unable to retrieve — check SIM, antenna, or coverage.")
    
    try:
        numbered_debug(f"LTE Network Registration (CEREG): {at_communicator.send_at_comm('AT+CEREG?')}")
    except Exception:
        numbered_debug(f"Network Registration: Could not check — device may not be registered.")
    
    try:
        numbered_debug(f"Serving Cell Info: {at_communicator.send_at_comm('AT+QNWINFO')}")
    except Exception:
        numbered_debug(f"Serving Cell Info: Could not retrieve — check network connection.")
    
    try:
        numbered_debug(f"Extended Signal Quality (QCSQ - RSRP/RSRQ/SINR): {at_communicator.send_at_comm('AT+QCSQ')}")
    except Exception:
        numbered_debug(f"Extended Signal Quality: Could not retrieve — weak or no signal detected.")
    
    try:
        numbered_debug(f"Signaling Connection Status (QCSCON): {at_communicator.send_at_comm('AT+QCSCON?')}\n")
    except Exception:
        numbered_debug(f"Signaling Connection Status: Could not retrieve — check radio link.\n")

# --------------- Packet Service and APN Check ---------------
# This section checks the packet data context (APN), assigned IP address,
# and whether the module is attached to the packet service (data-ready).
# Essential for troubleshooting mobile data connectivity issues.
def check_packet_service_status():
    debug.info("--- Packet Service and APN Info ---")
    try:
        numbered_debug(f"PDP Context (APN Settings): {at_communicator.send_at_comm('AT+CGDCONT?')}")
    except Exception:
        numbered_debug(f"PDP Context: Could not retrieve — check APN configuration.")
    
    try:
        numbered_debug(f"IP Address Info: {at_communicator.send_at_comm('AT+CGPADDR')}")
    except Exception:
        numbered_debug(f"IP Address: Could not retrieve — no IP assigned or network issue.")
    
    try:
        numbered_debug(f"Packet Attach Status (CGATT): {at_communicator.send_at_comm('AT+CGATT?')}\n")
    except Exception:
        numbered_debug(f"Packet Attach Status: Could not check — device may not be attached to data.\n")

# ------------------------- QPING Connectivity Check -------------------------
# This section runs a connectivity test by pinging an external host (like Google).
# It helps verify if the device has live internet access over the cellular connection.
def check_qping():
    debug.info("--- QPING Command ---")
    try:
        numbered_debug(f"QPING (Single Ping Test): {at_communicator.send_at_comm('AT+QPING=1,\"www.google.com\"')}")
    except Exception:
        numbered_debug(f"QPING Single: Could not retrieve — network unreachable or firewall issue.")
    
    try:
        numbered_debug(f"QPING (Detailed 10x Ping Test): {at_communicator.send_at_comm('AT+QPING=1,\"www.google.com\",10,10')}\n")
    except Exception:
        numbered_debug(f"QPING Detailed: Could not retrieve — likely no internet access.\n")

# --------------- Main Monitoring Function ---------------
# Runs all the above checks in sequence, providing a full diagnostic snapshot.
# No configurations are changed — this is a read-only status script.
def main():
    global SERIAL_COUNTER
    SERIAL_COUNTER = 1
    debug.info("========== PicoLTE Device and Network Status Check Start ==========\n")

    get_device_information()
    check_sim_information()
    check_network_type()
    check_signal_quality()
    check_network_status()
    check_packet_service_status()
    check_qping()

    debug.info("========== PicoLTE Device and Network Status Check Complete ==========")

if __name__ == "__main__":
    main()
