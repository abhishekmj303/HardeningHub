#!/bin/bash
# Check installation status of apparmor
echo -e "\n FireWall Status:"
dpkg-query -W -f='${binary:Package}\t${Status}\t${db:Status-Status}\n' ufw ufw

echo -e "\n Ensure ufw loopback traffic is configured:"

# Fetch UFW status and rules
ufw_rules=$(ufw status verbose)

# Expected rules
expected_rules=(
    "Anywhere on lo ALLOW IN Anywhere"
    "Anywhere DENY IN 127.0.0.0/8"
    "Anywhere (v6) on lo ALLOW IN Anywhere (v6)"
    "Anywhere (v6) DENY IN ::1"
    "Anywhere ALLOW OUT Anywhere on lo"
    "Anywhere (v6) ALLOW OUT Anywhere (v6) on lo"
)

# Function to check rule presence
check_rule() {
    local rule="$1"
    if echo "$ufw_rules" | grep -q "$rule"; then
        echo "PASS: Rule '$rule' is correctly set."
    else
        echo "FAIL: Rule '$rule' is NOT set."
    fi
}

# Loop through expected rules and check each
for rule in "${expected_rules[@]}"; do
    check_rule "$rule"
done


echo -e "\nEnsure ufw default deny firewall policy"
ufw status verbose | grep Default: