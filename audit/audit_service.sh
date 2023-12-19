#!/bin/bash

# Define an array of service packages
services=(
    "avahi-daemon"
    "cups"
    "isc-dhcp-server"
    "slapd"
    "nfs-kernel-server"
    "vsftpd"
    "apache2"
    "dovecot-imapd dovecot-pop3d"
    "samba"
    "squid"
    "snmpd"
    "nis"
    "rsync"
)

# Function to check the status of a service
check_service_status() {
    local service="$1"
    echo -e "\nChecking status of $service:"
    dpkg-query -W -f='${binary:Package}\t${Status}\t${db:Status-Status}\n' $service || echo "$service is not installed."
}

# Loop through the services and check each
for service in "${services[@]}"; do
    check_service_status "$service"
done
