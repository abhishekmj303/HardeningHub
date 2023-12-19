#!/bin/bash

# Check if prelink is removed
check_prelink_removal() {
    if ! command -v prelink > /dev/null 2>&1; then
        echo "Prelink is successfully removed."
    else
        echo "Prelink is still present."
        return 1
    fi
}

# Check if ASLR is enabled
check_aslr_enabled() {
    local aslr_status=$(cat /proc/sys/kernel/randomize_va_space)
    if [ "$aslr_status" -eq 2 ]; then
        echo "ASLR is enabled."
    else
        echo "ASLR is not enabled."
        return 1
    fi
}

# Check if error reporting is disabled
check_error_reporting_disabled() {
    if grep -qs "enabled=0" /etc/default/apport; then
        echo "Error reporting is disabled."
    else
        echo "Error reporting is not disabled."
        return 1
    fi
}

# Check if core dumps are restricted
check_core_dumps_restricted() {
    local core_setting=$(grep -E "^\\* hard core 0" /etc/security/limits.conf)
    local suid_dumpable=$(sysctl fs.suid_dumpable | awk '{ print $3 }')

    if [ -z "$core_setting" ] || [ "$suid_dumpable" -ne 0 ]; then
        echo "Core dumps are not properly restricted."
        return 1
    else
        echo "Core dumps are restricted."
    fi
}

# Main testing logic
main() {
    check_prelink_removal || return 1
    check_aslr_enabled || return 1
    check_error_reporting_disabled || return 1
    check_core_dumps_restricted || return 1

    echo "All tests passed."
}

main
