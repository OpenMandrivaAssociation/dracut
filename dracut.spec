%global optflags %{optflags} -Oz

# We ship a .pc file but don't want to have a dep on pkg-config. We
# strip the automatically generated dep here and instead co-own the
# directory.
%global __requires_exclude pkg-config

Summary:	Next generation initrd image generator
Name:		dracut
Version:	060
Release:	1
Group:		System/Base
License:	GPLv2+
URL:		https://dracut.wiki.kernel.org/
# Used to be at
# http://git.kernel.org/cgit/boot/dracut/dracut.git/
# https://mirrors.edge.kernel.org/pub/linux/utils/boot/dracut
# but apparently development moved without an announcement to
# https://github.com/dracutdevs/dracut
# Of course they've also stopped tagging releases, so now the way to
# track a release is to check when NEWS.md is updated. R. I. P. Sanity.
# 856e7acd... is 060
%define githash 856e7acdb1462803c2517c8d64afb2e34c73c735
Source0:	https://github.com/dracutdevs/dracut/archive/%{githash}.tar.gz
Source3:	50-dracut-distro.conf
# (bero) xorg.blacklist support
Source15:	xorgblacklist-module-setup.sh
Source16:	xorgblacklist-pre.sh
Source17:	xorgblacklist.sh
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:	asciidoc
BuildRequires:	systemd-rpm-macros
BuildRequires:	bash-completion
BuildRequires:	pkgconfig(libkmod)
Requires:	coreutils
Requires:	cpio
Requires:	filesystem
Requires:	findutils
Requires:	grep
Requires:	kmod >= 27-3
Requires:	sed
%ifarch %{armx}
# (tpg) arm bootloaders generally support gzip compression
Requires:	pigz
%else
Recommends:	xz
Recommends:	gzip
Recommends:	bzip2
Requires:	zstd
%endif
Requires:	util-linux
Requires:	systemd >= 228
Requires:	procps-ng
Requires:	kbd
Requires:	file
%ifarch %{ix86} %{x86_64} %{aarch64}
Recommends:	kernel
Recommends:	plymouth
%endif

%patchlist
# From upstream
https://github.com/dracutdevs/dracut/commit/1c762c0da6ed2bb6fa44d5e0968605cc4d45361c.patch
https://github.com/dracutdevs/dracut/commit/bddffedae038ceca263a904e40513a6e92f1b558.patch
https://github.com/dracutdevs/dracut/commit/1586af098fb17f7565d1699953e4e4b536304089.patch
https://github.com/dracutdevs/dracut/commit/4d594210d6ef4f04a9dbadacea73e9461ded352d.patch
https://github.com/dracutdevs/dracut/commit/4971f443726360216a4ef3ba8baea258a1cd0f3b.patch
https://github.com/dracutdevs/dracut/commit/de8ac6300d115a05d467dbb6b9a7c2599a2d306f.patch
https://github.com/dracutdevs/dracut/commit/4980bad34775da715a2639b736cba5e65a8a2604.patch
https://github.com/dracutdevs/dracut/commit/5d2bda46f4e75e85445ee4d3bd3f68bf966287b9.patch

# Fedora patches -- good to keep in sync, they are the upstream
# maintainers of dracut, but they rarely share what's needed
# to keep it working with upstream repositories...
# #include <redhat/sucks.h>
https://src.fedoraproject.org/rpms/dracut/raw/rawhide/f/0001-feat-kernel-install-do-nothing-when-KERNEL_INSTALL_I.patch
https://src.fedoraproject.org/rpms/dracut/raw/rawhide/f/0002-fix-systemd-pcrphase-rename-systemd-pcrphase-binary-.patch
https://src.fedoraproject.org/rpms/dracut/raw/rawhide/f/0003-fix-resume-add-new-systemd-hibernate-resume.service.patch
https://src.fedoraproject.org/rpms/dracut/raw/rawhide/f/0004-fix-wait-12-hours-before-halt-on-media-check-fail.patch
https://src.fedoraproject.org/rpms/dracut/raw/rawhide/f/0005-feat-network-include-98-default-mac-none.link-if-it-.patch
https://src.fedoraproject.org/rpms/dracut/raw/rawhide/f/0006-feat-kernel-modules-add-Qualcomm-IPC-router-to-enabl.patch
https://src.fedoraproject.org/rpms/dracut/raw/rawhide/f/0007-fix-kernel-install-do-not-generate-an-initrd-when-on.patch
# We already pull in the equivalent of 0008-fix-pkcs11-delete-trailing-dot-on-libcryptsetup-toke.patch from upstream
https://src.fedoraproject.org/rpms/dracut/raw/rawhide/f/0009-fix-pcsc-add-disable-polkit-to-pcscd.service.patch
https://src.fedoraproject.org/rpms/dracut/raw/rawhide/f/0010-fix-pcsc-add-opensc-load-module-file.patch

# OM patches
# Make sure ld-linux-aarch64.so.1 and friends end up
# being reachable in /lib even though the more
# obvious place is /lib64
dracut-055-lib-ld-linux-aarch64.patch
dracut-059-try-to-fix-lvm.patch
dracut-037-modprobe-loop.patch
# (tpg) disable it for now, as zstd is compresing kernel modules these days
#Patch1012:	dracut-044-dont-compress-kernel-modules-within-initramfs.patch

# Make cpio invocations more compatible with bsdcpio -- the mode
# indicator has to be the first argument
dracut-044-bsdcpio-compat.patch

