"""
Test module for the utils.debug module.
"""

import pytest
from machine import UART

from pico_lte.utils.debug import DebugChannel, DebugLevel, Debug


class TestDebugChannel:
    """
    Test class for DebugChannel.
    """

    def test_debug_channel_codes(self):
        """This method tests the attributes of DebugChannel class."""
        assert DebugChannel.USBC == 0
        assert DebugChannel.UART == 1


class TestDebugLevel:
    """
    Test class for DebugLevel
    """

    def test_debug_level_codes(self):
        """This method tests the attributes of DebugLevel class."""
        assert DebugLevel.DEBUG == 0
        assert DebugLevel.INFO == 1
        assert DebugLevel.WARNING == 2
        assert DebugLevel.ERROR == 3
        assert DebugLevel.CRITICAL == 4
        assert DebugLevel.FOCUS == -1


class TestDebug:
    """
    Test class for Debug.
    """

    @pytest.fixture
    def exemplary_debug_instance(self):
        """It is a fixture for quick initilization of the instance."""
        debug_instance = Debug()
        return debug_instance

    def test_default_parameters(self, exemplary_debug_instance):
        """This method creates Debug instance with its default
        parameters, and checks if the parameters are okay.
        """
        assert isinstance(exemplary_debug_instance.uart1, UART)
        assert exemplary_debug_instance.debug_enabled is True
        assert exemplary_debug_instance.debug_channel == DebugChannel.USBC
        assert exemplary_debug_instance.debug_level == DebugLevel.INFO

    def test_initilization_with_parameters(self):
        """This method creates Debug instance with different parameters
        then its defaults and tests them.
        """
        debug_instance = Debug(enabled=False, channel=DebugChannel.UART, level=DebugLevel.CRITICAL)

        assert isinstance(debug_instance.uart1, UART)
        assert debug_instance.debug_enabled is False
        assert debug_instance.debug_channel == DebugChannel.UART
        assert debug_instance.debug_level == DebugLevel.CRITICAL

    @pytest.mark.parametrize("desired_channel", [DebugChannel.UART, DebugChannel.USBC, -55, 0, 95])
    def test_set_channel(self, exemplary_debug_instance, desired_channel):
        """This method tests set_channel() method."""
        exemplary_debug_instance.set_channel(desired_channel)
        assert exemplary_debug_instance.debug_channel == desired_channel

    @pytest.mark.parametrize(
        "debug_level_wanted",
        [
            DebugLevel.DEBUG,
            DebugLevel.INFO,
            DebugLevel.CRITICAL,
            DebugLevel.FOCUS,
            DebugLevel.ERROR,
            DebugLevel.WARNING,
        ],
    )
    def test_set_level(self, exemplary_debug_instance, debug_level_wanted):
        """This method tests set_level() method."""
        exemplary_debug_instance.set_level(debug_level_wanted)
        assert exemplary_debug_instance.debug_level == debug_level_wanted

    def test_enable(self, exemplary_debug_instance):
        """This method tests enable() method."""
        exemplary_debug_instance.enable(True)
        assert exemplary_debug_instance.debug_enabled is True

        exemplary_debug_instance.enable(False)
        assert exemplary_debug_instance.debug_enabled is False

    def test_print_not_enabled(self):
        """This method tests the print() method when debug is not enabled."""
        assert True  # Nothing to test yet.

    def test_print_uart_channel(self, mocker, exemplary_debug_instance):
        """This method tests the printing method if it can print on UART channel."""
        mocker.patch("machine.UART.write")

        exemplary_debug_instance.set_channel(DebugChannel.UART)
        message_one = "An example"
        message_two = "print message."
        exemplary_debug_instance.print(message_one, message_two)

        UART.write.assert_any_call(message_one)
        UART.write.assert_any_call(" ")
        UART.write.assert_any_call(message_two)
        UART.write.assert_any_call("\n")

    def test_print_usbc_channel(self, mocker, exemplary_debug_instance):
        """This method tests the printing method if it can print on USBC channel."""
        mocker.patch("builtins.print")

        exemplary_debug_instance.set_channel(DebugChannel.USBC)
        message_one = "An example"
        message_two = "print message."
        exemplary_debug_instance.print(message_one, message_two)

        print.assert_called_with(message_one, message_two)

    def test_debug(self, mocker, exemplary_debug_instance):
        """This method tests debug() method with all cases."""
        mocker.patch("builtins.print")

        print.reset_mock()
        # Case 0: Not Enabled and Level is Above
        exemplary_debug_instance.enable(False)
        exemplary_debug_instance.set_level(DebugLevel.WARNING)
        exemplary_debug_instance.debug("This is a debug message but 0.")
        print.assert_not_called()

        print.reset_mock()
        # Case 1: Not Enabled and Level is Below or Equal
        exemplary_debug_instance.enable(False)
        exemplary_debug_instance.set_level(DebugLevel.DEBUG)
        exemplary_debug_instance.debug("This is a debug message but 1.")
        print.assert_not_called()

        print.reset_mock()
        # Case 2: Enabled and Level is Above
        exemplary_debug_instance.enable(True)
        exemplary_debug_instance.set_level(DebugLevel.WARNING)
        exemplary_debug_instance.debug("This is a debug message but 2.")
        print.assert_not_called()

        print.reset_mock()
        # Case 3: Enabled and Level is Below or Equal
        exemplary_debug_instance.enable(True)
        exemplary_debug_instance.set_level(DebugLevel.DEBUG)
        exemplary_debug_instance.debug("This is a debug message but 3.")
        print.assert_called_once_with("DEBUG:", "This is a debug message but 3.")

    def test_info(self, mocker, exemplary_debug_instance):
        """This method tests info() method with all cases."""
        mocker.patch("builtins.print")

        print.reset_mock()
        # Case 0: Not Enabled and Level is Above
        exemplary_debug_instance.enable(False)
        exemplary_debug_instance.set_level(DebugLevel.WARNING)
        exemplary_debug_instance.info("This is an info message but 0.")
        print.assert_not_called()

        print.reset_mock()
        # Case 1: Not Enabled and Level is Below or Equal
        exemplary_debug_instance.enable(False)
        exemplary_debug_instance.set_level(DebugLevel.DEBUG)
        exemplary_debug_instance.info("This is an info message but 1.")
        print.assert_not_called()

        print.reset_mock()
        # Case 2: Enabled and Level is Above
        exemplary_debug_instance.enable(True)
        exemplary_debug_instance.set_level(DebugLevel.WARNING)
        exemplary_debug_instance.info("This is an info message but 2.")
        print.assert_not_called()

        print.reset_mock()
        # Case 3: Enabled and Level is Below or Equal
        exemplary_debug_instance.enable(True)
        exemplary_debug_instance.set_level(DebugLevel.DEBUG)
        exemplary_debug_instance.info("This is an info message but 3.")
        print.assert_called_once_with("INFO:", "This is an info message but 3.")

    def test_warning(self, mocker, exemplary_debug_instance):
        """This method tests warning() method with all cases."""
        mocker.patch("builtins.print")

        print.reset_mock()
        # Case 0: Not Enabled and Level is Above
        exemplary_debug_instance.enable(False)
        exemplary_debug_instance.set_level(DebugLevel.ERROR)
        exemplary_debug_instance.warning("This is a warning message but 0.")
        print.assert_not_called()

        print.reset_mock()
        # Case 1: Not Enabled and Level is Below or Equal
        exemplary_debug_instance.enable(False)
        exemplary_debug_instance.set_level(DebugLevel.DEBUG)
        exemplary_debug_instance.warning("This is a warning message but 1.")
        print.assert_not_called()

        print.reset_mock()
        # Case 2: Enabled and Level is Above
        exemplary_debug_instance.enable(True)
        exemplary_debug_instance.set_level(DebugLevel.ERROR)
        exemplary_debug_instance.warning("This is a warning message but 2.")
        print.assert_not_called()

        print.reset_mock()
        # Case 3: Enabled and Level is Below or Equal
        exemplary_debug_instance.enable(True)
        exemplary_debug_instance.set_level(DebugLevel.WARNING)
        exemplary_debug_instance.warning("This is a warning message but 3.")
        print.assert_called_once_with("WARNING:", "This is a warning message but 3.")

    def test_error(self, mocker, exemplary_debug_instance):
        """This method tests error() method with all cases."""
        mocker.patch("builtins.print")

        print.reset_mock()
        # Case 0: Not Enabled and Level is Above
        exemplary_debug_instance.enable(False)
        exemplary_debug_instance.set_level(DebugLevel.CRITICAL)
        exemplary_debug_instance.warning("This is an error message but 0.")
        print.assert_not_called()

        print.reset_mock()
        # Case 1: Not Enabled and Level is Below or Equal
        exemplary_debug_instance.enable(False)
        exemplary_debug_instance.set_level(DebugLevel.DEBUG)
        exemplary_debug_instance.warning("This is an error message but 1.")
        print.assert_not_called()

        print.reset_mock()
        # Case 2: Enabled and Level is Above
        exemplary_debug_instance.enable(True)
        exemplary_debug_instance.set_level(DebugLevel.CRITICAL)
        exemplary_debug_instance.warning("This is an error message but 2.")
        print.assert_not_called()

        print.reset_mock()
        # Case 3: Enabled and Level is Below or Equal
        exemplary_debug_instance.enable(True)
        exemplary_debug_instance.set_level(DebugLevel.ERROR)
        exemplary_debug_instance.error("This is an error message but 3.")
        print.assert_called_once_with("ERROR:", "This is an error message but 3.")

    def test_critical(self, mocker, exemplary_debug_instance):
        """This method tests critical() method with all cases."""
        mocker.patch("builtins.print")

        print.reset_mock()
        # Case 0: Not Enabled
        exemplary_debug_instance.enable(False)
        exemplary_debug_instance.set_level(DebugLevel.CRITICAL)
        exemplary_debug_instance.critical("This is a critical message but 0.")
        print.assert_not_called()

        print.reset_mock()
        # Case 1: Enabled
        exemplary_debug_instance.enable(True)
        exemplary_debug_instance.set_level(DebugLevel.CRITICAL)
        exemplary_debug_instance.critical("This is a critical message but 1.")
        print.assert_called_once_with("CRITICAL:", "This is a critical message but 1.")

    def test_focus(self, mocker, exemplary_debug_instance):
        """This method tests focus() method with all cases."""
        mocker.patch("builtins.print")

        print.reset_mock()
        # Case 0: Not Enabled and Level is Above
        exemplary_debug_instance.enable(False)
        exemplary_debug_instance.set_level(DebugLevel.CRITICAL)
        exemplary_debug_instance.focus("This is a focus message but 0.")
        print.assert_not_called()

        print.reset_mock()
        # Case 1: Not Enabled and Level is Below or Equal
        exemplary_debug_instance.enable(False)
        exemplary_debug_instance.set_level(DebugLevel.FOCUS)
        exemplary_debug_instance.focus("This is a focus message but 1.")
        print.assert_not_called()

        print.reset_mock()
        # Case 2: Enabled and Level is Above
        exemplary_debug_instance.enable(True)
        exemplary_debug_instance.set_level(DebugLevel.CRITICAL)
        exemplary_debug_instance.focus("This is a focus message but 2.")
        print.assert_not_called()

        print.reset_mock()
        # Case 3: Enabled and Level is Below or Equal
        exemplary_debug_instance.enable(True)
        exemplary_debug_instance.set_level(DebugLevel.FOCUS)
        exemplary_debug_instance.focus("This is a focus message but 3.")
        print.assert_called_once_with("FOCUS:", "This is a focus message but 3.")
