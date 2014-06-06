Summary:	Next generation initrd image generator
Name:		dracut
Version:	037
Release:	7
Group:		System/Base
License:	GPLv2+
URL:		https://dracut.wiki.kernel.org/
# http://git.kernel.org/cgit/boot/dracut/dracut.git/
Source0:	http://www.kernel.org/pub/linux/utils/boot/dracut/%{name}-%{version}.tar.xz
Source3:	50-dracut-distro.conf
# (tpg) simple script to provide a backup for current working initrd file
Source4:	initrd-backup.sh
# (bero) uvesafb support scripts
Source10:	uvesafb-module-setup.sh
Source11:	uvesafb-pretrigger.sh
# (bero) load KMS drivers if possible (and before uvesafb is tried as an alternative)
Source12:	drm-pretrigger.sh
# (bero) xorg.blacklist support
Source15:	xorgblacklist-module-setup.sh
Source16:	xorgblacklist-pre.sh
Source17:	xorgblacklist.sh
# (bor) mdv-specific fixes
#Patch1000:	dracut-011-mdv.patch
# (bor) Restore original Mandriva behaviour of adding bootchart if RPM is installed.
Patch1001:	dracut-037-undisable_bootchart.patch
# (bor) compatibility with mkinitrd
Patch1002:	dracut-010-mkinitrd.patch
# (bor) Add support for KEYTABLE to dynamically determine whether to install UNICODE or non-UNICODE keymap version.
Patch1003:	dracut-007-aufs-mount.patch
Patch1005:	dracut-027-modprobe-dm-mod.patch
Patch1006:	dracut-037-modprobe-loop.patch

#Patch1005:	dracut-013-ld.so.conf.workaround.patch
#Patch1006:	dracut-014-multipath-udev-rules.patch
#Patch1007:	dracut-018-check-for-tty-and-use-it.patch
#Patch1008:	dracut-018-do-not-remount-twice-disk-partitions.patch
#Patch1009:	dracut-018-install-var-run-and-var-lock.patch
Patch1010:	dracut-037-busybox-fallback-to-busybox.static-if-no-busybox.patch
Patch1011:	dracut-037-use-busybox--list.patch
Patch1012:	dracut-024-dont-compress-kernel-modules-within-initramfs.patch
Patch1013:	dracut-034-fix-prelink.patch

# (bero) Don't let plymouth run the graphics system triggers -- graphics
# driver related bits (drm, uvesafb) should take care of themselves
#(tpg) disable this as it can trigger plymouth issues see bug #578
#Patch1014:	dracut-034-gpu-driver-triggers.patch

Patch1015:	dracut-037-use-initrd-in-stead-of-initramfs-filename.patch
Patch1016:	dracut-037-fix-keyctl-path.patch
# (tpg) workaround for bug https://issues.openmandriva.org/show_bug.cgi?id=669
#Patch1017:	dracut-037-fix-missing-locale-settings.patch
# Make cpio invocations more compatible with bsdcpio -- the mode
# indicator has to be the first argument
Patch1018:	dracut-037-bsdcpio-compat.patch

