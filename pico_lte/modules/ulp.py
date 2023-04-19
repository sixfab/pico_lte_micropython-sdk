"""
Module for including ultra low power functions of PicoLTE module.

This module uses ultra lower power load switch and timer hardwares.
"""

import os
from machine import Pin
from pico_lte.common import config, debug
from pico_lte.utils.helpers import read_json_file, write_json_file
from pico_lte.utils.status import Status


CONST_TIMER = 1  # minutes
DEFAULT_PERIOD = 60  # minutes
ULP_FILE_PATH = "ulp.json"


class ULP:
    """
    Class for including ultra low power functions of PicoLTE module.
    """

    timer_done_pin = Pin(11, Pin.OUT)

    def __init__(self):
        """
        Constructor for ULP class
        """
        config["ulp"] = {}
        file_existence = str(os.listdir()).find(ULP_FILE_PATH)

        if file_existence != -1:
            ulp = read_json_file(ULP_FILE_PATH)
            config["ulp"]["status"] = ulp.get("status", False)
            config["ulp"]["timer_count"] = ulp.get("timer_count", 0)
            config["ulp"]["desired_timer_count"] = ulp.get("desired_timer_count", DEFAULT_PERIOD)
        else:
            config["ulp"] = {}
            config["ulp"]["status"] = False
            config["ulp"]["timer_count"] = 0
            config["ulp"]["desired_timer_count"] = DEFAULT_PERIOD
            self.save_ulp_config()

    def save_ulp_config(self):
        """
        Function for saving ultra low power configuration
        """
        try:
            write_json_file(ULP_FILE_PATH, config["ulp"])
        except Exception as error:
            debug.error("save_ulp_config", error)
            return {"response": str(error), "status": Status.ERROR}

    def enable(self):
        """
        Function for enabling ultra low power shutdown
        """
        config["ulp"]["status"] = True
        self.save_ulp_config()

    def disable(self):
        """
        Function for disabling ultra low power shutdown
        """
        config["ulp"]["status"] = False
        self.save_ulp_config()

    def set_deep_sleep_period(self, period=60):
        """
        Function for setting timer period.

        Parameters
        ----------
        period : int, default: 60
            Timer period in minutes. Must be power of CONTS_TIMER.
        """
        config["ulp"]["desired_timer_count"] = int(period / CONST_TIMER)
        self.save_ulp_config()

    def deep_sleep(self):
        """
        Function for shutting down PicoLTE module
        """
        self.timer_done_pin.value(1)

    def increase_counter(self):
        """
        Function for increasing timer counter
        """
        config["ulp"]["timer_count"] += 1
        self.save_ulp_config()

    def reset_counter(self):
        """
        Function for resetting timer counter
        """
        config["ulp"]["timer_count"] = 0
        self.save_ulp_config()

    def check(self):
        """
        Function for checking timer done
        """
        debug.debug("ULP: Check")

        if not config["ulp"].get("status", False):
            return

        count = config["ulp"].get("timer_count")
        desired_count = config["ulp"].get("desired_timer_count")

        if count < desired_count - 1:
            self.increase_counter()
            self.deep_sleep()
        else:
            self.reset_counter()
            # do the job
