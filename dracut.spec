Summary:	Next generation initrd image generator
Name:		dracut
Version:	004
Release:	%mkrel 1
Group:		System/Base
License:	GPLv2+
URL:		http://apps.sourceforge.net/trac/dracut/wiki
Source0:	http://downloads.sourceforge.net/project/dracut/%{name}-%{version}.tar.bz2
Source1:	mkinitrd-dracut.sh
Patch0:		dracut-003-mdv.patch
Patch1:		dracut-003-kbd.patch
Patch2:		dracut-003-terminfo.patch
Patch3:		dracut-003-kogz.patch
Patch4:		dracut-003-addmod.patch
Patch5:		dracut-003-umount.patch
Patch6:		dracut-003-rdshell.patch
Patch7:		dracut-003-selinux.patch
Patch8:		dracut-003-multipath.patch
Patch9:		dracut-003-luks.patch
Patch10:	dracut-003-console.patch
Patch11:	dracut-003-unicode.patch
Patch12:	dracut-003-uswsusp.patch
Patch13:	dracut-003-firmware_sh.patch
Patch14:	dracut-003-initargs.patch
Requires:	filesystem
Requires:	udev
Requires:	util-linux-ng
Requires:	module-init-tools
Requires:	e2fsprogs
Requires:	cpio
Requires:	coreutils
Requires:	findutils
Requires:	binutils
Requires:	grep
Requires:	mktemp
Requires:	mount
Requires:	bash
Requires:	dash
Requires:	kbd
Requires:	tar
Requires:	gzip
Requires:	bzip2
Requires:	file
Requires:	module-init-tools
Requires:	bridge-utils
Requires:	initscripts
Requires(pre):	plymouth
Requires:	plymouth
Requires:	plymouth(system-theme)
Requires:	bootloader-utils
Requires(post,postun):	update-alternatives
Conflicts:	mkinitrd < 6.0.93-%manbo_mkrel 10
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Event driven initrd image generator based around udev.

%prep
%setup -q
%patch0 -p1 -b .mdv.orig
%patch1 -p1 -b .kbd.orig
%patch2 -p1 -b .terminfo.orig
%patch3 -p1 -b .kogz.orig
%patch4 -p1 -b .addmod.orig
%patch5 -p1 -b .umount.orig
%patch6 -p1 -b .rdshell.orig
%patch7 -p1 -b .selinux.orig
%patch8 -p1 -b .multipath.orig
%patch9 -p1 -b .luks.orig
%patch10 -p1 -b .console.orig
%patch11 -p1 -b .unicode.orig
%patch12 -p1 -b .uswsusp.orig
%patch13 -p1 -b .firmware.orig
%patch14 -p1 -b .initargs.orig

%build
export CFLAGS="%{optflags}"
%make

%install
rm -rf %{buildroot}
%makeinstall_std sbindir=/sbin sysconfdir=%{_sysconfdir} mandir=%{_mandir}

# bluca remove patch backup files
find %{buildroot} -name \*.\*.orig -exec rm {} \;

# fix permission of module files
chmod +x %{buildroot}%{_datadir}/dracut/modules.d/*/install
chmod +x %{buildroot}%{_datadir}/dracut/modules.d/*/installkernel
chmod +x %{buildroot}%{_datadir}/dracut/modules.d/*/check

mkdir -p %{buildroot}/boot/dracut
mkdir -p %{buildroot}%{_var}/lib/dracut/overlay

install -m 755 %{SOURCE1} %{buildroot}/sbin/mkinitrd-dracut

cat > README.urpmi << EOF

This ia a mkinitrd replacement.
Consider this software as experimental!

How to use:

dracut -v /boot/initrd-dracut-\$(uname -r).img \$(uname -r)

then run

bootloader-config --action add-kernel /boot/vmlinuz-\$(uname -r) --initrd /boot/initrd-dracut-\$(uname -r).img --kernel-version `uname -r` --label dracut

and reboot.

If you want to set dracut as an mkinitrd replacement run
update-alternatives --set mkinitrd /sbin/mkinitrd-dracut
EOF

%clean
rm -rf %{buildroot}

%post
update-alternatives --install /sbin/mkinitrd mkinitrd /sbin/mkinitrd-dracut 90 || :

%postun
[[ "$1" = "0" ]] && update-alternatives --remove mkinitrd /sbin/mkinitrd-dracut || :

%files
%defattr(-,root,root)
%doc README.generic README.modules README.kernel HACKING TODO AUTHORS 
%doc README.urpmi
%dir /boot/dracut
%dir %{_datadir}/dracut
%dir %{_var}/lib/dracut
%dir %{_var}/lib/dracut/overlay
%config(noreplace) %{_sysconfdir}/dracut.conf
/sbin/dracut
/sbin/dracut-gencmdline
/sbin/dracut-catimages
/sbin/mkinitrd-dracut
%{_datadir}/dracut/dracut-functions
%{_datadir}/dracut/modules.d
%{_mandir}/man8/dracut.8*
%{_mandir}/man5/dracut.conf.5*
