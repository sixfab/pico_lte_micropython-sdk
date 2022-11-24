"""
Test module for the modules.file module.
"""

import pytest

from core.modules.file import File
from core.utils.atcom import ATCom
from core.utils.status import Status


class TestFile:
    """
    Test class for File.
    """

    @pytest.fixture
    def file(self):
        """This fixtures returns a File instance."""
        atcom = ATCom()
        return File(atcom)

    def test_constructor(self, file):
        """This method checks the initialization of the object."""
        assert isinstance(file.atcom, ATCom)
        assert file.CTRL_Z == "\x1A"

    def test_get_file_list(self, mocker, file):
        """This method checks the get_file_list() with mocked ATCom responses."""
        mocked_return = {"status": Status.SUCCESS, "response": ["some", "response"]}
        mocking = mocker.patch("core.utils.atcom.ATCom.send_at_comm", return_value=mocked_return)

        result = file.get_file_list()

        mocking.assert_called_once_with('AT+QFLST="*"')
        assert result == mocked_return

    def test_delete_file_from_modem(self, mocker, file):
        """This method checks the delete_file_from_modem() with mocked ATCom responses."""
        mocked_return = {"status": Status.SUCCESS, "response": ["some", "response"]}
        mocking = mocker.patch("core.utils.atcom.ATCom.send_at_comm", return_value=mocked_return)

        result = file.delete_file_from_modem("file.pem")

        mocking.assert_called_once_with('AT+QFDEL="file.pem"')
        assert result == mocked_return

    def test_upload_file_to_modem_ordinary_case(self, mocker, file):
        """This method checks the upload_file_to_modem() with mocked ATCom responses."""
        # Mock the necessary function.
        mocker.patch("core.modules.file.len", return_value=60)
        mocker.patch("core.utils.atcom.ATCom.send_at_comm_once")
        mocked_responses = [
            {"status": Status.SUCCESS, "response": ["CONNECT"]},
            {"status": Status.SUCCESS, "response": ["OK"]},
        ]
        mocking = mocker.patch("core.utils.atcom.ATCom.send_at_comm", side_effect=mocked_responses)

        result = file.upload_file_to_modem("file.pem", None)

        mocking.assert_any_call('AT+QFUPL="file.pem",60,5000', "CONNECT", urc=True)
        mocking.assert_any_call(file.CTRL_Z)
        assert result == mocked_responses[1]

    def test_upload_file_to_modem_no_connect(self, mocker, file):
        """This method checks the upload_file_to_modem() with mocked ATCom responses
        but with no CONNECT returned.
        """
        # Mock the necessary function.
        mocker.patch("core.modules.file.len", return_value=60)
        mocked_response = {"status": Status.TIMEOUT, "response": "timeout"}
        mocking = mocker.patch("core.utils.atcom.ATCom.send_at_comm", return_value=mocked_response)

        result = file.upload_file_to_modem("file.pem", None)

        mocking.assert_any_call('AT+QFUPL="file.pem",60,5000', "CONNECT", urc=True)
        assert mocking.call_count == 1
        assert result == mocked_response
