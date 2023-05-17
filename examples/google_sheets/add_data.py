"""
Example code for data adding or updating operations of a Google Sheets document with using its API.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "google_sheets":{
        "api_key": "[API_KEY_OF_GOOGLE_SHEETS_DOCUMENT]",
        "OAuthToken": "[AUTHORIZATION_TOKEN]",
        "spreadsheetId": "[SPREAD_SHEET_ID]"
    }
}

"""
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

debug.info("Adding data to the Google Sheets table...")
result = picoLTE.google_sheets.add_data(data=[[1, 2, 3], [4, 5, 6]], data_range="A1:C2")
debug.info("Result:", result)
