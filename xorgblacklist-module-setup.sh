#!/bin/bash
check() {
    return 0
}

depends() {
    return 0
}

installkernel() {
    return 0
}

install() {
    inst_hook pre-udev 01 "$moddir/xorgblacklist-pre.sh"
    inst_hook cleanup 99 "$moddir/xorgblacklist.sh"
}
