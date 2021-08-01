#! /bin/bash

DISK=("a" "b" "c")
ATTRS=("^SMART overall-health" "Reallocated_Sector_Ct" "Reported_Uncorrect" "Command_Timeout" "Current_Pending_Sector" "Offline_Uncorrectable")

echo "" > /dev/shm/smartstat

for i in "${DISK[@]}"; do
    echo "/dev/sd$i" >> /dev/shm/smartstat
    SMART=$(/usr/sbin/smartctl --attributes -H /dev/sd"$i")
    for j in "${ATTRS[@]}"; do
        echo "$SMART" | grep -E "$j" >> /dev/shm/smartstat
    done
    echo "---" >> /dev/shm/smartstat
done

(cd "$(dirname $0)" && ./bucktrix send "$(cat /dev/shm/smartstat)")
rm /dev/shm/smartstat
