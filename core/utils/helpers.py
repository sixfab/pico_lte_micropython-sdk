"""
Module for storing helper functions
"""

import json
from core.temp import config, debug
from core.utils.status import Status

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


def get_desired_data(result, prefix, separator=",", data_index=0):
    """Function for getting actual data from response"""
    valuable_lines = None

    if result.get("status") != Status.SUCCESS:
        result["value"] = None
        return result

    response = result.get("response")

    for index, value in enumerate(response):
        if value == "OK" and index > 0:
            valuable_lines = [response[i] for i in range(0, index)]

    if valuable_lines:
        for line in valuable_lines:
            prefix_index = line.find(prefix)

            if prefix_index != -1:
                index =  prefix_index + len(prefix) # Find index of meaningful data
                data_array = line[index:].split(separator)

                if isinstance(data_index, list): # If desired multiple data
                    data_index = data_index[:len(data_array)] # Truncate data_index
                    result["value"] = [simplify(data_array[i]) for i in data_index] # Return list
                elif isinstance(data_index, int):
                    # If data_index is out of range, return first element
                    data_index = data_index if data_index < len(data_array) else 0
                    result["value"] = simplify(data_array[data_index]) # Return single data
                elif data_index == "all":
                    result["value"] = [simplify(data) for data in data_array]
                else:
                    # If data_index is unknown type, return first element
                    data_index = 0
                    result["value"] = simplify(data_array[data_index]) # Return single data
                return result
    # if no valuable data found
    result["value"] = None
    return result


def simplify(text):
    """Function for simplifying strings"""
    if isinstance(text, str):
        return text.replace('"', "").replace("'", "")
    return text


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


def get_parameter(path, default=None):
    """
    Function for getting parameters for SDK methods from global config dictionary.
    """
    desired = config.get("params", None)

    if isinstance(desired, dict):
        for element in path:
            if desired:
                desired = desired.get(element, None)
        if desired:
            return desired
    if default:
        return default
    return None
