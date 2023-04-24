"""
config.json
{
    "google_sheets":{
        "api_key":"[API_KEY]",
        "spreadsheetId": "[spreadsheetId]",
        "majorDimension": [majorDimension],
        "valueRenderOption": [valueRenderOption],
        "dateTimeRenderOption": [dateTimeRenderOption]
    }
}
"""
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

debug.info("Creating a google sheet...")
result = picoLTE.google_sheets.get_data()
debug.info("Result:", result)
