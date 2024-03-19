"""
Test module for the modules.ssl module.
"""

import pytest

from pico_lte.modules.ssl import SSL
from pico_lte.utils.atcom import ATCom
from pico_lte.utils.status import Status


def default_response_types():
    """This method returns default and mostly-used responses for ATCom messages."""
    return [
        {"status": Status.SUCCESS, "response": ["OK"]},
        {"status": Status.TIMEOUT, "response": "timeout"},
    ]


class TestSSL:
    """
    Test class for SSL.
    """

    @pytest.fixture
    def ssl(self):
        """This method returns a SSL instance."""
        atcom = ATCom()
        return SSL(atcom)

    @staticmethod
    def mock_send_at_comm(mocker, responses_to_return):
        """This is a wrapper function to repeated long mocker.patch() statements."""
        return mocker.patch(
            "pico_lte.utils.atcom.ATCom.send_at_comm", return_value=responses_to_return
        )

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_ca_cert_with_default_parameters(self, mocker, ssl, mocked_response):
        """This method tests set_ca_cert() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_ca_cert()

        mocking.assert_called_once_with('AT+QSSLCFG="cacert",2,"/security/cacert.pem"')
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_ca_cert_with_different_parameters(self, mocker, ssl, mocked_response):
        """This method tests set_ca_cert() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_ca_cert(1, "some/path.crt")

        mocking.assert_called_once_with('AT+QSSLCFG="cacert",1,"some/path.crt"')
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_client_cert_with_default_parameters(
        self, mocker, ssl, mocked_response
    ):
        """This method tests set_ca_cert() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_client_cert()

        mocking.assert_called_once_with(
            'AT+QSSLCFG="clientcert",2,"/security/client.pem"'
        )
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_client_cert_with_different_parameters(
        self, mocker, ssl, mocked_response
    ):
        """This method tests set_ca_cert() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_client_cert(1, "some/path.crt")

        mocking.assert_called_once_with('AT+QSSLCFG="clientcert",1,"some/path.crt"')
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_client_key_with_default_parameters(self, mocker, ssl, mocked_response):
        """This method tests set_ca_cert() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_client_key()

        mocking.assert_called_once_with(
            'AT+QSSLCFG="clientkey",2,"/security/user_key.pem"'
        )
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_client_key_with_different_parameters(
        self, mocker, ssl, mocked_response
    ):
        """This method tests set_ca_cert() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_client_key(1, "some/path.crt")

        mocking.assert_called_once_with('AT+QSSLCFG="clientkey",1,"some/path.crt"')
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_sec_level_with_default_parameters(self, mocker, ssl, mocked_response):
        """This method tests set_sec_level() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_sec_level()

        mocking.assert_called_once_with('AT+QSSLCFG="seclevel",2,2')
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_sec_level_with_different_parameters(
        self, mocker, ssl, mocked_response
    ):
        """This method tests set_sec_level() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_sec_level(1, 3)

        mocking.assert_called_once_with('AT+QSSLCFG="seclevel",1,3')
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_version_with_default_parameters(self, mocker, ssl, mocked_response):
        """This method tests set_version() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_version()

        mocking.assert_called_once_with('AT+QSSLCFG="sslversion",2,4')
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_version_with_different_parameters(self, mocker, ssl, mocked_response):
        """This method tests set_version() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_version(1, 3)

        mocking.assert_called_once_with('AT+QSSLCFG="sslversion",1,3')
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_cipher_suite_with_default_parameters(
        self, mocker, ssl, mocked_response
    ):
        """This method tests set_cipher_suite() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_cipher_suite()

        mocking.assert_called_once_with('AT+QSSLCFG="ciphersuite",2,0xFFFF')
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_cipher_suite_with_different_parameters(
        self, mocker, ssl, mocked_response
    ):
        """This method tests set_cipher_suite() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_cipher_suite(1, "0X0004")

        mocking.assert_called_once_with('AT+QSSLCFG="ciphersuite",1,0X0004')
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_ignore_local_time_with_default_parameters(
        self, mocker, ssl, mocked_response
    ):
        """This method tests set_ignore_local_time() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_ignore_local_time()

        mocking.assert_called_once_with('AT+QSSLCFG="ignorelocaltime",2,1')
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_ignore_local_time_with_different_parameters(
        self, mocker, ssl, mocked_response
    ):
        """This method tests set_ignore_local_time() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_ignore_local_time(1, 2)

        mocking.assert_called_once_with('AT+QSSLCFG="ignorelocaltime",1,2')
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_sni_enable(self, mocker, ssl, mocked_response):
        """This method tests set_sni() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_sni(1, 1)

        mocking.assert_called_once_with('AT+QSSLCFG="sni",1,1')
        assert result == mocked_response

    @pytest.mark.parametrize("mocked_response", default_response_types())
    def test_set_sni_disable(self, mocker, ssl, mocked_response):
        """This method tests set_sni() with its default parameters."""
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.set_sni(1, 0)

        mocking.assert_called_once_with('AT+QSSLCFG="sni",1,0')
        assert result == mocked_response

    def test_configure_for_x509_certification_all_success_case(self, mocker, ssl):
        """This method tests the state manager with mocking ATCom, and checks if
        they all called.
        """
        mocked_response = {"status": Status.SUCCESS, "response": "not important"}
        mocking = TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.configure_for_x509_certification()

        mocking.assert_any_call('AT+QSSLCFG="cacert",2,"/security/cacert.pem"')
        mocking.assert_any_call('AT+QSSLCFG="clientcert",2,"/security/client.pem"')
        mocking.assert_any_call('AT+QSSLCFG="clientkey",2,"/security/user_key.pem"')
        mocking.assert_any_call('AT+QSSLCFG="seclevel",2,2')
        mocking.assert_any_call('AT+QSSLCFG="sslversion",2,4')
        mocking.assert_any_call('AT+QSSLCFG="ciphersuite",2,0xFFFF')
        mocking.assert_any_call('AT+QSSLCFG="ignorelocaltime",2,1')
        assert result["status"] == mocked_response["status"]
        assert result["response"] == mocked_response["response"]

    def test_configure_for_x509_certification_fail(self, mocker, ssl):
        """This method tests the state manager with mocking ATCom as failed response.
        Hence, we can understand if failed responses also returned.
        """
        mocked_response = {"status": Status.ERROR, "response": "not important"}
        TestSSL.mock_send_at_comm(mocker, mocked_response)
        result = ssl.configure_for_x509_certification()

        assert result["status"] == mocked_response["status"]
        assert result["response"] == mocked_response["response"]
