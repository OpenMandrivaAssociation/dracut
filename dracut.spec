Summary:	Next generation initrd image generator
Name:		dracut
Version:	011
Release:	%mkrel 1
Group:		System/Base
License:	GPLv2+
URL:		http://apps.sourceforge.net/trac/dracut/wiki
Source0:	http://downloads.sourceforge.net/project/dracut/%{name}-%{version}.tar.bz2
Source3:	50-dracut-mandriva.conf
# (bor) mdv-specific fixes
Patch0:		dracut-011-mdv.patch
# (bor) Restore original Mandriva behaviour of adding bootchart if RPM is installed.
Patch1:		dracut-007-undisable_bootchart.patch
# (bor) compatibility with mkinitrd
Patch15:	dracut-010-mkinitrd.patch
# (bor) Add support for KEYTABLE to dynamically determine whether to install UNICODE or non-UNICODE keymap version.
Patch19:	dracut-008-fix_unicode_keytable.patch
Patch21:	dracut-007-aufs-mount.patch
# (bor) pass flag that dracut was started to systemd (GIT)
Patch22:	dracut-010-plymouth-touch-dev-systemd-plymouth.patch
# (anssi) handle gzip compressed KMS kernel modules
Patch26:	dracut-011-plymouth-compressed-kmod.patch
Patch100:       dracut-011-rosa-livecdfix.patch
Patch101:       dracut.error.workaround.patch
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
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc

%description
Event driven initrd image generator based around udev.

%prep
%setup -q
%patch0 -p1 -b .mdv.orig
%patch1 -p1 -b .undisable_bootchart.orig
%patch15 -p1 -b .mkinitrd.orig
%patch19 -p1 -b .fix_unicode_keytable.orig
%patch21 -p1 
#%patch22 -p1
%patch26 -p1
%patch100 -p1
#%patch101 -p1
%build
export CFLAGS="%{optflags}"
%make

%install
rm -rf %{buildroot}
%makeinstall_std sbindir=/sbin sysconfdir=%{_sysconfdir} mandir=%{_mandir}

install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/dracut.conf.d

# bluca remove patch backup files
find %{buildroot} -name \*.\*.orig -exec rm {} \;

# fix permission of module files
chmod +x %{buildroot}%{_datadir}/dracut/modules.d/*/*.sh
chmod +x %{buildroot}%{_datadir}/dracut/modules.d/99aufs-mount/install

mkdir -p %{buildroot}/boot/dracut
mkdir -p %{buildroot}%{_var}/lib/dracut/overlay

mv %{buildroot}/sbin/lsinitrd %{buildroot}/sbin/lsinitrd-dracut
mv %{buildroot}/sbin/mkinitrd %{buildroot}/sbin/mkinitrd-dracut

cat > README.urpmi << EOF
dracut is the default mkinitrd replacement in mandriva

If you relly want to use old mkinitrd instead of dracut run
update-alternatives --set mkinitrd /sbin/mkinitrd-mkinitrd
EOF

%clean
rm -rf %{buildroot}

%post
update-alternatives --install /sbin/mkinitrd mkinitrd /sbin/mkinitrd-dracut 110 || :
update-alternatives --install /sbin/lsinitrd lsinitrd /sbin/lsinitrd-dracut 110 || :

%postun
[ ! -e /sbin/mkinitrd-dracut ] && update-alternatives --remove mkinitrd /sbin/mkinitrd-dracut || :
[ ! -e /sbin/lsinitrd-dracut ] && update-alternatives --remove lsinitrd /sbin/lsinitrd-dracut || :

%files
%defattr(-,root,root)
%doc README.generic README.modules README.kernel HACKING TODO AUTHORS 
%doc README.urpmi
%dir /boot/dracut
%dir %{_datadir}/dracut
%dir %{_var}/lib/dracut
%dir %{_var}/lib/dracut/overlay
%config(noreplace) %{_sysconfdir}/dracut.conf
%dir %{_sysconfdir}/dracut.conf.d
%{_sysconfdir}/dracut.conf.d/50-dracut-mandriva.conf
/sbin/dracut
/sbin/dracut-gencmdline
/sbin/dracut-catimages
/sbin/lsinitrd-dracut
/sbin/mkinitrd-dracut
%{_datadir}/dracut/dracut-functions
%{_datadir}/dracut/modules.d
%{_datadir}/dracut/dracut-logger
%{_mandir}/man8/dracut*.8*
%{_mandir}/man7/dracut.kernel.7*
%{_mandir}/man5/dracut.conf.5*
