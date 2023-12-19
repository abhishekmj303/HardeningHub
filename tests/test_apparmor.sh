#!/bin/bash

# Function to check if AppArmor is installed
check_apparmor_installed() {
    if ! command -v apparmor_status > /dev/null; then
        echo "AppArmor is not installed."
        return 1
    else
        echo "AppArmor is installed."
    fi
}

# Function to check AppArmor mode
check_apparmor_mode() {
    local mode="$1"
    local mode_count

    if [ "$mode" == "enforce" ]; then
        mode_count=$(sudo aa-status | grep -c 'profiles are in enforce mode')
    elif [ "$mode" == "complain" ]; then
        mode_count=$(sudo aa-status | grep -c 'profiles are in complain mode')
    else
        echo "Invalid mode specified: $mode"
        return 1
    fi

    if [ "$mode_count" -gt 0 ]; then
        echo "AppArmor is set to $mode mode."
    else
        echo "AppArmor is not set to $mode mode."
        return 1
    fi
}

# Main testing logic
main() {
    check_apparmor_installed || return 1

    # You need to set the mode variable based on your configuration
    # For example, if your config sets AppArmor to enforce mode, use 'enforce'
    local mode="enforce"

    check_apparmor_mode "$mode" || return 1

    echo "All tests passed."
}

main
