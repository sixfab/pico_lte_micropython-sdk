"""
Example code for getting data from a Google Sheets document with using its API.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "google_sheets":{
        "api_key": "[API_KEY_OF_GOOGLE_SHEETS_DOCUMENT]",
        "spreadsheetId": "[SPREAD_SHEET_ID]",
        "client_id": "[CLIENT_ID]",
        "client_secret": "[CLIENT_SECRET]",
        "refresh_token": "[REFRESH_TOKEN]"
    }
}

"""
from pico_lte.core import PicoLTE
from pico_lte.common import debug

debug.set_level(0)
picoLTE = PicoLTE()

debug.info("Getting data from the Google Sheet document...")
result = picoLTE.google_sheets.get_data(sheet = "Sayfa1", data_range = "A1:C3")
debug.info("Result:", result)
