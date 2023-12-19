#!/bin/bash
# Check installation status of apparmor
echo -e "\nAppArmor status:"
dpkg-query -W -f='${binary:Package}\t${Status}\t${db:Status-Status}\n' apparmor