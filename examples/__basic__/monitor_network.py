"""
Full Device and Network Monitoring Script for PicoLTE and PicoLTE 2
This script is designed for technical support teams to perform detailed, read-only monitoring of the device and network status.

Each section includes clear comments explaining:
- What the code checks
- Why the check is important
- What the output can tell you when diagnosing issues
"""

from pico_lte.core import PicoLTE
from pico_lte.common import debug

# Initialize PicoLTE core; it internally initializes AT communicator, base, and network modules
pico_lte_device = PicoLTE()

# Serial counter for numbering debug outputs
SERIAL_COUNTER = 1

def numbered_debug(message):
    """Outputs a debug message with a serial number so logs are easier to follow."""
    global SERIAL_COUNTER
    if message:
        debug.info(f"{SERIAL_COUNTER}. {message}")
        SERIAL_COUNTER += 1

def safe_check(label, func):
    """
    Helper function to safely run checks with a label.
    Catches specific errors and outputs a clear debug message.
    """
    try:
        result = func()
        numbered_debug(f"{label}: {result}")
    except (RuntimeError, ValueError) as e:
        numbered_debug(f"{label}: Error retrieving data — {str(e)}")

# --------------- Device Information Check ---------------
def get_device_information():
    """Check device hardware presence and retrieve identifiers."""
    debug.info("--- Device Information ---")
    safe_check("Device General Info", lambda: pico_lte_device.at.send_at_comm('ATI'))
    safe_check("IMEI (Unique Module ID)", lambda: pico_lte_device.at.send_at_comm('AT+GSN'))
    safe_check("Firmware Version", lambda: pico_lte_device.at.send_at_comm('AT+QGMR'))
    safe_check("Manufacturer Name", lambda: pico_lte_device.at.send_at_comm('AT+CGMI'))
    safe_check("Model Name", lambda: pico_lte_device.at.send_at_comm('AT+CGMM'))

# --------------- SIM Card Status Check ---------------
def check_sim_information():
    """Check SIM card presence, ICCID, and readiness."""
    debug.info("--- SIM Card Information ---")
    safe_check("SIM ICCID (Card Serial Number)", lambda: pico_lte_device.base.get_sim_iccid())
    safe_check("SIM Ready Status", lambda: pico_lte_device.base.check_sim_ready())

# --------------- Network Configuration Check ---------------
def check_network_type():
    """Retrieve network scan modes and IoT optimization settings."""
    debug.info("--- Network Type Information ---")
    safe_check("Network Scan Mode", lambda: pico_lte_device.at.send_at_comm('AT+QCFG=\"nwscanmode\"'))
    safe_check("IoT Optimization Mode", lambda: pico_lte_device.at.send_at_comm('AT+QCFG=\"iotopmode\"'))
    safe_check("Current Network Technology", lambda: pico_lte_device.network.get_access_technology())

# --------------- Signal Quality Check ---------------
def check_signal_quality():
    """Retrieve basic signal strength and quality information."""
    debug.info("--- Signal Quality ---")
    safe_check("Signal Quality (CSQ - RSSI/BER)", lambda: pico_lte_device.at.send_at_comm('AT+CSQ'))

# --------------- Network Status Check ---------------
def check_network_status():
    """Retrieve operator, registration, cell, and connection status."""
    debug.info("--- Network Status ---")
    safe_check("Operator Info + Access Tech", lambda: pico_lte_device.at.send_at_comm('AT+COPS?'))
    safe_check("LTE Network Registration (CEREG)", lambda: pico_lte_device.at.send_at_comm('AT+CEREG?'))
    safe_check("Serving Cell Info", lambda: pico_lte_device.at.send_at_comm('AT+QNWINFO'))
    safe_check("Extended Signal Quality (QCSQ - RSRP/RSRQ/SINR)", lambda: pico_lte_device.at.send_at_comm('AT+QCSQ'))
    safe_check("Signaling Connection Status (QCSCON)", lambda: pico_lte_device.at.send_at_comm('AT+QCSCON?'))

# --------------- Packet Service and APN Check ---------------
def check_packet_service_status():
    """Check APN, IP assignment, and data attach status."""
    debug.info("--- Packet Service and APN Info ---")
    safe_check("PDP Context (APN Settings)", lambda: pico_lte_device.at.send_at_comm('AT+CGDCONT?'))
    safe_check("IP Address Info", lambda: pico_lte_device.at.send_at_comm('AT+CGPADDR'))
    safe_check("Packet Attach Status (CGATT)", lambda: pico_lte_device.at.send_at_comm('AT+CGATT?'))

# ------------------------- QPING Connectivity Check -------------------------
def check_qping():
    """Perform a ping test to check internet connectivity."""
    debug.info("--- QPING Command ---")
    safe_check("QPING (Single Ping Test)", lambda: pico_lte_device.at.send_at_comm('AT+QPING=1,\"www.google.com\"'))

# --------------- Main Monitoring Function ---------------
def main():
    """Run all diagnostic checks sequentially."""
    global SERIAL_COUNTER
    SERIAL_COUNTER = 1
    debug.info("========== PicoLTE Device and Network Status Check Start ==========")

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
