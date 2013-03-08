Summary:	Next generation initrd image generator
Name:		dracut
Version:	026
Release:	1
Group:		System/Base
License:	GPLv2+
URL:		https://dracut.wiki.kernel.org/
Source0:	http://www.kernel.org/pub/linux/utils/boot/dracut/%{name}-%{version}.tar.xz
Source3:	50-dracut-mandriva.conf
# (tpg) simple script to provide a backup for current working initrd file
Source4:	initrd-backup.sh
# (bor) mdv-specific fixes
#Patch1000:	dracut-011-mdv.patch
# (bor) Restore original Mandriva behaviour of adding bootchart if RPM is installed.
Patch1001:	dracut-007-undisable_bootchart.patch
# (bor) compatibility with mkinitrd
Patch1002:	dracut-010-mkinitrd.patch
# (bor) Add support for KEYTABLE to dynamically determine whether to install UNICODE or non-UNICODE keymap version.
Patch1003:	dracut-007-aufs-mount.patch
# (anssi) handle gzip compressed KMS kernel modules
Patch1004:	dracut-024.rosa.patch

#Patch1005:	dracut-013-ld.so.conf.workaround.patch
#Patch1006:	dracut-014-multipath-udev-rules.patch
#Patch1007:	dracut-018-check-for-tty-and-use-it.patch
#Patch1008:	dracut-018-do-not-remount-twice-disk-partitions.patch
#Patch1009:	dracut-018-install-var-run-and-var-lock.patch
Patch1010:	dracut-024-busybox-fallback-to-busybox.static-if-no-busybox.patch
Patch1011:	dracut-024-use-busybox--list.patch
Patch1012:	dracut-024-dont-compress-kernel-modules-within-initramfs.patch

### GIT PATCHES GOES HERE  ###
###

BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:	dash
BuildRequires:	bash
BuildRequires:	asciidoc

Requires:	systemd >= 198
Provides:	mkinitrd-command
Requires(pre):	filesystem
Requires(pre):	coreutils
Suggests:	plymouth
Requires:	udev
Requires:	util-linux-ng
%if %mdvver < 201200
Requires:	module-init-tools
%else
Requires:	kmod
%endif
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

%build
%serverbuild_hardened
%make

%install
%makeinstall_std \
	sbindir=/sbin \
	libdir=%{_prefix}/lib \
	bindir=%{_bindir} \
	sysconfdir=%{_sysconfdir} \
	systemdsystemunitdir=%{_unitdir} \
	mandir=%{_mandir}

install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/dracut.conf.d

%if %mdvver >= 201200
# (tpg) default image name in 2012 has changed
sed -i -e 's/welcome.png/backgorund.png/' %{buildroot}%{_prefix}/lib/dracut/modules.d/50plymouth/plymouth-populate-initrd.sh
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
dracut is the default mkinitrd replacement in mandriva

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
%{_sbindir}/dracut -f /boot/initrd-$(uname -r).img $(uname -r)

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
%dir %{_sysconfdir}/dracut.conf.d
%config %{_sysconfdir}/dracut.conf
%config %{_sysconfdir}/logrotate.d/dracut
%attr(0644,root,root) %ghost %config(missingok,noreplace) %{_localstatedir}/log/dracut.log
%{_sysconfdir}/dracut.conf.d/50-dracut-mandriva.conf
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
%{_prefix}/lib/dracut/dracut-install
%{_prefix}/lib/dracut/dracut-version.sh
%{_prefix}/lib/dracut/dracut-functions.sh
%{_prefix}/lib/dracut/dracut-functions
%{_prefix}/lib/dracut/modules.d/*
%{_prefix}/lib/dracut/dracut-initramfs-restore
%{_prefix}/lib/dracut/dracut-logger.sh
%{_mandir}/man1/lsinitrd.1.*
%{_mandir}/man8/dracut*.8*
%{_mandir}/man8/initrd-switch-root.service.8*
%{_mandir}/man8/udevadm-cleanup-db.service.8*
%{_mandir}/man7/dracut.kernel.7*
%{_mandir}/man7/dracut.cmdline.7*
%{_mandir}/man5/dracut.conf.5*


%changelog
* Fri Oct 19 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 024-2
+ Revision: 819042
- reupload
- update to new version 024
- remove duplicate requires on mount
- provide a initd-backup.sh script which should store as a backup current working initrd file and recreates new one
  o just add the script, in next step i'll have to figure out a best mechanism to execute the script on every systemd, dracut on any other core package update
- fix udevadm path
- do not suggest plymouth theme

