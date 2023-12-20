#!/bin/bash

echo "Auditing the /dev/shm partition for 'nodev' option..."

if findmnt --kernel /dev/shm | grep -q "nodev"; then
    echo "PASS: 'nodev' option is set for /dev/shm."
else
    echo "FAIL: 'nodev' option is NOT set for /dev/shm."
fi
