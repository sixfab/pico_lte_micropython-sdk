#!/bin/bash
# This script is used to run a MicroPython code on the PicoLTE device.

PROJECT_DIR=$(pwd)
PYBOARD_LOC="$PROJECT_DIR/tools/pyboard.py"

find_os_of_the_user() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        echo "- Unknown OS detected. Exiting!"
        exit 1
    fi
}

find_the_port_of_micropython_from_os() {
    # Do nothing if PORT is already set.
    if [ -n "$PORT" ]; then
        return
    fi

    if [ "$OS" == "macos" ]; then
        PORT=$(ls /dev/tty.usbmodem*)
    elif [ "$OS" == "linux" ]; then
        PORT=$(ls /dev/ttyACM*)
    fi

    # Select the first port if there are multiple ports.
    PORT=$(echo $PORT | cut -d ' ' -f 1)

    echo "- The port of the PicoLTE device is $PORT."
}

check_if_pyboard_tool_is_installed() {
    # This function checks if the pyboard.py available
    # in the same directory as this script.
    if [ ! -f $PYBOARD_LOC ]; then
        echo "- pyboard.py is not found in the same directory as this script."
        echo "- Please download it from GitHub."
        echo "https://github.com/micropython/micropython/blob/master/tools/pyboard.py"
        exit 1
    fi

    # Check if python is installed.
    if ! command -v python &> /dev/null
    then
        echo "- Python is not installed."
        exit 1
    fi
}

run_the_code() {
    # Check if the code is provided.
    if [ -z "$1" ]; then
        echo "- Please provide the code to run."
        exit 1
    fi

    # Check if the code is a file.
    if [ ! -f "$1" ]; then
        echo "- The code is not a file."
        exit 1
    fi

    # Check if the code is a Python file.
    if [[ "$1" != *.py ]]; then
        echo "- The code is not a Python file."
        exit 1
    fi

    # Print some blank lines.
    echo "- Running the code: $1"
    echo ""

    # Run the code.
    python $PYBOARD_LOC --device $PORT $1
}

# Run the script.
if [ ! -f "$PROJECT_DIR/tools/run.sh" ]; then
    echo "- This script must be run from the project root directory."
    exit 1
fi

find_os_of_the_user
check_if_pyboard_tool_is_installed
find_the_port_of_micropython_from_os
run_the_code $1