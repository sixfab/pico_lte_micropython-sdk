"""
Main code file.
"""

from pico_lte.modem import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

def main():
    debug.info("Hello from Sixfab...")
    debug.info("Your PicoLTE is ready to use!")
    debug.info("Visit the following link to get started")
    debug.info("http://sixfab.com/picolte/")


if __name__ == "__main__":
    main()
