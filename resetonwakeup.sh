#!/bin/bash
#
# located in /lib/systemd/system-sleep/

PATH=/sbin:/usr/sbin:/bin:/usr/bin

exec 2> /tmp/systemd_suspend_test_err.txt
if [ "${1}" = "pre" ]; then
  # Do the thing you want before suspend here
  echo "--SUSPEND FROM /lib/systemd/system-sleep --" > /tmp/systemd_suspend_test.txt
  date >> /tmp/systemd_suspend_test.txt
elif [ "${1}" = "post" ]; then
  # Do the thing you want after resume here
  echo "--RESUME /lib/systemd/system-sleep --" >> /tmp/systemd_suspend_test.txt
  date >> /tmp/systemd_suspend_test.txt
  systemctl stop gdm3 >> /tmp/systemd_suspend_test.txt
  rmmod nvidia_uvm >> /tmp/systemd_suspend_test.txt
  modprobe nvidia_uvm >> /tmp/systemd_suspend_test.txt
  systemctl start  gdm3 >> /tmp/systemd_suspend_test.txt
fi