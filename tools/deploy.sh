#!/bin/bash
# This script is used to embed the library and upload the firmware to the Pico board.

# Internal variables
PROJECT_DIR=$(pwd)
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

build_the_firmware() {
    # Run the build script.
    source $PROJECT_DIR/tools/build.sh $1
}

upload_the_script() {
    # Run the upload script.
    cd $PROJECT_DIR
    chmod a+x $PROJECT_DIR/tools/upload.sh
    $PROJECT_DIR/tools/upload.sh $BUILD_ID
}

# Main function
echo "[  BUILD  ]"
build_the_firmware $1
echo "[  UPLOAD  ]"
upload_the_script