### GIT PATCHES GOES HERE  ###
###
Patch2000:	2000-dracut-initramfs-restore-fix-unpacking-with-early-mi.patch
Patch2001:	2001-systemd-add-systemd-gpt-auto-generator.patch
Patch2002:	2002-fcoe-wait-for-lldpad-to-be-ready.patch
Patch2003:	2003-network-handle-ip-dhcp6-for-all-interfaces.patch
Patch2004:	2004-lsinitrd.sh-prevent-construct.patch
Patch2005:	2005-network-DCHPv6-set-valid_lft-and-preferred_lft.patch
Patch2006:	2006-dm-add-dm-cache-modules.patch
Patch2007:	2007-fcoe-workaround-fcoe-timing-issues.patch
Patch2008:	2008-fstab-do-not-mount-and-fsck-from-fstab-if-using-syst.patch
Patch2009:	2009-ifcfg-write-ifcfg.sh-turn-on-IPV6INIT-if-any-inet6-a.patch
Patch2010:	2010-lvm-module-setup.sh-check-for-existance-of-69-dm-lvm.patch
Patch2011:	2011-Break-at-switch_root-only-for-bare-rd.break.patch
Patch2012:	2012-dracut-initqueue-service-runs-before-remote-fs-pre.t.patch
Patch2013:	2013-fs-lib-always-install-fsck.-fs-if-present.patch
Patch2014:	2014-ifcfg-do-not-bind-persistent-interface-names-to-HWAD.patch
Patch2015:	2015-ifcfg-only-bind-to-HWADDR-if-addr_assign_type-0.patch
Patch2016:	2016-Specify-strstr-tightly-add-strglob-strglobin.patch
Patch2017:	2017-Correct-strstr-strglobin-in-test-suite.patch
Patch2018:	2018-i18n-parse-i18n.sh-fixed-typo-s-key-_key.patch
Patch2019:	2019-dracut-lib.sh-fixed-return-value-of-pidof.patch
Patch2020:	2020-Do-not-log-to-kmsg-syslog-and-files-for-print-cmdlin.patch
Patch2021:	2021-resume-parse-resume.sh-correctly-write-timeout-hook.patch
Patch2022:	2022-ifcfg-write-ifcfg.sh-IPV6INIT-yes-check-also-for-non.patch
Patch2023:	2023-cms-cmssetup.sh-convert-SUBCHANNELS-to-lowercase.patch
Patch2024:	2024-mdraid-module-setup.sh-fixed-print-cmdline-for-empty.patch
Patch2025:	2025-ifcfg-write-ifcfg.sh-include-net-lib.sh.patch
Patch2026:	2026-nbd-nbdroot.sh-call-nbd-client-with-systemd-mark.patch
Patch2027:	2027-fcoe-uefi-parse-uefifcoe.sh-fixed-parameter-generati.patch
Patch2028:	2028-dracut-functions.sh-print_vars-fix-for-values-with-s.patch
Patch2029:	2029-98systemd-fixup-rootfs-generator-installation-path.patch
Patch2030:	2030-udev-rules-include-59-scsi-sg3_utils.rules.patch
Patch2031:	2031-resume-module-setup.sh-filter-out-empty-resume-optio.patch
Patch2032:	2032-dracut-pre-pivot-pulls-in-remote-fs.target.patch
Patch2033:	2033-dracut-functions.sh-require_binaries-clarify-message.patch
Patch2034:	2034-kernel-modules-Fix-storage-module-selection-for-sdhc.patch
Patch2035:	2035-bonding-use-hwaddr-of-the-slave-rather-than-the-mast.patch
Patch2036:	2036-network-ifup.sh-Don-t-try-to-modprobe-ipv6-if-alread.patch
Patch2037:	2037-udev-rules-added-seat-rules.patch
Patch2038:	2038-udev-rules-add-uaccess-rules.patch

BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:	dash
BuildRequires:	bash
BuildRequires:	asciidoc
BuildRequires:	systemd-units
BuildRequires:	bash-completion

Requires:	systemd >= 198
%ifarch %{ix86} x86_64
Requires:	v86d
%endif
Provides:	mkinitrd-command
Requires(pre):	filesystem
Requires(pre):	coreutils
Suggests:	plymouth
Requires:	udev
Requires:	util-linux-ng
Requires:	kmod-compat
Requires:	e2fsprogs
Requires:	cpio
Requires:	findutils
Requires:	binutils
Requires:	grep
Requires:	mktemp
Requires:	bash
Requires:	dash
Requires:	kbd
Requires:	tar
Requires:	gzip
Requires:	bzip2
Requires:	file
Requires:	bridge-utils
Requires:	initscripts
#Requires:	bootloader-utils
Requires(pre):	rpm-helper
Requires(post,postun):	update-alternatives
Conflicts:	mkinitrd < 6.0.93-10
Conflicts:	nash < 6.0.93-11
Obsoletes:	dracut < 013

%description
Dracut contains tools to create a bootable initramfs for 2.6 Linux kernels.
Unlike existing implementations, dracut does hard-code as little as possible
into the initramfs. Dracut contains various modules which are driven by the
event-based udev. Having root on MD, DM, LVM2, LUKS is supported as well as
NFS, iSCSI, NBD, FCoE with the dracut-network package.

