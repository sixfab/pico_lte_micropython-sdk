"""
Test module for the modules.auth module.
"""

import pytest

from core.modules.auth import Auth
from core.modules.file import File
from core.utils.atcom import ATCom
from core.utils.status import Status


class TestAuth:
    """Test class for Auth module."""

    @pytest.fixture
    def auth(self):
        """It returns an Auth instance."""
        atcom = ATCom()
        return Auth(atcom)

    @staticmethod
    def prepare_mocked_functions(
        mocker,
        simulation_data,
        side_effect_delete_file_from_modem=None,
        return_value_upload_to_file=None,
        get_file_list_status=True,
        side_effect_os_remove=None,
    ):
        """This function crates mocked function with predefined return values
        which will be given by the simulation_data parameter.
        """
        mocked_response_get_file_list = {
            "status": Status.SUCCESS if get_file_list_status else Status.ERROR,
            "response": simulation_data["file_name"],
        }

        mocker.patch(
            "core.modules.auth.read_file", side_effect=simulation_data["file_inside"]
        )
        mocker.patch(
            "core.modules.file.File.delete_file_from_modem",
            return_value=None,
            side_effect=side_effect_delete_file_from_modem,
        )
        mocker.patch(
            "core.modules.file.File.upload_file_to_modem",
            return_value=return_value_upload_to_file,
        )
        mocker.patch("os.remove", side_effect=side_effect_os_remove)
        mocker.patch(
            "core.modules.file.File.get_file_list",
            return_value=mocked_response_get_file_list,
        )

    def test_constructor_method(self, auth):
        """This method tests the constructor method of the Auth class."""
        assert isinstance(auth.atcom, ATCom)
        assert isinstance(auth.file, File)

    def test_load_certificates_ordinary_case(self, mocker, auth):
        """This method tests the load_certificates() method with
        expected and ordinary usage.
        """
        # Data which simulates system behaviour.
        mocked_data = {
            "file_name": ["cacert.pem", "client.pem", "user_key.pem"],
            "file_inside": ["CACERT_CERT", "CLIENT_CERT", "USER_PRIV_KEY"],
        }

        # Assign mock functions.
        TestAuth.prepare_mocked_functions(mocker, mocked_data)

        result = auth.load_certificates()

        assert result["status"] == Status.SUCCESS
        assert result["response"] == "Certificates found in modem."

    def test_load_certificates_wrong_certificate_names(self, mocker, auth):
        """This method tests the load_certificates() method without
        proper names.
        """
        # Data which simulates system behaviour.
        mocked_data = {
            "file_name": ["ca.pem", "cli.pem", "user.pem"],
            "file_inside": ["CACERT_CERT", "CLIENT_CERT", "USER_PRIV_KEY"],
        }

        # Assign mock functions.
        TestAuth.prepare_mocked_functions(mocker, mocked_data)

        result = auth.load_certificates()

        assert result["status"] == Status.ERROR
        assert result["response"] == "Certificates couldn't find in modem!"

    def test_load_certificates_file_throws_exception(self, mocker, auth):
        """This method tests the load_certificates() method, and file methods
        throws exception.
        """
        # Data which simulates system behaviour.
        mocked_data = {
            "file_name": ["cacert.pem", "client.pem", "user_key.pem"],
            "file_inside": ["CACERT_CERT", "CLIENT_CERT", "USER_PRIV_KEY"],
        }

        # Assign mock functions.
        TestAuth.prepare_mocked_functions(
            mocker,
            simulation_data=mocked_data,
            side_effect_delete_file_from_modem=OSError("Example Exception"),
        )
        result = auth.load_certificates()

        assert result["status"] == Status.ERROR
        assert result["response"] == "Example Exception"

    def test_load_certificates_with_already_certificate_inside(self, mocker, auth):
        """This method tests if the load_certificates() method cannot find new
        certificates in cert/ directory, and gets the old ones from modem file system.
        """
        # Data which simulates system behaviour. Note that, since file_inside is None,
        # it won't run first_try block.
        mocked_data = {
            "file_name": ["cacert.pem", "client.pem", "user_key.pem"],
            "file_inside": None,
        }
        # Assign mock functions.
        TestAuth.prepare_mocked_functions(
            mocker, simulation_data=mocked_data, get_file_list_status=True
        )

        result = auth.load_certificates()

        assert result["status"] == Status.SUCCESS
        assert result["response"] == "Certificates found in modem."

    def test_load_certificates_with_error_on_get_file_list(self, mocker, auth):
        """This method tests load_certificates() method when it is not the first_try
        and there is an error at connection with modem.
        """
        # Data which simulates system behaviour.
        mocked_data = {
            "file_name": ["cacert.pem", "client.pem", "user_key.pem"],
            "file_inside": None,
        }
        # Assign mock functions.
        TestAuth.prepare_mocked_functions(
            mocker, simulation_data=mocked_data, get_file_list_status=False
        )

        result = auth.load_certificates()

        assert result["status"] == Status.ERROR
        assert (
            result["response"] == "Error occured while getting certificates from modem!"
        )

    def test_load_certificates_with_error_on_os_remove(self, mocker, auth):
        """This method tests load_certificates() method when it is the first try,
        but the os_remove() method raises exception.
        """
        # Data which simulates system behaviour.
        mocked_data = {
            "file_name": ["cacert.pem", "client.pem", "user_key.pem"],
            "file_inside": ["CACERT_CERT", "CLIENT_CERT", "USER_PRIV_KEY"],
        }

        # Assign mock functions.
        TestAuth.prepare_mocked_functions(
            mocker,
            simulation_data=mocked_data,
            side_effect_os_remove=OSError("Example Exception"),
        )

        result = auth.load_certificates()

        assert result["status"] == Status.ERROR
        assert result["response"] == "Example Exception"
