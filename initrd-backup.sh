#!/bin/bash
#
# Author: tpg@mandriva.org
# A simple script which does a backup of current initrd
# and creates new initrd then
# script does not handle BOOT_IMAGE=somestring
# where somestring does not point to a initrd file
#

DT=`date +%Y%m%d`
CMDL=`cat /proc/cmdline`
BOOT_IMG=`cat /proc/cmdline | awk 'BEGIN {RS = " "; FS = "=" } {if ($1 == "BOOT_IMAGE") print $2}'`
BOOT_IMG_NEW="$BOOT_IMG-$DT"
NEW_CMDL=`cat /proc/cmdline | sed -e "s@$BOOT_IMG@$BOOT_IMG_NEW@g"`


# fuction which converts LABEL/UUID to block name
# whih GURB can understand

UL_TO_BLOCK(){

UUID=`cat /proc/cmdline | awk -FUUID= '{print $2}' | awk '{print $1}'`
LABEL=`cat /proc/cmdline | awk -FLABEL= '{print $2}' | awk '{print $1}'`

if [[ ! $UUID = "" ]]; then
    dev=$(blkid -U $UUID)
else
    dev=$(blkid -L $LABEL)
fi

drive=$(echo -n ${dev:7:1} | od -A n -t dC)
    ((drive -= 97))
partition=${dev:8}
    ((partition--))

eval block="(hd${drive},${partition})"
}

# run then conversion
UL_TO_BLOCK block

# do the checks and all the tricks
if  [[ `rpm --eval %mandriva_branch` = "Cooker" ]]; then
    if [[ -e /boot/grub/install.sh ]]; then

        if [[ -e /boot/initrd-$BOOT_IMG.img ]]; then

	    echo "Storing current initrd."
	    mv -f /boot/initrd-$BOOT_IMG.img /boot/initrd-$BOOT_IMG_NEW.img
	    sleep 1
	    echo "Current initrd file has been stored in /boot/initrd-$BOOT_IMG_NEW.img"
	    grep -c "title.*$BOOT_IMG_NEW"
	    # do not add the same title value again
	    if [ $(grep -c "title.*$BOOT_IMG_NEW" /boot/grub/menu.lst) -ne 0 ]; then
		echo "Updating GRUB menu file."
		echo "" >> /boot/grub/menu.lst
		echo "title $BOOT_IMG_NEW" >> /boot/grub/menu.lst
		echo "kernel (`echo $block`)/boot/vmlinuz-$BOOT_IMG $CMDL_NEW"  >> /boot/grub/menu.lst
		echo "root (`echo $block`)" >> /boot/grub/menu.lst
		echo "initrd /boot/initrd-$BOOT_IMG_NEW.img"  >> /boot/grub/menu.lst
		echo "" >> /boot/grub/menu.lst
		sleep 1
		echo "Re-installing GRUB."
		/boot/grub/install.sh >/dev/null 2>&1
		sleep 1
	    fi
	    echo "Creating new initrd file."
	    dracut -f /boot/initrd-$BOOT_IMG.img $BOOT_IMG
	    sleep 1
	    echo "Done!"
	else
	    echo "System is missing initrd file."
	fi
    else
	echo "GRUB install.sh file does not exist.";
    fi

fi

# EOF
