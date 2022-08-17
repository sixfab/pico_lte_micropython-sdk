"""
Module for debugging purposes.
"""

from machine import Pin, UART


class DebugChannel:
    USBC = 0
    UART = 1


class DebugLevel:
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
    FOCUS = -1


class Debug:
    """Class for debugging purposes."""

    def __init__(self, enabled=True, channel=DebugChannel.USBC, level=DebugLevel.INFO):
        """Initializes the debug class."""
        self.uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))
        self.debug_enabled = enabled
        self.debug_channel = channel
        self.debug_level = level

    def set_debug_channel(self, channel):
        """Sets the debug channel."""
        self.debug_channel = channel

    def set_debug_level(self, level):
        """Sets the debug level."""
        self.debug_level = level

    def set_debug_enabled(self, enabled):
        """Sets the debug enabled."""
        self.debug_enabled = enabled

    def print(self, *args):
        """debug.prints the given arguments to the debug channel."""
        if self.debug_enabled:
            if self.debug_channel == DebugChannel.USBC:
                print(*args)
            elif self.debug_channel == DebugChannel.UART:
                for arg in args:
                    self.uart1.write(str(arg))
                    self.uart1.write(" ")
                self.uart1.write("\n")

    def debug(self, *args):
        """Function for DEBUG level messages."""
        if self.debug_enabled and self.debug_level <= DebugLevel.DEBUG:
            self.print("DEBUG:", *args)

    def info(self, *args):
        """Function for INFO level messages."""
        if self.debug_enabled and self.debug_level <= DebugLevel.INFO:
            self.print("INFO:", *args)

    def warning(self, *args):
        """Function for WARNING level messages."""
        if self.debug_enabled and self.debug_level <= DebugLevel.WARNING:
            self.print("WARNING:", *args)

    def error(self, *args):
        """Function for ERROR level messages."""
        if self.debug_enabled and self.debug_level <= DebugLevel.ERROR:
            self.print("ERROR:", *args)

    def critical(self, *args):
        """Function for CRITICAL level messages."""
        if self.debug_enabled and self.debug_level <= DebugLevel.CRITICAL:
            self.print("CRITICAL:", *args)

    def focus(self, *args):
        """Function for FOCUSSED level messages."""
        if self.debug_enabled and self.debug_level == DebugLevel.FOCUS:
            self.print("FOCUS:", *args)
