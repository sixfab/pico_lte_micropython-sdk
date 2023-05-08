"""
Example code for deleting targeted or all datas of a Google Sheets table with using its API.

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

debug.info("Posting data to the google sheet...")
result = picoLTE.google_sheets.clean_sheet(sheet="SHEET_NAME", data_range="A1:C3")
debug.info("Result:", result)
