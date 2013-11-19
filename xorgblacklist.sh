#!/bin/sh
for bl in $(getargs xorg.blacklist=); do
	rm -rf /sysroot/lib/modules/*/kernel/drivers/gpu/drm/$bl
	chroot /sysroot rpm -e x11-driver-video &>/dev/null || :
	chroot /sysroot rpm -e x11-driver-video-$bl
done
