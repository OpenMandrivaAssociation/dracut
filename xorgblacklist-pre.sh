#!/bin/sh
for bl in $(getargs xorg.blacklist=); do
    rm -rf /lib/modules/*/kernel/drivers/gpu/drm/$bl
done
