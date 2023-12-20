#!/bin/bash

output=""
l_chrony="" 
l_ntp=""
l_sdtd=""

# Check if chrony is installed
dpkg-query -W chrony > /dev/null 2>&1 && l_chrony="y"

# Check if ntp is installed
dpkg-query -W ntp > /dev/null 2>&1 && l_ntp="y"

# Check if systemd-timesyncd is enabled
if systemctl list-units --all --type=service | grep -q 'systemd-timesyncd.service'; then
    if systemctl is-enabled systemd-timesyncd.service | grep -q 'enabled'; then
        l_sdtd="y"
    fi
fi

# Determine which time synchronization daemon is in use
if [[ "$l_chrony" = "y" && "$l_ntp" != "y" && "$l_sdtd" != "y" ]]; then
    output="$output\n- chrony is in use on the system"
elif [[ "$l_chrony" != "y" && "$l_ntp" = "y" && "$l_sdtd" != "y" ]]; then
    output="$output\n- ntp is in use on the system"
    # Additional audit for ntp configuration
    grep -P '^(\s*(server|pool)\s+\S+)' /etc/ntp.conf && echo "NTP configuration is correct."
    ps -ef | awk '(/[n]tpd/ && $1!="ntp") { print $1 }' || echo "ntpd daemon is running as the user ntp."
    grep -P '^(\s*RUNASUSER=ntp)' /etc/init.d/ntp && echo "RUNASUSER is set to ntp in /etc/init.d/ntp."
elif [[ "$l_chrony" != "y" && "$l_ntp" != "y" && "$l_sdtd" = "y" ]]; then
    output="$output\n- systemd-timesyncd is in use on the system"
else
    [[ "$l_chrony" = "y" && "$l_ntp" = "y" ]] && output="$output\n- both chrony and ntp are in use on the system"
    [[ "$l_chrony" = "y" && "$l_sdtd" = "y" ]] && output="$output\n- both chrony and systemd-timesyncd are in use on the system"
    [[ "$l_ntp" = "y" && "$l_sdtd" = "y" ]] && output="$output\n- both ntp and systemd-timesyncd are in use on the system"
fi

# Output results
if [ -n "$output" ]; then
    echo -e "\n- PASS:\n$output\n"
else
    echo -e "\n- FAIL:\nNo time synchronization service is active or properly configured.\n"
fi
