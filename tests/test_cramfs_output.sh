#!/bin/bash

# Function to check if module is set to not load
check_module_not_loadable() {
    local module="$1"
    local conf_file="/etc/modprobe.d/$module.conf"

    if grep -Pq "^\s*install $module /bin/false" "$conf_file"; then
        echo "Module $module is set to not load in $conf_file."
    else
        echo "Module $module is NOT set to not load in $conf_file."
        return 1
    fi
}

# Function to check if module is unloaded
check_module_unloaded() {
    local module="$1"

    if lsmod | grep -q "$module"; then
        echo "Module $module is still loaded."
        return 1
    else
        echo "Module $module is unloaded."
    fi
}

# Function to check if module is blacklisted
check_module_blacklisted() {
    local module="$1"
    local blacklist_files="/etc/modprobe.d/*.conf"

    if grep -Pq "^\s*blacklist $module" $blacklist_files; then
        echo "Module $module is blacklisted."
    else
        echo "Module $module is NOT blacklisted."
        return 1
    fi
}

# Main testing logic
main() {
    # Replace "cramfs" with the modules you expect to be blocked
    local module_name="cramfs"
    check_module_not_loadable "$module_name" || return 1
    check_module_unloaded "$module_name" || return 1
    check_module_blacklisted "$module_name" || return 1

    echo "All tests passed."
}

main
