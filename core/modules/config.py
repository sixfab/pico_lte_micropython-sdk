"""
Module for including extended configuration function of picocell module.
"""

from core.temp import config
from core.utils.helpers import read_json_file

class Config:
    """
    Class for including extended configuration functions.
    """
    def __init__(self, atcom):
        """
        Constructor of the Config class.
        """
        self.atcom = atcom

    def set_parameters(self, parameters):
        """
        Function for setting parameters in config.json file.

        Parameters
        ----------
        parameters : dict
            Dictionary with parameters.

        Returns
        -------
        (response, status) : tuple
            response : str
                Response from the command
            status : int
                Status of the command.
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