%description
Dracut contains tools to create a bootable initramfs for 2.6 Linux kernels.
Unlike existing implementations, dracut does hard-code as little as possible
into the initramfs. Dracut contains various modules which are driven by the
event-based udev. Having root on MD, DM, LVM2, LUKS is supported as well as
NFS, iSCSI, NBD, FCoE with the dracut-network package.

%prep
%autosetup -p1 -n dracut-%{githash}

find . -type f |xargs sed -i -e 's,initramfs-,initrd-,g'
find . -type f |xargs sed -i -e 's,dracut-initrd-restore,dracut-initramfs-restore,g'

# And xorg.blacklist support
mkdir modules.d/01xorgblacklist
install -c -m 755 %{SOURCE15} modules.d/01xorgblacklist/module-setup.sh
install -c -m 755 %{SOURCE16} modules.d/01xorgblacklist/xorgblacklist-pre.sh
install -c -m 755 %{SOURCE17} modules.d/01xorgblacklist/xorgblacklist.sh

%build
%configure \
	--systemdsystemunitdir=%{_unitdir} \
	--bashcompletiondir=$(pkg-config --variable=completionsdir bash-completion) \
	--libdir=%{_prefix}/lib

# Setting DRACUT_VERSION and DRACUT_FULL_VERSION prevents
# the Makefile from generating a bogus version tag from
# "git describe" (which isn't there when building from
# a tarball)
%make_build CC="%{__cc}" DRACUT_VERSION=%{version} DRACUT_FULL_VERSION=%{version}

%install
%make_install

install -m 644 %{SOURCE3} %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d

%ifnarch %{ix86} %{x86_64}
# Microcode loading is x86 specific
sed -i -e '/^early_microcode="yes"/early_microcode="no"/' %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/50-dracut-distro.conf
%endif

%ifarch %{aarch64}
# aarch64 bootloaders generally support gzip compression
sed -i -e 's,^compress=.*$,compress="gzip",' %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/50-dracut-distro.conf
# no need to carry x86 legacy cruft in add_drivers for aarch64 -- but
# keeping evdev and friends there is probably useful
sed -i -e 's/pata_acpi ata_generic //' %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/50-dracut-distro.conf
%endif

mkdir -p %{buildroot}%{_sysconfdir}/dracut.conf.d

echo "DRACUT_VERSION=%{version}-%{release}" > %{buildroot}%{_prefix}/lib/dracut/dracut-version.sh

# bluca remove patch backup files
find %{buildroot} -type f -name '*.orig' -exec rm {} \;
find %{buildroot} -type f -name '*~' -exec rm {} \;

# fix permission of module files
chmod +x %{buildroot}%{_prefix}/lib/dracut/modules.d/*/*.sh

mkdir -p %{buildroot}%{_var}/lib/dracut/overlay
install -m 755 -d %{buildroot}%{_datadir}/dracut

# (tpg) remove not needed modules
for i in 00bootchart 00dash 05busybox 95dasd 95zfcp 95znet 50gensplash; do
    rm -rf %{buildroot}%{_prefix}/lib/dracut/modules.d/$i
done

%triggerpostun -- %{name} < %{version}
if [ $1 -gt 1 ] && [ -e /boot/vmlinuz-$(uname -r) ] && [ -e %{_sbindir}/depmod ] && [ -x %{_bindir}/dracut ]; then
    %{_sbindir}/depmod -a "$(uname -r)"
    %{_bindir}/dracut -f --kver "$(uname -r)"
fi

%files
%doc AUTHORS NEWS.md README.md
%dir %{_datadir}/%{name}
%dir %{_var}/lib/%{name}
%dir %{_var}/lib/%{name}/overlay
%dir %{_prefix}/lib/%{name}/modules.d
%dir %{_prefix}/lib/kernel/install.d
%dir %{_sysconfdir}/%{name}.conf.d
%dir %{_prefix}/lib/%{name}
%dir %{_prefix}/lib/%{name}/%{name}.conf.d
%config %{_sysconfdir}/%{name}.conf
%{_prefix}/lib/%{name}/%{name}.conf.d/50-%{name}-distro.conf
%{_bindir}/*
%{_unitdir}/*.service
%{_unitdir}/*/*.service
%{_prefix}/lib/kernel/install.d/5*-%{name}*.install
%{_prefix}/lib/%{name}/%{name}-util
%{_prefix}/lib/%{name}/%{name}-init.sh
%{_prefix}/lib/%{name}/skipcpio
%{_prefix}/lib/%{name}/%{name}-install
%{_prefix}/lib/%{name}/%{name}-version.sh
%{_prefix}/lib/%{name}/%{name}-functions.sh
%{_prefix}/lib/%{name}/%{name}-functions
%{_prefix}/lib/%{name}/modules.d/*
%{_prefix}/lib/%{name}/%{name}-initramfs-restore
%{_prefix}/lib/%{name}/%{name}-logger.sh
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/bash-completion/completions/lsinitrd
%doc %{_mandir}/man1/lsinitrd.1.*
%doc %{_mandir}/man5/%{name}.conf.5*
%doc %{_mandir}/man7/%{name}.bootup.7*
%doc %{_mandir}/man7/%{name}.kernel.7*
%doc %{_mandir}/man7/%{name}.cmdline.7*
%doc %{_mandir}/man7/%{name}.modules.7*
%doc %{_mandir}/man8/%{name}*.8*
%{_datadir}/pkgconfig/%{name}.pc
