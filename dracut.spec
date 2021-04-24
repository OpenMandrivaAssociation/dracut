# We ship a .pc file but don't want to have a dep on pkg-config. We
# strip the automatically generated dep here and instead co-own the
# directory.
%global __requires_exclude pkg-config

Summary:	Next generation initrd image generator
Name:		dracut
Version:	053
Release:	4
Group:		System/Base
License:	GPLv2+
URL:		https://dracut.wiki.kernel.org/
# http://git.kernel.org/cgit/boot/dracut/dracut.git/
Source0:	https://mirrors.edge.kernel.org/pub/linux/utils/boot/dracut/dracut-%{version}.tar.xz
Source3:	50-dracut-distro.conf
# (tpg) simple script to provide a backup for current working initrd file
Source4:	initrd-backup.sh
# (bero) xorg.blacklist support
Source15:	xorgblacklist-module-setup.sh
Source16:	xorgblacklist-pre.sh
Source17:	xorgblacklist.sh
# (bor) compatibility with mkinitrd
Patch1002:	dracut-010-mkinitrd.patch
# (bor) Add support for KEYTABLE to dynamically determine whether to install UNICODE or non-UNICODE keymap version.
Patch1003:	dracut-007-aufs-mount.patch
Patch1006:	dracut-037-modprobe-loop.patch
Patch1010:	dracut-037-busybox-fallback-to-busybox.static-if-no-busybox.patch
Patch1012:	dracut-044-dont-compress-kernel-modules-within-initramfs.patch

# (tpg) workaround for bug https://issues.openmandriva.org/show_bug.cgi?id=669
#Patch1017:	dracut-037-fix-missing-locale-settings.patch
# Make cpio invocations more compatible with bsdcpio -- the mode
# indicator has to be the first argument
Patch1018:	dracut-044-bsdcpio-compat.patch
#Patch1020:	dracut-045-fix-dash-syntax.patch

BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:	bash
BuildRequires:	asciidoc
BuildRequires:	systemd-macros
BuildRequires:	bash-completion
BuildRequires:	pkgconfig(libkmod)
Requires:	bash
Requires:	coreutils
Requires:	cpio
Requires:	filesystem
Requires:	findutils
Requires:	grep
Requires:	kmod >= 27-3
Requires:	sed
%ifarch %{armx}
Requires:	gzip
%else
Recommends:	xz
Recommends:	gzip
Recommends:	bzip2
Recommends:	gzip
Requires:	zstd
%endif
Requires:	util-linux
Requires:	systemd >= 228
Requires:	procps-ng
Requires:	kbd
Requires:	file
%ifarch %{ix86} %{x86_64}
Requires:	kernel
Suggests:	plymouth
%endif

Conflicts:	mkinitrd < 6.0.93-10
Conflicts:	nash < 6.0.93-10
Obsoletes:	dracut < 013
Obsoletes:	mkinitrd < 6.0.93-32
Provides:	mkinitrd = 6.0.93-32
Provides:	mkinitrd-command
Obsoletes:	nash < 6.0.93-32

%description
Dracut contains tools to create a bootable initramfs for 2.6 Linux kernels.
Unlike existing implementations, dracut does hard-code as little as possible
into the initramfs. Dracut contains various modules which are driven by the
event-based udev. Having root on MD, DM, LVM2, LUKS is supported as well as
NFS, iSCSI, NBD, FCoE with the dracut-network package.

%prep
%autosetup -p1
find . -type f |xargs sed -i -e 's,initramfs-,initrd-,g'
find . -type f |xargs sed -i -e 's,dracut-initrd-restore,dracut-initramfs-restore,g'

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
# Setting DRACUT_VERSION and DRACUT_FULL_VERSION prevents
# the Makefile from generating a bogus version tag from
# "git describe" (which isn't there when building from
# a tarball)
%make_build CC=%{__cc} DRACUT_VERSION=%{version} DRACUT_FULL_VERSION=%{version}

%install
%make_install

install -m 644 %{SOURCE3} %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d

