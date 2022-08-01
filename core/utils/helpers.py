"""
Module for storing helper functions
"""

import json
from core.temp import config

def read_json_file(file_path):
    """
    Function for reading json file
    """
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except:
        return None
    else:
        return data

def write_json_file(file_path, data):
    """
    Function for writing json file
    """
    try:
        with open(file_path, "w") as file:
            json.dump(data, file)
    except:
        return None
    else:
        return data


def get_desired_data_from_response(response, prefix, separator="\n", data_index=0):
    """Function for getting actual data from response"""
    print(response)
    response = response.replace("\r","\n").replace('"','') # Simplify response
    index = response.find(prefix) + len(prefix) # Find index of meaningful data
    data_array = response[index:].split("\n")[0].split(separator)

    if isinstance(data_index, list):    # If desired multiple data, data_index should be list
        return [data_array[i] for i in data_index]
    return data_array[data_index]


def read_file(file_path):
    """
    Function for reading file
    """
    try:
        with open(file_path, "r") as file:
            data = file.read()
    except:
        return None
    else:
        return data

def write_file(file_path, data):
    """
    Function for writing file
    """
    try:
        with open(file_path, "w") as file:
            file.write(data)
    except:
        return None
    else:
        return data


def get_parameter(key, default=None):
    """
    Function for getting parameters for SDK methods from global config dictionary.
    """
    if isinstance(config["params"], dict):
        return config["params"].get(key)
    if default:
        return default
    return None
