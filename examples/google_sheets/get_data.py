"""
Example code for getting data from a Google Sheets document with using its API.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "google_sheets":{
        "host": "[HOST_URL]",
        "api_key": "[API_KEY_OF_GOOGLE_SHEETS_DOCUMENT]",
        "token": "[AUTHORIZATION_TOKEN]",
        "spreadsheetId": "[SPREAD_SHEET_ID]",
        "get":{
            "data_range": "[DATA_RANGE_OF_TABLE]",
            "majorDimension": "[MAJOR_DIMENSION_OPTION]",
            "sheet": "[SHEET_NAME]",
            "valueRenderOption": "FORMATTED_VALUE"
        }
    }
}

"""
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

debug.info("Getting data from the google sheet...")
result = picoLTE.google_sheets.get_data()
debug.info("Result:", result)
