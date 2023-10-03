"""
Test module for the modules.gps module.
"""

import pytest

from pico_lte.modules.gps import GPS
from pico_lte.utils.atcom import ATCom
from pico_lte.utils.status import Status


def default_response_types():
    """This method returns default and mostly-used responses for ATCom messages."""
    return [
        {"status": Status.SUCCESS, "response": ["OK"]},
        {"status": Status.TIMEOUT, "response": "timeout"},
    ]


class TestGPS:
    """
    Test class for GPS.
    """

    @pytest.fixture
    def gps(self):
        """This fixture returns a GPS instance."""
        atcom = ATCom()
        return GPS(atcom)

    @staticmethod
    def mock_send_at_comm(mocker, responses_to_return):
        """This is a wrapper function to repeated long mocker.patch() statements."""
        return mocker.patch(
            "pico_lte.utils.atcom.ATCom.send_at_comm", return_value=responses_to_return
        )

    def test_constructor(self, gps):
        """This method tests the __init__ constructor."""
        assert isinstance(gps.atcom, ATCom)

    @pytest.mark.parametrize(
        "mocked_response",
        [
            {
                "status": Status.SUCCESS,
                "response": ["APP RDY", '+QGPSCFG: "priority",0,3', "OK"],
            },
            {"status": Status.SUCCESS, "response": ['+QGPSCFG: "priority",1,2', "OK"]},
        ]
        + default_response_types(),
    )
    def test_get_priority(self, mocker, gps, mocked_response):
        """This method tests the get_priority() with mocked ATCom responses."""
        mocking = TestGPS.mock_send_at_comm(mocker, mocked_response)
        result = gps.get_priority()

        mocking.assert_called_once_with('AT+QGPSCFG="priority"')
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_priority(self, mocker, gps, mocked_response):
        """This method tests the set_priority() with mocked ATCom responses."""
        mocking = TestGPS.mock_send_at_comm(mocker, mocked_response)

        for priority in [0, 1]:
            result = gps.set_priority(priority)
            mocking.assert_any_call(f'AT+QGPSCFG="priority",{priority}')
            assert result == mocked_response

    @pytest.mark.parametrize(
        "mocked_response",
        [{"status": Status.SUCCESS, "response": ["+CME ERROR: 504"]}]
        + default_response_types(),
    )
    def test_turn_on_default_parameters(self, mocker, gps, mocked_response):
        """This method tests the turn_on() with predefined parameters."""
        mocking = TestGPS.mock_send_at_comm(mocker, mocked_response)
        result = gps.turn_on()

        mocking.assert_called_once_with("AT+QGPS=1,3,0,1")
        assert result == mocked_response

    @pytest.mark.parametrize(
        "mode, accuracy, fix_count, fix_rate",
        [(1, 1, 45, 5), (2, 2, 1000, 11), (3, 3, 0, 1)],
    )
    def test_turn_on_with_different_parameters(
        self, mocker, gps, mode, accuracy, fix_count, fix_rate
    ):
        """This method tests the turn_on() with using parameter options."""
        mocked_response = {"status": Status.SUCCESS, "response": ["OK"]}
        mocking = TestGPS.mock_send_at_comm(mocker, mocked_response)
        result = gps.turn_on(mode, accuracy, fix_count, fix_rate)

        mocking.assert_called_once_with(
            f"AT+QGPS={mode},{accuracy},{fix_count},{fix_rate}"
        )
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_turn_off(self, mocker, gps, mocked_response):
        """This method tests turn_off() with mocked ATCom responses."""
        mocking = TestGPS.mock_send_at_comm(mocker, mocked_response)
        result = gps.turn_off()

        mocking.assert_called_once_with("AT+QGPSEND")
        assert result == mocked_response

    @pytest.mark.parametrize(
        "mocked_response",
        [
            {
                "status": Status.SUCCESS,
                "response": [
                    "+QGPSLOC: 061951.00,41.02044,28.99797,0.7,62.2,2,0.00,0.0,0.0,110513,09",
                    "OK",
                ],
            },
            {"status": Status.ERROR, "response": ["+CME ERROR: 516"]},
            {"status": Status.TIMEOUT, "response": "timeout"},
        ],
    )
    def test_get_location(self, mocker, gps, mocked_response):
        """This method tests get_location() with mocked ATCom responses."""
        mocking = TestGPS.mock_send_at_comm(mocker, mocked_response)
        result = gps.get_location()

        mocking.assert_called_once_with("AT+QGPSLOC=2", "+QGPSLOC: ")

        if result["status"] == Status.SUCCESS:
            assert result["value"] == ["41.02044", "28.99797"]
        assert result["status"] == mocked_response["status"]
        assert result["response"] == mocked_response["response"]
