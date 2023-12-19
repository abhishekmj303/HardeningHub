#!/bin/bash

# Function to check if a package is installed
check_package_installed() {
    local package="$1"
    if dpkg-query -W -f='${Status}' "$package" 2>/dev/null | grep -q "ok installed"; then
        echo "$package is installed."
    else
        echo "$package is NOT installed."
        return 1
    fi
}

# Function to check GDM user list configuration
check_gdm_user_list_disabled() {
    if grep -qs 'disable-user-list=true' /etc/dconf/db/gdm.d/00-login-screen; then
        echo "GDM user list is disabled."
    else
        echo "GDM user list is NOT disabled."
        return 1
    fi
}

# Function to check idle delay
check_idle_delay() {
    local expected_value="$1"
    local actual_value=$(dconf read /org/gnome/desktop/session/idle-delay)
    if [ "$actual_value" = "uint32 $expected_value" ]; then
        echo "Idle delay is correctly set to $expected_value."
    else
        echo "Idle delay is NOT set to $expected_value."
        return 1
    fi
}

# Function to check if autorun is disabled
check_autorun_disabled() {
    if grep -qs 'autorun-never=true' /etc/dconf/db/gdm.d/00-media-autorun; then
        echo "Autorun is disabled."
    else
        echo "Autorun is NOT disabled."
        return 1
    fi
}

# Add more functions as needed to check other configurations...

# Main testing logic
main() {
    check_package_installed "gdm3" || return 1
    check_gdm_user_list_disabled || return 1
    check_idle_delay 900 # Assuming you expect 900 seconds for idle delay
    check_autorun_disabled || return 1
    # Add calls to other test functions here...

    echo "All tests passed."
}

main
