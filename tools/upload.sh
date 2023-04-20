#!/bin/bash
# This script is used to upload the firmware to the PicoLTE.

# Internal variables
PYBOARD_LOC="$(pwd)/tools/pyboard.py"
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
    echo -e "${GREEN}- Please connect the PicoLTE board. Press any key to continue...${NOCOLOR}"

    # Wait for the user to press a key
    read -n 1 -s
}

enter_bootloader_mode_on_pico() {
    # This function uses pyboard tool to enter the bootloader mode on the PicoLTE.
    # with sending "import machine; machine.bootloader()"" command.
    echo -n -e "- Entering the bootloader mode on the PicoLTE..."
    python3 $PYBOARD_LOC -d /dev/cu.usbmodem* -c "import machine; machine.bootloader()" > /dev/null 2>&1
    sleep 1.5

    # Print OK for always since 'sleep' is always successes.
    print_the_status_of_command

}

check_board_connection() {
    # This function checks if the PicoLTE is connected to the computer.
    RPI_VENDOR_ID="2e8a"
    MP_PRODUCT_ID="0005"
    BOOT_PRODUCT_ID="0003"

    # It uses lsusb to check if the board is connected.
    # And the state of the connection as a storage or serial.
    if lsusb | grep -q "$VENDOR_ID:$MP_PRODUCT_ID"; then
        BOARD_MODE="serial"
    elif lsusb | grep -q "$VENDOR_ID:$BOOT_PRODUCT_ID"; then
        BOARD_MODE="storage"
    else
        BOARD_MODE="none"
    fi
}

check_pico_storage_attached() {
    # This function checks if the PicoLTE is connected to the computer.
    # If the board is connected, it returns 0. Otherwise, it returns 1.
    if [ "$OS" == "macos" ]; then
        if [ -d "/Volumes/RPI-RP2" ]; then
            return 0
        else
            return 1
        fi
    elif [ "$OS" == "linux" ]; then
        if [ -d "/media/$USER/RPI-RP2" ]; then
            return 0
        else
            return 1
        fi
    fi
}

pico_connection_logic() {
    check_board_connection

    # If the board is connected in serial mode, it enters the bootloader mode.
    # If the board is connected in storage mode, it does nothing.
    # If the board is not connected, it waits for the user to connect the board.
    if [ "$BOARD_MODE" == "serial" ]; then
        echo -e "- PicoLTE is connected in serial mode."
        enter_bootloader_mode_on_pico
    elif [ "$BOARD_MODE" == "storage" ]; then
        echo -e "- PicoLTE is connected in storage mode."
    elif [ "$BOARD_MODE" == "none" ]; then
        # If the board is not connected, it waits for the user to connect the board.
        wait_user_to_connect_the_pico
        check_board_connection

        # Does the same logic as above.
        if [ "$BOARD_MODE" == "serial" ]; then
            echo -e "- PicoLTE is connected in serial mode."
            enter_bootloader_mode_on_pico
        elif [ "$BOARD_MODE" == "storage" ]; then
            echo -e "- PicoLTE is connected in storage mode."
        elif [ "$BOARD_MODE" == "none" ]; then
            echo -e "${RED}- PicoLTE is not connected.${NOCOLOR}"
            exit 1
        fi
    fi

    # If the board is connected in storage mode, it uploads the firmware.
    if check_pico_storage_attached; then
        upload_the_firmware
    else
        echo -e "${RED}- PicoLTE is not connected. Please connect the PicoLTE and try again.${NOCOLOR}"
        exit 1
    fi
}

upload_the_firmware() {
    echo -n -e "- Uploading the firmware ${BUILD_ID} to the board..."

    if [ "$OS" == "macos" ]; then
        cp $FW_LOCATIONS/$BUILD_ID.uf2 /Volumes/RPI-RP2
    elif [ "$OS" == "linux" ]; then
        cp $FW_LOCATIONS/$BUILD_ID.uf2 /media/$USER/RPI-RP2
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
find_os_of_the_user
pico_connection_logic
echo "- Uploading process completed."