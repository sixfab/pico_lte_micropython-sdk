from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

debug.info("Setting quick event on Google Calendar.")
result = picoLTE.make_automation.send_data("Test Data")
debug.info("Result: ", result)
