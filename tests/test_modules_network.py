"""
Test module for the modules.network module.
"""

import pytest

from pico_lte.modules.network import Network
from pico_lte.modules.base import Base
from pico_lte.utils.atcom import ATCom
from pico_lte.utils.status import Status


def default_response_types():
    """This method returns default and mostly-used responses for ATCom messages."""
    return [
        {"status": Status.SUCCESS, "response": ["OK"]},
        {"status": Status.TIMEOUT, "response": "timeout"},
    ]


class TestNetwork:
    """
    Test class for Network.
    """

    @pytest.fixture
    def network(self):
        """This fixture returns a Network instance."""
        atcom = ATCom()
        base = Base(atcom)
        return Network(atcom, base)

    @staticmethod
    def mock_send_at_comm(mocker, response_to_return):
        """This is a wrapper function for repeated long mocker.patch() statements."""
        return mocker.patch("core.utils.atcom.ATCom.send_at_comm", return_value=response_to_return)

    def test_constructor(self, network):
        """This methods tests if the constructor correctly set the attributes."""
        assert isinstance(network.atcom, ATCom)
        assert isinstance(network.base, Base)

    @pytest.mark.parametrize(
        "response",
        [
            ['+CGDCONT: 1,"IP","super","0.0.0.0",0,0,0', "OK"],
            ["OK"],
        ],
    )
    def test_check_apn_ordinary(self, mocker, network, response):
        """This method tests check_apn() with possible mocked answers from ATCom."""
        mocked_response = {"status": Status.SUCCESS, "response": response}
        mocking = TestNetwork.mock_send_at_comm(mocker, mocked_response)
        result = network.check_apn()

        mocking.assert_called_once_with("AT+CGDCONT?", "super")
        assert result == mocked_response

    def test_check_apn_timeout(self, mocker, network):
        """This method tests it with mocked timeout response from ATCom."""
        mocking = TestNetwork.mock_send_at_comm(mocker, default_response_types()[1])
        result = network.check_apn()

        mocking.assert_called_once_with("AT+CGDCONT?", "super")
        assert result == default_response_types()[1]

    @pytest.mark.parametrize(
        "response, expected",
        [
            (['+CGDCONT: 1,"IP","super","0.0.0.0",0,0,0', "OK"], "super"),
            (['+CGDCONT: 2,"IP","example","0.0.0.0",0,0,0', "OK"], "example"),
        ],
    )
    def test_get_apn(self, mocker, network, response, expected):
        """This method tests get_apn() with possible mocked answers from ATCom."""
        mocked_response = {"status": Status.SUCCESS, "response": response}
        mocking = TestNetwork.mock_send_at_comm(mocker, mocked_response)
        result = network.get_apn()

        mocking.assert_called_once_with("AT+CGDCONT?")
        assert result["value"] == expected

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_apn_with_default_parameters(self, mocker, network, mocked_response):
        """This method tests set_apn() with default parameters."""
        mocking = TestNetwork.mock_send_at_comm(mocker, mocked_response)
        result = network.set_apn()

        mocking.assert_called_once_with('AT+CGDCONT=1,"IPV4V6","super"')
        assert result == mocked_response

    def test_set_apn_with_different_parameters(self, mocker, network):
        """This method tests set_apn() with different then default parameters."""
        mocking = TestNetwork.mock_send_at_comm(mocker, default_response_types()[0])
        network.set_apn(cid=3, pdp_type="IP", apn="something")

        mocking.assert_called_once_with('AT+CGDCONT=3,"IP","something"')

    @pytest.mark.parametrize("response", [["+CREG: 0,1", "OK"], ["+CREG: 0,5", "OK"]])
    def test_check_network_registration(self, mocker, network, response):
        """This method tests the check_network_registration() possible mocked answers from ATCom."""
        mocked_response = {"status": Status.SUCCESS, "response": response}
        mocking = TestNetwork.mock_send_at_comm(mocker, mocked_response)

        result = network.check_network_registration()

        mocking.assert_called_once_with(
            "AT+CREG?", desired=["+CREG: 0,1", "+CREG: 0,5"], fault="+CREG: 0,2"
        )
        assert result == mocked_response

    def test_check_network_registration_error(self, mocker, network):
        """This method tests the check_network_registration() with a timeout from ATCom."""
        mocked_response = {"status": Status.ERROR, "response": ["+CREG: 0,2", "OK"]}
        TestNetwork.mock_send_at_comm(mocker, mocked_response)
        result = network.check_network_registration()

        assert result == mocked_response

    def test_check_network_registration_timeout(self, mocker, network):
        """This method tests the check_network_registration() with a timeout from ATCom."""
        TestNetwork.mock_send_at_comm(mocker, default_response_types()[1])
        result = network.check_network_registration()

        assert result == default_response_types()[1]

    @pytest.mark.parametrize(
        "response, expected",
        [
            (['+COPS: 0,0,"operator",7', "OK"], "operator"),
            (['+COPS: 2,3,"example",0', "OK"], "example"),
        ],
    )
    def test_get_operator_information_ordinary(self, mocker, network, response, expected):
        """This method tests get_operator_information() with possible mocked answers from ATCom."""
        mocked_response = {"status": Status.SUCCESS, "response": response}
        mocking = TestNetwork.mock_send_at_comm(mocker, mocked_response)
        result = network.get_operator_information()

        mocking.assert_called_once_with("AT+COPS?")
        assert result["value"] == expected

    def test_get_operator_information_unordinary(self, mocker, network):
        """This method tests it when the ATCom response is without proper message."""
        mocked_response = {"status": Status.SUCCESS, "response": "+COPS: 0"}
        mocking = TestNetwork.mock_send_at_comm(mocker, mocked_response)
        result = network.get_operator_information()

        mocking.assert_called_once_with("AT+COPS?")
        assert result["value"] is None

    def test_get_operator_information_timeout(self, mocker, network):
        """This method tests it when the ATCom response is timeout."""
        mocking = TestNetwork.mock_send_at_comm(mocker, default_response_types()[1])
        result = network.get_operator_information()

        mocking.assert_called_once_with("AT+COPS?")
        assert result["value"] is None

    @pytest.mark.parametrize(
        "response, expected", [("8", "LTE CAT M1"), ("0", "GSM"), ("9", "LTE CAT NB1")]
    )
    def test_get_access_technology_ordinary(self, mocker, network, response, expected):
        """This method tests it when the ATCom response is in desired format."""
        mocked_response = {
            "status": Status.SUCCESS,
            "response": [f'+COPS: 0,0,"o",{response}', "OK"],
        }
        mocking = TestNetwork.mock_send_at_comm(mocker, mocked_response)
        result = network.get_access_technology()

        mocking.assert_called_once_with("AT+COPS?")
        assert result["value"] == expected

    def test_get_access_technology_unordinary(self, mocker, network):
        """This method tests when the response does not include OK message."""
        mocked_response = {"status": Status.SUCCESS, "response": '+COPS: 0,0,"o",0'}
        mocking = TestNetwork.mock_send_at_comm(mocker, mocked_response)
        result = network.get_access_technology()

        mocking.assert_called_once_with("AT+COPS?")
        assert result["value"] is None

    def test_get_access_technology_timeout(self, mocker, network):
        """This method tests the get_access_technology() with timeout mocked ATCom response."""
        mocking = TestNetwork.mock_send_at_comm(mocker, default_response_types()[1])
        result = network.get_access_technology()

        mocking.assert_called_once_with("AT+COPS?")
        assert result["value"] is None

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_configure_tcp_ip_context_with_default_parameters(
        self, mocker, network, mocked_response
    ):
        """This method tests the configure_tcp_ip_context() with mocked answers."""
        mocking = TestNetwork.mock_send_at_comm(mocker, mocked_response)

        result = network.configure_tcp_ip_context()

        mocking.assert_called_once_with('AT+QICSGP=1,1,"super","","",0')
        assert result == mocked_response

    @pytest.mark.parametrize(
        "parameters",
        [
            [2, 0, "example", "user", "pass", 1],
            [0, 1, "super", "", "", 0],
            [1, 1, "", "", "", 3],
        ],
    )
    def test_configure_tcp_ip_context_with_different_parameters(self, mocker, network, parameters):
        """This method tests the configure_tcp_ip_context() with different parameters."""
        mocking = TestNetwork.mock_send_at_comm(mocker, default_response_types()[0])

        network.configure_tcp_ip_context(
            context_id=parameters[0],
            context_type=parameters[1],
            apn=parameters[2],
            username=parameters[3],
            password=parameters[4],
            auth=parameters[5],
        )

        mocking.assert_called_once_with(
            f"AT+QICSGP={parameters[0]},{parameters[1]},"
            + f'"{parameters[2]}","{parameters[3]}",'
            + f'"{parameters[4]}",{parameters[5]}'
        )

    @pytest.mark.parametrize(
        "response",
        [["+CGACT: 1,0", "+CGACT: 2,0", "OK"]],
    )
    def test_check_pdp_context_status_default(self, mocker, network, response):
        """This method tests check_pdp_context_status() with successfull responses."""
        mocked_response = {"status": Status.SUCCESS, "response": response}
        mocking = TestNetwork.mock_send_at_comm(mocker, mocked_response)
        result = network.check_pdp_context_status()

        mocking.assert_called_once_with("AT+CGACT?", "+CGACT: 1,1")
        assert result == mocked_response

    def test_check_pdp_context_status_timeout(self, mocker, network):
        """This method tests it with timeout response from mocked ATCom."""
        TestNetwork.mock_send_at_comm(mocker, default_response_types()[1])
        result = network.check_pdp_context_status()

        assert result == default_response_types()[1]

    @pytest.mark.parametrize("cid", [0, 1, 2, -5])
    def test_check_pdp_context_status_with_parameters(self, mocker, network, cid):
        """This method tests check_pdp_context_status() with different parameters."""
        mocking = TestNetwork.mock_send_at_comm(mocker, default_response_types()[0])
        network.check_pdp_context_status(cid)

        mocking.assert_called_once_with("AT+CGACT?", f"+CGACT: {cid},1")

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_activate_pdp_context_default(self, mocker, network, mocked_response):
        """This method tests activate_pdp_context() with default parameters."""
        mocking = TestNetwork.mock_send_at_comm(mocker, mocked_response)
        result = network.activate_pdp_context()

        mocking.assert_called_once_with("AT+QIACT=1")
        assert result == mocked_response

    @pytest.mark.parametrize("cid", [1, 2, 3, 4, 5])
    def test_activate_pdp_context_with_parameters(self, mocker, network, cid):
        """This method tests activate_pdp_context() with non-default parameters."""
        mocking = TestNetwork.mock_send_at_comm(mocker, default_response_types()[0])
        network.activate_pdp_context(cid)

        mocking.assert_called_once_with(f"AT+QIACT={cid}")

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_deactivate_pdp_context_default(self, mocker, network, mocked_response):
        """This method tests if deactivate_pdp_context() calls correct AT command."""
        mocking = TestNetwork.mock_send_at_comm(mocker, mocked_response)
        result = network.deactivate_pdp_context()

        mocking.assert_called_once_with("AT+QIDEACT=1")
        assert result == mocked_response

    @pytest.mark.parametrize("cid", [1, 2, 3, 4, 5])
    def test_deactivate_pdp_context_with_parameters(self, mocker, network, cid):
        """This method tests deactivate_pdp_context() with non-default parameters."""
        mocking = TestNetwork.mock_send_at_comm(mocker, default_response_types()[0])
        network.deactivate_pdp_context(cid)

        mocking.assert_called_once_with(f"AT+QIDEACT={cid}")

    def test_register_network_all_success(self, mocker, network):
        """This method tests the register_network() state manager by looking its call traces,
        and checks if it calls all necessary AT commands when everything is succeed.
        """
        # Mock the time.sleep method to not wait in intervals.
        mocker.patch("time.sleep")

        mocked_response = {"status": Status.SUCCESS, "response": ""}
        mocking = TestNetwork.mock_send_at_comm(mocker, mocked_response)
        result = network.register_network()

        # Test if check_network_registration called
        mocking.assert_called_once_with(
            "AT+CREG?", desired=["+CREG: 0,1", "+CREG: 0,5"], fault="+CREG: 0,2"
        )
        assert result["status"] == mocked_response["status"]
        assert result["response"] == mocked_response["response"]

    def test_register_network_ordinary(self, mocker, network):
        """This method tests the register_network() state manager by looking its call traces,
        and checks if it calls all necessary AT commands when first check_network_registration()
        returns fail, and check_apn() returns success.
        """
        # Mock the time.sleep method to not wait in intervals.
        mocker.patch("time.sleep")

        # This order of responses is important for the logic of state manager.
        side_effect_responses = [
            {"status": Status.ERROR, "response": "check_network_registration 1"},
            {"status": Status.SUCCESS, "response": "check_atcom"},
            {"status": Status.SUCCESS, "response": "check_sim_ready"},
            {"status": Status.SUCCESS, "response": "check_apn"},
            {"status": Status.SUCCESS, "response": "check_network_registration 2"},
        ]
        mocking = mocker.patch(
            "core.utils.atcom.ATCom.send_at_comm", side_effect=side_effect_responses
        )
        result = network.register_network()

        # Test if called necessary functions.
        mocking.assert_any_call(
            "AT+CREG?", desired=["+CREG: 0,1", "+CREG: 0,5"], fault="+CREG: 0,2"
        )
        mocking.assert_any_call("AT+CPIN?", ["+CPIN: READY"])
        mocking.assert_any_call("AT+CGDCONT?", "super")
        assert result["status"] == side_effect_responses[4]["status"]
        assert result["response"] == side_effect_responses[4]["response"]

    def test_register_network_worst_case(self, mocker, network):
        """This method tests the register_network() state manager by looking its call traces,
        and checks if it calls all necessary AT commands when first check_network_registration()
        returns fail, and check_apn() returns fail.
        """
        # Mock the time.sleep method to not wait in intervals.
        mocker.patch("time.sleep")

        # This order of responses is important for the logic of state manager.
        side_effect_responses = [
            {"status": Status.ERROR, "response": "check_network_registration 1"},
            {"status": Status.SUCCESS, "response": "check_atcom"},
            {"status": Status.SUCCESS, "response": "check_sim_ready"},
            {"status": Status.ERROR, "response": "check_apn 1"},
            {"status": Status.SUCCESS, "response": "set_apn"},
            {"status": Status.SUCCESS, "response": "check_apn 2"},
            {"status": Status.SUCCESS, "response": "check_network_registration 2"},
        ]
        mocking = mocker.patch(
            "core.utils.atcom.ATCom.send_at_comm", side_effect=side_effect_responses
        )
        result = network.register_network()

        # Test if called necessary functions.
        mocking.assert_any_call(
            "AT+CREG?", desired=["+CREG: 0,1", "+CREG: 0,5"], fault="+CREG: 0,2"
        )
        mocking.assert_any_call("AT+CPIN?", ["+CPIN: READY"])
        mocking.assert_any_call("AT+CGDCONT?", "super")
        mocking.assert_any_call('AT+CGDCONT=1,"IPV4V6","super"')
        assert result["status"] == side_effect_responses[6]["status"]
        assert result["response"] == side_effect_responses[6]["response"]

    def test_register_network_fail_case(self, mocker, network):
        """This method tests the worst condition and its failed response for
        register_network() state manager.
        """
        # Mock the time.sleep method to not wait in intervals.
        mocker.patch("time.sleep")

        # This order of responses is important for the logic of state manager.
        side_effect_responses = [
            {"status": Status.ERROR, "response": "check_network_registration 1"},
            {"status": Status.ERROR, "response": "check_atcom"},
        ]
        mocker.patch("core.utils.atcom.ATCom.send_at_comm", side_effect=side_effect_responses)
        result = network.register_network()

        # Test if called necessary functions.
        assert result["status"] == side_effect_responses[1]["status"]
        assert result["response"] == side_effect_responses[1]["response"]

    def test_get_pdp_ready_all_success(self, mocker, network):
        """This method tests the get_pdp_ready() state manager by looking its call traces,
        and checks if it calls all necessary AT commands when all succeed.
        """
        # Mock the time.sleep method to not wait in intervals.
        mocker.patch("time.sleep")

        mocked_response = {"status": Status.SUCCESS, "response": ""}
        mocking = TestNetwork.mock_send_at_comm(mocker, mocked_response)
        result = network.get_pdp_ready()

        # Test if check_network_registration called
        mocking.assert_called_once_with("AT+CGACT?", "+CGACT: 1,1")
        assert result["status"] == mocked_response["status"]
        assert result["response"] == mocked_response["response"]

    def test_get_pdp_ready_ordinary(self, mocker, network):
        """This method tests the get_pdp_ready() state manager by looking its call traces,
        and checks if it calls necessary AT commands when deactivate needed.
        """
        # Mock the time.sleep method to not wait in intervals.
        mocker.patch("time.sleep")

        # This order of responses is important for the logic of state manager.
        side_effect_responses = [
            {"status": Status.ERROR, "response": "check_pdp_context_status 1"},
            {"status": Status.SUCCESS, "response": "configure_pdp_context"},
            {"status": Status.SUCCESS, "response": "deactivate_pdp_context"},
            {"status": Status.SUCCESS, "response": "activate_pdp_context"},
            {"status": Status.SUCCESS, "response": "check_pdp_context_status 2"},
        ]
        mocking = mocker.patch(
            "core.utils.atcom.ATCom.send_at_comm", side_effect=side_effect_responses
        )
        result = network.get_pdp_ready()

        # Test if called necessary functions.
        mocking.assert_any_call("AT+CGACT?", "+CGACT: 1,1")
        mocking.assert_any_call('AT+QICSGP=1,1,"super","","",0')
        mocking.assert_any_call("AT+QIDEACT=1")
        mocking.assert_any_call("AT+QIACT=1")
        assert result["status"] == side_effect_responses[4]["status"]
        assert result["response"] == side_effect_responses[4]["response"]

    def test_get_pdp_ready_fail(self, mocker, network):
        """This method tests the worst condition and its failed response for
        get_pdp_ready() state manager.
        """
        # Mock the time.sleep method to not wait in intervals.
        mocker.patch("time.sleep")

        # This order of responses is important for the logic of state manager.
        side_effect_responses = [
            {"status": Status.ERROR, "response": "check_pdp_context_status 1"},
            {"status": Status.ERROR, "response": "configure_pdp_context"},
        ]
        mocker.patch("core.utils.atcom.ATCom.send_at_comm", side_effect=side_effect_responses)
        result = network.get_pdp_ready()

        # Test if called necessary functions.
        assert result["status"] == side_effect_responses[1]["status"]
        assert result["response"] == side_effect_responses[1]["response"]
