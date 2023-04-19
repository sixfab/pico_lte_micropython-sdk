"""
Test module for the modules.base module.
"""

import pytest
from machine import Pin

from pico_lte.modules.base import Base
from pico_lte.utils.atcom import ATCom
from pico_lte.utils.status import Status


class TestBase:
    """
    Test class for Base.
    """

    @pytest.fixture
    def base(self):
        """This fixture returns a Base instance."""
        atcom = ATCom()
        return Base(atcom)

    def test_init_constructor(self, base):
        """This method tests the atcom attribute."""
        assert isinstance(base.atcom, ATCom)

    def test_power_on_off(self, mocker, base):
        """This method tests power_on_off() method."""
        mocker.patch("time.sleep")
        mocking = mocker.patch("machine.Pin.value")

        base.power_on_off()

        assert mocking.call_count == 2
        mocking.assert_any_call(1)
        mocking.assert_any_call(0)

    @pytest.mark.parametrize("status_pin_value", [0, 1])
    def test_power_status_response(self, mocker, base, status_pin_value):
        """This method tests the power_status() method by mocking Pin value."""
        mocking = mocker.patch("core.modules.base.Pin.value", return_value=status_pin_value)
        result = base.power_status()

        assert mocking.call_count == 2
        assert result == status_pin_value

    @pytest.mark.parametrize(
        "start_time, stop_time, power_status", [(0, 15, 0), (0, 31, 0), (0, 31, 1)]
    )
    def test_wait_until_status_on_with_default_timeout(
        self, mocker, base, start_time, stop_time, power_status
    ):
        """This method tests the wait_status_on() with mocked time."""
        mocker.patch("time.sleep")
        mocker.patch("time.time", side_effect=[start_time, stop_time, stop_time + 30])
        mocker.patch("core.modules.base.Base.power_status", return_value=power_status)

        result = base.wait_until_status_on()

        # If the power_status is not 0, and timeout has reached, we may expect timeout response.
        expected_result = {"status": Status.TIMEOUT, "response": "Timeout"}
        if power_status == 0 and stop_time - start_time < 30:
            expected_result = {"status": Status.SUCCESS, "response": "Success"}

        assert result == expected_result

    @pytest.mark.parametrize(
        "mocked_result",
        [
            {"status": Status.SUCCESS, "response": "OK"},
            {"status": Status.SUCCESS, "response": "APP RDY"},
            {"status": Status.TIMEOUT, "response": "timeout"},
        ],
    )
    def test_check_communication(self, mocker, base, mocked_result):
        """This method tests check_communication() with mocked ATCom."""
        mocking = mocker.patch("core.utils.atcom.ATCom.send_at_comm", return_value=mocked_result)
        result = base.check_communication()

        mocking.assert_called_once_with("AT")
        assert result == mocked_result

    @pytest.mark.parametrize(
        "start_time, stop_time, mocked_result",
        [
            (0, 15, {"status": Status.SUCCESS, "response": "OK"}),
            (0, 29, {"status": Status.ERROR, "reponse": "error"}),
            (0, 31, {"status": Status.ERROR, "reponse": "error"}),
        ],
    )
    def test_wait_until_modem_ready_to_communicate(
        self, mocker, base, start_time, stop_time, mocked_result
    ):
        """This method tests the wait_until_modem_ready_to_communicate() with mocked time."""
        mocker.patch("time.sleep")
        mocker.patch("time.time", side_effect=[start_time, stop_time, stop_time + 30])
        mocker.patch("core.utils.atcom.ATCom.send_at_comm", return_value=mocked_result)

        result = base.wait_until_modem_ready_to_communicate()

        # If the status is ERROR, or the timeout reached, we may expect a timeout response.
        expected_result = {"status": Status.TIMEOUT, "response": "timeout"}
        if mocked_result["status"] == Status.SUCCESS and stop_time - start_time < 30:
            expected_result = {"status": Status.SUCCESS, "response": "OK"}

        assert result == expected_result

    @pytest.mark.parametrize(
        "mocked_result",
        [
            {"status": Status.SUCCESS, "response": "OK"},
            {"status": Status.TIMEOUT, "response": "timeout"},
        ],
    )
    def test_set_echo_off(self, mocker, base, mocked_result):
        """This method tests the set_echo_off() with mocked ATCom."""
        mocking = mocker.patch("core.utils.atcom.ATCom.send_at_comm", return_value=mocked_result)

        result = base.set_echo_off()
        mocking.assert_called_once_with("ATE0")
        assert result == mocked_result

    @pytest.mark.parametrize(
        "mocked_result",
        [
            {"status": Status.SUCCESS, "response": "OK"},
            {"status": Status.TIMEOUT, "response": "timeout"},
        ],
    )
    def test_set_echo_on(self, mocker, base, mocked_result):
        """This method tests the set_echo_on() with mocked ATCom."""
        mocking = mocker.patch("core.utils.atcom.ATCom.send_at_comm", return_value=mocked_result)

        result = base.set_echo_on()
        mocking.assert_called_once_with("ATE1")
        assert result == mocked_result

    @pytest.mark.parametrize(
        "mocked_result",
        [
            {"status": Status.SUCCESS, "response": ["+CPIN: READY", "OK"]},
            {"status": Status.TIMEOUT, "response": "timeout"},
        ],
    )
    def test_check_sim_ready(self, mocker, base, mocked_result):
        """This method tests the check_sim_ready() with mocked ATCom."""
        mocking = mocker.patch("core.utils.atcom.ATCom.send_at_comm", return_value=mocked_result)

        result = base.check_sim_ready()
        mocking.assert_called_once_with("AT+CPIN?", ["+CPIN: READY"])
        assert result == mocked_result

    @pytest.mark.parametrize(
        "mocked_result",
        [
            {"status": Status.SUCCESS, "response": ["+CPIN: READY", "OK"]},
            {"status": Status.TIMEOUT, "response": "timeout"},
        ],
    )
    def test_enter_sim_pin_code(self, mocker, base, mocked_result):
        """This method tests the enter_sim_pin_code() with mocked ATCom."""
        mocking = mocker.patch("core.utils.atcom.ATCom.send_at_comm", return_value=mocked_result)

        result = base.enter_sim_pin_code(1234)
        mocking.assert_called_once_with('AT+CPIN="1234"')
        assert result == mocked_result

    @pytest.mark.parametrize(
        "mocked_result",
        [
            {
                "status": Status.SUCCESS,
                "response": ["+QCCID: 12345678910111213140", "OK"],
            },
            {"status": Status.TIMEOUT, "response": "timeout"},
        ],
    )
    def test_get_sim_iccid(self, mocker, base, mocked_result):
        """This method tests the get_sim_iccid() method with mocked ATCom."""
        mocking = mocker.patch("core.utils.atcom.ATCom.send_at_comm", return_value=mocked_result)

        result = base.get_sim_iccid()

        mocking.assert_called_once_with("AT+QCCID")
        assert result["status"] == mocked_result["status"]
        assert result["response"] == mocked_result["response"]
        assert result["value"] in ["12345678910111213140", None]

    @pytest.mark.parametrize("scan_mode", [0, 1, 3])
    def test_config_network_scan_mode(self, mocker, base, scan_mode):
        """This method tests the config_network_scan_mode() method with mocked ATCom."""
        mocked_result = {"status": Status.SUCCESS, "response": ["OK"]}
        mocking = mocker.patch("core.utils.atcom.ATCom.send_at_comm", return_value=mocked_result)

        result = base.config_network_scan_mode(scan_mode)

        mocking.assert_called_once_with(f'AT+QCFG="nwscanmode",{scan_mode}')
        assert result == mocked_result

    @pytest.mark.parametrize("scan_sequence", ["00", "01", "02", "03"])
    def test_config_network_scan_sequence(self, mocker, base, scan_sequence):
        """This method tests the config_network_scan_sequence() method with mocked ATCom."""
        mocked_result = {"status": Status.SUCCESS, "response": ["OK"]}
        mocking = mocker.patch("core.utils.atcom.ATCom.send_at_comm", return_value=mocked_result)

        result = base.config_network_scan_sequence(scan_sequence)

        mocking.assert_called_once_with(f'AT+QCFG="nwscanseq",{scan_sequence}')
        assert result == mocked_result

    @pytest.mark.parametrize("iotopmode", [0, 1, 2])
    def test_config_network_iot_operation_mode(self, mocker, base, iotopmode):
        """This method tests the config_network_iot_operation_mode() method with mocked ATCom."""
        mocked_result = {"status": Status.SUCCESS, "response": ["OK"]}
        mocking = mocker.patch("core.utils.atcom.ATCom.send_at_comm", return_value=mocked_result)

        result = base.config_network_iot_operation_mode(iotopmode)

        mocking.assert_called_once_with(f'AT+QCFG="iotopmode",{iotopmode}')
        assert result == mocked_result
