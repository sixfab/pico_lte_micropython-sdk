"""
Example code for creating a new Google Sheets spreadsheet and its sheets with using its API.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "google_sheets":{
        "api_key": "[API_KEY]",
        "client_id": "[CLIENT_ID]",
        "client_secret": "[CLIENT_SECRET]",
        "refresh_token": "[REFRESH_TOKEN]"
    }
}
"""
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

debug.info("Creating a new Google Sheets spreadsheet and its sheets...")
result = picoLTE.google_sheets.create_sheet(sheets=["Sheet1", "Sheet2"])
debug.info("Result:", result)
