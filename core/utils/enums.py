"""Enumerations for the Crux SDK"""


class Status:
    """Enumeration for Status responses."""
    SUCCESS = 0
    ERROR = 1
    TIMEOUT = 2
    ONGOING = 3
    UNKNOWN = 99

class Connection:
    """Enumeration for Connection responses."""
    CELLULAR = 0
    WIFI = 1
    BOTH = 2
