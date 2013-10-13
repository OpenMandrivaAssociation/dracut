#!/bin/sh
if getargbool 1 rd.uvesafb -n rd.NO_UVESAFB; then
	if [ ! -c /dev/fb0 -a -e /sbin/v86d ]; then
		modprobe uvesafb
		# Make sure tty changes, device nodes etc. are processed before
		# proceeding to a next step that may require a working framebuffer
		# driver (plymouth, gensplash, ...)
		udevadm trigger --action=add --subsystem-match=graphics --subsystem-match=drm --subsystem-match=tty
		udevadm settle --timeout=30 2>&1 |vinfo
	fi
fi
