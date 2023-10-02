"""
Test module for the modules.http module.
"""
import pytest

from pico_lte.modules.http import HTTP
from pico_lte.utils.atcom import ATCom
from pico_lte.utils.status import Status


def default_response_types():
    """This method returns default and mostly-used responses for ATCom messages."""
    return [
        {"status": Status.SUCCESS, "response": ["OK"]},
        {"status": Status.TIMEOUT, "response": "timeout"},
    ]


class TestHTTP:
    """
    Test class for HTTP.
    """

    @pytest.fixture
    def http(self):
        """This fixture returns a HTTP instance."""
        atcom = ATCom()
        return HTTP(atcom)

    @staticmethod
    def mock_send_at_comm(mocker, responses_to_return, is_side_effect=False):
        """This is a wrapper function to repeated long mocker.patch() statements."""
        patch_location = "pico_lte.utils.atcom.ATCom.send_at_comm"
        if is_side_effect:
            return mocker.patch(patch_location, side_effect=responses_to_return)

        return mocker.patch(patch_location, return_value=responses_to_return)

    def test_constructor(self, http):
        """This method tests if the HTTP constructor does its job."""
        assert isinstance(http.atcom, ATCom)

    def test_set_context_id_default(self, mocker, http):
        """This method tests set_context_id()'s default
        parameters.
        """
        mocking = TestHTTP.mock_send_at_comm(mocker, None)
        http.set_context_id()

        mocking.assert_called_once_with('AT+QHTTPCFG="contextid",1')

    @pytest.mark.parametrize("cid", [1, 2, 3, 4])
    def test_set_context_id_parameters(self, mocker, http, cid):
        """This method tests set_context_id()'s parameters,
        and if the ATCom send_at_comm() statement is correctly set.
        """
        mocking = TestHTTP.mock_send_at_comm(mocker, None)
        http.set_context_id(cid)

        mocking.assert_called_once_with(f'AT+QHTTPCFG="contextid",{cid}')

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_context_id_ordinary(self, mocker, http, mocked_response):
        """This method tests set_context_id() with different responses
        came from ATCom instance.
        """
        TestHTTP.mock_send_at_comm(mocker, mocked_response)
        result = http.set_context_id()

        assert result == mocked_response

    def test_set_request_header_status_default(self, mocker, http):
        """This method tests set_request_header_status() with its
        default parameter values.
        """
        mocking = TestHTTP.mock_send_at_comm(mocker, None)
        http.set_request_header_status()

        mocking.assert_called_once_with('AT+QHTTPCFG="requestheader",0')

    @pytest.mark.parametrize("status", [0, 1])
    def test_set_request_header_status_parameters(self, mocker, http, status):
        """This method tests set_request_header_status() for given different
        status parameters.
        """
        mocking = TestHTTP.mock_send_at_comm(mocker, None)
        http.set_request_header_status(status)

        mocking.assert_called_once_with(f'AT+QHTTPCFG="requestheader",{status}')

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_request_header_status_ordinary(self, mocker, http, mocked_response):
        """This method tests set_request_header_status() in its ordinary use-cases."""
        TestHTTP.mock_send_at_comm(mocker, mocked_response)
        result = http.set_request_header_status()

        assert result == mocked_response

    def test_set_response_header_status_default(self, mocker, http):
        """This method tests set_response_header_status() with default parameter."""
        mocking = TestHTTP.mock_send_at_comm(mocker, None)
        http.set_response_header_status()

        mocking.assert_called_once_with('AT+QHTTPCFG="responseheader",0')

    @pytest.mark.parametrize("status", [0, 1])
    def test_set_response_header_status_parameters(self, mocker, http, status):
        """This method tests set_response_header_status() for given parameters."""
        mocking = TestHTTP.mock_send_at_comm(mocker, None)
        http.set_response_header_status(status)

        mocking.assert_called_once_with(f'AT+QHTTPCFG="responseheader",{status}')

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_response_header_status_ordinary(self, mocker, http, mocked_response):
        """This method tests set_response_header_status() in its ordinary use-cases."""
        TestHTTP.mock_send_at_comm(mocker, mocked_response)
        result = http.set_response_header_status()

        assert result == mocked_response

    def test_set_ssl_context_id_default(self, mocker, http):
        """This method tests set_response_header_status() with default parameter."""
        mocking = TestHTTP.mock_send_at_comm(mocker, None)
        http.set_ssl_context_id()

        mocking.assert_called_once_with('AT+QHTTPCFG="sslctxid",1')

    @pytest.mark.parametrize("cid", [0, 1])
    def test_set_ssl_context_id_parameters(self, mocker, http, cid):
        """This method tests set_response_header_status() for given parameters."""
        mocking = TestHTTP.mock_send_at_comm(mocker, None)
        http.set_ssl_context_id(cid)

        mocking.assert_called_once_with(f'AT+QHTTPCFG="sslctxid",{cid}')

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_ssl_context_id_ordinary(self, mocker, http, mocked_response):
        """This method tests set_content_type() in its ordinary use-cases."""
        TestHTTP.mock_send_at_comm(mocker, mocked_response)
        result = http.set_ssl_context_id()

        assert result == mocked_response

    def test_set_content_type_default(self, mocker, http):
        """This method tests set_content_type() with default parameter."""
        mocking = TestHTTP.mock_send_at_comm(mocker, None)
        http.set_content_type()

        mocking.assert_called_once_with('AT+QHTTPCFG="contenttype",0')

    @pytest.mark.parametrize("content_type", [0, 1])
    def test_set_content_type_parameters(self, mocker, http, content_type):
        """This method tests set_content_type() for given parameters."""
        mocking = TestHTTP.mock_send_at_comm(mocker, None)
        http.set_content_type(content_type)

        mocking.assert_called_once_with(f'AT+QHTTPCFG="contenttype",{content_type}')

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_content_type_ordinary(self, mocker, http, mocked_response):
        """This method tests set_content_type() in its ordinary use-cases."""
        TestHTTP.mock_send_at_comm(mocker, mocked_response)
        result = http.set_content_type()

        assert result == mocked_response

    def test_set_auth_when_none_but_config_ok(self, mocker, http):
        """This method tests set_auth() with parameter from config."""
        mocker.patch(
            "pico_lte.modules.http.get_parameter", side_effect=["user", "pass"]
        )
        mocking = TestHTTP.mock_send_at_comm(mocker, None)
        http.set_auth()

        mocking.assert_called_once_with('AT+QHTTPCFG="auth","user:pass"')

    def test_set_auth_when_all_none(self, mocker, http):
        """This method tests set_auth() when get_parameter returns None."""
        mocker.patch("pico_lte.modules.http.get_parameter", return_value=None)
        result = http.set_auth()

        assert result["status"] == Status.ERROR
        assert result["response"] == "Missing arguments: username and password"

    @pytest.mark.parametrize(
        "username, password",
        [("johndoe", "doe2022"), ("john", "some"), ("123456", "123456")],
    )
    def test_set_auth_parameters(self, mocker, http, username, password):
        """This method tests set_auth() for given parameters."""
        mocking = TestHTTP.mock_send_at_comm(mocker, None)
        http.set_auth(username, password)

        mocking.assert_called_once_with(f'AT+QHTTPCFG="auth","{username}:{password}"')

    def test_set_custom_header_none(self, http):
        """This method tests set_custom_header() with None parameter for header.
        Also, this test covers the default case.
        """
        result = http.set_custom_header()

        assert result["status"] == Status.ERROR
        assert result["response"] == "Missing arguments : header"

    @pytest.mark.parametrize(
        "header",
        [
            "GET / HTTP/1.1\nHost: sixfab.com\nCustom-Header-Name: Custom-Data\n"
            + "Content-Type: application/json\nContent-Length: 0\n\n\n",
            "POST /xyz HTTP/1.1\nHost: example.com\nCustom: HelloWorld\n\n\n",
        ],
    )
    def test_set_custom_header_parameters(self, mocker, http, header):
        """This method tests set_custom_header() with given header parameter."""
        mocking = TestHTTP.mock_send_at_comm(mocker, None)
        http.set_custom_header(header)

        mocking.assert_called_once_with(f'AT+QHTTPCFG="customheader","{header}"')

    def test_set_server_url_when_all_none(self, mocker, http):
        """This method tests set_server_url() with a response of None from config.
        It also tests the default parameter.
        """
        mocker.patch("pico_lte.modules.http.get_parameter", return_value=None)
        result = http.set_server_url()

        assert result["status"] == Status.ERROR
        assert result["response"] == "Missing arguments : url"

    def test_set_server_url_with_none_but_config_ok(self, mocker, http):
        """This method tests set_server_url() with a mocked URL response from
        get_parameter().
        """
        # Mock the get_parameter() method.
        get_parameter_loc = "pico_lte.modules.http.get_parameter"
        mocker.patch(get_parameter_loc, return_value="https://sixfab.com")
        # Mock the ATCom.send_at_com() method.
        connect_success = {"status": Status.SUCCESS, "response": ["CONNECT", "OK"]}
        mocker_responses = [connect_success, default_response_types()[0]]
        mocking = TestHTTP.mock_send_at_comm(mocker, mocker_responses, True)
        http.set_server_url()

        mocking.assert_any_call("AT+QHTTPURL=18,5", "CONNECT", urc=True)
        mocking.assert_any_call("https://sixfab.com", line_end=False)

    def test_set_server_url_with_parameters(self, mocker, http):
        """This method tests set_server_url() with given parameters."""
        connect_success = {"status": Status.SUCCESS, "response": ["CONNECT", "OK"]}
        mocker_responses = [connect_success, default_response_types()[0]]
        mocking = TestHTTP.mock_send_at_comm(mocker, mocker_responses, True)
        http.set_server_url("https://sixfab.com")

        mocking.assert_any_call("AT+QHTTPURL=18,5", "CONNECT", urc=True)
        mocking.assert_any_call("https://sixfab.com", line_end=False)

    @pytest.mark.parametrize(
        "mocked_response",
        [
            {"status": Status.ERROR, "response": "+CME ERROR: X"},
            default_response_types()[1],
        ],
    )
    def test_set_server_url_error_at_connect(self, mocker, http, mocked_response):
        """This method tests set_server_url() when the CONNECT checking fails."""
        mocking = TestHTTP.mock_send_at_comm(mocker, mocked_response)
        result = http.set_server_url("https://sixfab.com")

        mocking.assert_called_once_with("AT+QHTTPURL=18,5", "CONNECT", urc=True)
        assert result == mocked_response

    @pytest.mark.parametrize(
        "mocked_response",
        [
            {"status": Status.ERROR, "response": "+CME ERROR: X"},
            default_response_types()[1],
        ],
    )
    def test_set_server_url_error_at_end(self, mocker, http, mocked_response):
        """This method tests set_server_url() when the CONNECT is catched,
        but no successfull return from URL sending.
        """
        connect_success = {"status": Status.SUCCESS, "response": ["CONNECT", "OK"]}
        mocker_responses = [connect_success, mocked_response]
        mocking = TestHTTP.mock_send_at_comm(mocker, mocker_responses, True)
        result = http.set_server_url("https://sixfab.com")

        mocking.assert_any_call("AT+QHTTPURL=18,5", "CONNECT", urc=True)
        mocking.assert_any_call("https://sixfab.com", line_end=False)
        assert result == mocked_response

    def test_get_default_parameters(self, mocker, http):
        """This method tests get() with a mocked response from
        send_at_comm().
        """
        response_sequence = [
            {"status": Status.SUCCESS, "response": ["requestheader_res", "OK"]},
            {"status": Status.SUCCESS, "response": ["qhttpget_res", "OK"]},
        ]
        mocking = TestHTTP.mock_send_at_comm(mocker, response_sequence, True)
        result = http.get()

        mocking.assert_any_call('AT+QHTTPCFG="requestheader",0')
        assert result == response_sequence[-1]

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_get_default_parameters_error_at_header(
        self, mocker, http, mocked_response
    ):
        """This method tests get() with its default parameters but with
        an ERROR return from the set_request_header_status() call.
        """
        mocking = TestHTTP.mock_send_at_comm(mocker, mocked_response)
        result = http.get()

        mocking.assert_any_call('AT+QHTTPCFG="requestheader",0')
        assert result == mocked_response

    def test_get_with_custom_header(self, mocker, http):
        """This method tests get() in header_mode=1 condition."""
        response_sequence = [
            {"status": Status.SUCCESS, "response": ["requestheader_res", "OK"]},
            {"status": Status.SUCCESS, "response": ["CONNECT", "OK"]},
            {"status": Status.SUCCESS, "response": ["OK", "+QHTTPGET: 1,200,0"]},
        ]
        mocking = TestHTTP.mock_send_at_comm(mocker, response_sequence, True)
        result = http.get(header_mode=1)

        mocking.assert_any_call('AT+QHTTPCFG="requestheader",1')
        mocking.assert_any_call(
            "AT+QHTTPGET=60,0,5",
            desired="CONNECT",
            fault="+CME ERROR:",
            urc=True,
            timeout=60,
        )
        assert mocking.call_count == 3
        assert result == response_sequence[-1]

    def test_get_with_custom_header_error_at_connect(self, mocker, http):
        """This method tests get() with header_mode = 1 and on the condition
        when there is no CONNECT catched.
        """
        response_sequence = [
            {"status": Status.SUCCESS, "response": ["requestheader_res", "OK"]},
            {"status": Status.ERROR, "response": ["+CME ERROR: x"]},
        ]
        mocking = TestHTTP.mock_send_at_comm(mocker, response_sequence, True)
        result = http.get(header_mode=1)

        mocking.assert_any_call('AT+QHTTPCFG="requestheader",1')
        mocking.assert_any_call(
            "AT+QHTTPGET=60,0,5",
            desired="CONNECT",
            fault="+CME ERROR:",
            urc=True,
            timeout=60,
        )
        assert mocking.call_count == 2
        assert result == response_sequence[-1]

    @pytest.mark.parametrize(
        "params",
        [
            ("something", 3, 20, "200", "703"),
            ("otherwise", 1, 10, ["222", "505"], "112"),
            ("different", 7, 2, "XXX", ["YYY", "ZZZ"]),
        ],
    )
    def test_get_all_parameters_custom_header(self, mocker, http, params):
        """This method tests get() if the parameters given are set correctly."""
        response_sequence = [
            {"status": Status.SUCCESS, "response": ["OK"]},
            {"status": Status.SUCCESS, "response": ["CONNECT", "OK"]},
            {"status": Status.SUCCESS, "response": ["OK", "+QHTTPGET: 1,200,0"]},
        ]
        mocking = TestHTTP.mock_send_at_comm(mocker, response_sequence, True)
        http.get(
            data=params[0],
            header_mode=1,
            input_timeout=params[1],
            timeout=params[2],
            desired_response=params[3],
            fault_response=params[4],
        )

        data_length = len(params[0])
        mocking.assert_any_call(
            f"AT+QHTTPGET={params[2]},{data_length},{params[1]}",
            desired="CONNECT",
            fault="+CME ERROR:",
            urc=True,
            timeout=60,
        )
        mocking.assert_any_call(
            params[0],
            desired=[f"+QHTTPGET: 0,{desired}" for desired in params[3]],
            fault=[f"+QHTTPGET: 0,{fault}" for fault in params[4]] + ["+CME ERROR:"],
            urc=True,
            line_end=False,
            timeout=params[2],
        )

    def test_post_default_parameters(self, mocker, http):
        """This method tests post() with a mocked response from
        send_at_comm().
        """
        response_sequence = [
            {"status": Status.SUCCESS, "response": ["requestheader_res", "OK"]},
            {"status": Status.SUCCESS, "response": ["CONNECT", "OK"]},
            {"status": Status.SUCCESS, "response": ["OK", "+QHTTPPOST: 0,200,0"]},
        ]
        mocking = TestHTTP.mock_send_at_comm(mocker, response_sequence, True)
        data = "Example Data"
        result = http.post(data)

        mocking.assert_any_call('AT+QHTTPCFG="requestheader",0')
        mocking.assert_any_call(
            f"AT+QHTTPPOST={len(data)},5,60",
            desired="CONNECT",
            fault="+CME ERROR:",
            urc=True,
            timeout=60,
        )
        assert mocking.call_count == 3
        assert result == response_sequence[-1]

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_post_default_parameters_header_error(self, mocker, http, mocked_response):
        """This method tests post() with its default parameters but with
        an ERROR return from the set_request_header_status() call.
        """
        mocking = TestHTTP.mock_send_at_comm(mocker, mocked_response)
        result = http.post("Example Data")

        mocking.assert_any_call('AT+QHTTPCFG="requestheader",0')
        assert result == mocked_response

    def test_post_error_at_connect(self, mocker, http):
        """This method tests post() in header_mode=1 condition."""
        response_sequence = [
            {"status": Status.SUCCESS, "response": ["requestheader_res", "OK"]},
            {"status": Status.ERROR, "response": ["+CME ERROR: XXX"]},
        ]
        mocking = TestHTTP.mock_send_at_comm(mocker, response_sequence, True)
        data = "data with header"
        result = http.post(data, header_mode=1)

        mocking.assert_any_call('AT+QHTTPCFG="requestheader",1')
        mocking.assert_any_call(
            f"AT+QHTTPPOST={len(data)},5,60",
            desired="CONNECT",
            fault="+CME ERROR:",
            urc=True,
            timeout=60,
        )
        assert mocking.call_count == 2
        assert result == response_sequence[-1]

    @pytest.mark.parametrize(
        "params",
        [
            ("something", 0, 3, 20, "200", "703"),
            ("otherwise", 1, 1, 10, ["222", "505"], "112"),
            ("different", 0, 7, 2, "XXX", ["YYY", "ZZZ"]),
        ],
    )
    def test_post_all_parameters(self, mocker, http, params):
        """This method tests post() if the parameters given are set correctly."""
        response_sequence = [
            {"status": Status.SUCCESS, "response": ["OK"]},
            {"status": Status.SUCCESS, "response": ["CONNECT", "OK"]},
            {"status": Status.SUCCESS, "response": ["OK", "+QHTTPPOST: 1,200,0"]},
        ]
        mocking = TestHTTP.mock_send_at_comm(mocker, response_sequence, True)
        http.post(
            data=params[0],
            header_mode=params[1],
            input_timeout=params[2],
            timeout=params[3],
            desired_response=params[4],
            fault_response=params[5],
        )

        mocking.assert_any_call(f'AT+QHTTPCFG="requestheader",{params[1]}')
        data_length = len(params[0])
        mocking.assert_any_call(
            f"AT+QHTTPPOST={data_length},{params[2]},{params[3]}",
            desired="CONNECT",
            fault="+CME ERROR:",
            urc=True,
            timeout=params[3],
        )
        mocking.assert_any_call(
            params[0],
            desired=[f"+QHTTPPOST: 0,{desired}" for desired in params[4]],
            fault=[f"+QHTTPPOST: 0,{fault}" for fault in params[5]] + ["+CME ERROR:"],
            urc=True,
            line_end=False,
            timeout=params[3],
        )

    def test_put_default_parameters(self, mocker, http):
        """This method tests put() with a mocked response from
        send_at_comm().
        """
        response_sequence = [
            {"status": Status.SUCCESS, "response": ["requestheader_res", "OK"]},
            {"status": Status.SUCCESS, "response": ["CONNECT", "OK"]},
            {"status": Status.SUCCESS, "response": ["OK", "+QHTTPPUT: 0,200,0"]},
        ]
        mocking = TestHTTP.mock_send_at_comm(mocker, response_sequence, True)
        data = "Example Data"
        result = http.put(data)

        mocking.assert_any_call('AT+QHTTPCFG="requestheader",0')
        mocking.assert_any_call(
            f"AT+QHTTPPUT={len(data)},5,60",
            desired="CONNECT",
            fault="+CME ERROR:",
            urc=True,
            timeout=60,
        )
        assert mocking.call_count == 3
        assert result == response_sequence[-1]

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_put_default_parameters_header_error(self, mocker, http, mocked_response):
        """This method tests put() with its default parameters but with
        an ERROR return from the set_request_header_status() call.
        """
        mocking = TestHTTP.mock_send_at_comm(mocker, mocked_response)
        result = http.put("Example Data")

        mocking.assert_any_call('AT+QHTTPCFG="requestheader",0')
        assert result == mocked_response

    def test_put_error_at_connect(self, mocker, http):
        """This method tests post() in header_mode=1 condition."""
        response_sequence = [
            {"status": Status.SUCCESS, "response": ["requestheader_res", "OK"]},
            {"status": Status.ERROR, "response": ["+CME ERROR: XXX"]},
        ]
        mocking = TestHTTP.mock_send_at_comm(mocker, response_sequence, True)
        data = "data with header"
        result = http.put(data)

        mocking.assert_any_call('AT+QHTTPCFG="requestheader",0')
        mocking.assert_any_call(
            f"AT+QHTTPPUT={len(data)},5,60",
            desired="CONNECT",
            fault="+CME ERROR:",
            urc=True,
            timeout=60,
        )
        assert mocking.call_count == 2
        assert result == response_sequence[-1]

    @pytest.mark.parametrize(
        "params",
        [
            ("something", 0, 3, 20, "200", "703"),
            ("otherwise", 1, 1, 10, ["222", "505"], "112"),
            ("different", 0, 7, 2, "XXX", ["YYY", "ZZZ"]),
        ],
    )
    def test_put_all_parameters(self, mocker, http, params):
        """This method tests post() if the parameters given are set correctly."""
        response_sequence = [
            {"status": Status.SUCCESS, "response": ["OK"]},
            {"status": Status.SUCCESS, "response": ["CONNECT", "OK"]},
            {"status": Status.SUCCESS, "response": ["OK", "+QHTTPPUT: 1,200,0"]},
        ]
        mocking = TestHTTP.mock_send_at_comm(mocker, response_sequence, True)
        http.put(
            data=params[0],
            header_mode=params[1],
            input_timeout=params[2],
            timeout=params[3],
            desired_response=params[4],
            fault_response=params[5],
        )

        mocking.assert_any_call(f'AT+QHTTPCFG="requestheader",{params[1]}')
        data_length = len(params[0])
        mocking.assert_any_call(
            f"AT+QHTTPPUT={data_length},{params[2]},{params[3]}",
            desired="CONNECT",
            fault="+CME ERROR:",
            urc=True,
            timeout=params[3],
        )
        mocking.assert_any_call(
            params[0],
            desired=[f"+QHTTPPUT: 0,{desired}" for desired in params[4]],
            fault=[f"+QHTTPPUT: 0,{fault}" for fault in params[5]] + ["+CME ERROR:"],
            urc=True,
            line_end=False,
            timeout=params[3],
        )

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_post_from_file_default(self, mocker, http, mocked_response):
        """This method tests post_from_file() with default parameters."""
        mocking = TestHTTP.mock_send_at_comm(mocker, mocked_response)
        result = http.post_from_file("file.txt")

        mocking.assert_any_call("AT+QHTTPPOSTFILE=file.txt,60")
        assert result == mocked_response

    def test_post_from_file_with_header(self, http):
        """This method tests post_from_file() with custom header."""
        result = http.post_from_file("file.txt", header_mode=1)

        assert result["status"] == Status.ERROR
        assert result["response"] == "Not implemented yet!"

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_put_from_file_default(self, mocker, http, mocked_response):
        """This method tests put_from_file() with default parameters."""
        mocking = TestHTTP.mock_send_at_comm(mocker, mocked_response)
        result = http.put_from_file("file.txt")

        mocking.assert_any_call("AT+QHTTPPUTFILE=file.txt,60,0")
        assert result == mocked_response

    def test_put_from_file_with_header(self, http):
        """This method tests put_from_file() with custom header."""
        result = http.put_from_file("file.txt", header_mode=1)

        assert result["status"] == Status.ERROR
        assert result["response"] == "Not implemented yet!"

    @pytest.mark.parametrize(
        "response, expected",
        [
            (
                ["CONNECT", "answer", "OK", "+QHTTPREAD: 0"],
                ["answer", "OK", "+QHTTPREAD: 0"],
            ),
            (
                ["CONNECT", "some", "OK", "+QHTTPREAD: 0"],
                ["some", "OK", "+QHTTPREAD: 0"],
            ),
            (["OK", "+QHTTPREAD: 0"], ["OK", "+QHTTPREAD: 0"]),
        ],
    )
    def test_read_response_default(self, mocker, http, response, expected):
        """This method tests the read_response() with its default parameters."""
        mocked_response = {"status": Status.SUCCESS, "response": response}
        mocking = TestHTTP.mock_send_at_comm(mocker, mocked_response)
        result = http.read_response()

        mocking.assert_called_once_with(
            "AT+QHTTPREAD=5",
            desired="+QHTTPREAD: 0",
            fault=[
                f"+QHTTPREAD: {str(error_code)}" for error_code in range(701, 731, 1)
            ],
            urc=True,
            timeout=5,
        )
        assert result["response"] == expected

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_read_response_to_file(self, mocker, http, mocked_response):
        """This method tests the read_response_to_file()."""
        mocking = TestHTTP.mock_send_at_comm(mocker, mocked_response)
        result = http.read_response_to_file("file.txt")

        mocking.assert_called_once_with("AT+QHTTPREADFILE=file.txt,60")
        assert result == mocked_response
