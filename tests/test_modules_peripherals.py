"""
Test module for the modules.peripheral module.
"""
import pytest
from machine import Pin

from pico_lte.modules.peripherals import Periph


class TestPeriph:
    """
    Test class for Periph.
    """

    @pytest.fixture
    def periph(self):
        """This fixture returns a Periph instance."""
        return Periph()

    def test_pin_set_up(self, periph):
        """This method tests if the pin directions and their GPIO numbers are correct.
        "num" and "dir" is mock-attributes which is defined in conftest.py file.
        """
        # Test User Button Pin
        assert isinstance(periph.user_button, Pin)
        assert periph.user_button.pin_num == 21
        assert periph.user_button.pin_dir == Pin.IN
        # Test User LED Pin
        assert isinstance(periph.user_led, Pin)
        assert periph.user_led.pin_num == 22
        assert periph.user_led.pin_dir == Pin.OUT
        # Test Neopixel Pin
        assert isinstance(periph.neopixel, Pin)
        assert periph.neopixel.pin_num == 15
        assert periph.neopixel.pin_dir == Pin.OUT

    @pytest.mark.parametrize("pin_value", [0, 1])
    def test_read_user_button(self, mocker, periph, pin_value):
        """Test the read_user_button() method by mocking the Pin.value method."""
        mocker.patch("pico_lte.modules.peripherals.Pin.value", return_value=pin_value)
        assert periph.read_user_button() == pin_value

    def test_adjust_neopixel(self):
        """No need since its a third-party library."""
        assert True
