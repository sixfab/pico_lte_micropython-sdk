"""
Test module for the utils.atcom module.
"""

import pytest
from machine import UART

from core.utils.atcom import ATCom
from core.utils.status import Status


class TestATCom:
    """The test class for ATCom module which lets us to communicate
    with the modem.
    """

    @pytest.fixture
    def atcom(self):
        """It returns an ATCom instance."""
        return ATCom()

    @pytest.fixture
    def example_response(self):
        """A fixtures simulates arbitrary response of the modem."""
        return [
            "+Q",
            "HT",
            "TP",
            "GET",
            ": ",
            "200",
            "\r\n",
            "OK\r",
            "\n" "AT",
            "",
            "&V",
            "\r\n",
            "",
            "OK",
            "\r\n",
        ]

    @pytest.fixture
    def example_urc_response(self):
        """A fixtures simulates arbitrary URC response of the modem."""
        return [
            "\r\nOK\r\n",
            "CONN",
            "ECT\r\n",
            "\r\n",
            "",
            "+QHTT",
            "PPOS",
            "T: 200\r",
            "\n",
        ]

    def test_initilization(self, atcom):
        """Test if the initilization creates an UART instance."""
        assert isinstance(atcom.modem_com, UART)

    def test_send_at_comm_once_default_parameters(self, mocker, atcom):
        """Test if the send_at_comm_once() method sends message to UART channel."""
        mocking = mocker.patch("machine.UART.write")

        message = "Example command to send"
        atcom.send_at_comm_once("Example command to send")

        encoded_message = (message + "\r").encode()
        mocking.assert_called_once_with(encoded_message)

    def test_send_at_comm_once_line_end_false(self, mocker, atcom):
        """Test the send_at_comm_once() method with line_end=True"""
        mocking = mocker.patch("machine.UART.write")

        message = "Example command to send"
        atcom.send_at_comm_once("Example command to send", line_end=False)

        encoded_message = message.encode()
        mocking.assert_called_once_with(encoded_message)

    def test_get_response_default_parameters(self, mocker, atcom, example_response):
        """Test the get_response() method with default parameters."""
        mocker.patch("time.sleep", return_value=None)  # Mock to not wait.
        # Mock the any() method to have dynamic return values.
        # Note that, in each UART read() turn, it is called twice if it's True.
        returns_any = [True for _ in range(len(example_response) * 2)] + [False]
        mocker.patch("machine.UART.any", side_effect=returns_any)

        # Mock the read() method to have dynamic and realistic
        # return values.
        returns_read = [fake.encode() for fake in example_response]
        mocker.patch("machine.UART.read", side_effect=returns_read)

        result = atcom.get_response()
        assert result == {
            "status": Status.SUCCESS,
            "response": ["+QHTTPGET: 200", "OK"],
        }

    def test_get_response_timeout_condition(self, mocker, atcom):
        """Test the get_response() method's timeout condition."""
        mocker.patch("machine.UART.any", return_value=False)
        mocker.patch("machine.UART.read", return_value=None)

        result = atcom.get_response(timeout=0.01)
        assert result["status"] == Status.TIMEOUT
        assert result["response"] == "timeout"

    def test_get_response_no_informative_response(self, mocker, atcom):
        """Test the get_response() method with no informative response from modem."""
        mocker.patch("machine.UART.any", side_effect=[True, True, False])
        mocker.patch("machine.UART.read", return_value="OK".encode())

        # No informative response.
        result = atcom.get_response(desired_responses="OK")
        assert result["status"] == Status.ERROR

    def test_get_response_found_desired_response(self, mocker, atcom, example_response):
        """Tests the get_response() method with given desired_response and finds it."""
        returns_any = [True for _ in range(len(example_response) * 2)] + [False]
        mocker.patch("machine.UART.any", side_effect=returns_any)

        returns_read = [fake.encode() for fake in example_response]
        mocker.patch("machine.UART.read", side_effect=returns_read)

        result = atcom.get_response(desired_responses="AT&V")
        assert result["status"] == Status.SUCCESS
        assert result["response"] == ["+QHTTPGET: 200", "OK", "AT&V", "OK"]

    def test_get_response_not_found_desired_response(self, mocker, atcom):
        """Tests the get_response() method with given desired_responses but couldn't find it."""
        mocker.patch(
            "machine.UART.any",
            side_effect=[True, True, True, True, False] + [False for _ in range(50)],
        )
        mocker.patch(
            "machine.UART.read",
            side_effect=["+QHTTP\r\n".encode(), "\r\nOK\r\n".encode()],
        )

        result = atcom.get_response(desired_responses="+GPSLOC:", timeout=0.5)
        assert result == {"status": Status.TIMEOUT, "response": "timeout"}

    def test_get_response_found_fault_response(self, mocker, atcom, example_response):
        """Tests the get_response() method with given fault_responses and finds it."""
        returns_any = [True for _ in range(len(example_response) * 2)] + [False]
        mocker.patch("machine.UART.any", side_effect=returns_any)

        returns_read = [fake.encode() for fake in example_response]
        mocker.patch("machine.UART.read", side_effect=returns_read)

        desired = ["+GPSLOC:", "SOME", "COMMMAND"]
        fault = ["+QHTTPGET: 200", "+QHTTPPOST: 200"]
        result = atcom.get_response(desired_responses=desired, fault_responses=fault)

        assert result["status"] == Status.ERROR
        assert result["response"] == ["+QHTTPGET: 200", "OK"]

    def test_get_response_found_cme_error_ok_is_after(self, mocker, atcom):
        """Tests the get_response() method and founds an error message."""
        example_response = ["CONNECT\r\n", "+CME ERROR: 703\r\n", "\r\nOK\r\n"]

        returns_any = [True for _ in range(len(example_response) * 2)] + [False]
        mocker.patch("machine.UART.any", side_effect=returns_any)

        returns_read = [fake.encode() for fake in example_response]
        mocker.patch("machine.UART.read", side_effect=returns_read)

        result = atcom.get_response()
        assert result["status"] == Status.ERROR
        assert result["response"] == ["CONNECT", "+CME ERROR: 703"]

    def test_get_response_found_cme_error_ok_is_before(self, mocker, atcom):
        """Tests the get_response() method and founds an error message."""
        example_response = ["CONNECT\r\n", "\r\nOK\r\n", "ERROR\r\n"]

        returns_any = [True for _ in range(len(example_response) * 2)] + [False]
        mocker.patch("machine.UART.any", side_effect=returns_any)

        returns_read = [fake.encode() for fake in example_response]
        mocker.patch("machine.UART.read", side_effect=returns_read)

        result = atcom.get_response(desired_responses="wanted response")
        assert result["status"] == Status.ERROR
        assert result["response"] == ["CONNECT", "OK", "ERROR"]

    def test_get_urc_response_default_parameters(self, atcom):
        """Test the get_urc_response() method with default parameters."""
        result = atcom.get_urc_response()
        assert result == {
            "status": Status.SUCCESS,
            "response": "No desired or fault responses",
        }

    def test_get_urc_response_timeout_condition(self, mocker, atcom):
        """Test the get_response() method's timeout condition."""
        mocker.patch("machine.UART.any", return_value=False)
        mocker.patch("machine.UART.read", return_value=None)

        result = atcom.get_response(timeout=0.01)
        assert result["status"] == Status.TIMEOUT
        assert result["response"] == "timeout"

    def test_get_urc_response_with_desired_response(self, mocker, atcom, example_urc_response):
        """Test the get_urc_response() method with desired_responses parameter."""
        returns_any = [True for _ in range(len(example_urc_response) * 2)] + [False]
        mocker.patch("machine.UART.any", side_effect=returns_any)

        returns_read = [fake.encode() for fake in example_urc_response]
        mocker.patch("machine.UART.read", side_effect=returns_read)

        desired = "CONNECT"
        result = atcom.get_urc_response(desired_responses=desired)

        assert result["status"] == Status.SUCCESS
        assert result["response"] == ["OK", "CONNECT"]

    def test_get_urc_response_with_fault_response(self, mocker, atcom, example_urc_response):
        """Test the get_urc_response() method with fault_responses parameter."""
        returns_any = [True for _ in range(len(example_urc_response) * 2)] + [False]
        mocker.patch("machine.UART.any", side_effect=returns_any)

        returns_read = [fake.encode() for fake in example_urc_response]
        mocker.patch("machine.UART.read", side_effect=returns_read)

        fault = "CONNECT"
        result = atcom.get_urc_response(fault_responses=fault)

        assert result["status"] == Status.ERROR
        assert result["response"] == ["OK", "CONNECT"]

    def test_get_urc_response_ordinary_case(self, mocker, atcom, example_urc_response):
        """Test the get_urc_response() method in ordinary case."""
        returns_any = [True for _ in range(len(example_urc_response) * 2)] + [False]
        mocker.patch("machine.UART.any", side_effect=returns_any)

        returns_read = [fake.encode() for fake in example_urc_response]
        mocker.patch("machine.UART.read", side_effect=returns_read)

        desired = "+QHTTPPOST: 200"
        fault = ["ERROR", "+CME ERROR"]
        result = atcom.get_urc_response(desired_responses=desired, fault_responses=fault)

        assert result["status"] == Status.SUCCESS
        assert result["response"] == ["OK", "CONNECT", "+QHTTPPOST: 200"]

    @pytest.mark.parametrize(
        "return_dict",
        [
            {"status": Status.SUCCESS, "response": "works"},
            {"status": Status.ERROR, "response": "doesn't work"},
            {"status": Status.TIMEOUT, "response": "timeout"},
        ],
    )
    def test_send_at_comm(self, mocker, atcom, return_dict):
        """Test the send_at_comm() method."""
        mocker.patch("core.utils.atcom.ATCom.send_at_comm_once", return_value=None)
        mocker.patch("time.sleep", return_value=None)
        mocker.patch("core.utils.atcom.ATCom.get_urc_response", return_value=return_dict)
        mocker.patch("core.utils.atcom.ATCom.get_response", return_value=return_dict)

        result_one = atcom.send_at_comm("example", desired="CONNECT", fault="ERROR", urc=True)
        assert result_one["status"] == return_dict["status"]

        result_sec = atcom.send_at_comm("example", urc=False)
        assert result_sec["status"] == return_dict["status"]
