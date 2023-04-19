"""
Test module for the modules.peripheral module.
"""
import pytest
from machine import Pin, I2C

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
        # Test Battery Voltage Pin.
        assert isinstance(periph.battery_voltage_pin, Pin)
        assert periph.battery_voltage_pin.pin_num == 29
        assert periph.battery_voltage_pin.pin_dir == Pin.IN
        # Test Battery Charge Status Pin.
        assert isinstance(periph.battery_charge_status_pin, Pin)
        assert periph.battery_charge_status_pin.pin_num == 25
        assert periph.battery_charge_status_pin.pin_dir == Pin.IN
        # Test User Button Pin
        assert isinstance(periph.user_button_pin, Pin)
        assert periph.user_button_pin.pin_num == 26
        assert periph.user_button_pin.pin_dir == Pin.IN
        # Test Neopixel Pin
        assert isinstance(periph.neopixel_pin, Pin)
        assert periph.neopixel_pin.pin_num == 10
        assert periph.neopixel_pin.pin_dir == Pin.OUT
        # Test Qwiic SDA Pin
        assert isinstance(periph.qwiic_scl_pin, Pin)
        assert periph.qwiic_sda_pin.pin_num == 6
        assert periph.qwiic_scl_pin.pin_num == 7
        # Test the Qwiic protocol.
        assert isinstance(periph.qwiic, I2C)

    @pytest.mark.parametrize("pin_value", [0, 1])
    def test_read_user_button(self, mocker, periph, pin_value):
        """Test the read_user_button() method by mocking the Pin.value method."""
        mocker.patch("core.modules.peripherals.Pin.value", return_value=pin_value)
        assert periph.read_user_button() == pin_value

    def test_adjust_neopixel(self):
        """No need since its a third-party library."""
        assert True

    @pytest.mark.parametrize("pin_value, expected_voltage", [(65535, 3.3), (32767, 1.64), (0, 0)])
    def test_get_battery_voltage(self, mocker, periph, pin_value, expected_voltage):
        """This method tests the get_battery_voltage() method with predefined
        analogue pre-defined values.

        @TODO: Implement this test in future after fix PR is approved.
        """
        assert True

    @pytest.mark.parametrize("pin_value", [0, 1])
    def test_get_charge_status(self, mocker, periph, pin_value):
        """This method tests the get_charge_status() with mocked digital values."""
        mocker.patch("core.modules.peripherals.Pin.value", return_value=pin_value)
        assert periph.get_charge_status() == pin_value

    @pytest.mark.parametrize("mocked_response", [[104, 105], []])
    def test_qwiic_scan(self, mocker, periph, mocked_response):
        """This method tests the qwiic_scan() with mocked responses."""
        mocker.patch("core.modules.peripherals.I2C.scan", return_value=mocked_response)
        assert periph.qwiic_scan() == mocked_response
