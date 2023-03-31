"""
Main code file.
"""

from core.sixfab_lte import SixfabLTE
from core.temp import debug

devboard = SixfabLTE()


def main():
    debug.info("Hello from Sixfab...")
    debug.info("Your Sixfab LTE Development Board is ready to use!")
    debug.info("Visit the following link to get started")
    debug.info("http://docs.sixfab.com/sixfab_lte_dev_board/")


if __name__ == "__main__":
    main()