%prep
%setup -q
%apply_patches
# We don't want to strip dracut-install, that's debuginfo's job
sed -i -e 's,\$(strip),,g' install/Makefile

# Splash screen bits require a framebuffer module -- loaded at 50drm
# or (now, after OMV changes) 51uvesafb
# So they should be loaded later than 51...
# Moving to 59 because we may want to do more GPU initialization later.
#(tpg) disable this as it can trigger plymouth issues see bug #578
#mv modules.d/50gensplash modules.d/59gensplash
#mv modules.d/50plymouth modules.d/59plymouth

# Push in uvesafb support
#(tpg) disable this as it can trigger plymouth issues see bug #578
#mkdir modules.d/51uvesafb
#install -c -m 755 %{SOURCE10} modules.d/51uvesafb/module-setup.sh
#install -c -m 755 %{SOURCE11} modules.d/51uvesafb/uvesafb-pretrigger.sh

# drm pretriggers
#(tpg) disable this as it can trigger plymouth issues see bug #578
#install -c -m 755 %{SOURCE12} modules.d/50drm/drm-pretrigger.sh

# And xorg.blacklist support
mkdir modules.d/01xorgblacklist
install -c -m 755 %{SOURCE15} modules.d/01xorgblacklist/module-setup.sh
install -c -m 755 %{SOURCE16} modules.d/01xorgblacklist/xorgblacklist-pre.sh
install -c -m 755 %{SOURCE17} modules.d/01xorgblacklist/xorgblacklist.sh

%build
%global optflags %{optflags} -Os
%serverbuild_hardened

%configure\
	--systemdsystemunitdir=%{_unitdir} \
	--bashcompletiondir=$(pkg-config --variable=completionsdir bash-completion) \
	--libdir=%{_prefix}/lib

%make CC=%{__cc}

%install
%makeinstall_std

install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/dracut.conf.d

echo "DRACUT_VERSION=%{version}-%{release}" > %{buildroot}%{_prefix}/lib/dracut/dracut-version.sh

%if %mdvver >= 201200
# (tpg) default image name in 2012 has changed
sed -i -e 's@PLYMOUTH_LOGO_FILE=.*@PLYMOUTH_LOGO_FILE="/usr/share/plymouth/themes/Mandriva-*/background.png"@' \
    %{buildroot}%{_prefix}/lib/dracut/modules.d/??plymouth/plymouth-populate-initrd.sh
%else
sed -i -e 's@PLYMOUTH_LOGO_FILE=.*@PLYMOUTH_LOGO_FILE="/usr/share/plymouth/themes/Mandriva-*/welcome.png"@' \
    %{buildroot}%{_prefix}/lib/dracut/modules.d/??plymouth/plymouth-populate-initrd.sh
%endif

# bluca remove patch backup files
find %{buildroot} -type f -name '*.orig' -exec rm {} \;
find %{buildroot} -type f -name '*~' -exec rm {} \;

