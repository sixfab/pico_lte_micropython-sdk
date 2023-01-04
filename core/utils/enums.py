"""Enumerations for the Crux SDK"""


class Status:
    """Enumeration for Status responses."""
    SUCCESS = 0
    ERROR = 1
    TIMEOUT = 2
    ONGOING = 3
    UNKNOWN = 99

class Connection:
    """Enumeration for connection types."""
    CELLULAR = 0
    WIFI = 1
    BOTH = 2

class WiFiSecurity:
    """Enumeration for WiFi security levels types."""
    OPEN = 0
    WEP = 1
    WPA_PSK = 2
    WPA2_PSK = 3
    WPA_WPA2_PSK = 4

class WiFiStatus:
    """Enumeration for status responses of WiFi driver."""  
    IDLE = 0
    CONNECTING = 1
    WRONG_PASSWORD = 2
    NO_AP_FOUND = 3
    CONNECTION_FAILED = 4
    GOT_IP = 5
