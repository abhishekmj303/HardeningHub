#!/bin/bash

# Function to run commands and handle errors
run_command() {
    "$@"
    if [ $? -ne 0 ]; then
        echo "Error: Command failed - $@"
        exit 1
    fi
}

# Set file paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
RULES_CONF_PATH="$SCRIPT_DIR/../BackEnd/rules.conf"


TEMP_DISABLE_FILE="$SCRIPT_DIR/disable_usbguard.tmp"
# Check if rules.conf exists
if [ ! -f "$RULES_CONF_PATH" ]; then
    echo "Error: rules.conf file not found."
    exit 1
fi

if [ -f "$TEMP_DISABLE_FILE" ]; then
    run_command sudo systemctl disable --now usbguard
    rm "$TEMP_DISABLE_FILE"  # Clean up the temporary file
else
    run_command sudo install -m 0600 -o root -g root "$RULES_CONF_PATH" 
    # Restart and enable USBGuard
    run_command sudo systemctl daemon-reload
    run_command sudo systemctl restart usbguard
    run_command sudo systemctl enable usbguard
fi

echo "Script execution completed successfully."
