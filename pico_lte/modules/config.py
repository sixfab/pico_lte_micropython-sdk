"""
Module for including extended configuration function of picocell module.
"""

from pico_lte.common import config
from pico_lte.utils.helpers import read_json_file


class Config:
    """
    Class for including extended configuration functions.
    """

    def set_parameters(self, parameters):
        """
        Function for setting parameters in config.json file.

        Parameters
        ----------
        parameters : dict
            Dictionary with parameters.

        Returns
        -------
        dict
            Result that includes "status" and "response" keys
        """
        config["params"] = parameters

    def read_parameters_from_json_file(self, path):
        """
        Function for reading parameters from json file.

        Parameters
        ----------
        path : str
            Path to json file.

        Returns
        -------
        parameters : dict
            Dictionary with parameters.
        """
        parameters = read_json_file(path)
        config["params"] = parameters
