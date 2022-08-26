"""
Main code file.
"""

from core.modem import Modem
from core.temp import debug

modem = Modem()

def main():
    debug.info("Hello from Sixfab...")
    debug.info("Your Picocell is ready to use!")
    debug.info("Visit the following link to get started")
    debug.info("http://docs.sixfab.com/picocell/")

if __name__ == "__main__":
    main()
