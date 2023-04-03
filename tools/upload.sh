#!/bin/bash
# This script is used to upload the firmware to the Pico board.

# Internal variables
FW_LOCATIONS=$(pwd)/build
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


find_os_of_the_user() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        echo -e "${RED}- ERROR: Unknown OS detected. Exiting!${NOCOLOR}"
        exit 1
    fi
}

wait_user_to_connect_the_pico() {
    # Display the prompts in green
    echo -e "${GREEN}- Please connect the PicoLTE board to your computer while pressing BOOTSEL button.${NOCOLOR}"
    echo -e "${GREEN}- Press any key to continue...${NOCOLOR}"

    # Wait for the user to press a key
    read -n 1 -s
}

upload_the_firmware() {
    echo -n -e "- Uploading the firmware ${BUILD_ID} to the board..."

    if [ "$OS" == "macos" ]; then
        # Check if the volume exists.
        if [ ! -d "/Volumes/RPI-RP2" ]; then
            echo -e " ${RED}ERROR: The PicoLTE is not connected. Exiting!${NOCOLOR}"
            exit 1
        else
            cp $FW_LOCATIONS/$BUILD_ID.uf2 /Volumes/RPI-RP2
        fi
    elif [ "$OS" == "linux" ]; then
        # Check if the volume exists.
        if [ ! -d "/media/$USER/RPI-RP2" ]; then
            echo -e "${RED}ERROR: The PicoLTE is not connected. Exiting!${NOCOLOR}"
            exit 1
        else
            cp $FW_LOCATIONS/$BUILD_ID.uf2 /media/$USER/RPI-RP2
        fi
    fi

    wait_until_volume_detached
    print_the_status_of_command
}

wait_until_volume_detached() {
    if [ "$OS" == "macos" ]; then
        while [ -d /Volumes/RPI-RP2 ]
        do
            sleep 0.5
        done
    elif [ "$OS" == "linux" ]; then
        while [ -d /media/$USER/RPI-RP2 ]
        do
        sleep 1
        done
    fi
}

argument_parser() {
    HELP_TEXT="Usage: $0 <firmware_build_id>\nExample: $0 picoLTE-2023-01-01-01"

    if [ -z "$1" ]; then
        echo -e $HELP_TEXT
        exit 1
    elif [ "$1" == "--help" ]; then
        echo -e $HELP_TEXT
        exit 0
    elif [ "$1" == "-h" ]; then
        echo -e $HELP_TEXT
        exit 0
    else
        BUILD_ID="$1"
    fi
}

# Main function
argument_parser $1
wait_user_to_connect_the_pico
find_os_of_the_user
upload_the_firmware
echo "- Uploading process completed."