#!/bin/bash
# Check installation status of apparmor
echo -e "\nAdvanced Intrusion Detection Environment status:"
dpkg-query -W -f='${binary:Package}\t${Status}\t${db:Status-Status}\n' aide aide-common