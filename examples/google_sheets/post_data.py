"""
Example code for posting data to a Google Sheets document with using its API.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "google_sheets":{
        "host": "[YOUR_HOST_URL]",
        "api_key": "[API_KEY_OF_GOOGLE_SHEETS_DOCUMENT]",
        "token": "[AUTHORIZATION_TOKEN]",
        "spreadsheetId": "[SPREAD_SHEET_ID]",
        "post": {
            "data_range": "[DATA_RANGE_OF_TABLE]",
            "valueInputOption": "[VALUE_RENDER_OPTION]",
            "majorDimension": "[MAJOR_DIMENSION_OPTION]",
            "sheet": "[SHEET_NAME]"
        }
    }
}
"""
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

debug.info("Posting data to the google sheet...")
result = picoLTE.google_sheets.post_data(data=[[7, 8, 9]], data_range="A5:C5")
debug.info("Result:", result)
