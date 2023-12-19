#!/bin/bash
# Check installation status of prelink
echo -e "\nPrelink status:"
dpkg-query -W -f='${binary:Package}\t${Status}\t${db:Status-Status}\n' prelink

echo -e "\nChecking Adress Space Layout Randomization (ASLR) status:"

{
    krp="" pafile="" fafile=""
    kpname="kernel.randomize_va_space"
    kpvalue="2"
    searchloc="/run/sysctl.d/*.conf /etc/sysctl.d/*.conf /usr/local/lib/sysctl.d/*.conf /usr/lib/sysctl.d/*.conf /lib/sysctl.d/*.conf /etc/sysctl.conf"

    # Get the current runtime value of the kernel parameter
    krp="$(sysctl "$kpname" | awk -F'= ' '{print $2}' | xargs)"

    # Search for the parameter set correctly in config files
    pafile="$(grep -Psl "^\\s*$kpname\\s*=\\s*$kpvalue\\b(\\s*#.*)?$" $searchloc)"

    # Search for the parameter set incorrectly in config files
    fafile="$(grep -s "^\\s*$kpname" $searchloc | grep -Pv "^\\s*$kpname\\s*=\\s*$kpvalue\\b(\\s*#.*)?$" | awk -F: '{print $1}')"

    # Output results
    if [ "$krp" = "$kpvalue" ] && [ -n "$pafile" ] && [ -z "$fafile" ]; then
        echo -e "\nPASS:\n\"$kpname\" is set to \"$kpvalue\" in the running configuration and in \"$pafile\""
    else
        echo -e "\nFAIL: "
        [ "$krp" != "$kpvalue" ] && echo -e "\"$kpname\" is set to \"$krp\" in the running configuration"
        [ -n "$fafile" ] && echo -e "\"$kpname\" is set incorrectly in \"$fafile\""
        [ -z "$pafile" ] && echo -e "\"$kpname = $kpvalue\" is not set in a kernel parameter configuration file"
    fi
}

echo -e "\nChecking if Automatic Error Reporting is disabled:"
# Check if the Apport Error Reporting Service is enabled
if dpkg-query -s apport > /dev/null 2>&1; then
    if grep -Psi '^\s*enabled\s*=\s*[^0]\b' /etc/default/apport; then
        echo "Audit FAILED: Apport Error Reporting Service is ENABLED."
    else
        echo "Audit PASSED: Apport Error Reporting Service is DISABLED."
    fi
else
    echo "Audit INFO: Apport package is not installed."
fi

# Check if the Apport service is active
if systemctl is-active apport.service | grep -q '^active'; then
    echo "Audit FAILED: Apport service is ACTIVE."
else
    echo "Audit PASSED: Apport service is INACTIVE."
fi

echo "Auditing Core Dump Settings..."

# Verify hard core limit setting
echo -e "\nChecking hard core limits in /etc/security/limits.conf and /etc/security/limits.d/*"
if grep -Es '^(\*|\s).*hard.*core.*(\s+#.*)?$' /etc/security/limits.conf /etc/security/limits.d/* | grep -q '* hard core 0'; then
    echo "PASS: Hard core limit is correctly set to 0"
else
    echo "FAIL: Hard core limit is NOT correctly set to 0"
fi

# Verify the fs.suid_dumpable sysctl setting
echo -e "\nChecking fs.suid_dumpable setting"
current_suid_dumpable=$(sysctl fs.suid_dumpable | awk '{print $3}')
if [ "$current_suid_dumpable" = "0" ]; then
    echo "PASS: fs.suid_dumpable is correctly set to 0 in the running configuration."
else
    echo "FAIL: fs.suid_dumpable is NOT set to 0 in the running configuration. Current value: $current_suid_dumpable"
fi

# Verify fs.suid_dumpable setting in sysctl configuration files
echo -e "\nChecking fs.suid_dumpable setting in sysctl configuration files:"
if grep -q "fs.suid_dumpable = 0" /etc/sysctl.conf /etc/sysctl.d/*; then
    echo "PASS: fs.suid_dumpable configuration is correctly set to 0."
else
    echo "FAIL: fs.suid_dumpable configuration is NOT correctly set to 0."
fi

# Check if systemd-coredump is installed
echo -e "\nChecking if systemd-coredump is installed:"
if systemctl is-enabled coredump.service | grep -qE 'enabled|masked|disabled'; then
    echo "INFO: systemd-coredump is installed (service status: $(systemctl is-enabled coredump.service))"
else
    echo "INFO: systemd-coredump is NOT installed."
fi

