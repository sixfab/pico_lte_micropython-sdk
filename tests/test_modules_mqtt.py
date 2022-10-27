"""
Test module for the modules.mqtt module.
"""

import pytest

from core.modules.mqtt import MQTT
from core.utils.atcom import ATCom
from core.utils.status import Status
from core.temp import config



def default_response_types():
    """This method returns default and mostly-used responses for ATCom messages."""
    return [
        {"status": Status.SUCCESS, "response": ["OK"]},
        {"status": Status.TIMEOUT, "response": "timeout"},
        {"status": Status.ERROR, "response": ["ERROR"]},
    ]


class TestMQTT:
    """
    Test class for MQTT.
    """

    @pytest.fixture
    def mqtt(self):
        """This fixture returns a MQTT instance."""
        atcom = ATCom()
        return MQTT(atcom)

    @staticmethod
    def mock_send_at_comm(mocker, responses_to_return, is_side_effect=False):
        """This is a wrapper function to repeated long mocker.patch() statements."""
        patch_location = "core.utils.atcom.ATCom.send_at_comm"
        if is_side_effect:
            return mocker.patch(patch_location, side_effect=responses_to_return)
        return mocker.patch(patch_location, return_value=responses_to_return)

    def test_constructor(self, mqtt):
        """This method tests if the constructor method sets right attributes."""
        assert isinstance(mqtt.atcom, ATCom)

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_version_config_default(self, mocker, mqtt, mocked_response):
        """This method tests set_version_config() with its default parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.set_version_config()

        mocking.assert_called_once_with('AT+QMTCFG="version",0,4')
        assert result == mocked_response

    @pytest.mark.parametrize("params", [(1, 3), (5, 4), (1, 6)])
    def test_set_version_config_parameters(self, mocker, mqtt, params):
        """This method tests set_version_config() with given arbitrary parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, None)
        mqtt.set_version_config(cid=params[0], version=params[1])

        mocking.assert_called_once_with(f'AT+QMTCFG="version",{params[0]},{params[1]}')

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_pdpcid_config_default(self, mocker, mqtt, mocked_response):
        """This method tests set_pdpcid_config() with its default parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.set_pdpcid_config()

        mocking.assert_called_once_with('AT+QMTCFG="pdpcid",0,0')
        assert result == mocked_response

    @pytest.mark.parametrize("params", [(1, 3), (5, 4), (2, 6)])
    def test_set_pdpcid_config_parameters(self, mocker, mqtt, params):
        """This method tests set_pdpcid_config() with given arbitrary parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, None)
        mqtt.set_pdpcid_config(cid=params[0], pdpcid=params[1])

        mocking.assert_called_once_with(f'AT+QMTCFG="pdpcid",{params[0]},{params[1]}')

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_ssl_mode_config_default(self, mocker, mqtt, mocked_response):
        """This method tests set_ssl_mode_config() with its default parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.set_ssl_mode_config()

        mocking.assert_called_once_with('AT+QMTCFG="SSL",0,1,2')
        assert result == mocked_response

    @pytest.mark.parametrize("params", [(5, 0, 1), (3, 1, 2), (6, 2, -1)])
    def test_set_ssl_mode_config_parameters(self, mocker, mqtt, params):
        """This method tests set_ssl_mode_config() with given arbitrary parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, None)
        mqtt.set_ssl_mode_config(
            cid=params[0], ssl_mode=params[1], ssl_ctx_index=params[2]
        )

        mocking.assert_called_once_with(
            f'AT+QMTCFG="SSL",{params[0]},{params[1]},{params[2]}'
        )

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_keep_alive_time_config_default(self, mocker, mqtt, mocked_response):
        """This method tests set_keep_alive_time_config() with its default parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.set_keep_alive_time_config()

        mocking.assert_called_once_with('AT+QMTCFG="keepalive",0,120')
        assert result == mocked_response

    @pytest.mark.parametrize("params", [(0, 60), (1, 75)])
    def test_set_keep_alive_time_config_parameters(self, mocker, mqtt, params):
        """This method tests set_keep_alive_time_config() with given arbitrary parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, None)
        mqtt.set_keep_alive_time_config(cid=params[0], keep_alive_time=params[1])

        mocking.assert_called_once_with(
            f'AT+QMTCFG="keepalive",{params[0]},{params[1]}'
        )

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_clean_session_config_default(self, mocker, mqtt, mocked_response):
        """This method tests set_clean_session_config() with its default parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.set_clean_session_config()

        mocking.assert_called_once_with('AT+QMTCFG="clean_session",0,0')
        assert result == mocked_response

    @pytest.mark.parametrize("params", [(0, 0), (0, 1), (1, 0)])
    def test_set_clean_session_config_parameters(self, mocker, mqtt, params):
        """This method tests set_clean_session_config() with given arbitrary parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, None)
        mqtt.set_clean_session_config(cid=params[0], clean_session=params[1])

        mocking.assert_called_once_with(
            f'AT+QMTCFG="clean_session",{params[0]},{params[1]}'
        )

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_timeout_config_default(self, mocker, mqtt, mocked_response):
        """This method tests set_timeout_config() with its default parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.set_timeout_config()

        mocking.assert_called_once_with('AT+QMTCFG="timeout",0,5,3,0')
        assert result == mocked_response

    @pytest.mark.parametrize("params", [(0, 5, 3, 4), (1, 3, 1, 2), (2, 10, 4, 0)])
    def test_set_timeout_config_parameters(self, mocker, mqtt, params):
        """This method tests set_timeout_config() with given arbitrary parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, None)
        mqtt.set_timeout_config(
            cid=params[0],
            timeout=params[1],
            retry_count=params[2],
            timeout_notice=params[3],
        )

        mocking.assert_called_once_with(
            f'AT+QMTCFG="timeout",{params[0]},{params[1]},{params[2]},{params[3]}'
        )

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_will_config_default(self, mocker, mqtt, mocked_response):
        """This method tests set_will_config() with its default parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.set_will_config("example", "message")

        mocking.assert_called_once_with('AT+QMTCFG="will",0,0,0,0,"example","message"')
        assert result == mocked_response

    @pytest.mark.parametrize(
        "params", [("will", "msg", 0, 1, 2, 1), ("try", "xyz", 1, 0, 1, 0)]
    )
    def test_set_will_config_parameters(self, mocker, mqtt, params):
        """This method tests set_will_config() with given arbitrary parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, None)
        mqtt.set_will_config(
            will_topic=params[0],
            will_message=params[1],
            cid=params[2],
            will_flag=params[3],
            will_qos=params[4],
            will_retain=params[5],
        )

        mocking.assert_called_once_with(
            f'AT+QMTCFG="will",{params[2]},{params[3]},{params[4]},'+\
            f'{params[5]},"{params[0]}","{params[1]}"'
        )

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_message_recieve_mode_config_default(self, mocker, mqtt, mocked_response):
        """This method tests set_message_recieve_mode_config() with its default parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.set_message_recieve_mode_config()

        mocking.assert_called_once_with('AT+QMTCFG="message_recieve_mode",0,0')
        assert result == mocked_response

    @pytest.mark.parametrize("params", [(0, 0), (0, 1), (1, 0)])
    def test_set_message_recieve_mode_config_parameters(self, mocker, mqtt, params):
        """This method tests set_message_recieve_mode_config() with given arbitrary parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, None)
        mqtt.set_message_recieve_mode_config(cid=params[0], message_recieve_mode=params[1])

        mocking.assert_called_once_with(
            f'AT+QMTCFG="message_recieve_mode",{params[0]},{params[1]}'
        )

    def test_open_connection_all_none(self, mocker, mqtt):
        """This method tests open_connect() when there is no given parameter,
        and config is empty.
        """
        mocker.patch("core.modules.mqtt.get_parameter", return_value=None)
        result = mqtt.open_connection()

        assert result["status"] == Status.ERROR
        assert result["response"] == "Missing parameters : host"

    def test_open_connection_with_host_parameter_no_config(self, mocker, mqtt):
        """This method tests open_connect() when only host parameter is set,
        but there is no information about port on neither config neither
        arguments.
        """
        # Mock config again not the be mixed with old test injections.
        config["params"] = {}

        mocked_responses = [
            {"status": Status.SUCCESS, "response": "OK"},
            {"status": Status.SUCCESS, "response": ["+QMTOPEN: 0,0"]},
        ]
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_responses[0])
        get_urc_response_loc = "core.utils.atcom.ATCom.get_urc_response"
        mocker.patch(get_urc_response_loc, return_value=mocked_responses[1])
        mqtt.open_connection(host="https://sixfab.com")

        mocking.assert_any_call('AT+QMTOPEN=0,"https://sixfab.com",8883')

    def test_open_connection_with_all_parameters(self, mocker, mqtt):
        """This method tests open_connect() when all parameters are set,
        and both atcom succeds.
        """
        # Mock config again not the be mixed with old test injections.
        config["params"] = {}

        mocked_responses = [
            {"status": Status.SUCCESS, "response": "OK"},
            {"status": Status.SUCCESS, "response": ["+QMTOPEN: 0,0"]},
        ]
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_responses[0])
        get_urc_response_loc = "core.utils.atcom.ATCom.get_urc_response"
        mocker.patch(get_urc_response_loc, return_value=mocked_responses[1])
        mqtt.open_connection(host="https://sixfab.com", port="1111")

        mocking.assert_any_call('AT+QMTOPEN=0,"https://sixfab.com",1111')

    def test_open_connection_without_success_atcom(self, mocker, mqtt):
        """This method tests open_connect() when there is no success
        answer from ATCom.send_at_comm().
        """
        mocked_response = default_response_types()[2]
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.open_connection(host="https://sixfab.com")

        mocking.assert_any_call('AT+QMTOPEN=0,"https://sixfab.com",8883')
        assert result["status"] == mocked_response["status"]
        assert result["response"] == mocked_response["response"]

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_has_opened_connection_default(self, mocker, mqtt, mocked_response):
        """This method tests has_opened_connection() with its default parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.has_opened_connection()

        mocking.assert_called_once_with("AT+QMTOPEN?", "+QMTOPEN: 0")
        assert result == mocked_response

    @pytest.mark.parametrize("params", [0, 1, 2, 3, 5])
    def test_has_opened_connection_parameters(self, mocker, mqtt, params):
        """This method tests has_opened_connection() with given parameters."""
        mocking = TestMQTT.mock_send_at_comm(mocker, default_response_types()[0])
        mqtt.has_opened_connection(params)

        mocking.assert_called_once_with("AT+QMTOPEN?", f"+QMTOPEN: {params}")

    def test_close_connection_default(self, mocker, mqtt):
        """This method tests close_connection() with its default parameters."""
        mocked_responses = [
            {"status": Status.SUCCESS, "response": "OK"},
            {"status": Status.SUCCESS, "response": ["+QMTCLOSE: 0,0"]},
        ]
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_responses[0])
        get_urc_response_loc = "core.utils.atcom.ATCom.get_urc_response"
        mocker.patch(get_urc_response_loc, return_value=mocked_responses[1])
        result = mqtt.close_connection()

        mocking.assert_any_call("AT+QMTCLOSE=0")
        assert result == mocked_responses[1]

    @pytest.mark.parametrize("params", [0, 1, 2, 3, 5])
    def test_close_connection_parameters(self, mocker, mqtt, params):
        """This method tests close_connection() with given parameters."""
        mocked_responses = [
            {"status": Status.SUCCESS, "response": "OK"},
            {"status": Status.SUCCESS, "response": ["+QMTCLOSE: 0,0"]},
        ]
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_responses[0])
        get_urc_response_loc = "core.utils.atcom.ATCom.get_urc_response"
        mocker.patch(get_urc_response_loc, return_value=mocked_responses[1])
        mqtt.close_connection(params)

        mocking.assert_called_once_with(f"AT+QMTCLOSE={params}")

    def test_close_connection_error_at_send(self, mocker, mqtt):
        """This method tests close_connection() with a error response
        from atcom.send_at_comm() code line.
        """
        mocked_response = default_response_types()[2]
        TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.close_connection()

        assert result == mocked_response
