#! /bin/bash

# add "script: /root/proxmox_backup_notif.sh" to /etc/vzdump.conf

# $1 = variable "phase" : job-start|job-end|job-abort, backup-start|backup-end|backup-abort|log-end|pre-stop|pre-restart|post-restart
# $2 = mode : stop/suspend/snapshot
# $3 = vmid

if [ "$1" == "backup-end" ]; then
	(cd "$(dirname $0)" && ./bucktrix send "Proxmox: VM $3 backup success")
fi 