%ifnarch %{ix86} %{x86_64}
# Microcode loading is x86 specific
sed -i -e 's,^early_microcode,# early_microcode,' %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/50-dracut-distro.conf
%endif

%ifarch %{aarch64}
# aarch64 bootloaders generally don't support zstd compressed initramfs
sed -i -e 's,^compress=.*$,compress="gzip",' %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/50-dracut-distro.conf
# do not add weird drivers for this arch
sed -i -e '/^add_drivers/d' %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/50-dracut-distro.conf
%endif

mkdir -p %{buildroot}%{_sysconfdir}/dracut.conf.d

echo "DRACUT_VERSION=%{version}-%{release}" > %{buildroot}%{_prefix}/lib/dracut/dracut-version.sh

sed -i -e 's@PLYMOUTH_LOGO_FILE=.*@PLYMOUTH_LOGO_FILE="/boot/grub2/themes/OpenMandriva/icons/openmandriva.png"@' \
    %{buildroot}%{_prefix}/lib/dracut/modules.d/??plymouth/plymouth-populate-initrd.sh

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

# rpmlint madness
chmod 755 %{buildroot}%{_prefix}/lib/dracut/modules.d/99aufs-mount/install

# (tpg) don't follow this usr madness
# systemctl sits in /bin, and it symlinks to /usr/bin
sed -i -e 's#/usr/bin/systemctl#/bin/systemctl#g' %{buildroot}%{_prefix}/lib/dracut/modules.d/98dracut-systemd/*.service
# (tpg) use real path for udevadm
sed -i -e 's#/usr/bin/udevadm#/sbin/udevadm#g' %{buildroot}%{_prefix}/lib/dracut/modules.d/98dracut-systemd/*.service

install -m755 %{SOURCE4} %{buildroot}%{_bindir}/initrd-backup.sh

# (tpg) compat symlinks to old mkinitrd
ln -sf  %{_sbindir}/mkinitrd %{buildroot}/sbin/mkinitrd
ln -sf  %{_sbindir}/lsinitrd %{buildroot}/sbin/lsinitrd

# (tpg) remove not needed modules
for i in 00bootchart 00dash 05busybox 95dasd 95zfcp 95znet 50gensplash; do
    rm -rf %{buildroot}%{_prefix}/lib/dracut/modules.d/$i
done

%triggerin -- %{name} < 050-3
# (tpg) remove wrong symlink
rm -rf %{_sbindir}/dracut-install ||:

%triggerpostun -- %{name} < %{version}
if [ $1 -gt 1 ] && [ -e /boot/vmlinuz-$(uname -r) ] && [ -x /sbin/depmod ] && [ -x /sbin/dracut ]; then
    /sbin/depmod -a "$(uname -r)"
    /sbin/dracut -f --kver "$(uname -r)"
fi

%files
%doc README.generic README.kernel AUTHORS HACKING.md NEWS.md
%dir %{_datadir}/dracut
%dir %{_var}/lib/dracut
%dir %{_var}/lib/dracut/overlay
%dir %{_prefix}/lib/dracut/modules.d
%dir %{_prefix}/lib/kernel/install.d
%dir %{_sysconfdir}/dracut.conf.d
%dir %{_prefix}/lib/dracut
%dir %{_prefix}/lib/dracut/dracut.conf.d
%config %{_sysconfdir}/dracut.conf
%{_prefix}/lib/dracut/dracut.conf.d/50-dracut-distro.conf
/sbin/dracut
/sbin/mkinitrd
/sbin/lsinitrd
%{_sbindir}/dracut
%{_bindir}/dracut
%{_bindir}/initrd-backup.sh
%{_sbindir}/dracut-catimages
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
%{_mandir}/man7/dracut.bootup.7*
%{_mandir}/man7/dracut.kernel.7*
%{_mandir}/man7/dracut.cmdline.7*
%{_mandir}/man7/dracut.modules.7*
%{_mandir}/man8/dracut*.8*
%{_mandir}/man8/mkinitrd*.8*
%dir %{_datadir}/pkgconfig
%{_datadir}/pkgconfig/dracut.pc
