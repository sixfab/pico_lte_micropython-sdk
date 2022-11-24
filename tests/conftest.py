import os
import errno
import pytest


def write_file(file_path, data, file_type="t"):
    """This function creates a file with data."""
    try:
        with open(file_path, "w" + file_type, encoding="utf-8") as file:
            file.write(data)
    except OSError:
        return None
    else:
        return data


def remove_file(file_path):
    """This function deletes a file in the file-system if exists."""
    try:
        os.remove(file_path)
    except OSError as error:
        if error.errno != errno.ENOENT:
            raise error


MOCK_MACHINE_PY = """
class UART:
    def __init__(self, *args, **kwargs):
        pass

    def write(self):
        pass

    def any(self):
        pass

    def read(self):
        pass


class Pin:

    OUT = 0
    IN = 1

    def __init__(self, pin_id=None, pin_dir=None, *args, **kwargs):
        self.pin_num = pin_id
        self.pin_dir = pin_dir
    
    def value(*args, **kwargs):
        pass

    def value(self, *args, **kwargs):
        pass


class I2C:
    def __init__(self, *args, **kwargs):
        pass

    def scan(self, *args, **kwargs):
        pass

class ADC:
    def __init__(self, *args, **kwargs):
        pass
"""

MOCK_NEOPIXEL_PY = """
class NeoPixel:
    
    def __init__(self, *args, **kwargs):
        pass
"""

MOCK_UBINASCII_PY = ""


def prepare_test_enviroment():
    """
    Function for preparing test enviroment
    """
    write_file("machine.py", MOCK_MACHINE_PY)
    write_file("neopixel.py", MOCK_NEOPIXEL_PY)
    write_file("ubinascii.py", MOCK_UBINASCII_PY)


@pytest.hookimpl()
def pytest_sessionstart(session):
    """This method auto-runs each time tests are started."""
    print("Test enviroment preparing...")
    prepare_test_enviroment()


@pytest.hookimpl()
def pytest_sessionfinish(session):
    """This method auto-runs each time tests are ended."""
    print("Test enviroment cleaning...")
    remove_file("machine.py")
    remove_file("neopixel.py")
    remove_file("ubinascii.py")
