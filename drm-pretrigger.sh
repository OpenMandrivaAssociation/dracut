#!/bin/sh
# trigger graphics subsystem
udevadm trigger --action=add --attr-match=class=0x030000 >/dev/null 2>&1
udevadm settle --timeout=30 2>&1 |vinfo
# trigger graphics and tty subsystem
udevadm trigger --action=add --subsystem-match=graphics --subsystem-match=drm --subsystem-match=tty >/dev/null 2>&1
udevadm settle --timeout=30 2>&1 |vinfo
