#!/usr/bin/env bash

{
    l_output="" 
    l_output2=""
    l_mname="squashfs"  # Set module name

    # Check how the module will be loaded
    l_loadable="$(modprobe -n -v "$l_mname")"
    if echo "$l_loadable" | grep -Pq '^install /bin/(true|false)'; then
        l_output="$l_output\n - Module: \"$l_mname\" is not loadable: $l_loadable"
    else
        l_output2="$l_output2\n - Module: \"$l_mname\" is loadable: $l_loadable"
    fi

    # Check if the module is currently loaded
    if ! lsmod | grep -q "$l_mname"; then
        l_output="$l_output\n - Module: \"$l_mname\" is not loaded"
    else
        l_output2="$l_output2\n - Module: \"$l_mname\" is loaded"
    fi

    # Check if the module is deny listed
    if grep -Pq "^\s*blacklist\s+$l_mname\b" /etc/modprobe.d/*; then
        deny_list_file="$(grep -Pl "^\s*blacklist\s+$l_mname\b" /etc/modprobe.d/*)"
        l_output="$l_output\n - Module: \"$l_mname\" is deny listed in: $deny_list_file"
    else
        l_output2="$l_output2\n - Module: \"$l_mname\" is not deny listed"
    fi

    # Report results. If no failures output in l_output2, we pass
    if [ -z "$l_output2" ]; then
        echo -e "\n- Audit Result:\n ** PASS **\n$l_output\n"
    else
        echo -e "\n- Audit Result:\n ** FAIL **\n - Reason(s) for audit failure:\n$l_output2\n"
        [ -n "$l_output" ] && echo -e "\n- Correctly set:\n$l_output\n"
    fi
}
