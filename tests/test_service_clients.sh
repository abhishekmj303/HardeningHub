#!/bin/bash

# Function to check if a package is removed
check_package_removed() {
    local package="$1"

    # Check if the package is removed
    if dpkg-query -W -f='${Status}' "$package" 2>/dev/null | grep -q "ok installed"; then
        echo "Package $package is still installed."
        return 1
    else
        echo "Package $package is removed."
    fi
}

# Main testing logic
main() {
    # Replace these with the packages you expect to be removed
    check_package_removed "nis" || return 1
    check_package_removed "rsh-client" || return 1
    check_package_removed "talk" || return 1
    check_package_removed "telnet" || return 1
    check_package_removed "ldap-utils" || return 1
    check_package_removed "rpcbind" || return 1

    echo "All tests passed."
}

main
