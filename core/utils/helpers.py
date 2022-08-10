"""
Module for storing helper functions
"""

import json
from core.temp import config, debug

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


def extract_messages(whole_message, prefix, remove_nones=True):
    """_Function for extracting meaningful messages as an array
    from the response of +QMTRECV.

    Args:
        whole_message (str): The response from the "+QMTRECV" command.
        prefix (str): The prefix string for each meaningful message.
        remove_nones (bool, optional): Delete None messages. Defaults to True.

    Returns:
        array: Array of messages arrays.
    """
    messages = []
    start_pos = 0
    end_pos = 0

    # Pre-processing the string.
    whole_message = whole_message.replace("\r","\n").replace('"','')

    while True:
        start_pos = whole_message.find(prefix, start_pos)

        # If there is no, exit the function.
        if start_pos == -1:
            return messages

        # Find the end
        end_pos = whole_message.find("\n", start_pos)

        # Extract the non-relational information.
        if "0,0,0,0,0,0" not in whole_message[start_pos:end_pos] and remove_nones is True:
            # Extract and clean the unformatted string.
            message = whole_message[(start_pos + len(prefix)) : end_pos]
            message_as_array = message.split(",")
            message_as_array[0] = int(message_as_array[0])
            # Save it to the array.
            messages.append(message_as_array)

        # Increase the searching position.
        start_pos += len(prefix)


def get_desired_data_from_response(response, prefix, separator="\n", data_index=0):
    """Function for getting actual data from response"""
    debug.debug(response)
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
