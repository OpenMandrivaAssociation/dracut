Summary:	Next generation initrd image generator
Name:		dracut
Version:	0.9
Release:	%mkrel 1
Group:		System/Base
License:	GPLv2+
URL:		http://apps.sourceforge.net/trac/dracut/wiki
Source0:	http://downloads.sourceforge.net/project/dracut/%{name}-%{version}.tar.bz2
Patch0:		dracut-0.9-mdv.patch
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
Requires:	plymouth
Requires:	plymouth-theme-mdv
Requires:	bootloader-utils
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Event driven initrd image generator based around udev.

%prep
%setup -q
%patch0 -p1

%build
export CFLAGS="%{optflags}"
%make

%install
rm -rf %{buildroot}
%makeinstall_std sbindir=/sbin sysconfdir=%{_sysconfdir} mandir=%{_mandir}

# (tpg) conflicts with util-linux-ng
rm -rf %{buildroot}/sbin/switch_root

mkdir -p %{buildroot}/boot/dracut
mkdir -p %{buildroot}%{_var}/lib/dracut/overlay

cat > README.urpmi << EOF

This ia a mkinitrd replacement.
Consider this software as experimental!

How to use:

dracut -v /boot/initrd-dracut-$(uname -r).img $(uname -r)

then run

bootloader-config --action add-kernel /boot/vmlinuz-$(uname -r)
--initrd /boot/initrd-dracut-$(uname -r).img --kernel-version `uname -r`
--label dracut

and reboot.
EOF

%clean
rm -rf %{buildroot}

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
%{_datadir}/dracut/dracut-functions
%{_datadir}/dracut/modules.d
%{_mandir}/man8/dracut.8*
