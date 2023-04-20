"""
config.json
{
    "google_sheets":{
        "create_url": "[CREATE_URL]"
    }
}
"""
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

debug.info("Creating a google sheet...")
result = picoLTE.google_sheets.create_sheet("It is test message from PicoLTE!")
debug.info("Result:", result)