# fix permission of module files
chmod +x %{buildroot}%{_prefix}/lib/dracut/modules.d/*/*.sh

mkdir -p %{buildroot}/boot/dracut
mkdir -p %{buildroot}%{_var}/lib/dracut/overlay
install -m 755 -d %{buildroot}%{_datadir}/dracut

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}/sbin
mv %{buildroot}%{_bindir}/* %{buildroot}%{_sbindir}/

ln -s %{_sbindir}/dracut %{buildroot}%{_bindir}/dracut
ln -s %{_sbindir}/dracut %{buildroot}/sbin/dracut
ln -s %{_prefix}/lib/dracut/dracut-install %{buildroot}%{_sbindir}/dracut-install

mkdir -p %{buildroot}%{_localstatedir}/log
touch %{buildroot}%{_localstatedir}/log/dracut.log
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 0644 dracut.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/dracut

mv %{buildroot}%{_sbindir}/lsinitrd %{buildroot}%{_sbindir}/lsinitrd-dracut
mv %{buildroot}%{_sbindir}/mkinitrd %{buildroot}%{_sbindir}/mkinitrd-dracut

cat > README.urpmi << EOF
dracut is the default mkinitrd replacement in %{distribution}

If you relly want to use old mkinitrd instead of dracut run
update-alternatives --set mkinitrd /sbin/mkinitrd-mkinitrd
EOF

# rpmlint madness
chmod 755 %{buildroot}%{_prefix}/lib/dracut/modules.d/99aufs-mount/install

# (tpg) don't follow this usr madness
# systemctl sits in /bin, and it symlinks to /usr/bin
sed -i -e 's#/usr/bin/systemctl#/bin/systemctl#g' %{buildroot}%{_prefix}/lib/dracut/modules.d/98systemd/*.service
# (tpg) use real path for udevadm
sed -i -e 's#/usr/bin/udevadm#/sbin/udevadm#g' %{buildroot}%{_prefix}/lib/dracut/modules.d/98systemd/*.service

# (tpg) this conflicts with mkinitrd
rm -rf %{buildroot}%{_mandir}/man8/mkinitrd.8*

install -m755 %{SOURCE4} %{buildroot}%{_bindir}/initrd-backup.sh

%post
update-alternatives --install /sbin/mkinitrd mkinitrd %{_sbindir}/mkinitrd-dracut 110 || :
update-alternatives --install /sbin/lsinitrd lsinitrd %{_sbindir}/lsinitrd-dracut 110 || :
if [ -d /lib/modules/$(uname -r) ]; then
    %{_sbindir}/dracut -f /boot/initrd-$(uname -r).img $(uname -r)
fi

%postun
[ ! -e /usr/sbin/mkinitrd-dracut ] && update-alternatives --remove mkinitrd %{_sbindir}/mkinitrd-dracut || :
[ ! -e /usr/sbin/lsinitrd-dracut ] && update-alternatives --remove lsinitrd %{_sbindir}/lsinitrd-dracut || :

%files
%doc README.generic README.modules README.kernel HACKING TODO AUTHORS
%doc README.urpmi
%dir /boot/dracut
%dir %{_datadir}/dracut
%dir %{_var}/lib/dracut
%dir %{_var}/lib/dracut/overlay
%dir %{_prefix}/lib/dracut/modules.d
%dir %{_prefix}/lib/kernel/install.d
%dir %{_sysconfdir}/dracut.conf.d
%config %{_sysconfdir}/dracut.conf
%config %{_sysconfdir}/logrotate.d/dracut
%attr(0644,root,root) %ghost %config(missingok,noreplace) %{_localstatedir}/log/dracut.log
%{_sysconfdir}/dracut.conf.d/50-dracut-distro.conf
/sbin/dracut
%{_sbindir}/dracut
%{_bindir}/dracut
%{_bindir}/initrd-backup.sh
%{_sbindir}/dracut-catimages
%{_sbindir}/dracut-install
%{_sbindir}/lsinitrd-dracut
%{_sbindir}/mkinitrd-dracut
%{_unitdir}/*.service
%{_unitdir}/*/*.service
%{_prefix}/lib/kernel/install.d/5*-dracut*.install
%{_prefix}/lib/dracut/skipcpio
%{_prefix}/lib/dracut/dracut-install
%{_prefix}/lib/dracut/dracut-version.sh
%{_prefix}/lib/dracut/dracut-functions.sh
%{_prefix}/lib/dracut/dracut-functions
%{_prefix}/lib/dracut/modules.d/*
%{_prefix}/lib/dracut/dracut-initramfs-restore
%{_prefix}/lib/dracut/dracut-logger.sh
%{_datadir}/bash-completion/completions/dracut
%{_datadir}/bash-completion/completions/lsinitrd
%{_mandir}/man1/lsinitrd.1.*
%{_mandir}/man5/dracut.conf.5*
%{_mandir}/man7/dracut.bootup.7.xz
%{_mandir}/man7/dracut.kernel.7*
%{_mandir}/man7/dracut.cmdline.7*
%{_mandir}/man7/dracut.modules.7*
%{_mandir}/man8/dracut*.8*
%{_mandir}/man8//mkinitrd-suse.8*
