#!/bin/bash

# Function to check if a service is inactive and its package is removed
check_service_removed() {
    local service="$1"
    local package="$2"

    # Check if the service is inactive
    if systemctl is-active --quiet "$service"; then
        echo "Service $service is still active."
        return 1
    else
        echo "Service $service is inactive."
    fi

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
    # Replace these with the services and packages you expect to be removed
    check_service_removed "avahi-daemon" "avahi-daemon" || return 1
    check_service_removed "cups" "cups" || return 1
    check_service_removed "isc-dhcp-server" "isc-dhcp-server" || return 1
    check_service_removed "slapd" "slapd" || return 1
    check_service_removed "nfs-kernel-server" "nfs-kernel-server" || return 1
    check_service_removed "vsftpd" "vsftpd" || return 1
    check_service_removed "apache2" "apache2" || return 1
    check_service_removed "dovecot" "dovecot-imapd" || return 1 # Assuming dovecot manages IMAP/POP3
    check_service_removed "smbd" "samba" || return 1 # 'smbd' is the Samba daemon
    check_service_removed "squid" "squid" || return 1
    check_service_removed "snmpd" "snmp" || return 1 # 'snmpd' is the SNMP daemon
    check_service_removed "ypserv" "nis" || return 1 # 'ypserv' is the NIS server daemon
    check_service_removed "rsync" "rsync" || return 1

    echo "All tests passed."
}

main
