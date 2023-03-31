"""
Main code file.
"""

from core.pico_lte import PicoLTE
from core.temp import debug

pico_lte = PicoLTE()


def main():
    debug.info("Hello from Sixfab...")
    debug.info("Your Sixfab Pico LTE is ready to use!")
    debug.info("Visit the following link to get started")
    debug.info("http://docs.sixfab.com/PicoLTE/")


if __name__ == "__main__":
    main()
