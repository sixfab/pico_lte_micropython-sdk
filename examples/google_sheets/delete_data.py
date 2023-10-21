"""
Example code for deleting targeted datas of a Google Sheets table with using its API.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "google_sheets":{
        "api_key": "[API_KEY]",
        "spreadsheetId": "[SPREAD_SHEET_ID]",
        "client_id": "[CLIENT_ID]",
        "client_secret": "[CLIENT_SECRET]",
        "refresh_token": "[REFRESH_TOKEN]"
    }
}
"""
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

debug.info("Cleaning data from the Google Sheets table...")
result = picoLTE.google_sheets.delete_data(sheet="Sheet1", data_range="A1:C2")
debug.info("Result:", result)
