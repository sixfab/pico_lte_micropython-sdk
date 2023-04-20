"""
Module for including functions of Google Sheets for Picocell module.
"""

from core.temp import config


class GoogleSheets:
    """
    Class for including functions of Google Sheets operations for Picocell module.
    """

    cache = config["cache"]

    def __init__(self, base, network, http):
        self.base = base
        self.network = network
        self.http = http
