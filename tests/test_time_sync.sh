#!/bin/bash

# Check if NTP package is installed
check_ntp_installed() {
    if dpkg-query -W -f='${Status}' ntp 2>/dev/null | grep -q "ok installed"; then
        echo "NTP package is installed."
    else
        echo "NTP package is NOT installed."
        return 1
    fi
}

# Check if NTP servers are correctly configured
check_ntp_servers() {
    local servers=("$@")  # Pass the server list as an array

    for server in "${servers[@]}"; do
        if ! grep -q "server $server iburst" /etc/ntp.conf; then
            echo "NTP server $server is NOT configured."
            return 1
        else
            echo "NTP server $server is configured."
        fi
    done
}

# Check if RUNASUSER is set for NTP
check_runasuser_ntp() {
    if grep -q 'RUNASUSER=ntp' /etc/init.d/ntp; then
        echo "RUNASUSER is set for NTP."
    else
        echo "RUNASUSER is NOT set for NTP."
        return 1
    fi
}

# Check if NTP service is active
check_ntp_service_active() {
    if systemctl is-active --quiet ntp.service; then
        echo "NTP service is active."
    else
        echo "NTP service is NOT active."
        return 1
    fi
}

# Main testing logic
main() {
    check_ntp_installed || return 1

    # Replace these with the NTP servers you expect to be configured
    local expected_servers=("ntp1.example.com" "ntp2.example.com")
    check_ntp_servers "${expected_servers[@]}" || return 1

    check_runasuser_ntp || return 1
    check_ntp_service_active || return 1

    echo "All tests passed."
}

main
