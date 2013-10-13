#!/bin/bash
check() {
	test -x /sbin/v86d -a -f "$srcmods"/kernel/drivers/video/uvesafb.ko*
}

depends() {
	return 0
}

installkernel() {
	hostonly='' instmods uvesafb
}

install() {
	dracut_install /sbin/v86d
	inst_hook pre-trigger 09 "$moddir/uvesafb-pretrigger.sh"
}
