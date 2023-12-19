#!/bin/bash

echo "Checking installation status of prelink and apparmor..."

# Check installation status of prelink
echo -e "\nPrelink status:"
dpkg-query -W -f='${binary:Package}\t${Status}\t${db:Status-Status}\n' prelink

# Check installation status of apparmor
echo -e "\nAppArmor status:"
dpkg-query -W -f='${binary:Package}\t${Status}\t${db:Status-Status}\n' apparmor

# Check Address Space Layout Randomization (ASLR) status
echo -e "\nAddress Space Layout Randomization (ASLR) status:"
sysctl kernel.randomize_va_space


# Check if Apport Error Reporting Service is enabled
echo "Checking if Apport Error Reporting Service is enabled..."
if dpkg-query -s apport > /dev/null 2>&1; then
    if grep -Psi '^\s*enabled\s*=\s*[^0]\b' /etc/default/apport; then
        echo "Apport Error Reporting Service is enabled."
    else
        echo "Apport Error Reporting Service is disabled."
    fi
else
    echo "Apport package is not installed."
fi

# Check if Apport service is active
echo "Checking if Apport service is active..."
if systemctl is-active apport.service | grep '^active'; then
    echo "Apport service is active."
else
    echo "Apport service is inactive."
fi


echo "Auditing core dump restrictions and fs.suid_dumpable settings..."


# Check the current running value of fs.suid_dumpable
echo -e "\nChecking the running value of fs.suid_dumpable:"
current_suid_dumpable=$(sysctl fs.suid_dumpable | awk '{print $3}')
if [ "$current_suid_dumpable" = "0" ]; then
    echo "fs.suid_dumpable is set correctly in the running system."
else
    echo "fs.suid_dumpable is NOT set correctly in the running system. Current value: $current_suid_dumpable"
fi

# Check fs.suid_dumpable setting in sysctl configuration files
echo -e "\nChecking fs.suid_dumpable setting in sysctl configuration files:"
if grep "fs.suid_dumpable" /etc/sysctl.conf /etc/sysctl.d/*; then
    echo "fs.suid_dumpable configuration is set Successfully."
else
    echo "fs.suid_dumpable configuration is NOT set."
fi

echo "Auditing NTP settings..."

echo "Checking if NTP package is installed..."
if dpkg-query -W -f='${binary:Package}\t${Status}\t${db:Status-Status}\n' ntp; then
    echo "NTP package is installed."
else
    echo "NTP package is not installed."
fi

echo "Checking NTP servers in ntp.conf..."
grep -E "^server" /etc/ntp.conf

echo "Checking if NTP service is active..."
if systemctl is-active ntp.service | grep '^active'; then
    echo "NTP service is active."
else
    echo "NTP service is inactive."
fi

