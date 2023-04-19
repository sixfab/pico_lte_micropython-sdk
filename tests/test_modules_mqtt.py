"""
Test module for the modules.mqtt module.
"""

import pytest

from pico_lte.modules.mqtt import MQTT
from pico_lte.utils.atcom import ATCom
from pico_lte.utils.status import Status
from pico_lte.common import config


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
        mqtt.set_ssl_mode_config(cid=params[0], ssl_mode=params[1], ssl_ctx_index=params[2])

        mocking.assert_called_once_with(f'AT+QMTCFG="SSL",{params[0]},{params[1]},{params[2]}')

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

        mocking.assert_called_once_with(f'AT+QMTCFG="keepalive",{params[0]},{params[1]}')

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

        mocking.assert_called_once_with(f'AT+QMTCFG="clean_session",{params[0]},{params[1]}')

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

    @pytest.mark.parametrize("params", [("will", "msg", 0, 1, 2, 1), ("try", "xyz", 1, 0, 1, 0)])
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
            f'AT+QMTCFG="will",{params[2]},{params[3]},{params[4]},'
            + f'{params[5]},"{params[0]}","{params[1]}"'
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

        mocking.assert_called_once_with(f'AT+QMTCFG="message_recieve_mode",{params[0]},{params[1]}')

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

    @pytest.mark.parametrize(
        "mocked_response",
        [
            {"status": Status.ERROR, "response": ["+QMTOPEN: 0,5"]},
            {"status": Status.ERROR, "response": ["+QMTOPEN: 0,4"]},
            {"status": Status.ERROR, "response": ["+QMTOPEN: 0,3"]},
            {"status": Status.ERROR, "response": ["+QMTOPEN: 0,2"]},
            {"status": Status.ERROR, "response": ["+QMTOPEN: 0,1"]},
            default_response_types()[2],
        ],
    )
    def test_open_connection_without_success_atcom(self, mocker, mqtt, mocked_response):
        """This method tests open_connect() when there is no success
        answer from ATCom.send_at_comm().
        """
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.open_connection(host="https://sixfab.com")

        mocking.assert_any_call('AT+QMTOPEN=0,"https://sixfab.com",8883')
        assert result["status"] == mocked_response["status"]
        assert result["response"] == mocked_response["response"]

    @pytest.mark.parametrize(
        "mocked_response",
        [
            {
                "status": Status.SUCCESS,
                "response": [
                    "AT+QMTOPEN?\r",
                    '+QMTOPEN: 0,"mqtt.thingspeak.com",1883',
                    "OK",
                ],
            },
            {
                "status": Status.SUCCESS,
                "response": ["OK", "+QMTOPEN: 0,0"],
            },
            {
                "status": Status.ERROR,
                "response": ["APP RDY", "+QMTOPEN: 0,3"],
            },
            default_response_types()[1:2],
        ],
    )
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

    @pytest.mark.parametrize(
        "mocked_response",
        [
            {
                "status": Status.ERROR,
                "response": ['AT+QMTCONN=0,"PicoLTE"\r', "ERROR"],
            },
            {"status": Status.SUCCESS, "response": ['AT+QMTCONN=0,"PicoLTE"\r', "OK"]},
            {
                "status": Status.ERROR,
                "response": ['AT+QMTCONN=0,"PicoLTE"\r', "OK", "+QMTSTAT: 0,3"],
            },
            default_response_types()[1],
            default_response_types()[2],
        ],
    )
    def test_connect_broker_when_username_and_pass_is_none_without_config(
        self, mocker, mqtt, mocked_response
    ):
        """This method tests connect_broker() without parameters, and without
        pre-defined config file which includes username and password."""
        # Mock config again not the be mixed with old test injections.
        config["params"] = {}
        mocker.patch(
            "core.utils.atcom.ATCom.get_urc_response",
        )
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        mqtt.connect_broker()

        mocking.assert_called_once_with('AT+QMTCONN=0,"PicoLTE"')

    @pytest.mark.parametrize(
        "mocked_response",
        [
            {
                "status": Status.ERROR,
                "response": ['AT+QMTCONN=0,"PicoLTE","john","doe123"\r', "ERROR"],
            },
            {
                "status": Status.SUCCESS,
                "response": ['AT+QMTCONN=0,"PicoLTE","john","doe123"\r', "OK"],
            },
            {
                "status": Status.ERROR,
                "response": [
                    'AT+QMTCONN=0,"PicoLTE","john","doe123"\r',
                    "OK",
                    "+QMTSTAT: 0,4",
                ],
            },
            {
                "status": Status.ERROR,
                "response": ["OK", "+QMTCONN: 0,0,4"],
            },
            default_response_types()[1],
            default_response_types()[2],
        ],
    )
    def test_connect_broker_when_username_and_pass_is_none_with_config(
        self, mocker, mqtt, mocked_response
    ):
        """This method tests connect_broker() without parameters, and with
        pre-defined config file which includes username and password."""
        config["params"] = {"mqtts": {"username": "john", "password": "doe123"}}
        urc_response_patch = "core.utils.atcom.ATCom.get_urc_response"
        mocker.patch(urc_response_patch, return_value=mocked_response)
        mocking = TestMQTT.mock_send_at_comm(mocker, default_response_types()[0])
        result = mqtt.connect_broker()

        mocking.assert_called_once_with('AT+QMTCONN=0,"PicoLTE","john","doe123"')
        assert result == mocked_response

    def test_connect_broker_when_send_at_comm_return_error(self, mocker, mqtt):
        """This method tests connect_broker() when the send_at_comm() returns
        an error response.
        """
        mocked_response = {"status": Status.ERROR, "response": ["some", "error"]}
        TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.connect_broker()

        assert result == mocked_response

    @pytest.mark.parametrize(
        "mocked_response",
        [
            {"status": Status.SUCCESS, "response": ["+QMTCONN: 0,3", "OK"]},
            {"status": Status.ERROR, "response": ["+QMTCONN: 0,2", "OK"]},
            {"status": Status.ERROR, "response": ["+QMTCONN: 0,4", "OK"]},
            default_response_types()[1],
        ],
    )
    def test_is_connected_to_broker(self, mocker, mqtt, mocked_response):
        """This method tests is_connected_to_broker() if it calls the
        right AT commands.
        """
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.is_connected_to_broker()

        mocking.assert_called_once_with("AT+QMTCONN?", "+QMTCONN: 0,3")
        assert result == mocked_response

    @pytest.mark.parametrize(
        "mocked_response",
        [
            {"status": Status.SUCCESS, "response": ["OK", "+QMTDISC: 0,0"]},
            {"status": Status.ERROR, "response": ["OK", "+QMTDISC: 0,-1"]},
            {
                "status": Status.ERROR,
                "response": ["OK", "+QMTDISC: 0,-1", "+CME ERROR: X"],
            },
            default_response_types()[1],
        ],
    )
    def test_disconnect_broker_default(self, mocker, mqtt, mocked_response):
        """This method tests disconnect_broker() if it calls the
        right AT commands in default parameters.
        """
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.is_connected_to_broker()

        mocking.assert_called_once_with("AT+QMTCONN?", "+QMTCONN: 0,3")
        assert result == mocked_response

    @pytest.mark.parametrize("cid", range(0, 5))
    def test_disconnect_broker_parameters(self, mocker, mqtt, cid):
        """This method tests disconnect_broker() if it calls the
        right AT commands in default parameters.
        """
        mocked_response = {
            "status": Status.SUCCESS,
            "response": ["OK", "+QMTDISC: 0,0"],
        }
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        mqtt.is_connected_to_broker(cid)

        mocking.assert_called_once_with("AT+QMTCONN?", f"+QMTCONN: {cid},3")

    @pytest.mark.parametrize(
        "mocked_response",
        [
            {"status": Status.SUCCESS, "response": ["OK", "+QMTSUB: 0,1,0,0,1,2"]},
            {"status": Status.ERROR, "response": ["OK", "+QMTSUB: 0,1,2"]},
            {
                "status": Status.ERROR,
                "response": ["OK", "+QMTSUB: 0,1,2", "+CME ERROR: X"],
            },
        ],
    )
    def test_subscribe_topics_parameter(self, mocker, mqtt, mocked_response):
        """This method tests subscribe_topics() with parameter installation."""
        get_urc_response_patch = "core.utils.atcom.ATCom.get_urc_response"
        mocker.patch(get_urc_response_patch, return_value=mocked_response)
        mocking = TestMQTT.mock_send_at_comm(mocker, default_response_types()[0])
        topics_list = [("topic1", 0), ("topic2", 1), ("topic2", 2)]
        result = mqtt.subscribe_topics(topics=topics_list)

        command = 'AT+QMTSUB=0,1,"topic1",0,"topic2",1,"topic2",2'
        mocking.assert_called_once_with(command)
        assert result == mocked_response

    def test_subscribe_topics_default_without_config(self, mqtt):
        """This method tests subscribe_topics() with its default parameters
        without config file.
        """
        # Mock config again not the be mixed with old test injections.
        config["params"] = {}
        result = mqtt.subscribe_topics()

        assert result["status"] == Status.ERROR
        assert result["response"] == "Missing parameter : topics"

    def test_unsubscribe_topic_without_parameter(self, mqtt):
        """This method tests unsubscribe_topic() without any parameter."""
        with pytest.raises(TypeError):
            mqtt.unsubscribe_topic()

    @pytest.mark.parametrize(
        "mocked_response",
        [
            {
                "status": Status.SUCCESS,
                "response": ['AT+QMTUNS=0,1,"an_example_topic"\r', "OK"],
            },
            {
                "status": Status.SUCCESS,
                "response": ["+QMTUNS: 0,1,0", 'AT+QMTUNS=0,1,"xxx"\r', "OK"],
            },
            default_response_types()[1],
        ],
    )
    def test_unsubsribe_topic_ordinary(self, mocker, mqtt, mocked_response):
        """This method tests unsubscribe_topic() ordinary usage."""
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.unsubscribe_topic("an_example_topic")

        mocking.assert_called_once_with('AT+QMTUNS=0,1,"an_example_topic"')
        assert result == mocked_response

    @pytest.mark.parametrize("params", [("topic1", 2, 3), ("topic2", 0, 1), ("topic3", 5, 65353)])
    def test_unscribe_topic_parameters(self, mocker, mqtt, params):
        """This method tests unsubscribe_topic() if it's parameters are working."""
        mocking = TestMQTT.mock_send_at_comm(mocker, default_response_types()[0])
        mqtt.unsubscribe_topic(params[0], cid=params[1], message_id=params[2])

        mocking.assert_called_once_with(f'AT+QMTUNS={params[1]},{params[2]},"{params[0]}"')

    def test_publish_message_without_payload(self, mqtt):
        """This method tests publish_message() without giving payload."""
        with pytest.raises(TypeError):
            mqtt.publish_message()

    def test_publish_message_without_topic(self, mqtt):
        """This method tests publish_message() without predefined config
        or topic parameter.
        """
        config["params"] = {}
        result = mqtt.publish_message("test")

        assert result["status"] == Status.ERROR
        assert result["response"] == "Missing parameter"

    def test_publish_message_everything_success(self, mocker, mqtt):
        """This method tests publish_message() when both send_at_comm()
        functions returns successfull responses.
        """
        send_at_comm_once_patch = "core.utils.atcom.ATCom.send_at_comm_once"
        mocker.patch(send_at_comm_once_patch)
        response_sequence = [
            {"status": Status.SUCCESS, "response": ["OK", ">"]},
            {"status": Status.SUCCESS, "response": ["OK", "+QMTPUB: 0,0,0"]},
        ]
        mocking = TestMQTT.mock_send_at_comm(mocker, response_sequence, True)
        result = mqtt.publish_message("test", topic="topic1")

        mocking.assert_any_call('AT+QMTPUB=0,1,1,0,"topic1"', ">", urc=True)
        mocking.assert_any_call("\x1A")
        assert result == response_sequence[-1]

    def test_publish_message_failed_status_on_first(self, mocker, mqtt):
        """This method tests publish_message() when the first send_at_comm()
        function returns error."""
        mocked_response = {"status": Status.ERROR, "response": "error"}
        TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.publish_message("test", topic="topic1")

        assert result == mocked_response

    def test_read_message_failed(self, mocker, mqtt):
        """This method tests read_messages() failed with mocked
        ATCom responses.
        """
        mocked_response = default_response_types()[1]
        TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.read_messages()

        assert result["status"] == mocked_response["status"]
        assert result["response"] == mocked_response["response"]
        assert result["messages"] == []

    @pytest.mark.parametrize(
        "mocked_response",
        [
            {
                "status": Status.SUCCESS,
                "response": [
                    '+QMTRECV: 0,51,"channel","message"',
                    "+QMTRECV: 0,0,0,0,0,0",
                    "OK",
                ],
            },
            {
                "status": Status.SUCCESS,
                "response": [
                    '+QMTRECV: 0,101,"channel","message1"',
                    '+QMTRECV: 0,151,"channel","message2"',
                    "+QMTRECV: 0,0,0,0,0,0",
                    "OK",
                ],
            },
            {
                "status": Status.SUCCESS,
                "response": ["+QMTRECV: 0,0,0,0,0,0", "OK"],
                "messages": [],
            },
            default_response_types()[1],
        ],
    )
    def test_read_message_success(self, mocker, mqtt, mocked_response):
        """This method tests read_messages() with succeed
        ATCom responses.
        """
        mocking = TestMQTT.mock_send_at_comm(mocker, mocked_response)
        result = mqtt.read_messages()

        mocking.assert_called_once_with("AT+QMTRECV?", "+QMTRECV:")
        assert result["status"] == mocked_response["status"]
        assert result["response"] == mocked_response["response"]
        assert isinstance(result["messages"], list)

    @pytest.mark.parametrize(
        "message, expected",
        [
            (
                [
                    '+QMTRECV: 0,101,"channel1","message1"',
                    '+QMTRECV: 0,151,"channel2","message2"',
                    "+QMTRECV: 0,0,0,0,0,0",
                    "OK",
                ],
                [
                    {"message_id": 101, "topic": "channel1", "message": "message1"},
                    {"message_id": 151, "topic": "channel2", "message": "message2"},
                ],
            ),
            (
                ['+QMTRECV: 0,51,"channel","message"', "+QMTRECV: 0,0,0,0,0,0", "OK"],
                [{"message_id": 51, "topic": "channel", "message": "message"}],
            ),
            ("timeout", []),
        ],
    )
    def test_extract_messages(self, mqtt, message, expected):
        """This method tests extract_messages()."""
        assert mqtt.extract_messages(message, "+QMTRECV: 0") == expected
