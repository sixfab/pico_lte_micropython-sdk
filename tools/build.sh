#!/bin/bash
# This script is used to embed the library as a frozen module and build the firmware.

DOWNLOAD_LOC="/tmp"

# Internal variables
PROJECT_DIR=$(pwd)
BUILD_ID="picoLTE-$(date +%Y-%m-%d-%H-%M-%S)"
GREEN='\033[0;32m'
RED='\033[0;31m'
NOCOLOR='\033[0m'

print_the_status_of_command() {
    if [ $? -eq 0 ]; then
        echo -e " ${GREEN}OK${NOCOLOR}"
    else
        echo -e " ${RED}FAILED${NOCOLOR}"
        exit 1
    fi
}

download_firmware() {
    cd $DOWNLOAD_LOC
    # Check if the MicroPython source code is already downloaded
    if [ -d "micropython" ]; then
        echo -n "- MicroPython source code already downloaded. Pulling the latest changes..."
        cd micropython
        git pull > /dev/null
    else
        echo -n "- Downloading latest MicroPython source code..."
        git clone --quiet git@github.com:micropython/micropython.git > /dev/null
    fi

    print_the_status_of_command
}

find_os_of_the_user() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "- Linux OS detected."
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "- MacOS detected."
        OS="macos"
    else
        echo "- Unknown OS detected. Exiting!"
        exit 1
    fi
}

download_the_toolchain_macos() {
    echo -n "- Downloading the toolset for MacOS..."
    # Download CMake using brew
    brew install cmake > /dev/null 2>&1
    # Download the toolchain using brew
    brew tap ArmMbed/homebrew-formulae > /dev/null 2>&1
    brew install arm-none-eabi-gcc > /dev/null 2>&1

    print_the_status_of_command
}

download_the_toolchain_linux() {
    echo -n "- Downloading the toolset for Linux with apt-get..."
    # Download CMake
    sudo apt-get install cmake > /dev/null 2>&1
    # Download the toolchain
    sudo apt-get install gcc-arm-none-eabi > /dev/null 2>&1

    print_the_status_of_command
}

prepare_the_environment() {
    find_os_of_the_user
    if [ "$OS" == "macos" ]; then
        download_the_toolchain_macos
    elif [ "$OS" == "linux" ]; then
        download_the_toolchain_linux
    fi

    cd $DOWNLOAD_LOC/micropython

    echo -n "- Building the MicroPython cross-compiler..."
    make -C mpy-cross > /dev/null
    print_the_status_of_command

    cd ports/rp2

    echo -n "- Building the git submodules..."
    make BOARD=PICO_W submodules > /dev/null 2>&1
    print_the_status_of_command

    echo -n "- Cleaning the older build files..."
    make BOARD=PICO_W clean > /dev/null
    print_the_status_of_command
}

copy_the_library_as_frozen_module() {
    echo -n "- Copying the library to frozen modules..."
    # Delete the older version of the library.
    rm -rf $DOWNLOAD_LOC/micropython/ports/rp2/modules/core > /dev/null 2>&1
    cp -r $PROJECT_DIR/core $DOWNLOAD_LOC/micropython/ports/rp2/modules/
    print_the_status_of_command
}

build_the_firmware() {
    echo -n "- Building the firmware with frozen module..."
    make BOARD=PICO_W > /dev/null 2>&1
    print_the_status_of_command
    
    # Copy the firmware to the project directory.
    mkdir -p $PROJECT_DIR/build
    echo -n "- Copying the firmware to the project directory..."
    cp build-PICO_W/firmware.uf2 $PROJECT_DIR/build/$BUILD_ID.uf2
    print_the_status_of_command

    echo "- Firmware build ID: $BUILD_ID"
}

# Main Function
download_firmware
prepare_the_environment
copy_the_library_as_frozen_module
build_the_firmware
echo "- Building process completed."