"""
Module for debugging purposes.
"""

from machine import Pin, UART


class DebugChannel:
    USBC = 0
    UART = 1


class Debug:
    """Class for debugging purposes."""

    def __init__(self, enabled=True, channel=DebugChannel.USBC):
        """Initializes the debug class."""
        self.uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))
        self.debug_enabled = enabled
        self.debug_channel = channel

    def set_debug_channel(self, channel):
        """Sets the debug channel."""
        self.debug_channel = channel

    def set_debug_enabled(self, enabled):
        """Sets the debug enabled."""
        self.debug_enabled = enabled

    def print(self, *args):
        """Prints the given arguments to the debug channel."""
        if self.debug_enabled:
            if self.debug_channel == DebugChannel.USBC:
                print(*args)
            elif self.debug_channel == DebugChannel.UART:
                self.uart1.write(str(*args))
                self.uart1.write("\n")
