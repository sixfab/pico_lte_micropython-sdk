import os
import pytest


def write_file(file_path, data, file_type="t"):
    try:
        with open(file_path, "w" + file_type) as file:
            file.write(data)
    except:
        return None
    else:
        return data


mock_machine = """
class UART:
    def __init__(self, *args, **kwargs):
        pass

    def write(self):
        pass


class Pin:

    OUT = None
    IN = None

    def __init__(self, *args, **kwargs):
        pass


class I2C:
    def __init__(self, *args, **kwargs):
        pass
"""

mock_neopixel = """
class NeoPixel:
    
    def __init__(self, *args, **kwargs):
        pass
"""

mock_ubinascii = ""


def prepare_test_enviroment():
    """
    Function for preparing test enviroment
    """

    write_file("machine.py", mock_machine)
    write_file("neopixel.py", mock_neopixel)
    write_file("ubinascii.py", mock_ubinascii)


@pytest.hookimpl()
def pytest_sessionstart(session):
    print("Test enviroment preparing...")
    prepare_test_enviroment()


@pytest.hookimpl()
def pytest_sessionfinish(session):
    print("Test enviroment cleaning...")
    os.remove("machine.py")
    os.remove("neopixel.py")
    os.remove("ubinascii.py")
