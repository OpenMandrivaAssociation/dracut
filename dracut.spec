Summary:	Next generation initrd image generator
Name:		dracut
Version:	045
Release:	1
Group:		System/Base
License:	GPLv2+
URL:		https://dracut.wiki.kernel.org/
# http://git.kernel.org/cgit/boot/dracut/dracut.git/
Source0:	http://www.kernel.org/pub/linux/utils/boot/dracut/%{name}-%{version}.tar.xz
Source3:	50-dracut-distro.conf
# (tpg) simple script to provide a backup for current working initrd file
Source4:	initrd-backup.sh
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
Patch1006:	dracut-037-modprobe-loop.patch

#Patch1005:	dracut-013-ld.so.conf.workaround.patch
#Patch1006:	dracut-014-multipath-udev-rules.patch
#Patch1007:	dracut-018-check-for-tty-and-use-it.patch
#Patch1008:	dracut-018-do-not-remount-twice-disk-partitions.patch
#Patch1009:	dracut-018-install-var-run-and-var-lock.patch
Patch1010:	dracut-037-busybox-fallback-to-busybox.static-if-no-busybox.patch
Patch1011:	dracut-037-use-busybox--list.patch
Patch1012:	dracut-044-dont-compress-kernel-modules-within-initramfs.patch
Patch1013:	dracut-034-fix-prelink.patch
Patch1015:	dracut-037-use-initrd-in-stead-of-initramfs-filename.patch
# (tpg) workaround for bug https://issues.openmandriva.org/show_bug.cgi?id=669
#Patch1017:	dracut-037-fix-missing-locale-settings.patch
# Make cpio invocations more compatible with bsdcpio -- the mode
# indicator has to be the first argument
Patch1018:	dracut-044-bsdcpio-compat.patch
# (tpg) https://github.com/haraldh/dracut/issues/118
Patch1019:	dracut-044-strip-NUL-bytes.patch
Patch1020:	dracut-044-add-support-for-F2FS.patch

### GIT PATCHES GOES HERE  ###
###

BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:	dash
BuildRequires:	bash
BuildRequires:	asciidoc
BuildRequires:	systemd
BuildRequires:	bash-completion

Requires:	systemd >= 228
Provides:	mkinitrd-command
Requires(pre):	filesystem
Requires(pre):	coreutils
Suggests:	plymouth
Requires:	udev
Requires:	util-linux
Requires:	kmod-compat
Requires:	e2fsprogs
Requires:	f2fs-tools
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
Requires:	lzop
Requires:	lz4
Requires:	file
Requires:	bridge-utils
Requires:	xz
Requires:	dmraid
Requires(pre):	rpm-helper
%ifarch %{ix86} x86_64
Requires(post): kernel
%endif
Conflicts:	mkinitrd < 6.0.93-10
Conflicts:	nash < 6.0.93-10
Obsoletes:	dracut < 013
Obsoletes:	mkinitrd < 6.0.93-32
Provides:	mkinitrd = 6.0.93-32
Obsoletes:	nash < 6.0.93-32

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

# And xorg.blacklist support
mkdir modules.d/01xorgblacklist
install -c -m 755 %{SOURCE15} modules.d/01xorgblacklist/module-setup.sh
install -c -m 755 %{SOURCE16} modules.d/01xorgblacklist/xorgblacklist-pre.sh
install -c -m 755 %{SOURCE17} modules.d/01xorgblacklist/xorgblacklist.sh

%build
%serverbuild_hardened

%configure \
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

cat > README.urpmi << EOF
dracut is the default mkinitrd replacement in %{distribution}
EOF

# rpmlint madness
chmod 755 %{buildroot}%{_prefix}/lib/dracut/modules.d/99aufs-mount/install

# (tpg) don't follow this usr madness
# systemctl sits in /bin, and it symlinks to /usr/bin
sed -i -e 's#/usr/bin/systemctl#/bin/systemctl#g' %{buildroot}%{_prefix}/lib/dracut/modules.d/98dracut-systemd/*.service
# (tpg) use real path for udevadm
sed -i -e 's#/usr/bin/udevadm#/sbin/udevadm#g' %{buildroot}%{_prefix}/lib/dracut/modules.d/98dracut-systemd/*.service

install -m755 %{SOURCE4} %{buildroot}%{_bindir}/initrd-backup.sh

# (tpg) not needed for now
rm -rf %{buildroot}%{_datadir}/pkgconfig/dracut.pc

# (tpg) compat symlinks to old mkinitrd
ln -sf  %{_sbindir}/mkinitrd %{buildroot}/sbin/mkinitrd
ln -sf  %{_sbindir}/lsinitrd %{buildroot}/sbin/lsinitrd

%post
# (tpg) run initrd rebuild only on dracut update
if [ $1 -ge 2 ]; then
    kver=$(uname -r)
    if [ -d /lib/modules/${kver} -a -x /usr/bin/kernel-install ]; then
	/usr/bin/kernel-install remove ${kver} ||:
	/usr/bin/kernel-install add ${kver} /boot/vmlinuz-${kver} ||:
    fi
fi

%files
%doc README.generic README.modules README.kernel HACKING TODO AUTHORS
%doc README.urpmi
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
/sbin/mkinitrd
/sbin/lsinitrd
%{_sbindir}/dracut
%{_bindir}/dracut
%{_bindir}/initrd-backup.sh
%{_sbindir}/dracut-catimages
%{_sbindir}/dracut-install
%{_sbindir}/lsinitrd
%{_sbindir}/mkinitrd
%{_unitdir}/*.service
%{_unitdir}/*/*.service
%{_prefix}/lib/kernel/install.d/5*-dracut*.install
%{_prefix}/lib/dracut/dracut-init.sh
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
%{_mandir}/man8//mkinitrd*.8*
