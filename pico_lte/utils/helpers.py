"""
Module for storing helper functions
"""

import json
from pico_lte.common import config
from pico_lte.utils.status import Status


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


def deep_copy_of_dictionary(dict_instance):
    """Create a deepcopy of the dictionary given.

    Parameters
    ----------
    dict_instance : dict
        It is the dictionary to be copied.
    """
    if isinstance(dict_instance, dict):
        dictionary_to_return = {}

        for key, value in dict_instance.items():
            dictionary_to_return[key] = value

        return dictionary_to_return
    else:
        return None


def get_desired_data(result, prefix, separator=",", data_index=0):
    """Function for getting actual data from response"""
    result_to_return = deep_copy_of_dictionary(result)

    valuable_lines = None

    if result.get("status") != Status.SUCCESS:
        result["value"] = None
        return result

    response = result_to_return.get("response")

    for index, value in enumerate(response):
        if value == "OK" and index > 0:
            valuable_lines = [response[i] for i in range(0, index)]

    if valuable_lines:
        for line in valuable_lines:
            prefix_index = line.find(prefix)

            if prefix_index != -1:
                index = prefix_index + len(prefix)  # Find index of meaningful data
                data_array = line[index:].split(separator)

                if isinstance(data_index, list):  # If desired multiple data
                    data_index = data_index[: len(data_array)]  # Truncate data_index
                    result_to_return["value"] = [
                        simplify(data_array[i]) for i in data_index
                    ]  # Return list
                elif isinstance(data_index, int):
                    # If data_index is out of range, return first element
                    data_index = data_index if data_index < len(data_array) else 0
                    result_to_return["value"] = simplify(
                        data_array[data_index]
                    )  # Return single data
                elif data_index == "all":
                    result_to_return["value"] = [simplify(data) for data in data_array]
                else:
                    # If data_index is unknown type, return first element
                    data_index = 0
                    result_to_return["value"] = simplify(
                        data_array[data_index]
                    )  # Return single data
                return result_to_return
    # if no valuable data found
    result_to_return["value"] = None
    return result_to_return


def simplify(text):
    """Function for simplifying strings"""
    if isinstance(text, str):
        return text.replace('"', "").replace("'", "")
    return text


def read_file(file_path, file_type="t"):
    """
    Function for reading file
    """
    try:
        with open(file_path, "r" + file_type) as file:
            data = file.read()
    except:
        return None
    else:
        return data


def write_file(file_path, data, file_type="t"):
    """
    Function for writing file
    """
    try:
        with open(file_path, "w" + file_type) as file:
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
