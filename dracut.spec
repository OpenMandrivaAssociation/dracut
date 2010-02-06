Summary:	Next generation initrd image generator
Name:		dracut
Version:	004
Release:	%mkrel 2
Group:		System/Base
License:	GPLv2+
URL:		http://apps.sourceforge.net/trac/dracut/wiki
Source0:	http://downloads.sourceforge.net/project/dracut/%{name}-%{version}.tar.bz2
Patch0:		dracut-003-mdv.patch
Patch13:	dracut-003-firmware_sh.patch
Patch14:	dracut-003-initargs.patch
Patch15:	dracut-004-mkinitrd.patch
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
Conflicts:	nash < 6.0.93-%manbo_mkrel 11
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Event driven initrd image generator based around udev.

%prep
%setup -q
%patch0 -p1 -b .mdv.orig
%patch13 -p1 -b .firmware.orig
%patch14 -p1 -b .initargs.orig
%patch15 -p1 -b .mkinitrd.orig

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

mv %{buildroot}/sbin/lsinitrd %{buildroot}/sbin/lsinitrd-dracut
mv %{buildroot}/sbin/mkinitrd %{buildroot}/sbin/mkinitrd-dracut

cat > README.urpmi << EOF

This ia a mkinitrd replacement.
Consider this software as experimental!

How to use:

dracut -v /boot/initrd-dracut-\$(uname -r).img \$(uname -r)

then run

bootloader-config --action add-kernel /boot/vmlinuz-\$(uname -r) --initrd /boot/initrd-dracut-\$(uname -r).img --kernel-version \$(uname -r) --label dracut

and reboot.

If you want to set dracut as an mkinitrd replacement run
update-alternatives --set mkinitrd /sbin/mkinitrd-dracut
EOF

%clean
rm -rf %{buildroot}

%post
update-alternatives --install /sbin/mkinitrd mkinitrd /sbin/mkinitrd-dracut 90 || :
update-alternatives --install /sbin/lsinitrd lsinitrd /sbin/lsinitrd-dracut 90 || :

%postun
[[ "$1" = "0" ]] && update-alternatives --remove mkinitrd /sbin/mkinitrd-dracut || :
[[ "$1" = "0" ]] && update-alternatives --remove lsinitrd /sbin/lsinitrd-dracut || :

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
/sbin/lsinitrd-dracut
/sbin/mkinitrd-dracut
%{_datadir}/dracut/dracut-functions
%{_datadir}/dracut/modules.d
%{_mandir}/man8/dracut*.8*
%{_mandir}/man5/dracut.conf.5*
