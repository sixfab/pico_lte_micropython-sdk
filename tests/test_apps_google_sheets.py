"""
Test module for the apps.google_sheets module.
"""

import pytest

from pico_lte.utils.status import Status
from pico_lte.apps.google_sheets import GoogleSheets
from pico_lte.utils.manager import StateManager, Step

from pico_lte.utils.atcom import ATCom
from pico_lte.modules.base import Base
from pico_lte.modules.http import HTTP
from pico_lte.modules.network import Network


class TestGoogleSheets:
    """
    Test class for Google Sheets.
    """

    @pytest.fixture()
    def google_sheets_object(self):
        """This fixture returns a GoogleSheets instance."""
        atcom = ATCom()
        base = Base(atcom)
        network = Network(atcom, base)
        http = HTTP(atcom)

        google_sheets = GoogleSheets(base, network, http)
        return google_sheets

    def test_constructor(self, google_sheets_object):
        """This method tests the __init__ constructor."""
        assert isinstance(google_sheets_object.base, Base)
        assert isinstance(google_sheets_object.network, Network)
        assert isinstance(google_sheets_object.http, HTTP)

    def test_set_network_success(self, mocker, google_sheets_object):
        """This method tests the set_network() with mocked StateManager responses."""
        mocker.patch(
            "pico_lte.utils.manager.StateManager.run",
            return_value={"status": Status.SUCCESS},
        )

        response = google_sheets_object.set_network()
        assert response == {"status": Status.SUCCESS}

    def test_set_network_error(self, mocker, google_sheets_object):
        """This method tests the set_network() with mocked StateManager responses."""
        mocker.patch(
            "pico_lte.utils.manager.StateManager.run",
            return_value={"status": Status.ERROR},
        )

        response = google_sheets_object.set_network()
        assert response == {"status": Status.ERROR}

    def test_get_data_success(self, mocker, google_sheets_object):
        """This method tests the get_data() with mocked StateManager responses."""
        mocker.patch(
            "pico_lte.utils.manager.StateManager.run",
            return_value={"status": Status.SUCCESS, "response": "", "interval": ""},
        )

        response = google_sheets_object.get_data(
            sheet="sheet", data_range="[DATA_RANGE]"
        )
        assert response == {"status": Status.SUCCESS, "response": ""}

    def test_get_data_error(self, mocker, google_sheets_object):
        """This method tests the get_data() with mocked StateManager responses."""
        mocker.patch(
            "pico_lte.utils.manager.StateManager.run",
            return_value={"status": Status.ERROR, "response": "", "interval": ""},
        )

        response = google_sheets_object.get_data(
            sheet="sheet", data_range="[DATA_RANGE]"
        )
        assert response == {"status": Status.ERROR, "response": ""}

    def test_add_row_success(self, mocker, google_sheets_object):
        """This method tests the add_row() with mocked StateManager responses."""
        mocker.patch(
            "pico_lte.utils.manager.StateManager.run",
            return_value={"status": Status.SUCCESS, "response": "", "interval": ""},
        )

        response = google_sheets_object.add_row(sheet="sheet", data=[])
        assert response == {"status": Status.SUCCESS, "response": ""}

    def test_add_row_error(self, mocker, google_sheets_object):
        """This method tests the add_row() with mocked StateManager responses."""
        mocker.patch(
            "pico_lte.utils.manager.StateManager.run",
            return_value={"status": Status.ERROR, "response": "", "interval": ""},
        )

        response = google_sheets_object.add_row(sheet="sheet", data=[])
        assert response == {"status": Status.ERROR, "response": ""}

    def test_add_data_success(self, mocker, google_sheets_object):
        """This method tests the add_data() with mocked StateManager responses."""
        mocker.patch(
            "pico_lte.utils.manager.StateManager.run",
            return_value={"status": Status.SUCCESS, "response": "", "interval": ""},
        )

        response = google_sheets_object.add_data(
            sheet="sheet", data=[], data_range="[DATA_RANGE]"
        )
        assert response == {"status": Status.SUCCESS, "response": ""}

    def test_add_data_error(self, mocker, google_sheets_object):
        """This method tests the add_data() with mocked StateManager responses."""
        mocker.patch(
            "pico_lte.utils.manager.StateManager.run",
            return_value={"status": Status.ERROR, "response": "", "interval": ""},
        )

        response = google_sheets_object.add_data(
            sheet="sheet", data=[], data_range="[DATA_RANGE]"
        )
        assert response == {"status": Status.ERROR, "response": ""}

    def test_create_sheet_success(self, mocker, google_sheets_object):
        """This method tests the create_sheet() with mocked StateManager responses."""
        mocker.patch(
            "pico_lte.utils.manager.StateManager.run",
            return_value={"status": Status.SUCCESS, "response": "", "interval": ""},
        )

        response = google_sheets_object.create_sheet(sheets=[])
        assert response == {"status": Status.SUCCESS, "response": ""}

    def test_create_sheet_error(self, mocker, google_sheets_object):
        """This method tests the create_sheet() with mocked StateManager responses."""
        mocker.patch(
            "pico_lte.utils.manager.StateManager.run",
            return_value={"status": Status.ERROR, "response": "", "interval": ""},
        )

        response = google_sheets_object.create_sheet(sheets=[])
        assert response == {"status": Status.ERROR, "response": ""}

    def test_delete_data_success(self, mocker, google_sheets_object):
        """This method tests the delete_data() with mocked StateManager responses."""
        mocker.patch(
            "pico_lte.utils.manager.StateManager.run",
            return_value={"status": Status.SUCCESS, "response": "", "interval": ""},
        )

        response = google_sheets_object.delete_data(
            sheet="sheet", data_range="[DATA_RANGE]"
        )
        assert response == {"status": Status.SUCCESS, "response": ""}

    def test_delete_data_error(self, mocker, google_sheets_object):
        """This method tests the delete_data() with mocked StateManager responses."""
        mocker.patch(
            "pico_lte.utils.manager.StateManager.run",
            return_value={"status": Status.ERROR, "response": "", "interval": ""},
        )

        response = google_sheets_object.delete_data(
            sheet="sheet", data_range="[DATA_RANGE]"
        )
        assert response == {"status": Status.ERROR, "response": ""}

    def test_generate_access_token_success(self, mocker, google_sheets_object):
        """This method tests the generate_access_token() with mocked StateManager responses."""
        mocker.patch(
            "pico_lte.utils.manager.StateManager.run",
            return_value={
                "status": Status.SUCCESS,
                "response": ['{"access_token": "[ACCESS_TOKEN]"}'],
            },
        )

        response = google_sheets_object.generate_access_token()
        assert response == {
            "status": Status.SUCCESS,
            "response": "Access token is generated.",
        }

    def test_generate_access_token_error(self, mocker, google_sheets_object):
        """This method tests the generate_access_token() with mocked StateManager responses."""
        mocker.patch(
            "pico_lte.utils.manager.StateManager.run",
            return_value={
                "status": Status.ERROR,
                "response": "",
            },
        )

        response = google_sheets_object.generate_access_token()
        assert response == {
            "status": Status.ERROR,
            "response": "Access token could not be generated.",
        }
