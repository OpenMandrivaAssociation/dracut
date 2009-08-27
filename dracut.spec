Summary:	Next generation initrd image generator
Name:		dracut
Version:	0.7
Release:	%mkrel 1
Group:		System/Base
License:	GPLv2+
URL:		http://apps.sourceforge.net/trac/dracut/wiki
Source0:	http://downloads.sourceforge.net/project/dracut/%{name}-%{version}.tar.bz2
Requires:	udev
Requires:	util-linux-ng
Requires:	module-init-tools
Requires:	cpio
Requires:	coreutils
Requires:	findutils
Requires:	binutils
Requires:	grep
Requires:	mktemp
Requires:	mount
Requires:	bash
Requires:	initscripts
#BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Event driven initrd image generator based around udev.

%prep
%setup -q

%build
export CFLAGS="%{optflags}"
%make

%install
rm -rf %{buildroot}
%makeinstall_std sbindir=/sbin sysconfdir=%{_sysconfdir} mandir=%{_mandir}

mkdir -p %{buildroot}/boot/dracut
mkdir -p %{buildroot}%{_var}/lib/dracut/overlay

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README* HACKING TODO AUTHORS
%dir /boot/dracut
%dir %{_datadir}/dracut
%dir %{_var}/lib/dracut
%dir %{_var}/lib/dracut/overlay
%config(noreplace) %{_sysconfdir}/dracut.conf
/sbin/dracut
/sbin/dracut-gencmdline
/sbin/dracut-catimages
/sbin/switch_root
%{_datadir}/dracut/dracut-functions
%{_datadir}/dracut/modules.d
%{_mandir}/man8/dracut.8*
